from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "EME"
TARGET_NAME = "EMCOR Group"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "EME_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL

DIRECT_PEERS = {
    "FIX",
    "IESC",
    "MYRG",
    "PWR",
}

INDUSTRIAL_ADJACENT = {
    "AAON",
    "ALLE",
    "CARR",
    "CAT",
    "CMI",
    "DCI",
    "DKILY",
    "DOV",
    "ECL",
    "FTV",
    "JCI",
    "MOD",
    "MSI",
    "NDSN",
    "PH",
    "PNR",
    "TMO",
    "TT",
    "TDY",
    "DHR",
    "DD",
    "MMM",
}

POWER_COOLING_ADJACENT = {
    "AEP",
    "BE",
    "BWXT",
    "CEG",
    "DTE",
    "ENS",
    "ET",
    "ETR",
    "FLNC",
    "GNRC",
    "OKLO",
    "PSIX",
    "RYCEY",
    "SMR",
    "VST",
}

UPSTREAM_EQUIPMENT = {
    "ABBNY",
    "AEIS",
    "ATKR",
    "ETN",
    "GEV",
    "HUBB",
    "HTHIY",
    "NVT",
    "POWL",
    "VRT",
}

PEER_SCORE_FLOORS = {
    # FIX and IESC use Chinese "亿美元" revenue ranges in the formal eval files.
    # The generic absolute-range parser can understate their growth scores, so
    # keep explicit floors tied to those formal assessments rather than letting
    # a unit parsing miss turn them into weak direct peers.
    "FIX": {
        "NTM兑现优先": 82,
        "右尾弹性优先": 84,
        "风险调整收益": 58,
        "下行保护优先": 70,
        "估值消化优先": 52,
        "近端催化优先": 78,
        "价格确认/动量": 48,
        "激进短线": 84,
    },
    "IESC": {
        "NTM兑现优先": 80,
        "右尾弹性优先": 86,
        "风险调整收益": 60,
        "下行保护优先": 64,
        "估值消化优先": 61,
        "近端催化优先": 80,
        "价格确认/动量": 68,
        "激进短线": 90,
    },
}

