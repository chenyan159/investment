from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_entg_company_comparison as framework


TARGET = "SOMMY"
TARGET_NAME = "住友化学 Sumitomo Chemical"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "SOMMY_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_MATERIAL_PEERS = {
    "AJNMY",
    "APD",
    "ASGLY",
    "AXTI",
    "CC",
    "DD",
    "DKILY",
    "ENTG",
    "HOCPY",
    "LIN",
    "MTRN",
    "Q",
    "ROG",
    "SHECY",
}
MATERIAL_ADJACENT = {
    "DHR",
    "ECL",
    "MMM",
    "MRAAY",
    "NDSN",
    "SMTOY",
    "TMO",
    "TTDKY",
}
SEMI_DOWNSTREAM_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "封测_检测_计量_光罩",
    "晶圆制造_前道设备",
    "云算力_IDC_AI软件平台",
}
ELECTRICAL_AND_DC_ADJACENT = {
    "ABBNY",
    "AEIS",
    "ETN",
    "GEV",
    "HUBB",
    "IFNNY",
    "MPWR",
    "NVT",
    "POWL",
    "VRT",
}


SOMMY_SCORES = {
    # SOMMY is a broad chemical turnaround with a real semiconductor-materials
    # line, not a pure AI hardware compounder. Keep NTM and right-tail below
    # high-growth AI leaders, but credit the low valuation, positive FCF and
    # official FY2026 operating-profit anchor.
    "NTM兑现优先": 65.0,
    "右尾弹性优先": 56.0,
    "风险调整收益": 56.0,
    "下行保护优先": 78.0,
    "估值消化优先": 65.0,
    "近端催化优先": 62.0,
    "价格确认/动量": 44.0,
    "激进短线": 45.0,
}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    framework.score_companies(companies)
    target = companies[TARGET]
    for strategy, score in SOMMY_SCORES.items():
        target.setdefault("scores", {})[strategy] = score  # type: ignore[index]
    framework.recompute_tiers(companies)


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    if ticker in DIRECT_MATERIAL_PEERS:
        return "直接同业"
    if ticker in MATERIAL_ADJACENT or category == "半导体材料_化学品_基板":
        return "相邻替代"
    if category in SEMI_DOWNSTREAM_CATS or category in HIGH_GROWTH_CATS:
        return "上下游"
    if ticker in ELECTRICAL_AND_DC_ADJACENT or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, b: dict[str, object], rel: str) -> str:
    ticker = str(b.get("ticker", ""))
    category = str(b.get("category", ""))
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A有FY2026指引和分部收入锚",
            "右尾弹性优先": "A高纯化学品/EUV材料有期权",
            "风险调整收益": "A低估值叠加正FCF修复赔率",
            "下行保护优先": "A低PE/PB和多元业务缓冲更强",
            "估值消化优先": "A低倍数更易被FY2026利润覆盖",
            "近端催化优先": "AUECC/Baytown/Osaka节点可验证",
            "价格确认/动量": "A一月反弹仍有低估值支撑",
            "激进短线": "A材料修复弹性强于弱势B",
        }[strategy]

    if tag.endswith("投B"):
        if rel == "直接同业":
            return {
                "NTM兑现优先": "B同业材料收入或订单更硬",
                "右尾弹性优先": "B同业小基数/高端材料右尾更大",
                "风险调整收益": "B同业估值、现金流或增长组合更优",
                "下行保护优先": "B同业资产质量或低波动更稳",
                "估值消化优先": "B同业利润增长更能覆盖倍数",
                "近端催化优先": "B客户认证/产能节点更近",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业短线弹性和关注度更高",
            }[strategy]
        if category in HIGH_GROWTH_CATS or category in SEMI_DOWNSTREAM_CATS:
            return {
                "NTM兑现优先": "B直接AI收入兑现更短链",
                "右尾弹性优先": "B直接AI右尾和小基数更大",
                "风险调整收益": "B上行空间更能覆盖风险",
                "下行保护优先": "B需求能见度或现金流更强",
                "估值消化优先": "B高增长更能消化估值",
                "近端催化优先": "B订单/RPO/产品催化更硬",
                "价格确认/动量": "B资金趋势确认更强",
                "激进短线": "B高beta叙事更适合进攻",
            }[strategy]
        if category in INFRA_CATS or ticker in ELECTRICAL_AND_DC_ADJACENT:
            return {
                "NTM兑现优先": "B订单/backlog兑现更清楚",
                "右尾弹性优先": "B AI电力机电右尾更直接",
                "风险调整收益": "B订单和估值组合更优",
                "下行保护优先": "B现金流或防御属性更强",
                "估值消化优先": "B backlog更能覆盖估值",
                "近端催化优先": "B项目/FID/产能催化更近",
                "价格确认/动量": "B价格趋势确认更强",
                "激进短线": "B事件弹性和关注度更高",
            }[strategy]
        return {
            "NTM兑现优先": "B收入兑现证据更强",
            "右尾弹性优先": "B右尾空间更大",
            "风险调整收益": "B风险收益组合更优",
            "下行保护优先": "B下行缓冲更强",
            "估值消化优先": "B增长更能消化估值",
            "近端催化优先": "B近端催化更明确",
            "价格确认/动量": "B价格确认更强",
            "激进短线": "B短线弹性更强",
        }[strategy]

    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "质量、估值和兑现接近"
    return "档位接近需再验证"


