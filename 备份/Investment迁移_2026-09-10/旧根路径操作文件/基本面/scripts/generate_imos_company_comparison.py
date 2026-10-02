from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "IMOS"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "IMOS_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_OSAT = {"ASX", "AMKR"}
PACKAGING_TEST_ADJACENT = {
    "AEHR",
    "ASMVY",
    "ATEYY",
    "BESIY",
    "CAMT",
    "COHU",
    "FORM",
    "KEYS",
    "KLIC",
    "MICLF",
    "ONTO",
    "PLAB",
    "TDY",
    "TMO",
    "TER",
}
MEMORY_AND_FOUNDARY_CHAIN = {
    "MU",
    "SNDK",
    "WDC",
    "STX",
    "SIMO",
    "RMBS",
    "TSM",
    "UMC",
    "GFS",
    "TSEM",
    "INTC",
}
AI_CHIP_AND_SYSTEM_DEMAND = {
    "NVDA",
    "AMD",
    "AVGO",
    "MRVL",
    "QCOM",
    "ARM",
    "ALAB",
    "CDNS",
    "SNPS",
    "ANET",
    "CRDO",
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
    "SMCI",
    "DELL",
    "HPE",
    "JBL",
    "CLS",
    "FLEX",
    "SANM",
    "PENG",
}
PACKAGING_SUPPLY_CHAIN = {
    "AJNMY",
    "ASGLY",
    "AXTI",
    "CC",
    "ENTG",
    "HOCPY",
    "LIN",
    "MTRN",
    "Q",
    "ROG",
    "SHECY",
    "SOMMY",
    "SMTOY",
    "MRAAY",
    "TTDKY",
    "DD",
    "AMAT",
    "ASML",
    "ASMIY",
    "DSCSY",
    "KLAC",
    "LRCX",
    "MKSI",
    "NVMI",
    "TOELY",
    "UCTT",
    "VECO",
    "ICHR",
    "ACMR",
}
SEMI_RELATED_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI服务器_存储_EMS",
    "AI网络_光互联_连接器",
    "半导体材料_化学品_基板",
    "封测_检测_计量_光罩",
    "晶圆制造_前道设备",
}


