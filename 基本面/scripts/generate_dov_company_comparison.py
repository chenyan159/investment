from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "DOV"
TARGET_NAME = "Dover Corporation"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "DOV_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL

DIRECT_PEERS = {
    "AAON",
    "CARR",
    "DCI",
    "DKILY",
    "JCI",
    "MOD",
    "PNR",
    "TT",
}

INDUSTRIAL_ADJACENT = {
    "ALLE",
    "CAT",
    "CMI",
    "ECL",
    "EME",
    "FIX",
    "FTV",
    "IESC",
    "MSI",
    "MYRG",
    "NDSN",
    "PH",
    "TMO",
    "TDY",
    "DHR",
    "DD",
    "MMM",
}

POWER_COOLING_ADJACENT = {
    "ABBNY",
    "AEIS",
    "AEP",
    "ATKR",
    "BE",
    "BWXT",
    "CEG",
    "DTE",
    "ENS",
    "ET",
    "ETN",
    "ETR",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "NVT",
    "OKLO",
    "POWL",
    "PSIX",
    "PWR",
    "RYCEY",
    "SMR",
    "VRT",
    "VST",
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
    for ticker, floors in calibrated.SCORE_FLOORS.items():
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

    dov = companies[TARGET]
    # DOV calibration from its 2026-06-12 formal assessment and 2026-06-22 daily data:
    # it has strong order and cash-flow evidence, but AI exposure is still a small,
    # undisclosed product subset, and price momentum/short-line beta are not top tier.
    calibrated_scores = {
        "NTM兑现优先": 67.0,
        "右尾弹性优先": 58.0,
        "风险调整收益": 70.0,
        "下行保护优先": 80.0,
        "估值消化优先": 66.0,
        "近端催化优先": 63.0,
        "价格确认/动量": 50.0,
        "激进短线": 43.0,
    }
    for strategy, score in calibrated_scores.items():
        dov.setdefault("scores", {})[strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
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
            return "DOV订单和FY2026指引更稳"
        if strategy == "右尾弹性优先":
            return "DOV液冷小件仍有小基数放大"
        if strategy == "风险调整收益":
            return "DOV现金流、估值和低IV更均衡"
        if strategy == "下行保护优先":
            return "DOV多元工业底盘和低IV更安全"
        if strategy == "估值消化优先":
            return "DOV约20x远期PE有业绩支撑"
        if strategy == "近端催化优先":
            return "DOV有CST订单转收入验证点"
        if strategy == "价格确认/动量":
            return "DOV价格修复但未明显过热"
        return "DOV液冷订单线索提供事件弹性"

    if strategy == "NTM兑现优先":
        if rel == "直接同业":
            return f"{ticker}同业收入或订单兑现更硬"
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
        return f"{ticker}近端订单或产品催化更强"
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
            return "DOV的低IV、FCF和多元工业底盘提供更好下行保护。"
        if a["scores"]["风险调整收益"] - b["scores"]["风险调整收益"] > 10:  # type: ignore[index,operator]
            return "DOV在订单能见度、估值和现金流之间更均衡。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
            return "DOV约20x远期PE更容易由FY2026业绩和现金流消化。"
        return "DOV有真实液冷组件订单线索和工业现金流底盘，对手证据不足以压过。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{ticker}的核心AI收入或小基数右尾明显强于DOV。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的订单/RPO/backlog或收入确认证据比DOV更硬。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的价格确认和短线资金偏好强于DOV。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker}的现金流、防御性或压力期表现明显优于DOV。"
    return f"{ticker}在多数投资思路下比DOV更符合项目内资金配置目标。"


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
            "FY2026收入指引+5%-7%，Q1收入+10.1%，总book-to-bill 1.20，CST 1.57、PPS 1.11",
            "CPC/SWEP产品收入未拆，PPS organic仍为-0.8%，订单需转收入",
        ),
        "右尾弹性优先": (
            "CPC UQD和SWEP BPHE是液冷高可靠瓶颈件，直接AI收入可从小基数继续放大",
            "全公司基数约86-89亿美元，AI组件仍只是个位数占比，极度乐观条件多",
        ),
        "风险调整收益": (
            "Forward PE 19.84、P/S 3.73、Call IV 29.0%，FY2025 FCF超过11亿美元",
            "估值已反映高质量工业溢价，若CST订单不兑现则上行受限",
        ),
        "下行保护优先": (
            "低IV、多元工业底盘、强FCF、利息覆盖高，SOXX压力窗口累计-38.86%好于高beta链条",
            "工业周期、并购整合、库存和应收占用仍会削弱现金流安全边际",
        ),
        "估值消化优先": (
            "约20x远期PE可由FY2026 adjusted EPS和订单兑现消化，估值低于纯AI热管理/电力高beta",
            "收入增速不是顶级，若AI占比不能提升到8%-12%，估值仍回到普通工业股框架",
        ),
        "近端催化优先": (
            "Q2/Q3 2026 CST bookings转收入、PPS organic转正、SWEP扩产和CPC客户线索可验证",
            "缺少客户名单、产品级订单金额和统一backlog，催化清晰度弱于RPO/订单硬锚公司",
        ),
        "价格确认/动量": (
            "2026-06-22价格229.40高于6月初213.51，低IV下有温和修复",
            "2026-06-03过去两周仅+1.20%、过去一月-5.44%，动量弱于AI主链高beta",
        ),
        "激进短线": (
            "液冷、热交换和AI电力外溢若被管理层继续点名，存在事件重估",
            "Call IV仅29.0%，工业复合体属性强，短线爆发力不如光互联、NeoCloud和AI电力高beta",
        ),
    }

    out: list[str] = []
    out += [
        "# DOV 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：DOV / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 DOV vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。DOV 的相对优势来自低IV、强FCF、多元工业底盘、FY2026收入/EPS指引和CST/PPS订单能见度。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是AI收入没有产品级披露，CPC/SWEP仍是公司小基数增量，价格动量和激进短线beta弱于AI主链。",
        "- A 最适合的投资者画像：希望配置高质量工业现金流，同时获得AI液冷快接、热交换和电力链小而真实期权，但不想承担纯AI硬件高波动的资金。",
        "- A 最不适合的投资者画像：只追求最高收入增速、最大右尾、强订单/RPO硬锚、或短期高beta爆发的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]])}。这些公司通常拥有更直接AI主链收入、订单/RPO/backlog、数据中心电力/网络/芯片核心利润池或更强价格确认。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：DOV 是项目内中上游的质量型工业+AI冷却小组件标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家。它明显强于大量高估值低兑现或现金流较弱公司，但面对NVDA/AVGO/MU/ALAB/CRDO/FLNC/CEG/POWL/VRT等AI主链或电力高景气公司通常不占优。",
        "- 后续最重要跟踪数据：CST bookings、book-to-bill、heat exchanger订单转收入、PPS organic、CPC UQD06/UQD08/UQDB客户/AVL线索、SWEP扩产产能利用率、inventory/receivables、CST margin、FCF conversion，以及管理层是否量化data center cooling/thermal connector收入。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "DOV"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "$8.65-8.90B"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "CST的1.57x book-to-bill和longer lead-time heat exchanger orders能否按期转成SWEP/BPHE收入；CPC高流量快接能否从design-in或BOM指定转成可确认出货。"]),
        base.row(["最大反证", "DOV不披露CPC/SWEP产品级收入、客户名单、订单金额或统一backlog；PPS organic仍为负，AI液冷仍可能被传统工业周期抵消。"]),
        base.row(["近端催化剂", "Q2/Q3 2026 segment revenue、CST bookings和margin、PPS organic转正、SWEP扩产进度、CPC UQD系列客户/标准动态、working capital和FCF conversion。"]),
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
        base.row(["直接同业", "与DOV在HVAC/冷却、热交换、流体处理、过滤/水处理、楼宇机电或工业组件需求池重叠，优先比较订单、margin、客户质量、产品代际和估值。", "TT、JCI、CARR、AAON、MOD、DKILY、DCI、PNR", "同业证据权重最高；若对手在液冷、热管理、订单或利润率上明显胜出，可给建议或强烈建议。"]),
        base.row(["相邻替代", "同属AI数据中心物理基础设施、电力、工程、机电、工业自动化或高质量工业资金篮子，但产品不完全竞争。", "VRT、ETN、NVT、GEV、CEG、POWL、FIX、EME、PH、FTV", "重点回答资金只能买一个时，谁的增长质量、估值消化、现金流和近端催化更好。"]),
        base.row(["上下游", "B位于DOV液冷快接、热交换、线缆检测或数据中心建设需求链的上游/下游，如芯片、服务器、云厂、光互联、半导体设备和制造链。", "NVDA、AVGO、AMD、MSFT、AMZN、DELL、SMCI、TSM、ASML、TER", "不把下游规模直接等同DOV利润池，核心看议价权、订单硬度、收入确认和利润捕获。"]),
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
        need = "需要DOV把CST高订单转成收入和margin，并披露CPC/SWEP客户、订单金额、产品收入或更高AI收入占比。"
        if comparison["rel"] == "直接同业":
            need = "需要DOV在冷却/热交换同业中证明CPC/SWEP收入、margin和客户指定强于B。"
        elif comparison["rel"] == "上下游":
            need = "需要DOV证明自己能从下游AI系统/芯片/云厂CapEx中捕获可观利润，而不只是小组件跟随。"
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
        "- 公司 A 公司调研文件：`公司调研/机电_冷却_工程_水处理_边缘工业AI/DOV_Dover_Corporation_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_液冷小组件与流体控制_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心风冷、冷水机组与HVAC_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_dov_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用既有正式脚本的最低分校准，对DOV的CST/PPS订单、CPC/SWEP小基数AI弹性、低IV、FCF、估值、价格动量和产品收入未披露反证做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
        raise SystemExit("缺少 DOV 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "dov_tiers": {strategy: companies[TARGET]["tiers"].get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
        "dov_scores": {strategy: round(companies[TARGET]["scores"][strategy], 2) for strategy in STRATS},  # type: ignore[index]
        "dov_ranks": {strategy: companies[TARGET]["ranks"].get(strategy) for strategy in STRATS},  # type: ignore[union-attr]
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
