from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "CC"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "CC_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_CHEMICAL_PEERS = {
    "ASGLY",
    "DD",
    "DKILY",
    "Q",
    "SHECY",
    "SOMMY",
}
MATERIAL_ADJACENT = {
    "AJNMY",
    "APD",
    "AXTI",
    "DHR",
    "ECL",
    "ENTG",
    "HOCPY",
    "LIN",
    "MMM",
    "MRAAY",
    "MTRN",
    "NDSN",
    "ROG",
    "SMTOY",
}
COOLING_AND_FACILITY = {
    "AAON",
    "CARR",
    "DCI",
    "DOV",
    "JCI",
    "MOD",
    "PNR",
    "TT",
    "VRT",
}
DOWNSTREAM_SEMI_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "晶圆制造_前道设备",
    "封测_检测_计量_光罩",
}
DOWNSTREAM_DATA_CENTER_CATS = {
    "云算力_IDC_AI软件平台",
    "机电_冷却_工程_水处理_边缘工业AI",
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

    # CC is a high-leverage fluorochemicals / TiO2 / performance materials
    # repair story. It has real 2P50 and semiconductor fluoropolymer optionality,
    # but current NTM revenue is guided by TSS, TT and APM normalization rather
    # than direct AI data-center orders. The override keeps valuation digestion
    # strong while penalizing downside, momentum and short-term aggression.
    cc = companies[TARGET]
    overrides = {
        "NTM兑现优先": 67.0,
        "右尾弹性优先": 52.0,
        "风险调整收益": 50.0,
        "下行保护优先": 45.0,
        "估值消化优先": 74.0,
        "近端催化优先": 62.0,
        "价格确认/动量": 30.0,
        "激进短线": 64.0,
    }
    for strategy, score in overrides.items():
        cc["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_CHEMICAL_PEERS:
        return "直接同业"
    if ticker in MATERIAL_ADJACENT or category == "半导体材料_化学品_基板":
        return "相邻替代"
    if ticker in COOLING_AND_FACILITY or category in DOWNSTREAM_DATA_CENTER_CATS:
        return "上下游"
    if category in DOWNSTREAM_SEMI_CATS or category == "云算力_IDC_AI软件平台":
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A有FY2026指引和Q2修复锚",
            "右尾弹性优先": "A有2P50和高纯氟材料期权",
            "风险调整收益": "A低PS/低FwdPE修复赔率更好",
            "下行保护优先": "B下行反证更重而A估值更低",
            "估值消化优先": "A低PS和EBITDA修复更易消化",
            "近端催化优先": "A有Q2修复和2P50验证节点",
            "价格确认/动量": "B动量更弱且A有事件反弹",
            "激进短线": "A小市值高IV和2P50更弹",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B订单/RPO或收入兑现更硬",
            "右尾弹性优先": "B直接AI右尾或小基数更大",
            "风险调整收益": "B上行/下行组合更好",
            "下行保护优先": "B现金流、负债或压力期更稳",
            "估值消化优先": "B增长更能覆盖估值",
            "近端催化优先": "B近端订单/产品催化更强",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B高beta和资金关注更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
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
    a_count, b_count, _neutral = direction_counts(cells)
    if a_count > b_count:
        return "A"
    if b_count > a_count:
        return "B"
    key_weight = (
        a["scores"]["估值消化优先"] * 1.15
        + a["scores"]["风险调整收益"]
        + a["scores"]["NTM兑现优先"] * 0.85
        + a["scores"]["下行保护优先"] * 0.20
        - b["scores"]["估值消化优先"] * 1.15
        - b["scores"]["风险调整收益"]
        - b["scores"]["NTM兑现优先"] * 0.85
        - b["scores"]["下行保护优先"] * 0.20
    )
    return "A" if key_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
            return "CC 的低P/S、低Forward PE和EBITDA修复让估值消化更容易。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 8:  # type: ignore[index,operator]
            return "CC 有FY2026指引、Q2修复和TSS利润池，B的兑现证据更弱。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 8:  # type: ignore[index,operator]
            return "CC 的Q2修复、APM恢复和2P50验证窗口比B更近。"
        return "CC 的估值消化和修复赔率略胜，B的增长证据不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI收入、小基数或高增长右尾明显强于 CC。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 订单/RPO/收入确认证据比 CC 更硬。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 10:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、资产负债表或压力窗口表现明显优于 CC。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和资金偏好明显强于 CC。"
    return f"{b['ticker']} 在多数投资思路下比 CC 更符合项目内资金配置目标。"


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


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    output: list[dict[str, object]] = []
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


def fmt_num(value: object, suffix: str = "", precision: int = 2) -> str:
    if value is None:
        return "缺失"
    if isinstance(value, float):
        return f"{value:.{precision}f}{suffix}"
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
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["估值消化优先"] - x["b"]["scores"]["估值消化优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:45]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:45]  # type: ignore[operator]
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker]["fin"] or not companies[ticker]["fin"].get("price")  # type: ignore[union-attr]
    ]

    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_snapshot = (
        f"2026-06-22 收盘价 `{fmt_num(fin.get('price'))}`，市值 `{fmt_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `不适用/TTM EPS为负`，Forward PE `{fmt_num(fin.get('forward_pe'))}`，P/S `{fmt_num(fin.get('ps'))}`，"
        f"P/B `{fmt_num(fin.get('pb'))}`，EV/EBITDA `{fmt_num(fin.get('ev_ebitda'))}`，"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`，Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03 过去两周 `{fmt_pct(mom2.get('mom2w'))}`、过去一月 `{fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04 三段 SOXX 压力窗口累计 `{fmt_pct(soxx.get('soxx_cum'))}`。"
    )

    product_names = []
    for product in a["products"][:8]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    support = {
        "NTM兑现优先": (
            "2026全年收入指引`+3-5%`、Adj. EBITDA `$800-900M`，Q2收入环比`+15-20%`、EBITDA `$220-250M`",
            "增速只是中个位数，TT/APM仍是修复而非爆发，2P50不进入基准主收入",
        ),
        "右尾弹性优先": (
            "Opteon 2P50、半导体高纯PFA/PTFE/FEP、3M PFAS退出和低GWP制冷剂构成长尾期权",
            "2P50缺订单金额/收入确认，两相/浸没2026仍多为pilot，TiO2拖累总公司右尾",
        ),
        "风险调整收益": (
            "2026-06-22 Forward PE`9.49`、P/S`0.55`，若EBITDA修复兑现则估值消化空间大",
            "TTM EPS为负、净杠杆/PFAS/环保现金义务、高IV和压力窗口大跌明显压低风险收益",
        ),
        "下行保护优先": (
            "低P/S、Kuan Yin土地出售和TSS高margin给资产负债表修复提供缓冲",
            "Call IV`63.3%`、过去一月`-18.46%`、SOXX压力窗口累计`-51.38%`，高杠杆化工股防守性弱",
        ),
        "估值消化优先": (
            "Forward PE`9.49`、P/S`0.55`，基准Adj. EBITDA `$820-940M`可支撑低估值修复",
            "低估值来自TiO2商品周期、APM outage、PFAS尾部负债和FCF conversion仅`>20%`",
        ),
        "近端催化优先": (
            "Q2 2026分部修复、TT价格行动、APM Washington Works恢复、Kuan Yin偿债和2P50合作进展均可跟踪",
            "缺少2P50大额订单、客户采购金额和收入确认，近端催化多是修复验证而非上修爆点",
        ),
        "价格确认/动量": (
            "截至2026-06-03过去两周`+1.53%`，高IV说明资金仍会交易事件弹性",
            "2026-06-22价格`21.46`低于6月初`22.61`，过去一月`-18.46%`且压力窗口很弱",
        ),
        "激进短线": (
            "小市值、高IV、低估值和2P50新闻流可以形成短线进攻素材",
            "趋势确认弱，若Q2/2P50无硬订单容易继续按高杠杆化工修复股折价",
        ),
    }

    out: list[str] = []
    out += [
        "# CC 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：CC / The Chemours Company",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 CC vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。CC 的项目内优势集中在低估值和EBITDA修复可消化当前市值；它不是项目内增长冠军。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。短板是价格确认差、下行保护弱、右尾缺订单金额，且2P50仍是2027+期权而非NTM主收入。",
        "- A 最适合的投资者画像：愿意买低估值、高波动、带氟化学/2P50期权的经营修复股，并能承受PFAS、杠杆、TiO2周期和负EPS噪音的逆向配置者。",
        "- A 最不适合的投资者画像：追求直接AI收入、订单/RPO硬兑现、低回撤防守、强动量或短线高确定性的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常拥有更直接的AI收入、更强NTM订单/客户证据、更稳现金流或更好的价格确认。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：CC 在全项目更像估值修复型材料期权，综合位置偏后；只在估值消化或对手更弱时胜出，不能与AI主链、设备龙头、网络/光互联强标的等量齐观。",
        "- 后续最重要跟踪数据：Q2 2026收入/Adj. EBITDA是否兑现、TSS Opteon/Freon价格与R32成本、TT价格/volume/margin、APM Washington Works恢复、2P50订单金额/客户/交付时间表、半导体高纯氟材料收入披露、PFAS/环保现金支出、净杠杆和FCF conversion。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "CC"]),
        base.row(["公司名称", "The Chemours Company"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`$6.00-6.20B`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "TT是最大收入池但毛利脆弱；APM必须证明outage后恢复并把半导体高纯材料转为可见收入；2P50必须从验证/合作进入订单和收入确认。"]),
        base.row(["最大反证", "TTM EPS为负、PFAS/环保和净杠杆压制估值；SOXX压力窗口和近月价格表现显示市场没有把CC当作确定性AI主线。"]),
        base.row(["近端催化剂", "Q2 2026分部收入和Adj. EBITDA、TT pricing、APM恢复、Kuan Yin债务偿还、2P50客户/订单/收入披露、半导体高纯氟材料客户验证。"]),
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
        base.row(["直接同业", "与CC在氟化学、低GWP制冷剂、半导体高纯氟材料、电子化学品或TiO2/特种材料需求池重叠，优先比较收入兑现、产品代际、客户认证、利润率、PFAS合规和估值折价。", "DD、DKILY、ASGLY、Q、SHECY、SOMMY", "同业证据权重最高；若对方在订单、利润质量、资产负债表或材料稀缺性上更强，会显著压低CC结论。"]),
        base.row(["相邻替代", "同属材料、化学品、工业气体、水处理、半导体材料或AI基础设施资金篮子，但产品不直接竞争；回答资金只能买一个时谁的增长质量和赔率更好。", "APD、LIN、ENTG、ECL、MTRN、ROG、HOCPY", "默认看估值消化、收入可见度、下行保护和材料端利润池；不因低估值或赛道相关就自动胜出。"]),
        base.row(["上下游", "一方处在CC可能服务的半导体制造、设备、AI芯片、服务器、云/IDC或数据中心冷却链条，重点看CC的材料利润捕获能否优于下游/设备端成长。", "TSM、ASML、AMAT、NVDA、VRT、TT、CARR、MSFT、AMZN", "不把AI capex或数据中心冷却TAM直接等同于CC收入；只有订单和收入确认才提高CC权重。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化。", "RKLB、TSLA、CRWD、MSI、CAT", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要 CC 披露2P50或高纯氟材料的客户、订单金额、交付窗口和收入确认，并把TT/APM修复转成FCF。"
        if comparison["rel"] == "直接同业":
            need = "需要 CC 在Opteon、APM高纯材料、TiO2价格和PFAS合规上拿出强于同业的收入、利润和现金流证据。"
        elif comparison["rel"] == "上下游":
            need = "需要 CC 证明材料端能捕获下游AI/半导体/冷却链条的稀缺利润，而不是只停留在小额试验或间接受益。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 CC 用更硬的低估值兑现、现金流修复或2P50订单抵消跨赛道标的的高增长/低风险优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提高收入兑现、利润/现金流质量或估值消化能力，或出现明确订单/指引上修。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要 B 把右尾叙事转为可确认收入和利润，并降低估值、波动或资产负债表反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/半导体材料_化学品_基板/CC_The_Chemours_Company_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/AI园区电力_机电_冷却/行业调研_冷却液、水处理、过滤与制冷剂_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_高纯氟聚合物流体系统_2026-06-23.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体高纯水、气体与化学流体系统_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装湿化学与表面处理材料_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：从 `分析报告/公司评估/结果/` 根层读取 `*_收入传导估值评估_*.md`，同一 Ticker 取文件名日期最新版本；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        "- 公司 A 日度数据摘录：2026-06-22 收盘价 `21.46`，市值 `$3.23B`，TTM PE 不适用/TTM EPS 为负，Forward PE `9.49`，P/S `0.55`，Call IV `63.3%`，Put IV `61.0%`；2026-06-03 过去两周 `+1.53%`、过去一月 `-18.46%`；2026-06-04 三段 SOXX 压力窗口累计 `-51.38%`。",
        "- 外部官方校验来源：Chemours Q1 2026 results `https://www.chemours.com/en/news-media-center/all-news/press-releases/2026/the-chemours-company-reports-first-quarter-results`；Chemours FY2025 results `https://www.chemours.com/en/news-media-center/all-news/press-releases/2026/the-chemours-company-reports-fourth-quarter-and-full-year-2025-results`；Opteon 2P50 product page `https://www.opteon.com/en/products/liquid-cooling/2p50`；Chemours/2CRSi JDA `https://www.chemours.com/en/news-media-center/all-news/press-releases/2026/following-successful-fluid-qualification-chemours-2crsi-join-forces-to-accelerate-deployment-of-two`；Chemours/Navin Fluorine manufacturing agreement `https://www.chemours.com/en/news-media-center/all-news/press-releases/2025/chemours-and-navin-fluorine-announce-agreement-to-manufacture-new-liquid-cooling-product`；Samsung qualification `https://www.chemours.com/en/news-media-center/all-news/press-releases/2025/samsung-electronics-successfully-qualifies-chemours-opteon-two-phase-immersion-cooling-fluid`。",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
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
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "cc_tiers": companies[TARGET]["tiers"],
        "cc_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
        "cc_ranks": companies[TARGET]["ranks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
