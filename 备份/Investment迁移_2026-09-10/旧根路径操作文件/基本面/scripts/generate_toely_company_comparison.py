from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "TOELY"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "TOELY_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH
base.FIN_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-23.md"
base.MOM2W_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去两周_2026-06-23.md"
base.MOM1M_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去1个月_2026-06-23.md"
base.SOXX_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md"

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
    "DSCSY",
    "KLAC",
    "LRCX",
    "NVMI",
    "VECO",
}
EQUIPMENT_SUPPLY_CHAIN = {
    "AEIS",
    "ENTG",
    "HOCPY",
    "ICHR",
    "MKSI",
    "MTRN",
    "PLAB",
    "Q",
    "ROG",
    "SHECY",
    "UCTT",
}
FOUNDRY_MEMORY_CUSTOMERS = {
    "GFS",
    "INTC",
    "MU",
    "SNDK",
    "STX",
    "TSEM",
    "TSM",
    "UMC",
    "WDC",
}
AI_DEMAND_CHAIN = {
    "ALAB",
    "AMD",
    "AMZN",
    "ANET",
    "APLD",
    "ARM",
    "AVGO",
    "BABA",
    "CDNS",
    "CRDO",
    "CRWV",
    "DELL",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "META",
    "MRVL",
    "MSFT",
    "NBIS",
    "NVDA",
    "ORCL",
    "QCOM",
    "SMCI",
    "SNPS",
}
PACKAGING_TEST_ADJACENT = {
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

    # TOELY calibration: Tokyo Electron has strong NTM operating visibility from
    # FY2027 H1 guidance, H2 > H1 management commentary, coater/developer share,
    # advanced packaging mix, Field Solutions, and bonding/laser optionality. The
    # offsets are high valuation, no formal backlog disclosure, OTC ADR/JPY
    # currency noise, no listed options chain in the daily source, and WFE cycle
    # / China / customer cleanroom acceptance risks.
    a = companies[TARGET]
    overrides = {
        "NTM兑现优先": 85.0,
        "右尾弹性优先": 86.0,
        "风险调整收益": 52.0,
        "下行保护优先": 56.0,
        "估值消化优先": 48.0,
        "近端催化优先": 82.0,
        "价格确认/动量": 88.0,
        "激进短线": 84.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_WFE_PEERS:
        return "直接同业"
    if ticker in EQUIPMENT_SUPPLY_CHAIN or ticker in FOUNDRY_MEMORY_CUSTOMERS or ticker in AI_DEMAND_CHAIN:
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
            "NTM兑现优先": "A有FY2027 H1指引和H2上修锚",
            "右尾弹性优先": "A的AP和bonding小基数更硬",
            "风险调整收益": "A设备瓶颈和利润质量更均衡",
            "下行保护优先": "A服务收入和高份额提供底盘",
            "估值消化优先": "A收入利润增速可部分消化估值",
            "近端催化优先": "A H1/H2订单验证窗口更近",
            "价格确认/动量": "A两周和一月动量更强",
            "激进短线": "A高动量叠加AP叙事更适合进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/RPO或订单兑现更硬",
            "右尾弹性优先": "B右尾更直接或小基数更弹",
            "风险调整收益": "B估值与下行组合更好",
            "下行保护优先": "B低估值/低IV或现金流更稳",
            "估值消化优先": "B估值消化压力更低",
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
            return "TOELY 的FY2027 H1指引、H2高于H1和coater高份额让NTM兑现更硬。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 10:  # type: ignore[index,operator]
            return "TOELY 的advanced packaging、bonding/laser和WFE上行右尾更可收入化。"
        if a["scores"]["价格确认/动量"] - b["scores"]["价格确认/动量"] > 10:  # type: ignore[index,operator]
            return "TOELY 近期价格确认明显更强，市场已开始验证设备景气和AP弹性。"
        return "TOELY 的WFE瓶颈稀缺性和利润质量更好，B 的优势不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI收入、小基数或短线右尾明显强于 TOELY。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的当前估值更容易被NTM业绩消化。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的低波动、低估值或现金流防守属性更好。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/RPO/订单兑现证据更强。"
    return f"{b['ticker']} 在多数投资思路下比 TOELY 更符合项目内资金配置目标。"


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
        f"2026-06-23 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}（USD/JPY币种错配，日度文件标为bad，估值列保守处理），"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-23 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-23 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "FY2027 H1指引收入`15,700亿日元`、OP`4,310亿日元`，H2预计高于H1，FY2027 `3万亿日元+`收入目标进入视野",
            "H2不是全量firm backlog，inquiry/production slot仍需转订单、出货、安装和验收",
        ),
        "右尾弹性优先": (
            "coater/developer市占约91%，advanced packaging FY2027预计>60%，bonding-related从约300亿日元向1-2年>1,000亿日元跃迁",
            "hybrid bonding、HBM4E、SoIC/BSPDN和3D DRAM大规模收入多数仍需客户POR和HVM确认",
        ),
        "风险调整收益": (
            "Field Solutions FY2026 6,260亿日元、+16.3%，coater高份额、权益比率71.5%和正经营现金流支撑质量",
            "2026-06-23 TTM PE 57.85，Forward PE缺失，P/S因币种错配不可直接使用，WFE周期和出口/China风险仍重",
        ),
        "下行保护优先": (
            "服务/备件/改造收入、客户工艺锁定和较强资产负债表提供底盘",
            "三段SOXX压力窗口累计`-57.10%`，接近SOXX整体压力，说明不是低回撤防守资产",
        ),
        "估值消化优先": (
            "NTM基准收入`31,000-33,000亿日元`、OPM`27%-30%`，若H1/H2兑现可部分消化高估值",
            "过去一月股价`+42.96%`后已提前交易乐观，Forward PE和期权IV缺失降低估值/波动判断可信度",
        ),
        "近端催化优先": (
            "FY2027 H1兑现、H2高于H1、coater>50%、etch>25%、AP>60%、bonding/laser订单和Q2/Q3设备景气均在1-2季验证",
            "催化强度依赖客户PO、cleanroom readiness、安装验收和价格调整，不能只靠AI capex叙事",
        ),
        "价格确认/动量": (
            "2026-06-23过去两周`+18.56%`、过去一月`+42.96%`，价格已经明显确认WFE/AP重估",
            "动量已高，且TOELY无干净期权链覆盖，短线过热和ADR流动性都要保守处理",
        ),
        "激进短线": (
            "强价格动量、WFE高景气、advanced packaging/bonding小基数和AI芯片前道设备叙事提供进攻弹性",
            "OTC ADR无IV覆盖，资金弹性和期权表达弱于高beta美股小盘、光互联、NeoCloud或核能标的",
        ),
    }

    out: list[str] = []
    out += [
        "# TOELY 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：TOELY / Tokyo Electron",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-23；过去两周和过去1个月区间涨跌为 2026-06-23；SOXX 三段压力窗口为 2026-06-23",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 TOELY vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。TOELY 的优势来自 FY2027 H1正式指引、H2高于H1、coater/developer高份额、advanced packaging和bonding/laser小基数右尾，以及6月下旬价格动量确认。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是当前估值已经明显上修，日度源Forward PE和IV缺失，WFE/China/客户验收反证仍在，且SOXX压力窗口并不防守。",
        "- A 最适合的投资者画像：希望配置AI半导体前道设备和先进封装工具链、重视NTM收入利润兑现和近端订单验证，同时能承受设备周期和高估值波动的成长资金。",
        "- A 最不适合的投资者画像：只追求最低估值、低波动防守、强期权流动性，或要求最直接AI收入和最高小盘beta的短线资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在直接AI收入、小基数右尾、估值消化、防守属性或高beta短线弹性上压过 TOELY。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：TOELY 是项目内半导体设备和先进封装受益链的强势核心标的，NTM兑现、右尾弹性、近端催化和价格确认均靠前；但风险调整、估值消化和下行保护不是顶档，更适合作为进攻型设备核心仓，而不是全项目低风险首选。",
        "- 后续最重要跟踪数据：FY2027 H1收入/OPM是否兑现，H2是否明确高于H1，coater/developer>50%、etch>25%、advanced packaging>60%是否逐项实现，bonding-related是否从300亿日元向1,000亿日元跨越，Field Solutions双位数增长，中国WFE份额、SEMI billings、客户HBM4/CoWoS/SoIC/cleanroom/良率信号。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "TOELY"]),
        base.row(["公司名称", "Tokyo Electron"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "31,000-33,000 亿日元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "H2 FY2027 inquiry转firm order、production slot转收入、客户cleanroom/良率/安装验收、etch share修复、中国和成熟节点抵消。"]),
        base.row(["最大反证", "缺少正式backlog/bookings；bonding/hybrid bonding大规模进入NTM仍需POR；估值已上修且日度源Forward PE/IV缺失。"]),
        base.row(["近端催化剂", "FY2027 H1兑现、H2订单和production slots、coater/etch/AP增长、bonding/laser订单、Field Solutions增长、SEMI设备景气。"]),
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
        base.row(["直接同业", "同属半导体前道/WFE设备资金池，优先看份额、订单/指引、产品代际、毛利率、服务收入、同业估值和客户工艺锁定。", "ASML、AMAT、LRCX、KLAC、ASMIY、ACMR、ACLS、VECO", "同业证据权重最高；若产品份额、收入兑现或估值差距大，结论力度可以上调。"]),
        base.row(["相邻替代", "同处AI半导体设备、封装测试、数据中心基础设施或AI资本开支受益篮子，但收入模式不完全相同。", "TER、ATEYY、BESIY、CAMT、VRT、ETN、GEV", "回答资金只能买一个时，谁的增长质量、订单可见度、估值消化和近端催化更好。"]),
        base.row(["上下游", "一方处在TOELY客户、供应商或终端需求链，重点看利润池位置、议价权、瓶颈稀缺性和收入确认链条。", "TSM、MU、INTC、NVDA、AVGO、MSFT、ENTG、MKSI、ICHR", "不把下游AI收入规模直接等同TOELY机会，也不把上游设备稀缺自动等同更好。"]),
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
        need = "需要 TOELY 继续上修FY2027订单覆盖，证明AP/bonding/etch增长转成收入、OPM和FCF，并降低估值透支反证。"
        if comparison["rel"] == "直接同业":
            need = "需要 TOELY 在同业中证明coater/AP/bonding优势能转化为更强收入、GM、service attach和订单持续性。"
        elif comparison["rel"] == "上下游":
            need = "需要 TOELY 证明比该上下游公司更能捕获AI半导体利润池，而不是只承担capex周期beta。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 TOELY 用更强现金流、估值消化或防守表现抵消跨赛道标的的低波动/防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更强NTM收入利润兑现、或更低估值/更好现金流来抵消TOELY的WFE/AP稀缺和近端催化。"
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
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-23.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md`。",
        f"- 日度金融数据覆盖：2026-06-23 金融快照覆盖 189 家；本次公司评估全集为 {n} 家，因此缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot} 备注：TOELY 行内 `Forward PE缺失`、`交易货币/财报货币不一致: USD/JPY`、`ADR/ADS比例需确认`、`call/put无期权链或数据源无覆盖`，因此估值消化、下行保护和激进短线列均降低结论力度。",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/晶圆制造_前道设备/TOELY_Tokyo Electron_公司调研_2026-06-23.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_AI芯片前道制造设备_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_存储前道制造设备_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-06-11.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 外部行情交叉检查：Yahoo Finance TOELY 历史行情页 <https://finance.yahoo.com/quote/TOELY/history/>；Yahoo Finance 8035.T 行情页 <https://finance.yahoo.com/quote/8035.T/>。",
        "- 自动化脚本：`scripts/generate_toely_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对TOELY的FY2027指引、coater/AP/bonding、日度估值缺口和价格动量做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
                "toely_tiers": companies[TARGET]["tiers"],
                "toely_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
