from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "DTE"
TARGET_NAME = "DTE Energy Company"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "DTE_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL

LOCAL_SCORE_FLOORS = {
    # CEG is a direct power peer for DTE. Its own formal company-comparison
    # generator calibrates it as a high-quality AI power and nuclear scarcity
    # compounder; apply that floor here so DTE does not over-win because CEG's
    # revenue ranges are hard for the generic parser.
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
}

DIRECT_PEERS = {
    "AEP",
    "CEG",
    "ETR",
    "VST",
}

INDUSTRIAL_ADJACENT = {
    "ALLE",
    "AAON",
    "CAT",
    "CMI",
    "CARR",
    "DCI",
    "DKILY",
    "ECL",
    "EME",
    "FIX",
    "FTV",
    "IESC",
    "JCI",
    "MOD",
    "MSI",
    "MYRG",
    "NDSN",
    "PH",
    "PNR",
    "TMO",
    "TT",
    "TDY",
    "DHR",
    "DD",
    "MMM",
    "DOV",
}

POWER_COOLING_ADJACENT = {
    "ABBNY",
    "AEIS",
    "ATKR",
    "BE",
    "BWXT",
    "ENS",
    "ENPH",
    "ET",
    "ETN",
    "FCEL",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "NVT",
    "NVTS",
    "OKLO",
    "POWI",
    "POWL",
    "PSIX",
    "PWR",
    "RYCEY",
    "SMR",
    "VRT",
    "WOLF",
    "AMPX",
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
    "TSM",
    "TSLA",
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
    for ticker, floors in {**calibrated.SCORE_FLOORS, **LOCAL_SCORE_FLOORS}.items():
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
    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target
    apply_global_floors(companies)

    dte = companies[TARGET]
    # DTE calibration from its 2026-06-12 formal assessment and 2026-06-22 daily data:
    # the regulated utility base, FY2026 operating earnings guidance, Oracle contract,
    # Google MPSC path and low IV support defensiveness and moderate NTM visibility.
    # Growth, right-tail and short-line beta remain capped by regulatory return,
    # high capex, equity issuance and delayed data-center load ramp.
    calibrated_scores = {
        "NTM兑现优先": 63.0,
        "右尾弹性优先": 45.0,
        "风险调整收益": 54.0,
        "下行保护优先": 91.0,
        "估值消化优先": 61.0,
        "近端催化优先": 63.0,
        "价格确认/动量": 38.0,
        "激进短线": 60.0,
    }
    for strategy, score in calibrated_scores.items():
        dte.setdefault("scores", {})[strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in INDUSTRIAL_ADJACENT or ticker in POWER_COOLING_ADJACENT:
        return "相邻替代"
    if ticker in AI_DOWNSTREAM_OR_CUSTOMERS:
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
            return "DTE受监管指引和Oracle合同更稳"
        if strategy == "右尾弹性优先":
            return "DTE数据中心负荷期权更清楚"
        if strategy == "风险调整收益":
            return "DTE低IV低PS且有合同保护"
        if strategy == "下行保护优先":
            return "DTE公用事业底盘和低IV更安全"
        if strategy == "估值消化优先":
            return "DTE约17.6x远期PE有业绩支撑"
        if strategy == "近端催化优先":
            return "DTE有Google审批和rate case节点"
        if strategy == "价格确认/动量":
            return "DTE价格修复但未明显过热"
        return "DTE数据中心电力事件弹性略优"

    if strategy == "NTM兑现优先":
        if rel == "直接同业":
            return f"{ticker}同业收入或订单兑现更硬"
        return f"{ticker}订单/RPO/backlog或收入兑现更强"
    if strategy == "右尾弹性优先":
        if rel == "直接同业":
            return f"{ticker} 电力长约/容量右尾更直接"
        return f"{ticker}核心AI或小基数右尾更大"
    if strategy == "风险调整收益":
        return f"{ticker}上行与下行组合更优"
    if strategy == "下行保护优先":
        return f"{ticker}现金流或压力期表现更安全"
    if strategy == "估值消化优先":
        return f"{ticker}业绩增速更能覆盖估值"
    if strategy == "近端催化优先":
        if rel == "直接同业":
            return f"{ticker} PPA/容量/核电催化更直接"
        return f"{ticker}近端订单或产品催化更强"
    if strategy == "价格确认/动量":
        return f"{ticker}价格确认和资金偏好更强"
    if rel == "直接同业":
        return f"{ticker} 电力主题beta更适合短线"
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
            return "DTE的低IV、受监管利润和压力期表现提供更好下行保护。"
        if a["scores"]["风险调整收益"] - b["scores"]["风险调整收益"] > 10:  # type: ignore[index,operator]
            return "DTE在合同能见度、低估值和下行保护之间更均衡。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
            return "DTE约17.6x远期PE和低P/S更容易由FY2026 operating EPS消化。"
        return "DTE有受监管utility底盘、Oracle/Google负荷期权和低波动，对手证据不足以压过。"
    if ticker in DIRECT_PEERS:
        if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
            return f"{ticker}的核电/容量/PPA或数据中心供电右尾比DTE更直接。"
        if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
            return f"{ticker}的2026兑现、发电资产或合同证据比DTE更硬。"
        if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
            return f"{ticker}的电力主题价格确认和资金偏好强于DTE。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{ticker}的核心AI收入或小基数右尾明显强于DTE。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的订单/RPO/backlog或收入确认证据比DTE更硬。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的价格确认和短线资金偏好强于DTE。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的现金流、防御性或压力期表现明显优于DTE。"
    return f"{ticker}在多数投资思路下比DTE更符合项目内资金配置目标。"


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

    product_names = []
    for product in a["products"][:8]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    support = {
        "NTM兑现优先": (
            "FY2026 operating earnings指引15.85-16.15亿美元，Electric/Gas受监管利润和Oracle 1.383GW合同支撑兑现",
            "基准收入相对TTM仅0%-4%增长，Google和额外pipeline在NTM内收入贡献有限",
        ),
        "右尾弹性优先": (
            "Oracle 1.383GW、Google 1.0GW和约5GW额外pipeline给2027-2030 rate base右尾",
            "受监管回报限制利润非线性，NTM上电、审批和融资节奏压制短期弹性",
        ),
        "风险调整收益": (
            "Forward PE 17.58、P/S 1.85、Call IV 23.2%，叠加低波动utility属性和数据中心负荷期权",
            "365亿美元五年capex、每年5-6亿美元股权发行和监管滞后会稀释上行",
        ),
        "下行保护优先": (
            "低IV、受监管Electric/Gas利润、客户粘性和SOXX压力窗口累计-5.13%明显优于高beta AI链",
            "自由现金流仍偏负，高capex、融资成本和rate case结果决定安全边际",
        ),
        "估值消化优先": (
            "低P/S、约17.6x远期PE和FY2026 operating EPS 7.59-7.73美元使估值消化压力可控",
            "低个位数基准增长和高资本开支使估值难靠短期爆发快速重估",
        ),
        "近端催化优先": (
            "Google MPSC路径、Oracle上电/billed load、DTE Electric rate case和Q2/Q3 operating earnings可验证",
            "多数数据中心收入和rate base兑现偏2027-2029，1-2个季度内更偏审批/进度信号",
        ),
        "价格确认/动量": (
            "2026-06-22价格146.83高于6月初141.81，低IV下有温和修复",
            "正式区间涨跌截至2026-06-03仍为两周-0.67%、一月-4.69%，动量弱于AI主链",
        ),
        "激进短线": (
            "Oracle/Google数据中心电力叙事若被审批或上电进度强化，存在事件重估",
            "Call IV仅23.2%，utility属性和监管回报使短线爆发力弱于NeoCloud、光互联和电力设备高beta",
        ),
    }

    out: list[str] = []
    out += [
        "# DTE 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：DTE / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 DTE vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。DTE 的相对优势来自低IV、受监管Electric/Gas利润、低P/S估值、FY2026 operating earnings指引和SOXX压力窗口表现。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是NTM收入基准仅低个位数增长、数据中心负荷收入偏2027-2029、自由现金流为负且短线beta弱于AI主链。",
        "- A 最适合的投资者画像：希望买电力/公用事业下行保护，同时获得Oracle、Google和额外hyperscaler负荷长期rate base期权的中期资金。",
        "- A 最不适合的投资者画像：只追求最高收入增速、最大右尾、小基数非线性利润杠杆或短期高IV爆发的进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]])}。这些公司通常拥有更直接AI主链收入、订单/RPO/backlog、数据中心电力设备利润池或更强价格确认。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：DTE 是项目内偏防御的电力负荷+数据中心rate base期权标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家。它强于不少高估值低兑现或现金流脆弱公司，但面对NVDA/AVGO/MU/ALAB/CRDO/FLNC/CEG/POWL/VRT等AI主链或电力高景气公司通常不占优。",
        "- 后续最重要跟踪数据：Google MPSC order及条件、Oracle energization/billed load、DTE Electric rate case、Q2/Q3 Electric revenue和sales MWh、capex/FFO-debt/equity issuance、DTE Vantage BTM项目、额外hyperscaler pipeline是否进入正式合同和监管申请。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "DTE"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`164-172 亿美元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "NTM内可上电、可监管批准、可成本回收、可融资的MW，而不是行业数据中心需求本身；Google仍需MPSC路径，额外pipeline尚未签约。"]),
        base.row(["最大反证", "数据中心售电包含燃料、购电、储能、输配电和折旧/融资成本，利润率不会像硬件/软件稀缺品一样非线性扩张；自由现金流仍偏负。"]),
        base.row(["近端催化剂", "Google MPSC审批和条件、Oracle上电/billed load、DTE Electric rate case、Q2/Q3 Electric operating earnings、capex和融资成本、额外hyperscaler合同进展。"]),
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
        base.row(["直接同业", "与DTE同属电力、公用事业或数据中心供电资金篮子，优先比较负荷增长、合同保护、rate base、监管风险、现金流和估值。", "AEP、ETR、CEG、VST", "同业证据权重最高；若对手在数据中心PPA、核电/发电利润池或监管兑现上明显更强，可放大到建议级别。"]),
        base.row(["相邻替代", "同属AI数据中心电力、配电、发电设备、储能、工程、冷却或物理基础设施链条，但商业模式和利润池不同。", "VRT、ETN、GEV、POWL、PWR、HUBB、NVT、TT、AAON、CARR", "重点回答资金只能买一个时，谁的增长质量、估值消化、下行保护和近端催化更好。"]),
        base.row(["上下游", "云厂、IDC、Neocloud、服务器和芯片平台是DTE数据中心用电需求的下游来源，部分也是资本开支周期的上游信号。", "ORCL、GOOGL、MSFT、AMZN、META、DLR、EQIX、CRWV、DELL、SMCI、NVDA", "不把下游客户规模直接等同DTE利润池，核心看负荷合同、成本回收、上电日期和DTE可捕获利润。"]),
        base.row(["跨赛道", "半导体设备、材料、封测、软件和部分工业公司与DTE业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益和估值消化。", "ASML、AMAT、LIN、ECL、TMO、ADBE、RKLB", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要DTE把Oracle/Google上电、MPSC审批、rate case和额外GW签约转成可确认收入、利润和rate base证据。"
        if comparison["rel"] == "直接同业":
            need = "需要DTE证明数据中心负荷、监管成本回收、EPS增长和估值消化优于电力直接同业。"
        elif comparison["rel"] == "上下游":
            need = "需要DTE证明自己能从下游AI负荷中捕获受监管回报，而不只是承担capex和融资压力。"
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
        "- 公司 A 公司调研文件：`公司调研/电力_发电_能源_储能/DTE_DTE_Energy_Company_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心开关设备与变压器_2026-06-10.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_dte_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用既有正式脚本的最低分校准，对DTE的FY2026 operating earnings、Oracle/Google数据中心负荷、MPSC/rate case节点、低IV、低P/S、价格动量、负FCF和高capex/融资约束做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
        raise SystemExit("缺少 DTE 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "dte_tiers": {strategy: companies[TARGET]["tiers"].get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
        "dte_scores": {strategy: round(companies[TARGET]["scores"][strategy], 2) for strategy in STRATS},  # type: ignore[index]
        "dte_ranks": {strategy: companies[TARGET]["ranks"].get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

