from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "GFS"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "GFS_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_FOUNDRY_PEERS = {
    "TSM",
    "UMC",
    "TSEM",
    "INTC",
}
FOUNDRY_IDM_ADJACENT = {
    "IFNNY",
    "STM",
    "TXN",
    "ON",
    "MCHP",
    "ADI",
    "DIOD",
    "AOSL",
}
WFE_SUPPLY_CHAIN = {
    "ACLS",
    "ACMR",
    "AMAT",
    "ASMIY",
    "ASML",
    "DSCSY",
    "KLAC",
    "LRCX",
    "NVMI",
    "TOELY",
    "VECO",
    "AEIS",
    "ICHR",
    "MKSI",
    "UCTT",
}
MATERIALS_SUPPLY_CHAIN = {
    "ENTG",
    "HOCPY",
    "PLAB",
    "Q",
    "SHECY",
    "MTRN",
    "ROG",
    "APD",
    "ASGLY",
    "AJNMY",
    "CC",
    "DD",
    "LIN",
    "SOMMY",
}
MEMORY_OSAT_CUSTOMERS = {
    "MU",
    "SNDK",
    "WDC",
    "STX",
    "ASX",
    "AMKR",
    "IMOS",
}
AI_COMPUTE_DESIGN = {
    "NVDA",
    "AMD",
    "AVGO",
    "MRVL",
    "QCOM",
    "ARM",
    "CDNS",
    "SNPS",
    "ALAB",
    "RMBS",
    "MXL",
}
AI_NETWORK_OPTICAL = {
    "AAOI",
    "ANET",
    "APH",
    "BDC",
    "BELFB",
    "CIEN",
    "COHR",
    "CRDO",
    "CSCO",
    "GLW",
    "LITE",
    "LWLG",
    "MTSI",
    "NOK",
    "POET",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}
CLOUD_SERVER_DEMAND = {
    "AMZN",
    "MSFT",
    "GOOGL",
    "META",
    "ORCL",
    "BABA",
    "IBM",
    "CRWV",
    "APLD",
    "IREN",
    "NBIS",
    "ANET",
    "CRDO",
    "SMCI",
    "DELL",
    "HPE",
    "FN",
    "JBL",
    "FLEX",
    "CLS",
    "SANM",
    "PENG",
}
PACKAGING_TEST_CHAIN = {
    "AEHR",
    "AMKR",
    "ASMVY",
    "ASX",
    "ATEYY",
    "BESIY",
    "CAMT",
    "COHU",
    "FORM",
    "IMOS",
    "KEYS",
    "KLIC",
    "MICLF",
    "ONTO",
    "TER",
}
SEMI_ADJACENT_CATS = {
    "晶圆制造_前道设备",
    "封测_检测_计量_光罩",
    "半导体材料_化学品_基板",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI服务器_存储_EMS",
}


def mid_growth(value: object) -> float | None:
    text = str(value).replace("−", "-").replace("～", "-").replace("—", "-").replace("–", "-")
    ranged = re.search(
        r"([+-]?)\s*(\d+(?:\.\d+)?)\s*%\s*(?:至|到|-)\s*([+-]?)\s*(\d+(?:\.\d+)?)\s*%",
        text,
    )
    if not ranged:
        ranged = re.search(r"([+-])\s*(\d+(?:\.\d+)?)\s*-\s*([+-]?)\s*(\d+(?:\.\d+)?)\s*%", text)
    if ranged:
        sign1, num1, sign2, num2 = ranged.groups()
        signed1 = -1 if sign1 == "-" else 1
        signed2 = -1 if sign2 == "-" else signed1 if sign2 == "" else 1
        return (signed1 * float(num1) + signed2 * float(num2)) / 2

    vals: list[float] = []
    for match in re.finditer(r"([+-]?)\s*(\d+(?:\.\d+)?)\s*%", text):
        vals.append((-1 if match.group(1) == "-" else 1) * float(match.group(2)))
    return sum(vals) / len(vals) if vals else None


