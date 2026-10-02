from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "DSCSY"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "DSCSY_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_WFE_PEERS = {
    "ACLS",
    "ACMR",
    "AMAT",
    "ASMIY",
    "ASML",
    "KLAC",
    "LRCX",
    "NVMI",
    "TOELY",
    "VECO",
}
EQUIPMENT_SUPPLY_CHAIN = {
    "AEIS",
    "ICHR",
    "MKSI",
    "UCTT",
    "ENTG",
    "HOCPY",
    "SHECY",
    "Q",
    "MTRN",
    "ROG",
}
CUSTOMERS_AND_DEMAND_CHAIN = {
    "TSM",
    "GFS",
    "UMC",
    "TSEM",
    "INTC",
    "MU",
    "SNDK",
    "WDC",
    "STX",
    "ASX",
    "AMKR",
    "IMOS",
    "NVDA",
    "AMD",
    "AVGO",
    "MRVL",
    "QCOM",
    "ARM",
    "CDNS",
    "SNPS",
    "ALAB",
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
}
PACKAGING_TEST_ADJACENT = {
    "AEHR",
    "ATEYY",
    "ASMVY",
    "BESIY",
    "CAMT",
    "COHU",
    "FORM",
    "KEYS",
    "KLIC",
    "MICLF",
    "ONTO",
    "PLAB",
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

    # DISCO-specific calibration. The generic model over-rewards the raw P/S
    # field because DSCSY trades in USD while the financials are in JPY and the
    # daily file explicitly marks P/S as bad(currency_mismatch). DISCO deserves
    # high NTM/right-tail/catalyst scores for HBM wafer thinning, dicing/laser,
    # precision tools and very high margins, but valuation digestion and
    # downside protection must be capped by high TTM PE, missing forward PE/IV,
    # severe SOXX-pressure drawdowns, and no disclosed bookings/backlog.
    a = companies[TARGET]
    overrides = {
        "NTM兑现优先": 72.0,
        "右尾弹性优先": 74.0,
        "风险调整收益": 48.0,
        "下行保护优先": 56.0,
        "估值消化优先": 43.0,
        "近端催化优先": 66.0,
        "价格确认/动量": 60.0,
        "激进短线": 82.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_WFE_PEERS:
        return "直接同业"
    if ticker in EQUIPMENT_SUPPLY_CHAIN or ticker in CUSTOMERS_AND_DEMAND_CHAIN:
        return "上下游"
    if ticker in PACKAGING_TEST_ADJACENT:
        return "相邻替代"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的shipment和高毛利兑现更清楚",
            "右尾弹性优先": "A的HBM薄化/切割右尾更硬",
            "风险调整收益": "A利润质量和工艺稀缺更均衡",
            "下行保护优先": "A耗材复购和高毛利底座更稳",
            "估值消化优先": "A的NTM增长可部分消化估值",
            "近端催化优先": "A有Q1实绩和shipment验证窗口",
            "价格确认/动量": "A近期价格修复和主题确认更强",
            "激进短线": "A半导体设备beta和HBM叙事更强",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B订单/RPO或收入兑现更硬",
            "右尾弹性优先": "B小基数或直接AI右尾更大",
            "风险调整收益": "B估值与下行组合更好",
            "下行保护优先": "B低IV/低估值或压力期更稳",
            "估值消化优先": "B估值消化压力更低",
            "近端催化优先": "B近端订单/产品催化更强",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B高beta/高IV事件弹性更强",
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
            return "DISCO 的FY2026 shipment、grinder/laser/tools和高利润率让NTM兑现更清楚。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 10:  # type: ignore[index,operator]
            return "DISCO 在HBM薄化、低损伤切割和耗材复购上有更硬的先进封装右尾。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
            return "DISCO 的FY2026 Q1实绩、shipment和产品mix验证窗口更近。"
        return "DISCO 的高毛利加工工艺和先进封装暴露更稀缺，B 的优势不足以覆盖反证。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化压力明显低于 DISCO。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的压力期表现、低IV或现金流防守属性更好。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的小基数、直接AI收入或短线右尾明显强于 DISCO。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/RPO/订单兑现证据更强。"
    return f"{b['ticker']} 在多数投资思路下比 DISCO 更符合项目内资金配置目标。"


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
    daily_snapshot = (
        f"2026-06-22 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S 原始字段 {fmt_num(fin.get('ps'))}（估值校验 bad/currency_mismatch），"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:6]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "FY2025收入`4,368.9亿日元`、OPM`42.3%`，FY2026 Q1 revenue指引`1,061亿`、shipment `1,320亿`，grinders +25%、blade/laser/dicers +15%",
            "公司不披露 bookings/backlog/取消率，shipment 到 revenue 仍受客户验收和交付节奏约束",
        ),
        "右尾弹性优先": (
            "HBM4/16Hi、advanced logic backside、薄晶圆、laser/SDBG和高端耗材可把极度乐观收入推至`6,400-7,300亿日元`",
            "玻璃/TGV、KABRA/GaN/diamond 和 CPO 多数仍缺NTM客户订单，不能当作基准收入",
        ),
        "风险调整收益": (
            "毛利率约70%、基准OPM`40.0%-43.5%`、耗材复购和高端设备mix提供质量",
            "2026-06-22 TTM PE `70.90`、Forward PE/IV缺失，P/S因USD/JPY口径被标记bad，SOXX压力窗口累计`-90.52%`",
        ),
        "下行保护优先": (
            "precision tools、maintenance parts 和高客户工艺粘性提供经营底座",
            "半导体设备周期、高估值、ADR流动性/IV缺失和历史压力窗口深回撤削弱防守属性",
        ),
        "估值消化优先": (
            "基准收入`4,850-5,250亿日元`、净利润`1,360-1,650亿日元`，若shipment转收入可部分消化估值",
            "当前估值已经要求乐观兑现；Forward PE缺失且P/S不可直接跨币种重算，消化置信度低",
        ),
        "近端催化优先": (
            "FY2026 Q1实绩、Q2指引、product shipment、HBM/CoWoS/SoIC客户扩产和laser saw新型号均在1-2季可验证",
            "没有公开订单簿，若shipment强但revenue/OPM不跟，催化会变成反证",
        ),
        "价格确认/动量": (
            "2026-06-03两周`+8.88%`，2026-06-22价格已升至`55.30`，主题确认有所增强",
            "一个月仍为`-6.93%`，区间涨跌文件停在2026-06-03，SOXX压力窗口回撤很深",
        ),
        "激进短线": (
            "HBM薄化/切割稀缺性、半导体设备beta和近期价格修复提供进攻弹性",
            "ADR无干净期权IV、不是小市值高beta标的，短线爆发力低于部分光互联/AI芯片/NeoCloud公司",
        ),
    }

    out: list[str] = []
    out += [
        "# DSCSY 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：DSCSY / DISCO",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 DSCSY vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。A侧外部网页仅用于核验 2026-06-23 附近 IR/行情状态，不替代项目金融资料建档。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。DSCSY 的优势来自 HBM/advanced packaging 相关 wafer thinning、dicing/laser、precision tools 复购、70% 左右毛利率和FY2026 Q1 shipment高于revenue指引。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是高估值、Forward PE/期权IV缺失、P/S跨币种不可直接用、没有公开bookings/backlog，以及SOXX压力窗口中回撤很深。",
        "- A 最适合的投资者画像：希望配置先进封装和HBM制造瓶颈、重视高毛利工艺设备和耗材复购，但能接受日本设备股估值、ADR数据缺口和半导体设备周期波动的中期成长资金。",
        "- A 最不适合的投资者画像：只追求最低估值、最高短线IV/小市值右尾、明确订单簿，或要求公用事业式下行保护的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在直接AI收入、订单/RPO、小基数右尾、估值消化、价格确认或防御属性上压过 DSCSY。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：DSCSY 是项目内高质量半导体设备瓶颈股，NTM兑现、右尾和近端催化属于中上层强项；但按估值消化和下行保护看明显不是顶层，更适合作为高毛利设备链核心卫星仓，而不是最激进或最防守的唯一选择。",
        "- 后续最重要跟踪数据：FY2026 Q1实际收入/shipment/OPM、Q2指引、grinders/laser saws/blade dicers/precision tools shipment、tools复购、HBM4/CoWoS/SoIC客户扩产、laser saw新型号、KABRA/GaN/diamond和玻璃/TGV是否出现明确客户订单、应收/库存/FCF。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "DSCSY"]),
        base.row(["公司名称", "DISCO"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "4,850-5,250 亿日元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "不披露 bookings、backlog 和取消率；需求到收入的关键约束是客户验收、shipment 与 revenue 时间差、grinder/laser saw产能、现场工艺认证和HBM/先进封装客户扩产节奏。"]),
        base.row(["最大反证", "FY2026 Q1 revenue指引低于FY2025 Q4 run-rate且OPM降至39.6%；Forward PE/IV缺失，TTM PE较高；玻璃/TGV、KABRA/GaN/diamond多数缺少NTM订单。"]),
        base.row(["近端催化剂", "FY2026 Q1实绩、Q2指引、product shipment、grinders/laser saw/tools、HBM4/CoWoS/SoIC客户扩产、laser saw新型号和玻璃/TGV/KABRA订单证据。"]),
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
        base.row(["直接同业", "同属半导体前道/WFE和晶圆精密加工设备资金池，优先看订单/指引、产品代际、客户验收、毛利率、耗材复购和同业估值消化。", "AMAT、ASML、TOELY、LRCX、KLAC、ASMIY、ACMR、ACLS、VECO", "同业证据权重最高；若对手有更硬订单、backlog、收入确认或估值优势，结论力度可以上调。"]),
        base.row(["相邻替代", "同处AI半导体设备、封装测试、光互联、数据中心电力/冷却或AI基础设施资金篮子，但收入模式不完全相同。", "TER、ATEYY、BESIY、CAMT、VRT、ETN、GEV、ANET、CRDO", "回答资金只能买一个时，谁的增长质量、订单可见度、估值消化和近端催化更好。"]),
        base.row(["上下游", "一方处在DISCO客户、供应商、封测/晶圆制造或终端AI芯片需求链，重点看利润池位置、议价权、瓶颈稀缺性和收入确认链条。", "TSM、MU、INTC、NVDA、AVGO、AMKR、ASX、ENTG、MKSI", "不把下游AI收入规模直接等同DISCO机会，也不把上游设备稀缺自动等同更好。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较风险调整收益、估值消化、下行保护和催化可见度。", "LIN、TMO、DHR、CAT、MSI、RYCEY", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要 DISCO 披露更硬的shipment转收入、Q2/Q3指引、产品shipment延续、毛利率/FCF修复，并降低估值和压力期回撤反证。"
        if comparison["rel"] == "直接同业":
            need = "需要 DISCO 在同业中证明grinder/laser/tools增速、客户验收和利润质量比该设备商更强，且估值压力可被兑现覆盖。"
        elif comparison["rel"] == "上下游":
            need = "需要 DISCO 证明比该上下游公司更能捕获HBM/先进封装利润池，而不是只承担设备周期beta。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 DISCO 用更强现金流、估值消化或防守表现抵消跨赛道标的的低波动/防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更强NTM收入利润兑现、或更低估值/更好现金流来抵消DISCO的高毛利工艺和HBM加工稀缺性。"
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
        "- 其他主要项目来源：`公司调研/公司索引.md`、`公司调研/晶圆制造_前道设备/DSCSY_DISCO_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_AI芯片前道制造设备_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_玻璃基板、TGV与玻璃检测_2026-06-11.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 外部日期敏感校验（仅用于核验 A 侧 2026-06-23 附近 IR/行情状态，不替代项目统一日度建档）：DISCO IR News `https://www.disco.co.jp/eg/ir/news/`；DISCO Investors `https://www.disco.co.jp/eg/ir/`；Yahoo Finance DSCSY `https://finance.yahoo.com/quote/DSCSY/`；MarketWatch DSCSY `https://www.marketwatch.com/investing/stock/dscsy`；Citi DR DSCSY corporate action page `https://depositaryreceipts.citi.com/adr/notices/pgm_dispCA.aspx?cusip=25461D100&pageid=15&subpageID=113`。",
        "- 自动化脚本：`scripts/generate_dscsy_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间做同号区间修正后建档；未读取下游量化目录或现成排序结论。",
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
                "dscsy_tiers": companies[TARGET]["tiers"],
                "dscsy_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