def mid_growth(value: object) -> float | None:
    text = str(value).replace("−", "-").replace("～", "-").replace("—", "-").replace("–", "-")
    ranged = re.search(
        r"([+-]?)\s*(\d+(?:\.\d+)?)\s*%\s*(?:至|到|-)\s*([+-]?)\s*(\d+(?:\.\d+)?)\s*%",
        text,
    )
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

    # IMOS-specific calibration. Generic scoring overstates cheapness because
    # the daily P/S field is flagged as USD/TWD currency mismatch, and it
    # understates the near-term monthly-revenue catalyst because ChipMOS uses
    # monthly Taiwan revenue releases instead of US-style backlog/RPO.
    imos = companies[TARGET]
    overrides = {
        "NTM兑现优先": 76.0,
        "右尾弹性优先": 68.0,
        "风险调整收益": 55.0,
        "下行保护优先": 72.0,
        "估值消化优先": 54.0,
        "近端催化优先": 70.0,
        "价格确认/动量": 91.0,
        "激进短线": 90.0,
    }
    for strategy, score in overrides.items():
        imos["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_OSAT:
        return "直接同业"
    if ticker in PACKAGING_TEST_ADJACENT:
        return "相邻替代"
    if ticker in MEMORY_AND_FOUNDARY_CHAIN or ticker in AI_CHIP_AND_SYSTEM_DEMAND or ticker in PACKAGING_SUPPLY_CHAIN:
        return "上下游"
    if category == "封测_检测_计量_光罩":
        return "相邻替代"
    if category in SEMI_RELATED_CATS:
        return "上下游"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A月营收和memory/test兑现更清楚",
            "右尾弹性优先": "A存储后道小基数弹性更好",
            "风险调整收益": "A有增速但需扣高PE和低毛利",
            "下行保护优先": "A现金和压力窗口韧性较好",
            "估值消化优先": "A高增长可部分消化估值",
            "近端催化优先": "A月营收/Q2毛利验证更近",
            "价格确认/动量": "A近期价格确认更强",
            "激进短线": "A高IV叠加存储后道更易进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/RPO或订单兑现更硬",
            "右尾弹性优先": "B右尾更大或更接近AI主链",
            "风险调整收益": "B赔率、现金流或估值更好",
            "下行保护优先": "B现金流/防守属性更强",
            "估值消化优先": "B估值消化压力更低",
            "近端催化优先": "B近端客户/产品催化更强",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B短线关注度和爆发力更强",
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
    a_count, b_count, _neutral = direction_counts(cells)
    if a_count > b_count:
        return "A"
    if b_count > a_count:
        return "B"
    return "A" if a["scores"]["风险调整收益"] >= b["scores"]["风险调整收益"] else "B"  # type: ignore[index,operator]


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "IMOS 的月营收、存储后道和testing需求让NTM兑现更清楚。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
            return "IMOS 的6月营收、Q2毛利率和memory mix验证窗口更近。"
        if a["scores"]["价格确认/动量"] - b["scores"]["价格确认/动量"] > 10:  # type: ignore[index,operator]
            return "IMOS 近期价格已验证存储后道复苏和AI storage外溢。"
        return "IMOS 的存储后道兑现和短线确认略好，B 的优势不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI收入、平台利润池或小基数右尾明显强于 IMOS。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化压力明显低于 IMOS。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的风险调整收益、现金流或估值安全边际更好。"
    return f"{b['ticker']} 在多数投资思路下比 IMOS 更符合项目内资金配置目标。"


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
        key=lambda x: (
            x["bc"] - x["ac"],
            x["b"]["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            x["ac"] - x["bc"],
            a["scores"]["近端催化优先"] - x["b"]["scores"]["近端催化优先"],  # type: ignore[index,operator]
        ),
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
        f"2026-06-22 IMOS ADS价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"日度P/S源字段 {fmt_num(fin.get('ps'))} 但已被标记为USD/TWD币种错配；"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = []
    for product in a["products"]:  # type: ignore[index]
        name = str(product[0]).split("：")[0]
        if any(excluded in name for excluded in ["HBM stack", "CoWoS", "GPU package", "CPO 光口直接收入"]):
            continue
        product_names.append(name)
        if len(product_names) >= 6:
            break
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "2026Q1收入+25.4% YoY，4月+32.2%、5月+17.7%，NTM基准NT$30.5-33.5B",
            "没有传统backlog/RPO；客户forecasts和LTA金额未披露，毛利率尚未非线性扩张",
        ),
        "右尾弹性优先": (
            "DRAM/DDR5、Flash/NAND/eSSD、testing bottleneck和DDR5 PMIC/AI ASIC support提供小基数上行",
            "AI传导是二阶存储后道；无HBM stack、CoWoS、GPU package或CPO直接主链收入证据",
        ),
        "风险调整收益": (
            "基准收入增速27%-40%，Q1 FCF NT$1.1093B，现金NT$12.3869B",
            "Forward PE约69.6、Call IV 66.7%，OSAT毛利率低且新增capex可能先压现金流",
        ),
        "下行保护优先": (
            "DDIC/gold bump现金流底座、现金余额和SOXX压力窗口累计-18.37%提供韧性",
            "存储/Flash周期、金价/BT substrate/电费和折旧会在下行期放大利润波动",
        ),
        "估值消化优先": (
            "若月营收维持NT$2.35B以上且毛利率回到15%+，收入增长可部分消化估值",
            "日度P/S字段币种错配不可当低估依据，PE仍高，利润率兑现是硬约束",
        ),
        "近端催化优先": (
            "6月月营收、2026Q2财报、H1毛利率、memory/Flash/DDIC mix和LTA/take-or-pay线索都很近",
            "催化主要是月度和毛利率验证，不是单个可披露GPU/HBM主链订单",
        ),
        "价格确认/动量": (
            "2026-06-03两周+29.41%、一月+37.61%，2026-06-22价格进一步到70.29美元",
            "涨幅已部分交易存储后道复苏，高IV说明短线预期拥挤",
        ),
        "激进短线": (
            "高IV、小市值、强动量和AI storage/DDR5后道叙事使短线进攻属性上升",
            "直接AI主链证据不足，爆发力仍弱于GPU/HBM/光互联/NeoCloud高关注标的",
        ),
    }

    out: list[str] = []
    out += [
        "# IMOS 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：IMOS / ChipMOS Technologies 南茂科技",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 IMOS vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。IMOS 的优势来自 2026Q1和4-5月月营收高增、存储后道/testing供需紧、近期价格确认和1-2个季度内的月营收/毛利率验证。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是AI传导仍是二阶存储后道，缺少HBM/CoWoS/GPU/CPO直接主链收入，Forward PE和IV偏高，且毛利率、折旧和材料成本会限制估值消化。",
        "- A 最适合的投资者画像：愿意押注AI storage、DDR5和存储测试外溢，偏好月度数据快速验证和中小市值高弹性，同时能承受OSAT低毛利、客户forecast不等于backlog和高IV回撤的进取型资金。",
        "- A 最不适合的投资者画像：只追求最高定价权、直接GPU/HBM主链、低估值低波动下行保护，或要求订单/RPO和客户金额已经完全披露的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常拥有更直接AI收入、平台利润池、更低估值消化压力或更强右尾叙事。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：IMOS 位于项目内中游偏上；它强于很多低增长/弱动量公司，也能在近端催化和动量列战胜部分大盘防守标的，但总体仍弱于直接AI主链、先进封装龙头、核心设备/EDA和部分订单更硬的电力/光互联标的。",
        "- 后续最重要跟踪数据：2026年6月及后续月营收、2026Q2财报、H1毛利率和经营利润率、memory/Flash/DDIC mix、testing utilization、LTA/take-or-pay或客户forecast转订单、AI-related ASIC/DDR5 PMIC认证与量产、金价/BT substrate/电费传导。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "IMOS"]),
        base.row(["公司名称", "ChipMOS Technologies 南茂科技"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "NT$30.5-33.5B"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI/cloud memory需求必须转成客户订单、后道产能、测试设备/人力、价格重谈和收入确认；当前客户forecasts、LTA金额和AI ASIC量产收入未充分披露。"]),
        base.row(["最大反证", "没有公开证据显示IMOS是NVIDIA GPU、HBM stack、CoWoS或CPO主链供应商；Q1毛利率未非线性扩张，新增testing/memory capex可能先压现金流。"]),
        base.row(["近端催化剂", "2026年6月月营收、2026Q2/H1毛利率、memory/Flash/DDIC mix、testing utilization、LTA/take-or-pay披露、DDR5 PMIC/AI ASIC认证和量产信息。"]),
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
        base.row(["直接同业", "同属OSAT/封测服务，优先比较先进封装、memory后道、testing收入、客户认证、毛利率、capex和现金流。", "ASX、AMKR", "同业证据权重最高；IMOS若只在存储后道强而对手在先进封装/规模更强，结论需压低力度。"]),
        base.row(["相邻替代", "同处测试设备、后段设备、封装材料或AI基础设施资金篮子，但收入模式不同。", "ATEYY、TER、FORM、COHU、KLIC、BESIY、CAMT、VRT", "重点看资金只能买一个时，谁的订单可见度、利润池、估值消化和近端催化更好。"]),
        base.row(["上下游", "B 是 IMOS 的需求源、客户、存储/foundry平台、材料/设备供应链或AI系统链条。", "MU、SNDK、TSM、NVDA、AMD、AVGO、AMAT、ASML、AJNMY", "不把下游AI收入规模直接等同IMOS收入，也不把上游设备/材料稀缺自动等同更好；核心看利润捕获和反证。"]),
        base.row(["跨赛道", "业务差异大，但仍作为项目内资金配置替代比较风险调整收益、估值消化、下行保护和催化可见度。", "LIN、DHR、TMO、CAT、MSI、RYCEY", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要 IMOS 连续月营收和毛利率超预期，披露更明确LTA/take-or-pay或AI ASIC/DDR5 PMIC量产收入，并证明高PE和高IV可被利润兑现消化。"
        if comparison["rel"] == "直接同业":
            need = "需要 IMOS 在同业中证明memory/test收入和利润弹性强于B，同时缩小先进封装、规模和客户质量差距。"
        elif comparison["rel"] == "上下游":
            need = "需要 IMOS 证明比该上下游公司更能捕获AI存储/后段利润池，而不是只承担客户capex周期和折旧风险。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 IMOS 用更强现金流、估值消化或压力期韧性抵消跨赛道标的的防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更强NTM收入利润兑现、或更好近端价格确认来抵消IMOS的月营收和存储后道弹性。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要 B 把右尾叙事转成可确认收入/利润，并降低估值、现金流或执行反证。"
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
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/封测_检测_计量_光罩/IMOS_ChipMOS_Technologies_南茂科技_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_HBM与存储测试设备_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_探针卡、ATE与系统级测试_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_封装基板、中介层与RDL_2026-06-10.md`、`行业调研/产业背景/AI产业链瓶颈与反证指标总表_2026-06-10.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 自动化脚本：`scripts/generate_imos_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+27%-40%` 做同号区间修正后建档；未读取下游量化目录或现成排序结论。",
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
                "imos_tiers": companies[TARGET]["tiers"],
                "imos_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
