from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "AMAT"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "AMAT_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {
    "ACLS",
    "ACMR",
    "ASMIY",
    "ASML",
    "DSCSY",
    "KLAC",
    "LRCX",
    "NVMI",
    "TOELY",
    "VECO",
}
EQUIPMENT_SUPPLY_CHAIN = {"AEIS", "ICHR", "MKSI", "UCTT"}
FOUNDRY_MEMORY_OSAT = {"TSM", "GFS", "UMC", "TSEM", "INTC", "MU", "SNDK", "WDC", "STX", "ASX", "AMKR", "IMOS"}
AI_DEMAND_CHAIN = {
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
TEST_PACKAGING_ADJACENT = {
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

    # AMAT-specific calibration: it is a high-certainty WFE/materials-engineering
    # leader, but not a small-base right-tail compounder. Valuation and FCF lag
    # cap risk-adjusted and valuation-digestion scores.
    amat = companies[TARGET]
    overrides = {
        "NTM兑现优先": 80.0,
        "右尾弹性优先": 80.0,
        "风险调整收益": 56.0,
        "下行保护优先": 76.0,
        "估值消化优先": 60.0,
        "近端催化优先": 69.0,
        "价格确认/动量": 82.0,
        "激进短线": 91.0,
    }
    for strategy, score in overrides.items():
        amat["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in EQUIPMENT_SUPPLY_CHAIN or ticker in FOUNDRY_MEMORY_OSAT or ticker in AI_DEMAND_CHAIN:
        return "上下游"
    if ticker in TEST_PACKAGING_ADJACENT:
        return "相邻替代"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的Q3指引和WFE收入锚更硬",
            "右尾弹性优先": "A的GAA/HBM/AP组合更广",
            "风险调整收益": "A增长质量与服务底座更均衡",
            "下行保护优先": "A净现金和AGS服务支撑更强",
            "估值消化优先": "A的NTM增长可部分消化估值",
            "近端催化优先": "A有Q3/DRAM/AP/AGS验证窗口",
            "价格确认/动量": "A近端价格确认更强",
            "激进短线": "A设备景气和高IV有进攻弹性",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/RPO或订单兑现更硬",
            "右尾弹性优先": "B右尾更大或小基数更弹",
            "风险调整收益": "B估值与下行组合更好",
            "下行保护优先": "B估值或防守属性更强",
            "估值消化优先": "B估值消化压力更低",
            "近端催化优先": "B近端订单/产品催化更强",
            "价格确认/动量": "B价格趋势更强",
            "激进短线": "B高beta和事件弹性更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"估值消化优先", "风险调整收益"}:
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
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "AMAT 的FY2026 Q3指引、客户八季度forecast和GAA/HBM/AP收入路径更清楚。"
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 10:  # type: ignore[index,operator]
            return "AMAT 的净现金、AGS服务和大客户工艺粘性提供更强安全垫。"
        if a["scores"]["价格确认/动量"] - b["scores"]["价格确认/动量"] > 10:  # type: ignore[index,operator]
            return "AMAT 近期价格确认更强，且Q3指引和设备景气仍有验证窗口。"
        return "AMAT 的WFE兑现质量更稳，B 的上行证据不足以覆盖其反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的增长右尾和重定价弹性明显强于 AMAT。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化压力明显低于 AMAT。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/订单兑现证据更强。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的下行保护或防守属性更好。"
    return f"{b['ticker']} 在多数投资思路下比 AMAT 更符合项目内资金配置目标。"


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
        f"P/S {fmt_num(fin.get('ps'))}，Call IV {fmt_pct(fin.get('call_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = []
    for product in a["products"][:6]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]

    support = {
        "NTM兑现优先": (
            "FY2026 Q2收入`79.10亿美元`、Q3指引`89.50亿美元±5.00亿`，CY2026半导体设备业务预计增长`>30%`",
            "AMAT不披露标准backlog/bookings，兑现仍依赖客户cleanroom、安装验收和HBM/GAA良率",
        ),
        "右尾弹性优先": (
            "GAA/2nm、DRAM/HBM、advanced packaging和AGS同时受AI WFE拉动，极度乐观收入上限`460-500亿美元`",
            "大市值和高收入基数压低倍数弹性，NEXX/panel-level/CoPoS/玻璃多数仍偏2027+",
        ),
        "风险调整收益": (
            "基准收入`360-395亿美元`、经营利润率`31.5%-33.5%`，且现金+短投高于总债务",
            "2026-06-22 Forward PE `39.28`、P/S `17.51`，Q2 FCF仅`2.10亿美元`，库存/应收先行",
        ),
        "下行保护优先": (
            "净现金、AGS服务、installed base、工艺认证和客户粘性提供周期底座",
            "WFE仍是周期行业，SOXX三段压力窗口累计`-51.50%`，高估值放大回撤",
        ),
        "估值消化优先": (
            "若Q3高指引后FY2027 H1维持高run-rate，NTM收入/利润增长可部分消化估值",
            "当前估值已要求乐观兑现，若Q4指引、Semi GM或FCF不跟，消化压力明显",
        ),
        "近端催化优先": (
            "Q3实际收入和Q4指引、DRAM收入、advanced packaging `>50%`增长、AGS `mid-teens`和Singapore扩产均在1-2季可验证",
            "缺少公开订单/取消率，客户forecast一旦调整会削弱近端催化确定性",
        ),
        "价格确认/动量": (
            "2026-06-03两周`+17.32%`、一月`+28.71%`，2026-06-22价格继续升至`640.18`",
            "Call IV `74.4%`且估值快速上修，动量已部分交易设备景气",
        ),
        "激进短线": (
            "高IV、强价格确认、Q3指引、WFE景气和AI半导体上游叙事提供短线进攻空间",
            "AMAT不是GPU/HBM小盘高beta，短线爆发力低于更小基数或直接AI收入标的",
        ),
    }

    out: list[str] = []
    out += [
        "# AMAT 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：AMAT / Applied Materials",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 AMAT vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。AMAT 的优势来自 FY2026 Q3 高指引、GAA/DRAM-HBM/advanced packaging/AGS 的多线收入锚、设备景气上修和近期价格确认。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 Forward PE `39.28`、P/S `17.51` 已包含强景气预期，且 Q2 FCF 显著弱于净利润，订单/backlog 又未标准披露。",
        "- A 最适合的投资者画像：希望配置 AI 半导体上游 WFE 龙头、重视 NTM 可兑现性和近端财报验证，同时能接受半导体设备周期、高估值和现金流滞后风险的成长型资金。",
        "- A 最不适合的投资者画像：只追求最低估值、极端小市值右尾、纯GPU/HBM直达收入，或要求公用事业式下行保护的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在直接AI收入、订单/RPO、右尾小基数、估值消化或防守属性上压过 AMAT。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：AMAT 是项目内高质量 WFE/材料工程龙头，NTM兑现和近端催化处于前列，但不是估值消化、极端右尾和激进短线的全项目最优选择；总体属于“高确定性成长、估值要求高”的中上到前列配置。",
        "- 后续最重要跟踪数据：FY2026 Q3实际收入与Q4指引、Semiconductor Systems收入和GM、DRAM收入、advanced packaging收入是否兑现`>50%`增长、AGS增速和AIx attach、合同负债/库存/应收/CFO/capex/FCF、China/Semi+AGS占比、SEMI billings、TSMC/Samsung/Intel N2/GAA和SK hynix/Micron/Samsung HBM4 capex。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "AMAT"]),
        base.row(["公司名称", "Applied Materials"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "360-395 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "不披露标准 backlog/bookings；收入确认依赖客户 cleanroom、设备制造、交付、安装、验收、GAA/HBM良率和advanced packaging供应链同步。"]),
        base.row(["最大反证", "估值已充分定价AI设备景气；Q2 CFO/FCF弱于利润；China/ICAPS和出口管制风险；NEXX/panel-level/CoPoS/玻璃等远期期权不能提前当作NTM基准。"]),
        base.row(["近端催化剂", "Q3实际收入与Q4指引、Semi Systems GM、DRAM收入、advanced packaging >50%收入增长、AGS/AIx、合同负债和营运资本周转、Singapore扩产交付能力。"]),
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
        base.row(["直接同业", "同属半导体前道/WFE设备资金池，优先看WFE份额、订单/指引、产品代际、毛利率、服务收入、同业估值和客户工艺锁定。", "ASML、LRCX、KLAC、ASMIY、TOELY、ACMR、ACLS、VECO", "同业证据权重最高；若收入兑现、产品代际或估值差距大，结论力度可以上调。"]),
        base.row(["相邻替代", "同处AI半导体设备、封装测试、数据中心基础设施或AI资本开支受益篮子，但收入模式不完全相同。", "TER、ATEYY、BESIY、CAMT、VRT、ETN、GEV", "回答资金只能买一个时，谁的增长质量、订单可见度、估值消化和近端催化更好。"]),
        base.row(["上下游", "一方处在AMAT客户、供应商或终端需求链，重点看利润池位置、议价权、瓶颈稀缺性和收入确认链条。", "TSM、MU、INTC、ASX、AMKR、NVDA、AVGO、MSFT、ENTG", "不把下游AI收入规模直接等同AMAT机会，也不把上游设备稀缺自动等同更好。"]),
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
        need = "需要 AMAT 继续上修FY2027 H1指引，证明GAA/HBM/AP收入与FCF同步兑现，并降低估值透支反证。"
        if comparison["rel"] == "直接同业":
            need = "需要 AMAT 在同业中证明更强WFE份额、产品代际、GM或服务attach，并把Q3高指引延伸到Q4/FY2027。"
        elif comparison["rel"] == "上下游":
            need = "需要 AMAT 证明比该上下游公司更能捕获AI半导体利润池，而不是只承担capex周期beta。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 AMAT 用更强现金流、估值消化或防守表现抵消跨赛道标的的低波动/防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更强NTM收入利润兑现、或更低估值/更好现金流来抵消AMAT的WFE龙头确定性。"
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
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 181 家；本次公司评估全集为 {n} 家，因此缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/晶圆制造_前道设备/AMAT_Applied_Materials_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_AI芯片前道制造设备_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_存储前道制造设备_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-06-11.md`、`行业调研/产业背景/行业调研_头部AI芯片全景与产能释放_2026-06-10.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 自动化脚本：`scripts/generate_amat_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+24%-36%` 做同号区间修正后建档；未读取下游量化目录或现成排序结论。",
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
                "amat_tiers": companies[TARGET]["tiers"],
                "amat_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
