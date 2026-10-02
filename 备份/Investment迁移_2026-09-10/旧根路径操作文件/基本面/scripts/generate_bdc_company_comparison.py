from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "BDC"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "BDC_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {
    "AAOI",
    "ANET",
    "APH",
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

ACTIVE_CONNECTIVITY_ADJACENT = {
    "ALAB",
    "AVGO",
    "MRVL",
    "MXL",
    "ADI",
    "QCOM",
    "NVDA",
    "AMD",
    "ARM",
}

PHYSICAL_INFRA_ADJACENT = {
    "ABBNY",
    "ATKR",
    "ETN",
    "HUBB",
    "NVT",
    "POWL",
    "POWI",
    "MPWR",
    "VICR",
    "NVTS",
    "IFNNY",
    "DIOD",
    "AOSL",
    "LFUS",
    "ST",
    "MIELY",
    "TTDKY",
    "MRAAY",
    "VRT",
    "TT",
    "AAON",
    "CARR",
    "JCI",
    "MOD",
    "DOV",
    "PNR",
    "DCI",
    "PH",
    "FTV",
    "MSI",
    "ALLE",
}

DATA_CENTER_DEMAND_CHAIN = {
    "AMZN",
    "MSFT",
    "GOOGL",
    "META",
    "ORCL",
    "BABA",
    "IBM",
    "EQIX",
    "DLR",
    "CRWV",
    "APLD",
    "IREN",
    "NBIS",
    "NTNX",
    "CRWD",
    "ADBE",
}

SERVER_STORAGE_CHAIN = {
    "DELL",
    "HPE",
    "SMCI",
    "PENG",
    "CLS",
    "FLEX",
    "JBL",
    "SANM",
    "FN",
    "PSTG",
    "NTAP",
    "STX",
    "WDC",
    "MU",
    "SNDK",
    "RMBS",
    "SIMO",
    "MRAM",
}