def label_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    at = str(a["tiers"][strategy])  # type: ignore[index]
    bt = str(b["tiers"][strategy])  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        if at == "资料不足" and bt == "资料不足":
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    score_diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
    tier_diff = tier_value(at) - tier_value(bt)
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
    return f"{tag}：{reason_for(strategy, tag, b, rel)}"


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
    quality_weight = (
        float(a["scores"]["风险调整收益"]) * 0.9
        + float(a["scores"]["下行保护优先"]) * 0.8
        + float(a["scores"]["估值消化优先"]) * 0.8
        + float(a["scores"]["NTM兑现优先"]) * 0.6
        - float(b["scores"]["风险调整收益"]) * 0.9
        - float(b["scores"]["下行保护优先"]) * 0.8
        - float(b["scores"]["估值消化优先"]) * 0.8
        - float(b["scores"]["NTM兑现优先"]) * 0.6
    )
    return "A" if quality_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if float(a["scores"]["下行保护优先"]) - float(b["scores"]["下行保护优先"]) > 12:
            return "SOMMY的低PE/PB、多元分部和正FCF给出更好下行缓冲。"
        if float(a["scores"]["估值消化优先"]) - float(b["scores"]["估值消化优先"]) > 10:
            return "SOMMY当前估值低，FY2026利润修复更容易消化价格。"
        if float(a["scores"]["风险调整收益"]) - float(b["scores"]["风险调整收益"]) > 8:
            return "SOMMY低估值和修复现金流使风险调整收益略优。"
        return "SOMMY在估值、防守和分部修复上略胜，B的增长证据不足以覆盖反证。"

    if float(b["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]) > 18:
        return f"{b['ticker']}的直接AI收入、小基数或平台型右尾明显强于SOMMY。"
    if float(b["scores"]["NTM兑现优先"]) - float(a["scores"]["NTM兑现优先"]) > 12:
        return f"{b['ticker']}的订单/RPO/backlog或收入确认证据比SOMMY更硬。"
    if float(b["scores"]["近端催化优先"]) - float(a["scores"]["近端催化优先"]) > 12:
        return f"{b['ticker']}的近端订单、客户认证或产品催化更明确。"
    if float(b["scores"]["价格确认/动量"]) - float(a["scores"]["价格确认/动量"]) > 12:
        return f"{b['ticker']}的价格确认和资金趋势明显强于SOMMY。"
    return f"{b['ticker']}在多数投资思路下比SOMMY更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong, b_strong, close = [], [], []
    for strategy in STRATS:
        diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
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
    rows: list[dict[str, object]] = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(a, b, strategy, rel) for strategy in STRATS]
        a_count, b_count, neutral = direction_counts(cells)
        final = final_choice(a, b, cells)
        rows.append(
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
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return sorted(rows, key=lambda item: (rel_order.get(str(item["rel"]), 9), str(item["ticker"])))


def fmt_num(value: object, precision: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{precision}f}"
    except Exception:
        return "缺失"


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"${float(value):.2f}B"
    except Exception:
        return "缺失"


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.2f}%"
    except Exception:
        return "缺失"


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = sorted(str(company["date"]) for company in companies.values())
    date_range = f"{company_dates[0]} 至 {company_dates[-1]}"

    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][base.tag_in_cell(cell)] += 1
    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]

    strong_b = sorted(
        comparisons,
        key=lambda row: (
            int(row["bc"]) - int(row["ac"]),
            float(row["b"]["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]),  # type: ignore[index]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda row: (
            int(row["ac"]) - int(row["bc"]),
            float(a["scores"]["下行保护优先"]) - float(row["b"]["scores"]["下行保护优先"]),  # type: ignore[index]
        ),
        reverse=True,
    )
    strong_b_rows = [row for row in strong_b if int(row["bc"]) >= 5 and int(row["bc"]) - int(row["ac"]) >= 3][:45]
    strong_a_rows = [row for row in strong_a if int(row["ac"]) >= 5 and int(row["ac"]) - int(row["bc"]) >= 3][:45]
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker].get("fin") or not companies[ticker].get("fin", {}).get("price")  # type: ignore[union-attr]
    ]

    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {
        strategy: f"第 {a['ranks'][strategy]}/{n}，{a['tiers'][strategy]} 档"  # type: ignore[index]
        for strategy in STRATS
    }

    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    close_0603 = mom2.get("latest_close")
    post_interval = "缺失"
    if fin.get("price") is not None and close_0603:
        post_interval = fmt_pct((float(fin["price"]) / float(close_0603) - 1) * 100)  # type: ignore[index]
    daily_snapshot = (
        f"金融快照文件生成于2026-06-22，SOMMY行内价格日期为`{fin.get('price_date')}`；"
        f"最新价格 `{fmt_num(fin.get('price'))}`，市值 `{fmt_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `{fmt_num(fin.get('ttm_pe'))}`，Forward PE `{fmt_num(fin.get('forward_pe'))}`，"
        f"源字段P/S `{fmt_num(fin.get('ps'), 4)}`但估值校验为`{fin.get('valuation_check')}`，不作为核心倍数；"
        f"P/B `{fmt_num(fin.get('pb'))}`，EV/EBITDA `{fmt_num(fin.get('ev_ebitda'))}`，"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`，Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03过去两周 `{fmt_pct(mom2.get('mom2w'))}`，过去一月 `{fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04三段SOXX压力窗口累计 `{fmt_pct(soxx.get('soxx_cum'))}`；"
        f"从2026-06-03收盘到价格日期收盘约 `{post_interval}`。"
    )

    product_names = []
    for product in a["products"]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])
        if len(product_names) >= 8:
            break

    support = {
        "NTM兑现优先": (
            "FY2026官方指引收入`¥2.36tn`、核心营业利润`¥215bn`、FCF`¥60bn`；Agro、Pharma、ICT和Essential分部均有正式锚",
            "公司基准收入增速仅`+0.5%-+2.2%`，半导体材料被显示/基础化工/Pharma口径抵消，产品级订单不披露",
        ),
        "右尾弹性优先": (
            "UHP IPA/H2O2、EUV/ArF、High-NA、先进后道、HPA、glass core和AUECC/Baytown提供材料右尾",
            "集团收入基数大，极度乐观也只有约`+10.8%-+15.9%`；High-NA/glass core多为FY2027以后或认证期权",
        ),
        "风险调整收益": (
            "2026-06-18价格对应TTM PE约`15.22x`、P/B约`0.92x`、EV/EBITDA约`3.57x`，且基准FCF仍为正",
            "带息负债、石化周期、Pharma一次性和FCF从FY2025`¥159.9bn`降至FY2026指引`¥60bn`限制赔率",
        ),
        "下行保护优先": (
            "低估值、多元分部、Agro/Pharma现金流、基础化工重组和半导体材料客户粘性提供缓冲",
            "SOXX三段压力窗口累计`-24.06%`，显示其不是纯防御资产；周期化工和ADR流动性仍会放大回撤",
        ),
        "估值消化优先": (
            "低PE/PB/EVEBITDA和FY2026核心营业利润修复，使估值不需要极端AI情景才能解释",
            "Forward PE缺失，P/S因USD/JPY币种错配不可用；收入低增长意味着估值上移要靠利润率和现金流",
        ),
        "近端催化优先": (
            "AUECC审批/整合、Baytown UHP IPA、Osaka光刻胶中心、FY2026 Q1/Q2分部利润和Pharma/Agro兑现可跟踪",
            "缺少客户名、订单金额、POR/HVM时间表和产品级backlog，催化强度弱于订单/RPO型AI主链公司",
        ),
        "价格确认/动量": (
            "截至2026-06-03过去一月`+11.35%`，低估值化工修复已有阶段性反弹",
            "过去两周`-1.91%`且6月18日价格较6月3日约`-1.67%`，缺少持续趋势确认和期权IV支持",
        ),
        "激进短线": (
            "如果只押低估值材料修复，A有一定反弹 beta 和半导体材料新闻流",
            "无期权链/IV，ADR流动性和直接AI收入纯度低，短线进攻性弱于AI芯片、光互联、NeoCloud和高beta电力股",
        ),
    }

    lines: list[str] = []
    lines += [
        "# SOMMY 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：SOMMY / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV主体为 `金融资料/每日金融数据/每日金融数据_2026-06-22.md`；SOMMY行内价格日期为2026-06-18；过去1个月/过去两周区间涨跌为2026-06-03；SOXX压力窗口为2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 SOMMY vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或项目根 `tmp/` 的结论；SOMMY 的 AI 暴露只按高纯化学品、光刻胶、先进封装材料、HPA、glass core 和客户认证路径处理，不把AI数据中心CapEx直接并入公司收入。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。SOMMY 的相对优势集中在下行保护、估值消化和风险调整收益：它不是高增速AI主链，但低PE/PB、正FCF、FY2026利润修复和多元化分部使其比大量高估值、弱现金流或资料不足公司更稳。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是激进短线、价格确认和右尾弹性：无期权链/IV，价格趋势不强，半导体材料大多在ICT内被显示、基础化工和Pharma大基数稀释。",
        "- A 最适合的投资者画像：愿意买“低估值综合化工修复 + 半导体材料期权”的稳健配置者，重视估值缓冲、官方指引、FCF为正和AUECC/Baytown/Osaka等可验证节点。",
        "- A 最不适合的投资者画像：只追求直接AI收入、高订单/RPO、强价格趋势、高IV和小基数非线性爆发的进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(row['ticker']) for row in strong_b_rows[:10]])}。这些公司通常具备更直接AI收入、更强订单/RPO/backlog、更高右尾或更强价格确认。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：SOMMY 是项目内偏防守/估值修复型材料公司，不是全项目增长冠军；它能压过部分高反证、弱现金流或估值难消化公司，但面对NVDA/AVGO/MU/TSM、AI光互联、服务器/云算力、强电力机电和高纯半导体材料强同业时，多数思路通常落后。",
        "- 后续最重要跟踪数据：FY2026 Q1/Q2 ICT半导体材料是否单独披露；AUECC审批和并表时间；Baytown UHP IPA客户和投产节奏；Osaka光刻胶中心进度；High-NA/有机分子resist认证；advanced back-end/glass core是否有POR/HVM；Agro/Pharma是否兑现指引；FCF、债务和D/E。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "SOMMY"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`¥2,340-2,380bn`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "ICT半导体材料产品级收入、客户名、订单、AUECC并表、High-NA/advanced back-end/glass core客户认证和量产节奏均未充分披露。"]),
        base.row(["最大反证", "FY2026总收入增长低，FCF指引较FY2025显著下降；显示材料、基础化工、Pharma一次性和石化周期会抵消半导体材料增长。"]),
        base.row(["近端催化剂", "AUECC审批/整合、Baytown UHP IPA、Osaka先进光刻胶技术中心、FY2026 Q1/Q2分部收入和利润、Agro/Pharma兑现、FCF和债务下降。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        lines.append(base.row([strategy, a["tiers"][strategy], rank_text[strategy], support[strategy][0], support[strategy][1]]))  # type: ignore[index]

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与SOMMY在半导体材料、电子化学品、光刻胶、高纯化学品、工业气体、基板/玻璃/封装材料或特种化学品需求池重叠，优先比较客户认证、产品收入、利润率、FCF和估值。", "SHECY、ENTG、Q、AJNMY、ASGLY、DD、HOCPY、APD、LIN、MTRN、ROG", "同业证据权重最高；若B有更明确订单、客户POR、产品代际或更高材料增长，可直接压过SOMMY。"]),
        base.row(["相邻替代", "同属材料、电子元件、工业化学品、生命科学工具或AI基础设施资金篮子，但产品不完全竞争；回答资金只能买一个时谁的增长质量和赔率更好。", "MRAAY、SMTOY、DHR、TMO、ECL、VRT、ETN、GEV", "重点比较增长质量、估值消化、现金流和近端催化；不因低估值或材料属性相近而自动胜出。"]),
        base.row(["上下游", "B处于SOMMY材料需求链的晶圆制造、前道设备、封测、AI芯片、光互联、服务器、云算力或终端需求池。", "TSM、ASML、AMAT、LRCX、NVDA、MU、AVGO、SMCI、MSFT、AMZN", "不把下游AI capex自动映射为SOMMY收入；若B直接捕获利润池和订单，B的结论力度会更强。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "RKLB、TSLA、CRWD、CAT、MSI", "默认降低结论力度；除非档位差明显，否则优先微倾向或中性。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]

    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    lines.append(base.row(headers))
    lines.append(base.row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for index, comparison in enumerate(comparisons, start=1):
        b = comparison["b"]
        lines.append(
            base.row(
                [
                    index,
                    base.short_name(b),  # type: ignore[arg-type]
                    base.category_short(str(b.get("category", ""))),  # type: ignore[union-attr]
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],  # type: ignore[list-item]
                    majority(int(comparison["ac"]), int(comparison["bc"]), int(comparison["nc"])),
                    comparison["final"],
                    comparison["reason"],
                ]
            )
        )

    lines += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        lines.append(base.row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    lines += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要SOMMY把高纯化学品、光刻胶、先进后道或glass core从产品图谱转成客户POR、订单金额、产品收入和利润率上修。"
        if comparison["rel"] == "直接同业":
            need = "需要SOMMY在直接材料同业中证明更高客户份额、更快收入确认、更强利润率和更低现金流反证。"
        elif comparison["rel"] == "上下游":
            need = "需要SOMMY证明能实际捕获下游AI芯片/晶圆制造/云算力利润池，而不是只有间接受益。"
        elif comparison["rel"] == "跨赛道":
            need = "需要SOMMY用更强利润兑现、价格确认和估值消化抵消跨赛道标的的高增长或防守属性。"
        lines.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    lines += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B提高NTM收入确认、利润/现金流质量和估值消化能力，或出现明确订单/指引上修。"
        if float(b["scores"]["右尾弹性优先"]) > float(a["scores"]["右尾弹性优先"]):  # type: ignore[index]
            need = "需要B把右尾叙事转成可确认收入和利润，并降低估值、波动或资产负债表反证。"
        lines.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/半导体材料_化学品_基板/SOMMY_住友化学_Sumitomo_Chemical_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/晶圆制造_设备_材料_测试/行业调研_硅片、光刻胶与前道材料_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体高纯水、气体与化学流体系统_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装湿化学与表面处理材料_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_玻璃基板、TGV与玻璃检测_2026-06-11.md`；`行业调研/产业背景/AI产业链瓶颈与反证指标总表_2026-06-10.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`分析报告/公司排序/`、`分析报告/简单排序/`、项目根 `tmp/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV或正式金融行的公司为 {('、'.join(missing_fin) if missing_fin else '无')}。缺失或币种错配字段在估值、价格确认和激进短线列按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_sommy_company_comparison_20260623.py`。脚本复用项目内正式评估与金融资料解析函数，应用项目已有强公司校准，并对SOMMY的综合化工修复、半导体材料期权、低估值、FCF下降、产品级披露不足、ADR缺IV和价格动量偏弱做人工校准后建档。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    base.TARGET = "ALLE"
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 SOMMY 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    a = companies[TARGET]
    print(
        json.dumps(
            {
                "target": TARGET,
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "size": OUT_PATH.stat().st_size,
                "sommy_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "sommy_scores": {strategy: round(float(a.get("scores", {}).get(strategy, 0)), 2) for strategy in STRATS},
                "sommy_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
