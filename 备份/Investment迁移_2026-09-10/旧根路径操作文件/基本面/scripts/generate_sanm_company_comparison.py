from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated
import generate_cls_company_comparison as cls_calibrated
import generate_dell_company_comparison as dell_calibrated
import generate_flex_company_comparison as flex_calibrated
import generate_fn_company_comparison as fn_calibrated
import generate_jbl_company_comparison as jbl_calibrated


TARGET = "SANM"
TARGET_NAME = "Sanmina Corporation"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "SANM_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_EMS_PEERS = {"DELL", "HPE", "SMCI", "PENG", "JBL", "FLEX", "CLS", "FN"}
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
POWER_COOLING_CHAIN = {
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
    "DTE",
    "EME",
    "ENS",
    "ENPH",
    "ET",
    "ETN",
    "ETR",
    "FCEL",
    "FIX",
    "FLNC",
    "GEV",
    "GNRC",
    "HPE",
    "HTHIY",
    "HUBB",
    "IESC",
    "IFNNY",
    "JCI",
    "MIELY",
    "MOD",
    "MRAAY",
    "MYRG",
    "NVT",
    "OKLO",
    "POWI",
    "POWL",
    "PSIX",
    "PWR",
    "SMR",
    "TT",
    "TTDKY",
    "VICR",
    "VRT",
    "VST",
}

