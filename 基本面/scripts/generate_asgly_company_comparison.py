from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "ASGLY"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ASGLY_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_MATERIAL_PEERS = {
    "AJNMY",
    "AXTI",
    "CC",
    "DD",
    "DKILY",
    "ENTG",
    "GLW",
    "HOCPY",
    "MTRN",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
}
MATERIAL_ADJACENT = {"APD", "LIN", "MMM", "NDSN", "ECL"}
SEMI_DOWNSTREAM_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "晶圆制造_前道设备",
    "封测_检测_计量_光罩",
    "云算力_IDC_AI软件平台",
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

    # ASGLY is a diversified glass / chemicals company with real semiconductor
    # material exposure. The generic model over-rewards the stale early-June
    # momentum and under-rewards low valuation / Q1 profit repair.
    a = companies[TARGET]
    overrides = {
        "NTM兑现优先": 70.0,
        "右尾弹性优先": 56.0,
        "风险调整收益": 57.0,
        "下行保护优先": 72.0,
        "估值消化优先": 74.0,
        "近端催化优先": 62.0,
        "价格确认/动量": 80.5,
        "激进短线": 78.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_MATERIAL_PEERS:
        return "直接同业"
    if ticker in MATERIAL_ADJACENT or category == "半导体材料_化学品_基板":
        return "相邻替代"
    if category in SEMI_DOWNSTREAM_CATS:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A分部指引和Q1利润修复更稳",
            "右尾弹性优先": "A有EUV/CCL/TGV材料期权",
            "风险调整收益": "A低估值和修复赔率更均衡",
            "下行保护优先": "A低PB、多元分部和杠杆温和",
            "估值消化优先": "A低估值更易被利润修复消化",
            "近端催化优先": "A有Q2/Q3分部和材料更新",
            "价格确认/动量": "A近月涨幅已确认修复",
            "激进短线": "A小市值材料期权更有弹性",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B订单/RPO或收入兑现更硬",
            "右尾弹性优先": "B直接AI右尾更大",
            "风险调整收益": "B上行、现金流或反证组合更好",
            "下行保护优先": "B现金流/低波动/压力期更稳",
            "估值消化优先": "B增长更能覆盖估值",
            "近端催化优先": "B近端订单/产品节点更强",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B高beta和事件弹性更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "估值安全和增长证据接近"
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
        a["scores"]["NTM兑现优先"]
        + a["scores"]["风险调整收益"]
        + a["scores"]["估值消化优先"]
        + a["scores"]["价格确认/动量"] * 0.5
        - b["scores"]["NTM兑现优先"]
        - b["scores"]["风险调整收益"]
        - b["scores"]["估值消化优先"]
        - b["scores"]["价格确认/动量"] * 0.5
    )
    return "A" if key_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
            return "ASGLY 的低PB/低估值和FY2026利润修复更容易消化当前价格。"
        if a["scores"]["价格确认/动量"] - b["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
            return "ASGLY 近月价格已确认半导体材料重估，B尚缺价格验证。"
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 10:  # type: ignore[index,operator]
            return "ASGLY 的多元传统分部、温和杠杆和低估值提供更好缓冲。"
        return "ASGLY 在估值消化、分部修复和材料期权组合上略胜。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI收入右尾和重定价弹性明显强于 ASGLY。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的NTM收入/订单兑现证据比 ASGLY 更硬。"
    if b["scores"]["近端催化优先"] - a["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的近端订单、产品或财报催化更清楚。"
    if b["scores"]["激进短线"] - a["scores"]["激进短线"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的高beta、IV或事件弹性更适合短线进攻。"
    return f"{b['ticker']} 在多数投资思路下比 ASGLY 更符合项目内资金配置目标。"


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
    ps_text = fmt_num(fin.get("ps"), precision=4)
    daily_snapshot = (
        f"2026-06-22 金融快照生成；ASGLY价格日期 {fin.get('price_date', '缺失')}，价格 {fmt_num(fin.get('price'))} 美元，"
        f"市值 {fmt_b(fin.get('market_cap_b'))}，TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"源字段P/S {ps_text}（交易货币/财报货币不一致，估值重算标记bad；公司调研口径约0.5x-0.6x），"
        f"P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = []
    for product in a["products"][:8]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    support = {
        "NTM兑现优先": (
            "FY2026销售`22,000亿日元`、经营利润`1,500亿日元`指引维持；Q1销售`5,380亿日元`、经营利润`385亿日元`已显示利润修复",
            "NTM基准增速仅约`+8%-+12%`，半导体材料占集团比例仍小，AI/DC收入未单独披露",
        ),
        "右尾弹性优先": (
            "EUV mask blanks、半导体含氟材料、METEORWAVE低损耗CCL、TGV/glass core和CPO光学件构成长右尾",
            "224Gbps CCL、TGV和CPO多偏2027-2029，极度乐观可信度低，NTM不能提前计入大额收入",
        ),
        "风险调整收益": (
            "2026-06-22金融快照显示市值约`$9.70B`、TTM PE`22.27`、P/B`1.05`，估值低于多数AI主链，Q1利润修复提供赔率",
            "传统玻璃/化学周期、Life Science减亏、CAPEX和营运资本仍会限制FCF；ADR价格/估值字段存在滞后和币种警示",
        ),
        "下行保护优先": (
            "多元分部、D/E约`0.41`、低PB和低估值提供缓冲；SOXX三段压力窗口累计约`-17.24%`，未出现高beta式崩盘",
            "建筑/汽车/显示玻璃和基础化学品周期会拖累，下行保护弱于公用事业、低IV现金流公司和部分成熟云巨头",
        ),
        "估值消化优先": (
            "低PB、低市销口径和FY2026利润修复，使NTM基准业绩更容易消化当前估值；半导体材料mix提升可带来结构重估",
            "ROE仍低、Forward PE缺失，若高毛利材料占比不能扩大，低估值可能只是周期材料折价",
        ),
        "近端催化优先": (
            "FY2026 Q2/Q3分部收入、Electronic Materials、半导体相关业务使用量、Life Science减亏和CAPEX下降可在1-2季验证",
            "缺少大额订单/backlog和明确客户认证时间表；TGV/CPO/224Gbps多为中长期，不是强近端催化",
        ),
        "价格确认/动量": (
            "截至2026-06-03过去两周`+29.76%`、过去一月`+44.94%`，价格已反映半导体材料重估",
            "2026-06-22金融快照的最新价日期为`2026-06-18`且低于6月初收盘，说明动量已有回吐；ASGLY OTC流动性和ADR口径需折扣",
        ),
        "激进短线": (
            "小市值、低估值、近月强动量和EUV/CCL/TGV材料叙事提供进攻弹性",
            "无干净期权链/IV、OTC流动性弱，远期期权多且缺NTM订单，短线爆发力不如高IV AI主线",
        ),
    }

    out: list[str] = []
    out += [
        "# ASGLY 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：ASGLY / AGC Inc",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22金融快照，ASGLY价格字段最新交易日为2026-06-18；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 ASGLY vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ASGLY 的优势不是高增速，而是低估值、FY2026利润修复、半导体材料mix提升和近月价格确认的组合。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是AI/DC收入占比小、TGV/CPO/224Gbps CCL多为远期、无产品级backlog/订单披露，且ASGLY ADR流动性和IV覆盖弱。",
        "- A 最适合的投资者画像：愿意用低估值周期材料公司承接半导体材料结构重估、重视估值消化和风险调整收益，但不要求GPU/服务器式高速增长的中期配置者。",
        "- A 最不适合的投资者画像：只追求直接AI收入爆发、高IV短线进攻、强订单/RPO和1-2个季度硬催化的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常具备更直接AI收入、更硬订单/RPO、更高右尾或更强短线资金确认。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：ASGLY 属于项目内中上防守修复型材料标的，不是顶级高增长主线；在估值消化、动量和下行缓冲上可打，但在右尾、催化和NTM订单确定性上弱于AI主链。",
        "- 后续最重要跟踪数据：FY2026 Q2/Q3分部收入和经营利润、Electronic Materials与Display拆分、半导体相关业务客户使用量、EUV mask blanks进度、METEORWAVE/224Gbps客户导入、Performance Chemicals半导体应用销售、Life Science减亏、CAPEX/营运资本/FCF。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ASGLY"]),
        base.row(["公司名称", "AGC Inc"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`22,200-23,100亿日元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AGC参与AI/先进半导体材料的产品多，但AI/DC收入、产品级backlog、客户订单和交付时间表未披露，需求到收入仍需客户认证和收入确认。"]),
        base.row(["最大反证", "半导体相关业务2025年约`1,000亿日元`、占集团约5%，当前仍不足以完全改写建筑/汽车/显示/基础化学品的周期属性；Q1 FCF仍为负。"]),
        base.row(["近端催化剂", "FY2026 Q2/Q3分部收入和利润、EUV blanks客户使用量、METEORWAVE/CCL客户导入、Performance Chemicals半导体销售、Life Science减亏和CAPEX/FCF改善。"]),
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
        base.row(["直接同业", "与ASGLY在半导体材料、玻璃/光学材料、含氟材料、EUV mask blanks、CCL、基板或电子化学品需求池重叠，优先比较客户认证、收入兑现、产品代际、利润率和同业估值。", "HOCPY、SHECY、ENTG、Q、DD、DKILY、ROG、GLW", "同业证据权重最高；若对方在订单、份额、利润质量或估值消化上明显更强，会直接压低ASGLY结论。"]),
        base.row(["相邻替代", "同属半导体材料、工业气体、先进材料或AI基础设施资金篮子，但产品不完全竞争；回答资金只能买一个时谁的增长质量和赔率更好。", "APD、LIN、ECL、NDSN、ETN、VRT、GEV", "默认看估值消化、订单可见度、下行保护和增长弹性；不因赛道更热自动胜出。"]),
        base.row(["上下游", "一方处在ASGLY材料所服务的晶圆制造、光罩、封测、AI芯片、AI网络、服务器或云客户链条。", "TSM、ASML、AMAT、NVDA、MU、CRDO、ANET、SMCI、AMZN", "不把下游AI收入规模直接等同于ASGLY机会，重点看ASGLY能否捕获材料端利润池。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化。", "RKLB、TSLA、TMO、CAT、MSI", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要 ASGLY 把EUV/CCL/含氟材料转成可量化订单、分部收入和利润率上修，并证明FCF改善。"
        if comparison["rel"] == "直接同业":
            need = "需要 ASGLY 在EUV blanks、CCL/含氟材料或TGV客户导入上拿出强于同业的量化份额、订单和利润率证据。"
        elif comparison["rel"] == "上下游":
            need = "需要 ASGLY 证明材料端利润捕获能接近下游AI芯片、设备、网络或云公司的成长斜率。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 ASGLY 用更强估值消化、现金流和价格确认抵消跨赛道标的的高增长或防守质量。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提高收入确认可信度、现金流质量和估值消化能力，或拿出更强价格确认。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要 B 把右尾叙事转成可确认收入/利润，并降低估值、IV或现金流反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/半导体材料_化学品_基板/ASGLY_AGC_Inc_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_玻璃基板、TGV与玻璃检测_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_封装基板、中介层与RDL_2026-06-10.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_高端光罩与先进封装掩模_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_硅光材料、光子材料与电光聚合物_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_先进封装材料与热界面材料_2026-06-10.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_asgly_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对ASGLY的半导体材料修复、低估值、远期期权、OTC流动性和最新价格滞后做人工校准后建档。",
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
        "asgly_tiers": companies[TARGET]["tiers"],
        "asgly_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