def fix_growth_ranges(companies: dict[str, dict[str, object]]) -> None:
    for company in companies.values():
        for scenario, field in [
            ("bear", "bear_growth"),
            ("base", "base_growth"),
            ("bull", "bull_growth"),
            ("extreme", "extreme_growth"),
        ]:
            record = company.get("scenarios", {}).get(scenario, {})  # type: ignore[union-attr]
            for key, value in record.items():
                if "增速" in key or "绝对" in key:
                    parsed = mid_growth(value)
                    if parsed is not None:
                        company[field] = parsed
                    break


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for strategy in STRATS:
        ordered = sorted(companies.items(), key=lambda item: item[1]["scores"][strategy], reverse=True)  # type: ignore[index]
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
        if not company["fin"].get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company["tiers"][strategy] = "资料不足"  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    fix_growth_ranges(companies)
    base.score_companies(companies)

    # GFS-specific calibration: baseline revenue is visible through 2025
    # end-market anchors and 2026Q1/Q2 guidance, but growth is modest and the
    # SiPh/CPO upside remains gated by qualification and revenue recognition.
    a = companies[TARGET]
    overrides = {
        "NTM兑现优先": 65.0,
        "右尾弹性优先": 65.0,
        "风险调整收益": 48.0,
        "下行保护优先": 48.0,
        "估值消化优先": 48.0,
        "近端催化优先": 62.0,
        "价格确认/动量": 84.0,
        "激进短线": 84.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_FOUNDRY_PEERS:
        return "直接同业"
    if ticker in WFE_SUPPLY_CHAIN or ticker in MATERIALS_SUPPLY_CHAIN:
        return "上下游"
    if ticker in AI_COMPUTE_DESIGN or ticker in AI_NETWORK_OPTICAL or ticker in CLOUD_SERVER_DEMAND:
        return "上下游"
    if ticker in PACKAGING_TEST_CHAIN or ticker in MEMORY_OSAT_CUSTOMERS or ticker in FOUNDRY_IDM_ADJACENT:
        return "相邻替代"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A有Q1/Q2指引和end-market收入锚",
            "右尾弹性优先": "A有SiPh/Fotonix/CPO可选项",
            "风险调整收益": "A特种代工底盘较均衡",
            "下行保护优先": "A汽车/IoT/RF收入底座较稳",
            "估值消化优先": "A若利润率修复可部分消化估值",
            "近端催化优先": "A有Q2和SiPh项目验证窗口",
            "价格确认/动量": "A近期价格趋势确认较强",
            "激进短线": "A高IV叠加硅光/CPO叙事",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/RPO或订单兑现更硬",
            "右尾弹性优先": "B的AI利润池或小基数右尾更大",
            "风险调整收益": "B增长/估值/现金流组合更好",
            "下行保护优先": "B低IV/现金流或防守更稳",
            "估值消化优先": "B用NTM业绩消化估值更容易",
            "近端催化优先": "B近端订单/产品催化更强",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B高beta和事件弹性更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "估值和安全边际接近"
    return "档位接近需再验证"


def label_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    at = a["tiers"][strategy]  # type: ignore[index]
    bt = b["tiers"][strategy]  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        if at == "资料不足" and bt == "资料不足":
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    tier_diff = TIER_VAL[at] - TIER_VAL[bt]  # type: ignore[index,operator]
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
        if tag == "强烈建议投A" and not (abs(score_diff) >= 38 or abs(tier_diff) >= 4):
            tag = "建议投A"
        elif tag == "强烈建议投B" and not (abs(score_diff) >= 38 or abs(tier_diff) >= 4):
            tag = "建议投B"
        elif tag == "建议投A" and abs(score_diff) < 18 and abs(tier_diff) < 2:
            tag = "微倾向投A"
        elif tag == "建议投B" and abs(score_diff) < 18 and abs(tier_diff) < 2:
            tag = "微倾向投B"
    if rel == "直接同业" and abs(score_diff) >= 18 and tag.startswith("建议"):
        tag = "强烈" + tag
    return tag


def cell_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    tag = label_for(a, b, strategy, rel)
    return f"{tag}：{reason_for(strategy, tag, rel)}"


def direction_counts(cells: list[str]) -> tuple[int, int, int]:
    a_count = b_count = neutral = 0
    for cell in cells:
        tag = base.tag_in_cell(cell) or ""
        if tag.endswith("投A"):
            a_count += 1
        elif tag.endswith("投B"):
            b_count += 1
        else:
            neutral += 1
    return a_count, b_count, neutral


def final_choice(a: dict[str, object], b: dict[str, object], cells: list[str]) -> str:
    a_count, b_count, _ = direction_counts(cells)
    if a_count > b_count:
        return "A"
    if b_count > a_count:
        return "B"
    return "A" if a["scores"]["风险调整收益"] >= b["scores"]["风险调整收益"] else "B"  # type: ignore[index,operator]


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "GFS 的2025收入基数、2026Q1实际和Q2指引让NTM兑现比B更清楚。"
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 10:  # type: ignore[index,operator]
            return "GFS 的汽车、IoT、RF SOI和non-wafer底盘提供更强收入下限。"
        if a["scores"]["价格确认/动量"] - b["scores"]["价格确认/动量"] > 10:  # type: ignore[index,operator]
            return "GFS 近期价格确认更强，且Q2和SiPh/光互联项目仍有验证窗口。"
        return "GFS 的特种代工收入底盘更清楚，B 的优势不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI收入、小基数或短线右尾明显强于 GFS。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的当前估值更容易被NTM业绩消化。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/RPO/订单兑现证据更强。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的低波动、低估值或现金流防守属性更好。"
    return f"{b['ticker']} 在多数投资思路下比 GFS 更符合项目内资金配置目标。"


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    output = []
    for ticker in sorted(companies):
        if ticker == TARGET:
            continue
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(a, b, strategy, rel) for strategy in STRATS]
        a_count, b_count, neutral = direction_counts(cells)
        final = final_choice(a, b, cells)
        output.append(
            {
                "ticker": ticker,
                "b": b,
                "rel": rel,
                "cells": cells,
                "ac": a_count,
                "bc": b_count,
                "nc": neutral,
                "final": final,
                "summary": base.grade_diff_summary(a, b),
                "reason": key_reason(a, b, final),
            }
        )
    return output