EXTRA_SCORE_FLOORS = {
    **calibrated.SCORE_FLOORS,
    **cls_calibrated.EXTRA_SCORE_FLOORS,
    **dell_calibrated.EXTRA_SCORE_FLOORS,
    **jbl_calibrated.EXTRA_SCORE_FLOORS,
    "CLS": cls_calibrated.CLS_SCORE_OVERRIDES,
    "DELL": dell_calibrated.DELL_OVERRIDES,
    "FLEX": flex_calibrated.FLEX_OVERRIDES,
    "FN": fn_calibrated.FN_OVERRIDES,
    "JBL": jbl_calibrated.JBL_SCORE_OVERRIDES,
    "PENG": {
        "NTM兑现优先": 76,
        "右尾弹性优先": 78,
        "风险调整收益": 52,
        "下行保护优先": 28,
        "估值消化优先": 78,
        "近端催化优先": 82,
        "价格确认/动量": 98,
        "激进短线": 94,
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

SANM_SCORE_OVERRIDES = {
    "NTM兑现优先": 70.0,
    "右尾弹性优先": 68.0,
    "风险调整收益": 64.0,
    "下行保护优先": 66.0,
    "估值消化优先": 74.0,
    "近端催化优先": 68.0,
    "价格确认/动量": 64.0,
    "激进短线": 72.0,
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
        if not company or ticker == TARGET:
            continue
        for strat, floor in floors.items():
            current = company.setdefault("scores", {}).get(strat, 0)
            company["scores"][strat] = max(float(current), float(floor))

    for strat, score in SANM_SCORE_OVERRIDES.items():
        companies[TARGET].setdefault("scores", {})[strat] = score

    calibrated.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_EMS_PEERS:
        return "直接同业"
    if ticker in SERVER_STORAGE_ADJACENT or category == "AI服务器_存储_EMS":
        return "相邻替代"
    if ticker in AI_NETWORK_UPDOWN or ticker in AI_COMPUTE_UPSTREAM or ticker in DOWNSTREAM_CLOUD:
        return "上下游"
    if ticker in POWER_COOLING_CHAIN or category in INFRA_CATS:
        return "相邻替代"
    if category in {"AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if winner == "A":
        return {
            "NTM兑现优先": "A有ZT已确认收入和FY2026指引硬锚",
            "右尾弹性优先": "A的AI rack/accelerated compute右尾可收入化",
            "风险调整收益": "A低P/S、正FCF和增长组合较均衡",
            "下行保护优先": "A有Core IMS/CPS底座和现金流缓冲",
            "估值消化优先": "A用低P/S和ZT增长消化估值",
            "近端催化优先": "A有Q3、FY2027目标和下一代项目验证",
            "价格确认/动量": "A前期涨幅确认AI制造重估",
            "激进短线": "A高IV叠加AI rack事件弹性",
        }[strat]
    if winner == "B":
        if ticker in DIRECT_EMS_PEERS or category == "AI服务器_存储_EMS":
            return {
                "NTM兑现优先": "B同业订单或AI服务器兑现更硬",
                "右尾弹性优先": "B同业小基数或客户项目弹性更大",
                "风险调整收益": "B同业上行下行组合更优",
                "下行保护优先": "B同业波动、现金流或压力期更稳",
                "估值消化优先": "B同业倍数更易被业绩消化",
                "近端催化优先": "B同业订单/财报催化更近",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业短线爆发力更强",
            }[strat]
        if ticker in POWER_COOLING_CHAIN or category in INFRA_CATS:
            return {
                "NTM兑现优先": "B电力/冷却订单兑现更短链",
                "右尾弹性优先": "B电力或冷却瓶颈右尾更直接",
                "风险调整收益": "B订单可见度和利润池更优",
                "下行保护优先": "B现金流、长约或公用属性更稳",
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
        if at == bt:
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"
    diff = a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0)
    tier_gap = tier_value(at) - tier_value(bt)
    abs_diff = abs(diff)
    if abs_diff < 4:
        return "中性"
    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 26, 13, 4
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
    ac, bc = row_obj["ac"], row_obj["bc"]
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
            return "SANM的低P/S和ZT增长使估值消化更有吸引力。"
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 10:
            return "SANM的Core IMS/CPS、现金流和压力期表现更稳。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:
            return "SANM的ZT已确认收入和FY2026指引使NTM兑现更清楚。"
        return "SANM在估值、兑现和AI rack可收入化之间的组合更均衡。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 12:
        return f"{b['ticker']}的右尾或小基数弹性明显强于SANM。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 10:
        return f"{b['ticker']}的NTM订单/收入兑现证据更强。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 12:
        return f"{b['ticker']}的现金流、波动或压力期防御明显优于SANM。"
    return f"{b['ticker']}在多数投资思路下比SANM更符合该资金目标。"


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
    missing_fin = sorted(
        [
            ticker
            for ticker, company in companies.items()
            if not company.get("fin") or not company.get("fin", {}).get("price")
        ]
    )
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

    strong_b = majority_rows(comparisons, "B", 45)
    strong_a = majority_rows(comparisons, "A", 45)
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "B")
    final_neutral = len(comparisons) - final_a - final_b
    a_side = {
        strat: stats[strat]["强烈建议投A"] + stats[strat]["建议投A"] + stats[strat]["微倾向投A"]
        for strat in STRATS
    }
    b_side = {
        strat: stats[strat]["微倾向投B"] + stats[strat]["建议投B"] + stats[strat]["强烈建议投B"]
        for strat in STRATS
    }
    a_best = sorted(STRATS, key=lambda strat: a_side[strat] - b_side[strat], reverse=True)[:2]
    a_worst = sorted(STRATS, key=lambda strat: a_side[strat] - b_side[strat])[:2]

    product_names = []
    for product in a.get("products", [])[:6]:
        product_names.append(str(product[0]).split("：")[0])

    support = {
        "NTM兑现优先": (
            "中上档",
            "FY2026 Q2收入40.13亿美元、ZT收入18.8亿美元、FY2026收入指引137-143亿美元、NTM基准收入145-158亿美元",
            "Q3 ZT指引10-12亿美元低于Q2，且公司不披露传统backlog/book-to-bill或分客户订单",
        ),
        "右尾弹性优先": (
            "中上档",
            "乐观/极度乐观收入165-185亿美元/200-230亿美元，来自AI rack、accelerated compute、power/liquid cooling/test cell能力",
            "EMS收入含大量低毛利BOM pass-through，缺多客户订单金额和独立服务定价",
        ),
        "风险调整收益": (
            "强势档",
            "P/S 1.20、Forward PE 19.46、Q2 FCF强，AI rack增量和估值消化仍有组合赔率",
            "TTM PE 53.81、Call IV 81.0%，客户集中、营运资本和低毛利制造会抵消上行",
        ),
        "下行保护优先": (
            "中性档",
            "Core IMS/CPS底座、Q2 FCF 3.42亿美元、三段SOXX压力累计-38.88%优于多数高beta AI硬件",
            "AI rack工作资本、客户排产、部件短缺和IV偏高使其不是防御型资产",
        ),
        "估值消化优先": (
            "强势档",
            "P/S 1.20、Forward PE 19.46，对应FY2026/FY2027收入台阶和ZT并表增长，估值不如高beta主链拥挤",
            "如果收入增长主要来自低毛利pass-through，利润和FCF消化会慢于收入消化",
        ),
        "近端催化优先": (
            "强势档",
            "Q3 FY2026、FY2027 16B+目标、下一代accelerated compute从pre-production转production、ZT收入恢复节奏可在1-2季验证",
            "Q3 ZT低于Q2说明前移和块状性，若连续低于10-12亿美元会伤害催化",
        ),
        "价格确认/动量": (
            "中档",
            "2026-06-03口径两周+22.29%、一月+26.63%，市场已经确认ZT/AI制造重估",
            "2026-06-22收盘253.45低于6月3日282.72，短期动量不如PENG/DELL/HPE等高beta同业",
        ),
        "激进短线": (
            "弱势档",
            "Call IV 81.0%、AI rack/ZT/AMD生态叙事和FY2027目标使事件交易弹性存在",
            "相对小盘光互联、NeoCloud、核电和电力设备，关注度和非线性爆发力仍不足",
        ),
    }

    file_list = "；".join(
        [f"{ticker}:{Path(companies[ticker]['path']).name}" for ticker in sorted(companies)]
    )

    lines: list[str] = []
    lines.append("# SANM 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：SANM / {TARGET_NAME}")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(comparisons)}")
    lines.append(f"公司评估文件日期范围：{date_range}")
    lines.append("日度数据日期：2026-06-22 金融数据；2026-06-03 区间涨跌；2026-06-04 SOXX 压力窗口")
    lines.append("")
    lines.append("> 口径说明：本报告读取 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/公司索引.md`、SANM正式公司调研、相关正式行业调研和 `金融资料/` 金融及区间涨跌文件；未读取、引用或继承 `特征量化/`、Signals、回归、模型比较、`公司排序/`、`简单排序/`、备份目录或临时结果。每一行是 SANM 与一家项目内公司 B 的二选一判断。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.append(f"- A 最占优的投资思路：`{'`、`'.join(a_best)}`。SANM最强的是风险调整、估值消化和NTM兑现的组合：ZT并表带来AI rack收入台阶，但P/S仍只有约1.2倍，且Core IMS/CPS与Q2 FCF提供缓冲。")
    lines.append(f"- A 最吃亏的投资思路：`{'`、`'.join(a_worst)}`。主要短板是右尾和短线动量不如高beta同业/AI主链，且ZT Q3低于Q2暴露季度前移和项目块状性。")
    lines.append("- A 最适合的投资者画像：想要AI rack/accelerated compute制造收入兑现，但同时重视估值消化、现金流和不愿买极端高估值AI主链的风险调整型资金。")
    lines.append("- A 最不适合的投资者画像：只追求最高右尾、最强价格动量、芯片/IP高毛利利润池或极端短线爆发的进攻型资金。")
    lines.append("- 多数思路下最强反方公司：" + "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]]) + "。这些公司通常在AI主链利润池、订单/RPO、右尾弹性、价格确认或电力/光互联瓶颈上强于SANM。")
    lines.append(f"- 如果只追求更高增长、更好公司，A 的总体位置：SANM是项目内中上游的AI制造兑现型标的，不是全项目最强右尾；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家。")
    lines.append("- 后续最重要跟踪数据：ZT当季收入是否从Q3 10-12亿美元恢复；FY2027 16B+目标是否转为正式指引；下一代accelerated compute production revenue；客户/平台是否从AMD扩展到更多hyperscaler或ASIC rack；CPS收入和毛利率；non-GAAP OPM；库存、应收、客户预付款、CapEx和FCF；power/liquid cooling/test cell扩产利用率。")
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | SANM |")
    lines.append(f"| 公司名称 | {TARGET_NAME} |")
    lines.append(f"| 产业链分类 | {a.get('category', 'AI服务器_存储_EMS')} |")
    lines.append(f"| 重要产品/业务线 | {'；'.join(product_names) if product_names else 'ZT / accelerated compute制造与整柜集成；Core IMS excluding ZT；CPS高端部件、产品与服务；Power / liquid cooling / test cell / burn-in能力'} |")
    lines.append(f"| NTM 基准收入 | {a.get('base_rev') or '$14.5B-$15.8B'} |")
    lines.append(f"| 乐观/极度乐观收入 | 乐观：{a.get('bull_rev') or '$16.5B-$18.5B'}；极度乐观：{a.get('extreme_rev') or '$20.0B-$23.0B'} |")
    lines.append(f"| 利润和现金流结论 | 基准经营利润率：{a.get('base_margin') or 'non-GAAP 6.3%-6.8%'}；利润/现金流：{a.get('base_profit') or 'EBITDA近似$1.05B-$1.30B'}；{a.get('base_cash') or 'FCF约$0.35B-$0.65B，取决于库存/应收/客户预付款'} |")
    lines.append("| 最大传导瓶颈 | ZT的客户排产、下一代accelerated compute从pre-production转production、关键部件到货、整柜测试/液冷/电源联调和收入确认节奏。 |")
    lines.append("| 最大反证 | Q3 ZT指引10-12亿美元低于Q2的18.8亿美元；无公开backlog/book-to-bill；低毛利BOM pass-through可能让收入上修弱于利润上修；营运资本可能吞噬FCF。 |")
    lines.append("| 近端催化剂 | Q3 FY2026收入与ZT收入、FY2027 16B+目标转指引、下一代accelerated compute production revenue、多客户AI rack、CPS毛利率和FCF。 |")
    lines.append("| 日度数据 | " + daily_snapshot + " |")
    lines.append("")
    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append("| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for strat in STRATS:
        tier = a.get("tiers", {}).get(strat, "资料不足")
        position = f"{support[strat][0]}；评分排名 {a.get('ranks', {}).get(strat)}/{len(companies)}"
        lines.append(f"| {strat} | {tier} | {position} | {support[strat][1]} | {support[strat][2]} |")
    lines.append("")
    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | AI服务器/存储/EMS、ODM/OEM、整机/机架集成和复杂系统制造同池比较，优先看客户订单、收入兑现、毛利率、交付能力、营运资本和估值消化 | DELL、HPE、SMCI、PENG、JBL、FLEX、CLS、FN | 判断力度最高；同业中若一方订单、margin或估值明显更硬，可以给建议或强烈建议 |")
    lines.append("| 相邻替代 | 同属AI基础设施资金篮子但不完全同业，重点比较增长质量、兑现确定性、估值、催化和资金偏好 | MU、STX、WDC、PSTG、VRT、ETN、GEV、PWR、POWL、MOD | 保持中等力度；赛道更热不能自动胜出，必须有订单或收入传导证据 |")
    lines.append("| 上下游 | SANM的芯片/ASIC/GPU、交换、光互联、连接器、电源/液冷或云客户链条上下游，重点看利润池、议价权和谁捕获瓶颈价值 | AMD、NVDA、AVGO、MRVL、ANET、CIEN、CRDO、COHR、MSFT、AMZN、GOOGL、META | 不把下游收入规模或上游瓶颈自动等同于胜出；强调利润捕获、估值消化和反证 |")
    lines.append("| 跨赛道 | 半导体材料、前道设备、封测、工业/化工等与SANM业务差异大但可作为资金配置替代 | ASML、AMAT、LIN、ECL、TMO、DHR、CAT | 默认降低结论力度；除非增长质量、估值消化或下行保护明显拉开 |")
    lines.append("")
    lines.append("## 5. 全项目逐行投资思路决策表")
    lines.append("")
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要", *STRATS, "多数思路方向", "最终更值得投", "最关键理由"]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---:" if header == "序号" else "---" for header in headers]) + " |")
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
        need = "SANM需要披露更明确的ZT/FY2027订单、客户、backlog或production revenue，并证明AI rack增长能带来利润率和FCF改善。"
        lines.append(f"| {idx} | {base.md(row_obj['ticker'] + ' / ' + row_obj['name'])} | {'、'.join(wins[:6])} | {base.md(row_obj['key_reason'])} | {need} |")
    lines.append("")
    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for idx, row_obj in enumerate(strong_a, 1):
        wins = [strat for strat in STRATS if "投A" in row_obj[strat]]
        need = "B需要拿出更硬的NTM收入/利润兑现、客户订单、估值消化证据或价格确认，才能抵消SANM的ZT收入台阶和低P/S优势。"
        lines.append(f"| {idx} | {base.md(row_obj['ticker'] + ' / ' + row_obj['name'])} | {'、'.join(wins[:6])} | {base.md(row_obj['key_reason'])} | {need} |")
    lines.append("")
    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。")
    lines.append(f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告，同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}。")
    lines.append(f"- 公司全集最新正式评估文件清单：{file_list}")
    lines.append(f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据或价格的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。")
    lines.append("- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。")
    lines.append("- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md`、`公司调研/AI服务器_存储_EMS/SANM_Sanmina_Corporation_公司调研_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI服务器整机与机架集成_2026-06-10.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AI以太网交换系统与Fabric芯片_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`、`行业调研/AI网络_光互联_铜互联/行业调研_高速连接器、背板与结构化布线_2026-06-11.md`。")
    lines.append(f"- SANM 日度数据快照：{daily_snapshot}")
    lines.append("- 生成脚本：`scripts/generate_sanm_company_comparison.py`。")
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
                "size": OUT_PATH.stat().st_size,
                "sanm_tiers": {strat: a.get("tiers", {}).get(strat) for strat in STRATS},
                "sanm_ranks": {strat: a.get("ranks", {}).get(strat) for strat in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