MEP_POWER_CHAIN = {
    "PWR",
    "EME",
    "FIX",
    "MYRG",
    "IESC",
    "GEV",
    "AEP",
    "CEG",
    "DTE",
    "ETR",
    "VST",
    "ET",
    "BE",
    "BWXT",
    "SMR",
    "OKLO",
    "RYCEY",
    "GNRC",
    "CMI",
    "FCEL",
    "FLNC",
    "ENS",
    "PSIX",
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
    values: list[float] = []
    for match in re.finditer(r"([+-]?)\s*(\d+(?:\.\d+)?)\s*%", text):
        values.append((-1 if match.group(1) == "-" else 1) * float(match.group(2)))
    return sum(values) / len(values) if values else None


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

    # BDC-specific calibration:
    # - NTM base is supported by Q1 revenue, Q2 guidance, Automation margin, and Smart Buildings growth.
    # - It is not a pure AI networking/high-speed silicon name; AI data center order/backlog disclosure is still thin.
    # - RUCKUS improves right-tail and mix if it closes, but leverage, integration, and channel risk cap downside quality.
    bdc = companies[TARGET]
    overrides = {
        "NTM兑现优先": 68.5,
        "右尾弹性优先": 55.0,
        "风险调整收益": 63.0,
        "下行保护优先": 53.5,
        "估值消化优先": 74.0,
        "近端催化优先": 65.0,
        "价格确认/动量": 56.0,
        "激进短线": 78.0,
    }
    for strategy, score in overrides.items():
        bdc["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in DATA_CENTER_DEMAND_CHAIN or ticker in SERVER_STORAGE_CHAIN or ticker in MEP_POWER_CHAIN:
        return "上下游"
    if ticker in ACTIVE_CONNECTIVITY_ADJACENT or ticker in PHYSICAL_INFRA_ADJACENT:
        return "相邻替代"
    if category == "AI网络_光互联_连接器":
        return "直接同业"
    if category in INFRA_CATS or category == "配电_电源_功率器件":
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "云算力_IDC_AI软件平台", "电力_发电_能源_储能"}:
        return "上下游"
    return "跨赛道"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong, b_strong, close = [], [], []
    for strategy in STRATS:
        diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
        label = strategy.replace("优先", "").replace("/动量", "动量")
        if diff >= 8:
            a_strong.append(label)
        elif diff <= -8:
            b_strong.append(label)
        else:
            close.append(label)

    def joined(items: list[str]) -> str:
        if not items:
            return "无"
        return "、".join(items[:3]) + ("等" if len(items) > 3 else "")

    return f"A强：{joined(a_strong)}；B强：{joined(b_strong)}；接近：{joined(close)}"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的Q1/Q2收入锚更清楚",
            "右尾弹性优先": "A有RUCKUS和AI布线期权",
            "风险调整收益": "A低PS和基准可信度更均衡",
            "下行保护优先": "A利润底座和低估值有缓冲",
            "估值消化优先": "A低Forward PE/P/S更易消化",
            "近端催化优先": "A有Q2/Q3订单和RUCKUS节点",
            "价格确认/动量": "A价格已从6月初继续确认",
            "激进短线": "A小市值和并购节点可重定价",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B订单/RPO或收入兑现更硬",
            "右尾弹性优先": "B直接AI右尾或小基数更大",
            "风险调整收益": "B上行/下行组合更好",
            "下行保护优先": "B现金流或压力期更稳",
            "估值消化优先": "B业绩增速更能消化估值",
            "近端催化优先": "B近端订单/产品催化更强",
            "价格确认/动量": "B价格确认更强",
            "激进短线": "B高beta和市场关注更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "估值消化优先", "下行保护优先"}:
        return "估值、安全性和兑现证据接近"
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
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
            return "BDC 的低 Forward PE/P/S 与 NTM +8-12% 基准收入让估值消化更容易。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 8:  # type: ignore[index,operator]
            return "BDC 的Q1/Q2收入锚、Automation利润池和Smart Buildings增长让NTM兑现更清楚。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
            return "BDC 的RUCKUS交割、Smart Buildings订单和Q2/Q3指引窗口更近。"
        return "BDC 的估值、基准兑现和IT/OT解决方案质量略优，B 的上行证据不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI收入、小基数或高增长右尾明显强于 BDC。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 订单/RPO/收入确认证据更硬。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 10:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、防守性或压力窗口表现更好。"
    if b["scores"]["近端催化优先"] - a["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
        return f"{b['ticker']} 的近端订单、产品或财报催化更可见。"
    return f"{b['ticker']} 在多数投资思路下比 BDC 更符合项目内资金配置目标。"


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
                "summary": grade_diff_summary(a, b),
                "reason": key_reason(a, b, final),
            }
        )
    return output


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
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:2]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:2]
    strong_b = sorted(
        comparisons,
        key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["估值消化优先"] - x["b"]["scores"]["估值消化优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:45]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:45]  # type: ignore[operator]
    missing_fin = [ticker for ticker in sorted(companies) if not companies[ticker]["fin"].get("price")]  # type: ignore[union-attr]

    product_names = []
    for product in a["products"][:6]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_snapshot = (
        f"2026-06-22 收盘价 `{fin.get('price')}`，市值 `${fin.get('market_cap_b')}B`，"
        f"TTM PE `{fin.get('ttm_pe')}`，Forward PE `{fin.get('forward_pe')}`，P/S `{fin.get('ps')}`，"
        f"P/B `{fin.get('pb')}`，EV/EBITDA `{fin.get('ev_ebitda')}`，Call IV `{fin.get('call_iv')}%`，Put IV `{fin.get('put_iv')}%`；"
        f"2026-06-03 过去两周 `{mom2.get('mom2w')}%`、过去一月 `{mom1.get('mom1m')}%`；"
        f"2026-06-04 三段 SOXX 压力窗口累计 `{soxx.get('soxx_cum')}%`。"
    )
    support = {
        "NTM兑现优先": (
            "2026Q1收入`$696.4M`、有机`+7%`、Q2指引`$735-750M`、交易前NTM基准`$2.92-3.05B`",
            "Q1 orders仅`+4%`且未披露可建模backlog，AI DC项目确认仍需客户/交付证据",
        ),
        "右尾弹性优先": (
            "Smart Buildings AI白空间、Automation灰空间OT网络、RUCKUS高毛利企业网络构成上限路径",
            "不是光模块/AEC/交换ASIC核心环节，极度乐观依赖订单披露、RUCKUS交割和解决方案mix同时成立",
        ),
        "风险调整收益": (
            "2026-06-22 Forward PE`13.72`、P/S`1.70`，基准可信度中高，NTM收入和EBITDA都有可解释锚",
            "RUCKUS现金收购推高杠杆，利息/整合/渠道风险会压制FCF和估值容忍度",
        ),
        "下行保护优先": (
            "Automation segment EBITDA margin`21.0%`、经营FCF为正，低估值提供一部分缓冲",
            "SOXX三段压力窗口累计`-59.64%`，且并购后杠杆和普通线缆/铜价/关税风险不低",
        ),
        "估值消化优先": (
            "Forward PE`13.72`、P/S`1.70`，交易前NTM`+8-12%`和EBITDA`$495-530M`足以支撑消化",
            "若订单继续降速或RUCKUS延期，市场可能把低倍数视为周期线缆折价而非网络平台重估",
        ),
        "近端催化优先": (
            "Q2指引兑现、Q3订单/book-to-bill、Smart Buildings organic、RUCKUS H2 close 是1-2季度可跟踪节点",
            "缺少已披露大额AI DC订单/RPO，催化强度弱于AI芯片、光模块、云算力和电力设备主链龙头",
        ),
        "价格确认/动量": (
            "2026-06-22价格`121.65`高于6月3日`110.60`，价格已对低估值和并购叙事有所确认",
            "2026-06-03过去一月为`-3.11%`，历史压力窗口回撤深，动量质量不是全项目顶档",
        ),
        "激进短线": (
            "市值`$4.74B`、Call IV`55.2%`，RUCKUS交割和AI结构化布线叙事可带来短线重定价",
            "短线爆发力仍不如纯AI网络、光模块、NeoCloud、小基数电力设备或高beta半导体标的",
        ),
    }

    out: list[str] = []
    out += [
        "# BDC 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：BDC / Belden",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 BDC vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。BDC 的核心优势来自低 Forward PE/P/S、Q1/Q2收入锚、Automation利润池、Smart Buildings数据中心结构化布线增长，以及RUCKUS若按期交割带来的高毛利并表期权。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是它不是纯AI芯片、光模块、AEC或交换ASIC核心标的，公开披露缺少可建模AI数据中心订单/backlog，短线动量和历史压力窗口也不是项目内顶档。",
        "- A 最适合的投资者画像：愿意买低估值工业网络/连接解决方案、重视估值消化和NTM基准兑现，同时接受RUCKUS并购杠杆与AI数据中心二阶暴露不如主链直接的资金。",
        "- A 最不适合的投资者画像：只追求纯AI高增速、已披露RPO/backlog、极强右尾弹性、短线高beta或公用事业式下行保护的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在直接AI收入、订单/RPO、右尾弹性、近端催化、价格确认或现金流防守性上压过 BDC。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：BDC 是项目内中上但非顶尖的AI数据中心二阶基础设施标的；在估值消化、NTM兑现和部分近端催化思路下有配置价值，但在右尾至上、动量至上、激进短线至上思路下会输给更直接的AI网络、云算力、芯片、电力设备或电气基础设施龙头。",
        "- 后续最重要跟踪数据：Q2/Q3收入和orders/book-to-bill、Smart Buildings organic growth、数据中心结构化布线订单金额、Automation data center gray-space案例和margin、solutions wins占比、RUCKUS审批/close date/渠道留存、并购后净杠杆和FCF conversion、铜价/关税/普通线缆mix对毛利率的影响。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "BDC"]),
        base.row(["公司名称", "Belden"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["scenarios"]["base"].get("NTM 公司收入", "缺失")]),  # type: ignore[index]
        base.row(["乐观/极度乐观收入", f"{a['scenarios']['bull'].get('NTM 公司收入', '缺失')} / {a['scenarios']['extreme'].get('NTM 公司收入', '缺失')}"]),  # type: ignore[index]
        base.row(["利润和现金流结论", f"{a['scenarios']['base'].get('EBITDA/净利润', '')}；{a['scenarios']['base'].get('自由现金流方向', '')}"]),  # type: ignore[index]
        base.row(["最大传导瓶颈", "没有披露可直接建模backlog；Q1 orders `+4%`只是健康而非爆发，AI DC项目到收入确认仍受客户AVL、EPC/SI、交付和RUCKUS交割约束"]),
        base.row(["最大反证", "AI DC垂直收入/客户金额未披露；RUCKUS提高杠杆和整合风险；普通线缆、铜价、关税和项目固定价可能稀释margin"]),
        base.row(["近端催化剂", "Q2/Q3收入和订单、Smart Buildings double-digit延续、Automation 20%+ margin、数据中心订单披露、RUCKUS 2026H2 close和渠道稳定"]),
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
        base.row(["直接同业", "产品、客户或需求池与 BDC 的AI网络、光/铜连接、结构化布线、工业网络、企业网络或光接入路径高度重叠。", "APH、TEL、GLW、CSCO、ANET、CIEN、CRDO、AAOI、COHR、BELFB、NOK、VIAV", "优先看同一AI网络/数据中心连接需求池中的订单、客户、产品代际、收入兑现、margin和同业估值。"]),
        base.row(["相邻替代", "同属AI数据中心物理基础设施、电气/配电/电源/冷却、主动连接硅片或资金会二选一配置的AI基础设施篮子。", "ALAB、MRVL、AVGO、VRT、ETN、NVT、HUBB、ATKR、POWL、AAON", "回答资金只能买一个时，谁的增长质量、利润捕获、估值消化、近端催化和风险调整收益更好。"]),
        base.row(["上下游", "一方处于云/IDC/服务器/EMS/EPC/MEP/电力接入等需求链，另一方是网络连接和物理层解决方案供应端。", "MSFT、AMZN、META、EQIX、DLR、DELL、SMCI、PWR、EME、GEV", "不把下游CapEx或服务器收入直接等同 BDC 收入，重点看利润池、议价权、订单可见度和项目兑现。"]),
        base.row(["跨赛道", "半导体设备、材料、软件、工业、生物工具等与 BDC 业务差异大，但作为项目内资金配置替代仍比较。", "ASML、AMAT、TSM、LIN、TMO、CDNS、SNPS", "默认降低结论力度；除非增长质量、估值消化或风险收益明显拉开，否则使用中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
        base.row(["序号", "公司B", "公司B分类", "可比关系", "档位差摘要", *STRATS, "多数思路方向", "最终更值得投", "最关键理由"]),
        base.row(["---:", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"]),
    ]
    for index, comparison in enumerate(comparisons, start=1):
        b = comparison["b"]
        out.append(
            base.row(
                [
                    index,
                    base.short_name(b),
                    base.category_short(str(b["category"])),
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],
                    majority(comparison["ac"], comparison["bc"], comparison["nc"]),
                    "BDC" if comparison["final"] == "A" else b["ticker"],
                    comparison["reason"],
                ]
            )
        )

    out += [
        "",
        "## 6. 投资思路统计",
        "",
        base.row(["投资思路", *TAG_ORDER, "A侧合计", "B侧合计"]),
        base.row(["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]),
    ]
    for strategy in STRATS:
        out.append(base.row([strategy, *[stats[strategy][tag] for tag in TAG_ORDER], a_side[strategy], b_side[strategy]]))

    out += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要 BDC 披露可量化AI数据中心收入/backlog/客户项目，证明Q2/Q3 orders再加速、Smart Buildings持续双位数、Automation margin保持20%+，且RUCKUS按期交割后净杠杆可控。"
        if comparison["rel"] == "直接同业":
            need = "需要 BDC 在同业中证明更强结构化布线/工业网络份额、更高解决方案mix、更快收入确认，或RUCKUS把企业网络转成清晰收入协同。"
        elif comparison["rel"] == "上下游":
            need = "需要 BDC 证明自己能比上下游公司更有效捕获AI数据中心利润池，而不是只得到普通物理层和项目材料收入。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 BDC 用更强增长、订单可见度、现金流或估值消化来抵消跨赛道标的的技术、订单或右尾优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更强NTM收入利润兑现，或证明估值、现金流和下行反证低于 BDC。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要 B 把右尾叙事转成可确认收入/利润，并证明估值和现金流反证可控。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 181 家，本次公司评估全集为 {n} 家；缺少可用价格/估值或价格缺失的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/AI网络_光互联_连接器/BDC_Belden_公司调研_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_高速连接器、背板与结构化布线_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AEC、DAC与高速铜缆_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_宽带接入、PON、DOCSIS 4.0与Wi-Fi 7_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_导管、桥架与线缆管理_2026-06-10.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_bdc_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对 BDC 做专门档位校准；未读取下游量化目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "output": str(OUT_PATH),
        "size": OUT_PATH.stat().st_size,
        "company_count": len(companies),
        "comparison_count": len(comparisons),
        "bdc_tiers": companies[TARGET]["tiers"],
        "bdc_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