def fmt_num(value: object, suffix: str = "") -> str:
    if value is None:
        return "缺失"
    if isinstance(value, float):
        return f"{value:.2f}{suffix}"
    return f"{value}{suffix}"


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    return f"${float(value):.2f}B"


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    return f"{float(value):.2f}%"


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(company_dates)} 至 {max(company_dates)}"
    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][base.tag_in_cell(cell)] += 1
    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b = sorted(
        comparisons,
        key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["NTM兑现优先"] - x["b"]["scores"]["NTM兑现优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:45]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:45]  # type: ignore[operator]
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker]["fin"] or not companies[ticker]["fin"].get("price")  # type: ignore[union-attr]
    ]

    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    latest_vs_june3 = ""
    try:
        latest_vs_june3 = f"，且6/22价格较6/3收盘约{(float(fin.get('price')) / float(mom2.get('latest_close')) - 1) * 100:+.2f}%"
    except Exception:
        latest_vs_june3 = ""
    daily_snapshot = (
        f"2026-06-22 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}{latest_vs_june3}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:6]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "2025收入67.91亿美元、2026Q1收入16.42亿美元、Q2收入指引中点17.60亿美元，NTM基准71-73亿美元",
            "基准增速仅约+4%-+7%；Smart Mobile/RF SOI大基数和成熟节点周期会抵消部分specialty增量",
        ),
        "右尾弹性优先": (
            "SiPh/Fotonix、SCALE、AMF/InfiniLink、CPO optical module、GaN和Processor IP使极度乐观收入可到80-85亿美元",
            "CPO/OCI、GaN和新增IP多为低至中低可信度期权，NTM内缺少大额客户收入披露",
        ),
        "风险调整收益": (
            "汽车、IoT、non-wafer/NRE和CIDC specialty平台提升收入质量，基准Adjusted EBITDA约24-26亿美元",
            "2026-06-22 Forward PE 35.61、P/S 7.19、Call IV 75.0%且压力窗口累计-53.28%，赔率不如更低倍数或更高增长标的",
        ),
        "下行保护优先": (
            "Smart Mobile/RF SOI、汽车、IoT和non-wafer形成多元收入底盘，基准情景仍有正EBITDA和正FCF方向",
            "SOXX压力窗口累计-53.28%、IV约75%、成熟节点周期和capex/利用率变量使其不是强防守资产",
        ),
        "估值消化优先": (
            "若NTM收入71-73亿美元、毛利率27%-29%、Adjusted EBITDA 24-26亿美元兑现，可部分支撑当前市值",
            "P/S 7.19和Forward PE 35.61对中个位数基准增速要求偏高，需利润率/mix明显修复才容易消化",
        ),
        "近端催化优先": (
            "2026Q2实际收入、毛利率、Adjusted EBITDA、wafer shipments、CIDC/SiPh项目和Renesas/汽车IoT量产节奏均可近端验证",
            "缺少标准backlog/RPO和SiPh/CPO单项收入披露，催化强度弱于已有大额订单或明确客户认证的公司",
        ),
        "价格确认/动量": (
            "2026-06-03两周+21.47%、一月+32.48%，2026-06-22价格89.67较6/3继续上涨约+4.28%",
            "强动量已经包含SiPh/CPO和特种代工重估，若Q2或margin没有跟上会转为估值压力",
        ),
        "激进短线": (
            "Call IV 75.0%、近月强价格趋势、硅光/CPO/AI数据中心特种工艺叙事提供短线进攻属性",
            "GFS基数不小且核心收入仍是成熟节点/特种工艺，短线爆发力通常弱于小盘光互联、NeoCloud或GPU/HBM主链",
        ),
    }

    out: list[str] = []
    out += [
        "# GFS 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：GFS / GlobalFoundries",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04。",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 GFS vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。GFS 的相对优势主要来自近期价格确认、SiPh/Fotonix/CPO题材、2026Q1/Q2收入锚、汽车/IoT/non-wafer收入底盘和特种工艺长期可选性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是基准收入增速只有约+4%-+7%、P/S 7.19和Forward PE 35.61要求偏高、SOXX压力窗口回撤深，且AI硅光/CPO在NTM内仍缺大额收入披露。",
        "- A 最适合的投资者画像：愿意买特种晶圆代工、硅光/高速连接和汽车/IoT组合修复，同时接受中等增长、高估值和较高波动的主题型成长资金。",
        "- A 最不适合的投资者画像：只追求最高AI主链增速、最低估值消化压力、明确RPO/backlog、大额近端订单，或要求强防守低波动的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在直接AI收入、HBM/GPU/custom ASIC利润池、明确订单/backlog、估值消化、现金流防守或小基数高beta上压过 GFS。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：GFS 对 {sum(1 for x in comparisons if x['final'] == 'A')}/{n - 1} 家公司多数思路占优，对 {sum(1 for x in comparisons if x['final'] == 'B')}/{n - 1} 家公司多数思路落后；在项目内更像“特种代工+硅光期权的中档进攻资产”，不是全项目最高增长/最高确定性资产。",
        "- 后续最重要跟踪数据：2026Q2实际收入、毛利率、Adjusted EBITDA和wafer shipments；Smart Mobile/RF是否拖累；汽车/IoT项目交付；CIDC中SiGe/CBIC/SiPh/Fotonix/SCALE/AMF客户收入；non-wafer/IP收入；GaN量产；库存、capex、营运资本和FCF。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "GFS"]),
        base.row(["公司名称", "GlobalFoundries"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "71-73亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI光互联需求需经过客户design-in、工艺平台锁定、封装测试、良率、验收和收入确认；CPO/OCI的NTM收入可信度低于800G/1.6T可插拔相关SiPh/SiGe机会。"]),
        base.row(["最大反证", "Smart Mobile/RF SOI和IoT若继续拖累，可能抵消CIDC/SiPh小基数增量；高估值已反映硅光和特种代工重估，若毛利率/FCF没有跟上，估值消化失败。"]),
        base.row(["近端催化剂", "2026Q2实际收入、毛利率、Adjusted EBITDA、wafer shipments、各end-market增速、SiPh/Fotonix/SCALE/AMF客户项目、Renesas/汽车IoT量产、库存/capex/FCF。"]),
        base.row(["日度市场数据", daily_snapshot]),
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
        base.row(["直接同业", "同属晶圆代工/IDM代工或成熟节点/特种工艺制造资金池，优先比较收入兑现、客户结构、产品mix、毛利率、capex、利用率、估值和AI相关收入真实占比。", "TSM、UMC、TSEM、INTC", "同业证据权重最高；若对手在先进制程、利用率、现金流或估值消化上明显强，结论力度可上调。"]),
        base.row(["相邻替代", "同属半导体制造、IDM、存储、封测或AI基础设施受益篮子，但产品/利润池不完全重叠。", "MU、SNDK、WDC、ASX、AMKR、IFNNY、STM、TXN", "回答资金只能买一个时，谁的增长质量、估值消化、近端催化和下行边界更好。"]),
        base.row(["上下游", "B 位于GFS的设备/材料/封装供应链、芯片设计客户、光互联/网络需求链或云/服务器终端需求端。", "ASML、AMAT、ENTG、NVDA、AVGO、AMD、MRVL、CRDO、COHR、MSFT、AMZN", "不把下游AI capex或上游稀缺自动等同GFS收入；重点看谁捕获利润池、议价权和可确认收入。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较风险调整收益、估值消化、下行保护和催化可见度。", "LIN、TMO、DHR、CAT、MSI、RYCEY", "默认降低结论力度；除非增长质量、估值消化或下行保护明显拉开，否则使用中性或微倾向。"]),
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
                    base.category_short(str(b["category"])),  # type: ignore[index]
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
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要 GFS 披露更硬的SiPh/CIDC/CPO客户收入、证明Q2后毛利率/FCF同步改善，并降低当前估值和高IV反证。"
        if comparison["rel"] == "直接同业":
            need = "需要 GFS 在同业中证明特种工艺、汽车/IoT和SiPh收入化强于B，并且估值没有透支。"
        elif comparison["rel"] == "上下游":
            need = "需要 GFS 证明比该上下游公司更能捕获AI半导体利润池，而不是只承接低毛利成熟节点或验证期项目。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 GFS 用更强现金流、估值消化或防守表现抵消跨赛道标的的低波动/防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更强NTM收入利润兑现、或更低估值/更好现金流来抵消GFS的特种代工底盘和价格确认。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要 B 把右尾叙事转成可确认收入/利润，并证明估值、现金流和执行反证可控。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 181 家；本次公司评估全集为 {n} 家，因此缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/晶圆制造_前道设备/GFS_GlobalFoundries_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_特种晶圆代工_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_硅光材料、光子材料与电光聚合物_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_CPO／NPO与交换侧光引擎_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_OCI（光学计算互连）／Open CPX／XPO_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_gfs_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对GFS的2026Q1/Q2指引、Smart Mobile/RF SOI基盘、汽车/IoT、CIDC、SiPh/Fotonix/SCALE/AMF/CPO、non-wafer/IP、估值、高IV、压力窗口和价格确认做人工校准后建档；未读取下游量化目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    print(
        json.dumps(
            {
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "size": OUT_PATH.stat().st_size,
                "gfs_tiers": companies[TARGET]["tiers"],
                "gfs_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
