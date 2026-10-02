from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "LFUS"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "LFUS_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_COMPONENT_PEERS = {
    "BELFB",
    "VSH",
    "POWI",
    "DIOD",
    "AOSL",
    "ST",
    "IFNNY",
    "MRAAY",
    "TTDKY",
    "MIELY",
    "MPWR",
    "VICR",
    "NVTS",
    "ON",
    "MCHP",
}

ELECTRICAL_ADJACENT = {
    "ETN",
    "HUBB",
    "NVT",
    "ABBNY",
    "POWL",
    "ATKR",
    "AEIS",
    "APD",
    "ENS",
    "FLNC",
    "GEV",
}

DEMAND_CHAIN = {
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
    "DELL",
    "HPE",
    "SMCI",
    "PENG",
    "CLS",
    "FLEX",
    "JBL",
    "PWR",
    "EME",
    "FIX",
    "MYRG",
    "IESC",
    "VRT",
    "TT",
    "CARR",
    "JCI",
    "MOD",
    "AAON",
}


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
    base.score_companies(companies)

    # LFUS-specific calibration:
    # - Current NTM path is well supported by Q2 guidance, Electronics recovery,
    #   Industrial/Basler contribution, and positive FCF.
    # - The AI/DC opportunity is real but still mostly mix and optionality because
    #   data-center revenue, customer design wins, and backlog dollars are not disclosed.
    # - Downside protection deserves only mid-tier treatment because Yahoo shows
    #   negative TTM EPS, IV is not low, and SOXX stress-window drawdown was large.
    lfus = companies[TARGET]
    overrides = {
        "NTM兑现优先": 66.8,
        "右尾弹性优先": 53.5,
        "风险调整收益": 48.8,
        "下行保护优先": 71.0,
        "估值消化优先": 57.5,
        "近端催化优先": 60.5,
        "价格确认/动量": 65.0,
        "激进短线": 76.0,
    }
    for strategy, score in overrides.items():
        lfus["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_COMPONENT_PEERS:
        return "直接同业"
    if ticker in DEMAND_CHAIN:
        return "上下游"
    if ticker in ELECTRICAL_ADJACENT:
        return "相邻替代"
    if category == "配电_电源_功率器件":
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "云算力_IDC_AI软件平台", "电力_发电_能源_储能"}:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
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
            "NTM兑现优先": "A指引/Basler和分部恢复更可兑现",
            "右尾弹性优先": "A有AI机柜保护件和高压保护期权",
            "风险调整收益": "A现金流与增长赔率更均衡",
            "下行保护优先": "A现金流和分散终端更稳",
            "估值消化优先": "A业绩增长更能消化估值",
            "近端催化优先": "A有Q2/Q3、Basler和708验证",
            "价格确认/动量": "A近月价格确认更强",
            "激进短线": "A AI rack保护件叙事可重定价",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/订单兑现更硬",
            "右尾弹性优先": "B右尾收入弹性更大",
            "风险调整收益": "B上行下行组合更好",
            "下行保护优先": "B现金流或压力期更稳",
            "估值消化优先": "B估值更容易被业绩消化",
            "近端催化优先": "B近端订单/产品催化更强",
            "价格确认/动量": "B价格确认更强",
            "激进短线": "B高beta和事件弹性更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "估值消化优先"}:
        return "估值和兑现证据接近"
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
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 8:  # type: ignore[index,operator]
            return "LFUS 的 Q2 指引、Electronics 恢复和 Basler 年化让 NTM 路径更清楚。"
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 10:  # type: ignore[index,operator]
            return "LFUS 的自由现金流和分散终端需求给组合提供更好缓冲。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 8:  # type: ignore[index,operator]
            return "LFUS 的基准增长、EBITDA 和 FCF 更能支撑当前估值。"
        return "LFUS 的经营兑现和现金流质量略好，B 的上行证据不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接 AI 收入、订单/RPO 或小基数右尾明显强于 LFUS。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/订单兑现证据更硬。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 10:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、防守属性或压力期表现更好。"
    if b["scores"]["近端催化优先"] - a["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
        return f"{b['ticker']} 的近端订单、产品或财报催化更可见。"
    return f"{b['ticker']} 在多数投资思路下比 LFUS 更符合项目内资金配置目标。"


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
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["NTM兑现优先"] - x["b"]["scores"]["NTM兑现优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:40]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:40]  # type: ignore[operator]
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
        f"TTM PE 不适用，Forward PE `{fin.get('forward_pe')}`，P/S `{fin.get('ps')}`，"
        f"EV/EBITDA `{fin.get('ev_ebitda')}`，Call IV `{fin.get('call_iv')}%`，Put IV `{fin.get('put_iv')}%`；"
        f"2026-06-03 过去两周 `{mom2.get('mom2w')}%`、过去一月 `{mom1.get('mom1m')}%`；"
        f"2026-06-04 三段 SOXX 压力窗口累计 `{soxx.get('soxx_cum')}%`。"
    )
    support = {
        "NTM兑现优先": (
            "2026Q1收入`$657M`、Q2指引`$690-710M`、NTM基准`$2.78-2.95B`，Basler和Electronics恢复有收入表支撑",
            "未披露data center收入、backlog dollar、客户名和book-to-bill，AI/DC子集不能放大",
        ),
        "右尾弹性优先": (
            "48V/54V AI rack保护、NANO2 708、Basler data center/grid、800VDC/solid-state protection提供期权",
            "极度乐观需要客户AVL/设计赢单和多项目兑现；公司不是AI电源/UPS/PDU总包商",
        ),
        "风险调整收益": (
            "基准FCF`$300-430M`、EBITDA`$625-700M`和分散终端需求提供经营底座",
            "Forward PE`28.33`、P/S`4.97`不便宜，Yahoo TTM EPS为负，压力期回撤大",
        ),
        "下行保护优先": (
            "保护件/熔断器/Transportation现金流和Basler高可靠控制业务具备一定防守性",
            "Call IV约`51.6%`且SOXX三段压力累计`-63.23%`，不是防守顶档",
        ),
        "估值消化优先": (
            "FY2025收入`$2.386B`到NTM基准`$2.78-2.95B`，利润和FCF可随mix改善",
            "当前价格已反映部分周期修复，若Electronics/Industrial不继续上修则估值消化一般",
        ),
        "近端催化优先": (
            "Q2/Q3实际与指引、Electronics organic、Industrial/Basler、708 Series设计赢单都是近端跟踪项",
            "缺少可量化订单/RPO，催化强度弱于AI芯片、光互联、NeoCloud和电力设备龙头",
        ),
        "价格确认/动量": (
            "过去两周`+9.83%`、过去一月`+19.06%`，2026-06-22价格高于6月3日收盘",
            "动量更多是周期修复和AI/DC期权重估，不是全项目最强价格确认",
        ),
        "激进短线": (
            "中等偏高IV、近期涨幅和AI rack保护件新品可支持事件交易",
            "右尾、市值弹性和资金关注度弱于纯AI小基数或高beta标的",
        ),
    }

    out: list[str] = []
    out += [
        "# LFUS 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：LFUS / Littelfuse",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 LFUS vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。LFUS 的强项是 NTM 经营兑现、Electronics/Industrial 分部恢复、Basler 年化、FCF 和 48V/高压保护件可选性，而不是纯 AI 高 beta。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 data center/AI revenue、客户 design-win、backlog dollar 未披露，估值不低且 SOXX 压力窗口历史回撤较大。",
        "- A 最适合的投资者画像：希望买高质量电子/工业保护件公司、能接受传统汽车/工业周期，但想保留 AI 数据中心电力保护期权的中期基本面资金。",
        "- A 最不适合的投资者画像：只追求最强 AI 右尾、明确 RPO/backlog、极端短线高弹性或公用事业式防守的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在直接 AI 收入、订单/RPO、右尾弹性、近端产品催化、估值消化或压力期防守上压过 LFUS。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：LFUS 是全项目中上质量的电气/保护件复合标的；多数情况下适合 NTM兑现和稳健增长，不适合右尾至上或激进短线至上。",
        "- 后续最重要跟踪数据：2026Q2实际收入和Q3指引、Electronics organic/passive/protection semiconductor、Industrial organic和Basler margin、data center/grid项目措辞、708 Series客户AVL/订单/lead time、800VDC/HVDC design-win、gross margin、adjusted EBITDA、FCF和库存周转。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "LFUS"]),
        base.row(["公司名称", "Littelfuse"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["scenarios"]["base"].get("NTM 公司收入", "缺失")]),  # type: ignore[index]
        base.row(["乐观/极度乐观收入", f"{a['scenarios']['bull'].get('NTM 公司收入', '缺失')} / {a['scenarios']['extreme'].get('NTM 公司收入', '缺失')}"]),  # type: ignore[index]
        base.row(["利润和现金流结论", f"{a['scenarios']['base'].get('EBITDA/净利润', '')}；{a['scenarios']['base'].get('自由现金流方向', '')}"]),  # type: ignore[index]
        base.row(["最大传导瓶颈", "未披露 data center revenue、AI revenue、segment backlog、book-to-bill、客户项目金额或 hyperscaler design win。"]),
        base.row(["最大反证", "AI/DC子集无法可靠拆分；power semiconductor sales lower；800VDC/HVDC更偏远期期权；SOXX压力窗口回撤大。"]),
        base.row(["近端催化剂", "2026Q2实际与Q3指引、Electronics和Industrial/Basler走势、708 Series客户验证、data center/grid订单措辞、800VDC/HVDC design-win。"]),
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
        base.row(["直接同业", "产品、客户或需求池与 LFUS 的熔断、保护件、分立/功率器件、被动元件或电源保护环节高度重叠。", "BELFB、VSH、POWI、DIOD、AOSL、ST、IFNNY、MRAAY、MPWR", "优先看同一电子/工业/电源保护需求池中的收入兑现、margin、客户认证、产品代际和估值。"]),
        base.row(["相邻替代", "同属数据中心电力、配电、电源、工业电气或高可靠保护投资篮子，但产品不直接互替。", "ETN、HUBB、NVT、ABBNY、POWL、ATKR、VRT", "回答资金只能买一个时，谁的增长质量、订单可见度、估值消化和风险收益更好。"]),
        base.row(["上下游", "一方处在 AI 数据中心、服务器、云/IDC、电网/MEP 或设备需求链，另一方是保护/控制/电气部件供应端。", "MSFT、AMZN、DELL、SMCI、PWR、EME、FIX、GEV、VRT", "不把下游收入规模直接等同 LFUS 机会，重点看利润捕获、认证壁垒和订单可确认性。"]),
        base.row(["跨赛道", "半导体设备、材料、软件、光互联或其他业务差异较大的公司，仍作为项目资金配置替代比较。", "NVDA、ASML、TSM、CDNS、LIN、TMO、COHR", "默认降低结论力度；只有增长质量、估值消化或风险收益明显拉开时才给建议/强烈建议。"]),
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
                    "LFUS" if comparison["final"] == "A" else b["ticker"],
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
        need = "需要 LFUS 披露 data center/AI revenue、客户AVL、backlog/order dollar，并证明Electronics和Industrial margin连续上修。"
        if comparison["rel"] == "直接同业":
            need = "需要 LFUS 在同业中证明更强保护件design-win、认证壁垒、margin和估值消化，而不是只靠宽泛AI电力叙事。"
        elif comparison["rel"] == "上下游":
            need = "需要 LFUS 证明自己能比上下游公司更有效捕获AI数据中心利润池，并把保护件机会转成可确认收入。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 LFUS 用更强增长、现金流或估值消化抵消跨赛道标的的技术、订单或右尾优势。"
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
        need = "需要 B 提供更硬订单/RPO、更强NTM收入利润兑现，或证明估值/现金流反证低于 LFUS。"
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
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 181 家，本次公司评估全集为 {n} 家；缺少可用价格/估值或价格缺失的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/配电_电源_功率器件/LFUS_Littelfuse_公司调研_2026-06-12.md`、`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心低压配电、PDU与母线槽_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_lfus_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对 LFUS 做专门档位校准；未读取下游量化目录或现成排序结论。",
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
        "lfus_tiers": companies[TARGET]["tiers"],
        "lfus_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
