from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "VECO"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "VECO_逐家公司投资思路对比_2026-06-23.md"

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
    "TOELY",
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
FOUNDRY_MEMORY_OSAT_CUSTOMERS = {
    "AMKR",
    "ASX",
    "GFS",
    "IMOS",
    "INTC",
    "MU",
    "SNDK",
    "STX",
    "TSEM",
    "TSM",
    "UMC",
    "WDC",
}
OPTICAL_DOWNSTREAM = {
    "AAOI",
    "ANET",
    "COHR",
    "CRDO",
    "FN",
    "LITE",
    "LWLG",
    "MTSI",
    "POET",
    "SMTC",
    "VIAV",
}
AI_DEMAND_CHAIN = {
    "ALAB",
    "AMD",
    "AMZN",
    "APLD",
    "ARM",
    "AVGO",
    "BABA",
    "CDNS",
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

    # VECO calibration: the 250M+ InP laser equipment order is hard near-term
    # evidence relative to company size, while valuation, gross-margin repair,
    # inventory/revenue-recognition timing and the pending Axcelis deal cap
    # risk-adjusted and downside scores.
    a = companies[TARGET]
    overrides = {
        "NTM兑现优先": 78.0,
        "右尾弹性优先": 95.0,
        "风险调整收益": 58.0,
        "下行保护优先": 64.0,
        "估值消化优先": 62.0,
        "近端催化优先": 84.0,
        "价格确认/动量": 82.0,
        "激进短线": 96.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_WFE_PEERS:
        return "直接同业"
    if ticker in EQUIPMENT_SUPPLY_CHAIN or ticker in FOUNDRY_MEMORY_OSAT_CUSTOMERS or ticker in OPTICAL_DOWNSTREAM or ticker in AI_DEMAND_CHAIN:
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
            "NTM兑现优先": "A的InP订单和FY2026指引更清楚",
            "右尾弹性优先": "A小基数叠加InP/NSA右尾更大",
            "风险调整收益": "A订单上行可抵消部分估值压力",
            "下行保护优先": "A净现金和SOXX压力表现较好",
            "估值消化优先": "A若订单兑现可消化部分估值",
            "近端催化优先": "A有InP/NSA/LUMINA+连续验证",
            "价格确认/动量": "A两周和一月动量更强",
            "激进短线": "A高IV叠加订单右尾更适合进攻",
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
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
            return "VECO 的InP订单、NSA follow-on和LUMINA+资格认证给1-2季验证点更集中。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
            return "VECO 小基数下2.5亿美元以上InP订单对收入和利润弹性更大。"
        if a["scores"]["价格确认/动量"] - b["scores"]["价格确认/动量"] > 10:  # type: ignore[index,operator]
            return "VECO 近期价格确认更强，且订单证据仍有后续收入验证窗口。"
        return "VECO 的InP/NSA订单弹性和近端验证更好，B 的优势不足以覆盖反证。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值、现金流和下行组合明显好于 VECO。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的低波动、低估值或现金流防守属性更强。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的当前估值更容易被NTM业绩消化。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/RPO/订单兑现证据更硬。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI收入或小基数右尾强于 VECO。"
    return f"{b['ticker']} 在多数投资思路下比 VECO 更符合项目内资金配置目标。"


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
        key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["风险调整收益"] - a["scores"]["风险调整收益"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["近端催化优先"] - x["b"]["scores"]["近端催化优先"]),  # type: ignore[index,operator]
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
        f"P/S {fmt_num(fin.get('ps'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:6]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "FY2026收入指引`7.40-8.00亿美元`、Q2指引`1.70-1.90亿美元`，InP订单从2026开始交付、2027加速",
            "Q1收入同比`-5.4%`、non-GAAP GM仅`36.2%`，订单仍需发货、安装和验收",
        ),
        "右尾弹性优先": (
            "`2.5亿美元+`多客户InP订单相当于FY2026收入指引中点`32%+`，小市值下收入弹性大",
            "NSA500多客户HVM和InP追加订单仍需验证，极度乐观对客户排产和毛利mix要求高",
        ),
        "风险调整收益": (
            "净现金、流动比率高，且InP/NSA/AP/IBD多线给上行空间",
            "2026-06-23 TTM PE `195.92`、P/S `6.93`、Call IV `90.8%`，估值和波动已较高",
        ),
        "下行保护优先": (
            "三段SOXX压力窗口累计`-25.98%`优于多数半导体beta股，资产负债表仍有净现金",
            "库存`2.822亿美元`、DIO`245天`和验收延迟会放大毛利和现金流波动",
        ),
        "估值消化优先": (
            "若NTM收入`7.80-8.60亿美元`、non-GAAP OI`1.05-1.35亿美元`兑现，Forward PE可被部分消化",
            "当前价格已提前交易InP订单和2027上台阶，Q2/Q3或毛利修复低于预期会压缩估值",
        ),
        "近端催化优先": (
            "InP订单进入RPO/收入、NSA500 follow-on、第三客户评估、LUMINA+验收和Q2/Q3指引均在1-2季内验证",
            "催化不是新闻标题本身，必须看到Compound Semi/Semiconductor收入、合同负债和毛利率同步上台阶",
        ),
        "价格确认/动量": (
            "2026-06-23过去两周`+11.25%`、过去一月`+25.52%`，价格已确认订单重估",
            "高IV和较高估值说明预期不低，若订单收入化慢，动量可能反转",
        ),
        "激进短线": (
            "Call IV `90.8%`、小市值、InP/1.6T光互联和NSA500叙事集中，适合进攻型交易",
            "同池还有更直接AI收入或更高beta小盘，VECO短线并非无风险右尾",
        ),
    }

    out: list[str] = []
    out += [
        "# VECO 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：VECO / Veeco Instruments",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-23；过去两周和过去1个月区间涨跌为 2026-06-23；SOXX 三段压力窗口为 2026-06-23",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 VECO vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。VECO 的优势集中在 InP 激光设备订单、NSA500 follow-on、LUMINA+ 商业验收、1.6T/硅光/先进逻辑叙事和近期价格确认。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 TTM PE `195.92`、P/S `6.93`、EV/EBITDA `94.15`、Call IV `90.8%`，且Q1毛利率、库存、验收节奏和Axcelis交易仍是反证。",
        "- A 最适合的投资者画像：愿意押注小型半导体设备商从InP光互联订单和先进逻辑退火中放大收入、能承受高IV和估值波动的进攻型成长资金。",
        "- A 最不适合的投资者画像：只追求低估值、低波动、公用事业式下行保护、或要求已经稳定释放FCF的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在直接AI收入、现金流质量、估值消化、防守属性或更强价格趋势上压过 VECO。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：VECO 是项目内小盘设备链里右尾和近端催化最突出的标的之一，但它不是低风险核心仓；在全项目中更像“订单驱动的高弹性进攻仓”，而不是“估值安全垫很厚的稳健配置”。",
        "- 后续最重要跟踪数据：Q2/Q3收入和指引、Compound Semi收入是否从约2,000万美元/季上台阶、合同负债/RPO、InP订单新增和交付节奏、NSA500第三客户评估、LUMINA+多客户导入、non-GAAP GM能否回到41%-43%、库存/DIO/应收/FCF、Axcelis/SAMR进度、1.6T光模块和InP laser行业库存/ASP。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "VECO"]),
        base.row(["公司名称", "Veeco Instruments"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "7.80-8.60 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "订单到收入确认的时间差：工具发货、安装、客户验收、海关/出口管制、客户fab readiness和InP激光厂扩产节奏。"]),
        base.row(["最大反证", "产品收入拆分不足；NSA500仍early adoption；InP订单未披露具体季度排产、客户名、ASP和book-to-bill；库存和应收占用高；Axcelis并表不进入独立NTM基准。"]),
        base.row(["近端催化剂", "Q2/Q3收入、合同负债/RPO、Compound Semi收入、InP订单追加或交付、NSA500第三客户评估、LUMINA+多客户资格、non-GAAP GM修复、Axcelis/SAMR。"]),
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
        base.row(["直接同业", "同属前道/WFE/专用制程设备资金池，优先看订单/RPO、产品代际、客户POR、毛利率、收入兑现和同业估值。", "AMAT、LRCX、TOELY、ASML、KLAC、ASMIY、ACMR、ACLS", "同业证据权重最高；若B拥有更硬规模、订单或利润质量，VECO的右尾也要被估值和执行反证校准。"]),
        base.row(["相邻替代", "同属AI半导体设备、封装测试、数据中心基础设施或高beta AI受益篮子，但收入模式不同。", "TER、ATEYY、BESIY、CAMT、VRT、ETN、GEV", "比较资金只能买一个时的增长质量、估值消化、近端催化和波动容忍度。"]),
        base.row(["上下游", "B处在VECO的客户、供应商或终端需求链，重点看利润池位置、议价权、瓶颈稀缺性和订单向收入确认的距离。", "COHR、LITE、AAOI、TSM、MU、NVDA、AVGO、ENTG、MKSI", "不把下游AI收入规模直接等同VECO收入，也不把VECO上游瓶颈自动等同更好。"]),
        base.row(["跨赛道", "业务差异大但作为项目内资金替代仍比较风险调整收益、估值消化、下行保护和催化可见度。", "LIN、TMO、DHR、CAT、MSI、RYCEY", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要 VECO 证明InP订单进入收入/RPO、毛利率回到41%-43%、库存周转改善，并用Q2/Q3连续兑现降低高估值和高IV反证。"
        if comparison["rel"] == "直接同业":
            need = "需要 VECO 在同业中证明InP/NSA订单的收入增速和利润质量足以弥补规模、backlog披露和现金流劣势。"
        elif comparison["rel"] == "上下游":
            need = "需要 VECO 证明自己比该上下游公司更能捕获AI光互联/先进逻辑利润池，而不是只承担设备交付和验收风险。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 VECO 用更强收入兑现、FCF和估值消化抵消跨赛道公司的低波动或防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更强NTM收入利润兑现、更低估值或更好价格确认，才能抵消VECO的InP/NSA订单右尾。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "需要 B 把防守优势外再提供增长催化，否则很难压过VECO的近端订单弹性。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-23.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md`。",
        f"- 日度金融数据覆盖：2026-06-23 金融快照解析 189 家；本次公司评估全集为 {n} 家，缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他项目内来源：`公司调研/公司索引.md`、`公司调研/晶圆制造_前道设备/VECO_Veeco Instruments_公司调研_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_激光器、EML与光器件_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_AI芯片前道制造设备_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装湿化学与表面处理材料_2026-06-11.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 外部官方核验：Veeco 2026Q1 results release（https://ir.veeco.com/news-and-events/news-details/2026/Veeco-Reports-First-Quarter-2026-Financial-Results/default.aspx）；Veeco 2.5亿美元以上InP laser equipment orders（https://ir.veeco.com/news-and-events/news-details/2026/Veeco-Announces-250-Million-in-Equipment-Orders-for-Manufacturing-Indium-Phosphide-Lasers/default.aspx）；Veeco NSA500 follow-on order（https://ir.veeco.com/news-and-events/news-details/2026/Veeco-Receives-Follow-On-Order-for-Nanosecond-Annealing-System-Expands-Evaluation-Activity/default.aspx）；Veeco LUMINA+ Ennostar qualification（https://ir.veeco.com/news-and-events/news-details/2026/Ennostar-Qualifies-Veecos-New-LUMINA-MOCVD-System-for-Advanced-Product-Applications/default.aspx）。",
        "- 自动化脚本：`scripts/generate_veco_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+17%-30%` 做同号区间修正后建档；未读取下游量化目录或现成排序结论。",
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
                "veco_tiers": companies[TARGET]["tiers"],
                "veco_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