AI_DOWNSTREAM_OR_CUSTOMERS = {
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

SEMI_CHAIN = {
    "ACLS",
    "ACMR",
    "AMAT",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "BESIY",
    "CAMT",
    "COHU",
    "DSCSY",
    "FORM",
    "GFS",
    "ICHR",
    "IMOS",
    "KEYS",
    "KLAC",
    "KLIC",
    "LRCX",
    "MKSI",
    "NVMI",
    "ONTO",
    "PLAB",
    "TER",
    "TOELY",
    "TSM",
    "TSEM",
    "UCTT",
    "UMC",
    "VECO",
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def apply_global_floors(companies: dict[str, dict[str, object]]) -> None:
    for ticker, floors in {**calibrated.SCORE_FLOORS, **PEER_SCORE_FLOORS}.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[assignment]
            company["scores"][strategy] = max(current, floor)  # type: ignore[index]


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for strategy in STRATS:
        ordered = sorted(
            companies.items(),
            key=lambda item: item[1].setdefault("scores", {}).get(strategy, 0),  # type: ignore[union-attr]
            reverse=True,
        )
        total = len(ordered)
        for rank, (_ticker, company) in enumerate(ordered, start=1):
            pct = rank / total
            if pct <= 0.07:
                tier = "S"
            elif pct <= 0.25:
                tier = "A"
            elif pct <= 0.55:
                tier = "B"
            elif pct <= 0.85:
                tier = "C"
            else:
                tier = "D"
            company.setdefault("tiers", {})[strategy] = tier  # type: ignore[index]
            company.setdefault("ranks", {})[strategy] = rank  # type: ignore[index]

    for company in companies.values():
        if not company.get("fin", {}).get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    calibrated.fix_growth_ranges(companies)
    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target
    apply_global_floors(companies)

    eme = companies[TARGET]
    # EME calibration from its 2026-06-12 formal assessment and 2026-06-22 daily data:
    # strong FY2026 guidance, Q1 +19.7% revenue growth, $15.62B RPO and net-cash balance
    # support NTM/catalyst/valuation quality. Right-tail and short-line beta are capped by
    # engineering-services economics, undisclosed AI-only revenue, weak recent momentum and
    # working-capital pressure.
    calibrated_scores = {
        "NTM兑现优先": 74.0,
        "右尾弹性优先": 60.0,
        "风险调整收益": 62.0,
        "下行保护优先": 76.0,
        "估值消化优先": 68.0,
        "近端催化优先": 70.0,
        "价格确认/动量": 34.0,
        "激进短线": 68.0,
    }
    for strategy, score in calibrated_scores.items():
        eme.setdefault("scores", {})[strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in UPSTREAM_EQUIPMENT:
        return "上下游"
    if ticker in INDUSTRIAL_ADJACENT or ticker in POWER_COOLING_ADJACENT:
        return "相邻替代"
    if ticker in AI_DOWNSTREAM_OR_CUSTOMERS or ticker in SEMI_CHAIN:
        return "上下游"
    if category in {"机电_冷却_工程_水处理_边缘工业AI", "配电_电源_功率器件", "电力_发电_能源_储能"}:
        return "相邻替代"
    if category in {
        "AI服务器_存储_EMS",
        "AI网络_光互联_连接器",
        "AI计算芯片_EDA_IP_custom_ASIC",
        "云算力_IDC_AI软件平台",
        "晶圆制造_前道设备",
        "封测_检测_计量_光罩",
    }:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str, company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    if tag == "中性":
        if rel == "跨赛道":
            return "业务差异较大且档位接近"
        return "档位接近需继续验证"

    a_win = tag.endswith("投A")
    if a_win:
        if strategy == "NTM兑现优先":
            return "EME RPO和FY2026指引更硬"
        if strategy == "右尾弹性优先":
            return "EME机电交付瓶颈仍有上修"
        if strategy == "风险调整收益":
            return "EME增长、估值和净现金更均衡"
        if strategy == "下行保护优先":
            return "EME净现金和多元项目底盘更稳"
        if strategy == "估值消化优先":
            return "EME低P/S和NTM利润能消化估值"
        if strategy == "近端催化优先":
            return "EME Q2/Q3 RPO和指引验证更近"
        if strategy == "价格确认/动量":
            return "EME估值不高但价格仍待确认"
        return "EME有AI机电工程事件弹性"

    if strategy == "NTM兑现优先":
        if rel == "直接同业":
            return f"{ticker}同业收入或backlog兑现更硬"
        return f"{ticker}订单/RPO/backlog或收入兑现更强"
    if strategy == "右尾弹性优先":
        return f"{ticker}核心AI或小基数右尾更大"
    if strategy == "风险调整收益":
        return f"{ticker}上行与下行组合更优"
    if strategy == "下行保护优先":
        return f"{ticker}现金流或压力期表现更安全"
    if strategy == "估值消化优先":
        return f"{ticker}业绩增速更能覆盖估值"
    if strategy == "近端催化优先":
        return f"{ticker}近端订单/RPO或产品催化更强"
    if strategy == "价格确认/动量":
        return f"{ticker}价格确认和资金偏好更强"
    return f"{ticker}高波动和主题beta更适合短线"


def label_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    at = a["tiers"][strategy]  # type: ignore[index]
    bt = b["tiers"][strategy]  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        tag = "中性"
    else:
        tier_diff = tier_value(str(at)) - tier_value(str(bt))
        score_diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
        if score_diff >= 28 or tier_diff >= 3:
            tag = "强烈建议投A"
        elif score_diff >= 13 or tier_diff >= 2:
            tag = "建议投A"
        elif score_diff >= 5:
            tag = "微倾向投A"
        elif score_diff <= -28 or tier_diff <= -3:
            tag = "强烈建议投B"
        elif score_diff <= -13 or tier_diff <= -2:
            tag = "建议投B"
        elif score_diff <= -5:
            tag = "微倾向投B"
        else:
            tag = "中性"

        if rel == "跨赛道":
            if tag == "强烈建议投A" and not (score_diff >= 38 or tier_diff >= 4):  # type: ignore[name-defined]
                tag = "建议投A"
            elif tag == "强烈建议投B" and not (score_diff <= -38 or tier_diff <= -4):  # type: ignore[name-defined]
                tag = "建议投B"
            elif tag == "建议投A" and abs(score_diff) < 18 and abs(tier_diff) < 2:  # type: ignore[name-defined]
                tag = "微倾向投A"
            elif tag == "建议投B" and abs(score_diff) < 18 and abs(tier_diff) < 2:  # type: ignore[name-defined]
                tag = "微倾向投B"

        if rel == "直接同业" and tag.startswith("建议") and abs(score_diff) >= 18:  # type: ignore[name-defined]
            tag = "强烈" + tag

    return tag


def cell_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    tag = label_for(strategy, a, b, rel)
    return f"{tag}：{reason_for(strategy, tag, rel, b)}"


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


def direction_counts(cells: list[str]) -> tuple[int, int, int]:
    a_count = 0
    b_count = 0
    neutral = 0
    for cell in cells:
        tag = tag_in_cell(cell) or "中性"
        if tag.endswith("投A"):
            a_count += 1
        elif tag.endswith("投B"):
            b_count += 1
        else:
            neutral += 1
    return a_count, b_count, neutral


def final_choice(a: dict[str, object], b: dict[str, object], cells: list[str]) -> str:
    a_count, b_count, _neutral = direction_counts(cells)
    if a_count >= b_count + 2:
        return "A"
    if b_count >= a_count + 2:
        return "B"
    risk_diff = a["scores"]["风险调整收益"] - b["scores"]["风险调整收益"]  # type: ignore[index,operator]
    if abs(risk_diff) >= 4:
        return "A" if risk_diff > 0 else "B"
    return "A" if a["scores"]["估值消化优先"] >= b["scores"]["估值消化优先"] else "B"  # type: ignore[index,operator]


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    ticker = str(b["ticker"])
    if final == "A":
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 12:  # type: ignore[index,operator]
            return "EME的净现金、多元项目和低P/S提供更好下行保护。"
        if a["scores"]["风险调整收益"] - b["scores"]["风险调整收益"] > 10:  # type: ignore[index,operator]
            return "EME在RPO能见度、估值和执行质量之间更均衡。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
            return "EME约2x P/S和FY2026业绩路径更容易消化当前估值。"
        return "EME有真实RPO、FY2026指引和AI机电交付瓶颈，对手证据不足以压过。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{ticker}的核心AI收入或小基数右尾明显强于EME。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的订单/RPO/backlog或收入确认证据比EME更硬。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的价格确认和短线资金偏好强于EME。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的现金流、防御性或压力期表现明显优于EME。"
    return f"{ticker}在多数投资思路下比EME更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong: list[str] = []
    b_strong: list[str] = []
    close: list[str] = []
    for strategy in STRATS:
        diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
        short = strategy.replace("/", "")
        if diff >= 8:
            a_strong.append(short)
        elif diff <= -8:
            b_strong.append(short)
        else:
            close.append(short)
    return (
        f"A强：{base.md('、'.join(a_strong[:3]) or '无')}；"
        f"B强：{base.md('、'.join(b_strong[:3]) or '无')}；"
        f"接近：{base.md('、'.join(close[:3]) or '无')}"
    )


def comparison_order(item: dict[str, object]) -> tuple[int, str, str]:
    rel_rank = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    b = item["b"]
    return (rel_rank.get(str(item["rel"]), 9), str(b["category"]), str(b["ticker"]))  # type: ignore[index]


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    output: list[dict[str, object]] = []
    for ticker in sorted(companies):
        if ticker == TARGET:
            continue
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(strategy, a, b, rel) for strategy in STRATS]
        ac, bc, nc = direction_counts(cells)
        final = final_choice(a, b, cells)
        output.append(
            {
                "ticker": ticker,
                "b": b,
                "rel": rel,
                "cells": cells,
                "ac": ac,
                "bc": bc,
                "nc": nc,
                "final": final,
                "summary": grade_diff_summary(a, b),
                "reason": key_reason(a, b, final),
            }
        )
    return sorted(output, key=comparison_order)


def fmt_num(value: object, decimals: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{decimals}f}"
    except Exception:
        return str(value)


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"${float(value):.2f}B"
    except Exception:
        return str(value)


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):+.2f}%"
    except Exception:
        return str(value)


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def top_majority(comparisons: list[dict[str, object]], final: str, limit: int = 40) -> list[dict[str, object]]:
    if final == "B":
        rows = [c for c in comparisons if c["bc"] >= 5 and c["bc"] - c["ac"] >= 3]  # type: ignore[operator]
        return sorted(rows, key=lambda c: (c["bc"] - c["ac"], c["b"]["scores"]["右尾弹性优先"]), reverse=True)[:limit]  # type: ignore[index,operator]
    rows = [c for c in comparisons if c["ac"] >= 5 and c["ac"] - c["bc"] >= 3]  # type: ignore[operator]
    return sorted(rows, key=lambda c: (c["ac"] - c["bc"], c["b"]["scores"]["下行保护优先"]), reverse=True)[:limit]  # type: ignore[index,operator]


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(company_dates)} 至 {max(company_dates)}"
    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][tag_in_cell(cell)] += 1
    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b_rows = top_majority(comparisons, "B")
    strong_a_rows = top_majority(comparisons, "A")
    final_a = sum(1 for c in comparisons if c["final"] == "A")
    final_b = sum(1 for c in comparisons if c["final"] == "B")
    missing_fin = [ticker for ticker in sorted(companies) if not companies[ticker]["fin"]]

    fin = a.get("fin", {})
    mom2 = a.get("mom2", {})
    mom1 = a.get("mom1", {})
    soxx = a.get("soxx", {})
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]

    product_names = [
        "N&C电气/低压/数据中心电气施工",
        "N&C机械/冷却/数据中心MEP",
        "其他美国电气与机械工程",
        "Building Services HVAC retrofit/controls/O&M",
        "Industrial Services",
    ]

    support = {
        "NTM兑现优先": (
            "2026Q1收入+19.7%、有机+16.8%，FY2026收入/OM/EPS指引上修，RPO 156.2亿美元且一年内确认121.7亿美元",
            "RPO到收入仍受设备交期、劳动力、许可、验收和营运资本节奏约束",
        ),
        "右尾弹性优先": (
            "AI数据中心time-to-power、time-to-cool、MEP和commissioning瓶颈使N&C电气/机械仍有上修空间",
            "公司不披露AI-only收入或订单，且工程服务不拥有GPU、UPS、变压器、CDU等硬件ASP",
        ),
        "风险调整收益": (
            "P/S 2.18、Forward PE 26.60、净现金、RPO和基准收入增速形成较均衡组合",
            "股价已给高质量承包平台溢价，Q1经营现金流几乎持平，FCF转化仍需验证",
        ),
        "下行保护优先": (
            "净现金、极低债务、多元非住宅项目和Building Services稳定层提供基本防守",
            "SOXX三段压力窗口累计-54.09%，Call IV 42.7%，项目制营运资本会放大回撤",
        ),
        "估值消化优先": (
            "2.18x P/S、26.60x Forward PE与基准收入188-196亿美元、OM 9.0%-9.4%匹配度较好",
            "若RPO只带来低毛利pass-through或现金流持续落后净利润，估值消化会下修",
        ),
        "近端催化优先": (
            "Q2/Q3 2026 RPO、N&C增长、Electrical/Mechanical margin、Miller协同和FY2026指引是近端验证点",
            "缺少AI-only backlog和客户项目金额，催化更偏财报/RPO验证而非单一产品发布",
        ),
        "价格确认/动量": (
            "2026-06-22价格868.88高于6月初839.54，估值没有明显泡沫化",
            "2026-06-03过去两周-1.60%、过去一月-7.08%，趋势确认显著弱于AI主链和高beta电力股",
        ),
        "激进短线": (
            "AI数据中心工程交付、Miller整合和RPO再创新高可带来事件弹性",
            "工程服务基数大、价格动量弱，短线爆发力不如光互联、NeoCloud、AI芯片和高IV电力设备",
        ),
    }

    out: list[str] = []
    out += [
        "# EME 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：EME / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 EME vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。EME 的优势来自 FY2026 指引、156.2亿美元 RPO、一年内可确认 RPO、净现金和较低 P/S，而不是最高右尾。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 AI-only 收入/订单未披露、工程服务利润率不会像硬件垄断品一样非线性扩张，且近期价格确认弱。",
        "- A 最适合的投资者画像：希望配置 AI 数据中心电气/机械/MEP 交付瓶颈，同时更重视可见订单、估值消化和资产负债表质量的中期资金。",
        "- A 最不适合的投资者画像：只追求最高收入增速、最大小市值右尾、强价格爆发、或短期高IV主题弹性的进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]])}。这些公司通常拥有更直接AI主链收入、硬件利润池、订单/RPO/backlog、数据中心电力设备稀缺性或更强价格确认。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：EME 是项目内偏强的AI物理基础设施执行端标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家。它明显强于不少估值消化弱、现金流薄或兑现不足的公司，但面对NVDA/AVGO/MU/ALAB/ETN/GEV/POWL/VRT等核心AI硬件、电力设备或平台标的通常不占右尾优势。",
        "- 后续最重要跟踪数据：季度 RPO 总额及分部RPO、一年内RPO占比、Network and Communications 是否继续作为最大RPO增量、Electrical/Mechanical收入和margin、Miller Electric整合、合同资产/应收/预付款、经营现金流转化、FY2026 revenue/OM/EPS 指引调整，以及大型AI campus开工/验收节奏。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "EME"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "$8.65-8.90B"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "从RPO到revenue的项目交付链条：电力设备、熟练工、现场许可、commissioning、客户验收和收款节奏必须同步。"]),
        base.row(["最大反证", "公司不披露AI-only数据中心收入、订单或RPO；若N&C增长失速、margin下滑或经营现金流连续落后净利润，乐观情景需要下修。"]),
        base.row(["近端催化剂", "Q2/Q3 2026 RPO、N&C增长、Electrical/Mechanical revenue和margin、Miller协同、合同资产/应收、经营现金流和FY2026指引更新。"]),
        base.row([
            "日度市场数据",
            f"2026-06-22 收盘价 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，P/S {fmt_num(fin.get('ps'))}，P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。",
        ]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        out.append(base.row([strategy, a["tiers"][strategy], rank_text[strategy], support[strategy][0], support[strategy][1]]))  # type: ignore[index]

    out += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与EME在电气施工、MEP、专业承包、数据中心工程交付或公用事业/高科技项目施工上重叠，优先比较backlog/RPO、收入burn、margin、项目质量和现金流。", "FIX、IESC、MYRG、PWR", "同业证据权重最高；若对手在backlog转收入、利润率或价格确认上明显胜出，可给建议或强烈建议。"]),
        base.row(["相邻替代", "同属AI数据中心物理基础设施、电力、冷却、工业自动化或高质量工业资金篮子，但产品和利润池不完全相同。", "CARR、TT、JCI、DOV、MOD、CEG、VST、AEP、DTE", "重点回答资金只能买一个时，谁的增长质量、估值消化、现金流和近端催化更好。"]),
        base.row(["上下游", "B是EME工程交付的上游设备商、下游云/IDC/服务器客户、或同一AI建设需求链中的芯片/网络/半导体设备信号。", "ETN、VRT、POWL、HUBB、NVDA、AVGO、MSFT、AMZN、DELL、SMCI、ASML", "不把下游规模或上游硬件稀缺自动等同EME利润池，核心看议价权、订单硬度、收入确认和利润捕获。"]),
        base.row(["跨赛道", "业务差异较大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "材料、化学品、软件、存储、航天和部分平台公司", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    out.append(base.row(headers))
    out.append(base.row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for index, comparison in enumerate(comparisons, start=1):
        b = comparison["b"]
        out.append(
            base.row(
                [
                    index,
                    base.short_name(b),  # type: ignore[arg-type]
                    base.category_short(str(b["category"])),
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],  # type: ignore[list-item]
                    majority(comparison["ac"], comparison["bc"], comparison["nc"]),  # type: ignore[arg-type]
                    comparison["final"],
                    comparison["reason"],
                ]
            )
        )

    out += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        out.append(base.row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要EME把RPO继续转成高质量收入和margin，并披露更清晰的N&C/数据中心订单、收入或现金流转化。"
        if comparison["rel"] == "直接同业":
            need = "需要EME在工程/MEP同业中证明RPO增长、收入burn、margin和现金流转化强于B。"
        elif comparison["rel"] == "上下游":
            need = "需要EME证明自己能从上游设备和下游云厂CapEx中捕获更高利润，而不只是施工收入跟随。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B提高收入确认可信度、现金流质量和估值消化能力，或出现明确订单/指引上修。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要B把右尾叙事转成可确认收入/利润，并降低估值、现金流或波动反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/机电_冷却_工程_水处理_边缘工业AI/EME_EMCOR Group_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_液冷小组件与流体控制_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心风冷、冷水机组与HVAC_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_eme_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用既有正式脚本的最低分校准，对EME的FY2026指引、156.2亿美元RPO、一年内可确认RPO、N&C工程交付瓶颈、净现金、低P/S、弱价格动量、AI-only披露缺口和营运资本反证做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
        "",
        "### 公司全集最新正式评估文件清单",
        "",
        base.row(["股票代号", "公司名称", "评估日期", "正式评估文件"]),
        base.row(["---", "---", "---", "---"]),
    ]
    for ticker in sorted(companies):
        company = companies[ticker]
        out.append(base.row([ticker, company["name"], company["date"], f"`分析报告/公司评估/结果/{company['path'].name}`"]))  # type: ignore[index,union-attr]

    out.append("")
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 EME 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "eme_tiers": {strategy: companies[TARGET]["tiers"].get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
        "eme_scores": {strategy: round(companies[TARGET]["scores"][strategy], 2) for strategy in STRATS},  # type: ignore[index]
        "eme_ranks": {strategy: companies[TARGET]["ranks"].get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
