from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "EQIX"
TARGET_NAME = "Equinix"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "EQIX_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL

DIRECT_PEERS = {"DLR", "APLD", "IREN"}
ADJACENT_PEERS = {"CRWV", "NBIS", "NTNX", "PSTG", "HPE", "CRWD", "ADBE"}
HYPERSCALER_CUSTOMERS = {"AMZN", "MSFT", "GOOGL", "META", "ORCL", "BABA", "IBM"}
UPSTREAM_CATS = {
    "AI服务器_存储_EMS",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "电力_发电_能源_储能",
    "机电_冷却_工程_水处理_边缘工业AI",
    "配电_电源_功率器件",
}
DISTANT_CATS = {"半导体材料_化学品_基板", "晶圆制造_前道设备", "封测_检测_计量_光罩"}


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

    # Manual calibration from the EQIX formal evaluation:
    # mature data-center and interconnection platform, high recurring revenue,
    # strong EBITDA/AFFO visibility and low IV, but lower growth/right-tail than
    # NeoCloud, AI chips, power bottleneck suppliers, and high-beta AI hardware.
    a = companies[TARGET]
    overrides = {
        "NTM兑现优先": 73.0,
        "右尾弹性优先": 58.0,
        "风险调整收益": 57.5,
        "下行保护优先": 88.0,
        "估值消化优先": 56.0,
        "近端催化优先": 63.0,
        "价格确认/动量": 43.0,
        "激进短线": 58.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in HYPERSCALER_CUSTOMERS:
        return "上下游"
    if ticker in ADJACENT_PEERS or category == "云算力_IDC_AI软件平台":
        return "相邻替代"
    if category in UPSTREAM_CATS:
        return "上下游"
    if category in DISTANT_CATS:
        return "跨赛道"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A收入/AFFO和bookings更稳",
            "右尾弹性优先": "A的xScale/atNorth期权更稳",
            "风险调整收益": "A低IV和现金流更均衡",
            "下行保护优先": "A低IV且压力期更稳",
            "估值消化优先": "A的EBITDA/AFFO更可见",
            "近端催化优先": "A有Q2指引和容量节点",
            "价格确认/动量": "A价格稳定未明显破位",
            "激进短线": "A事件确定性略高",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/利润兑现更强",
            "右尾弹性优先": "B右尾收入弹性更大",
            "风险调整收益": "B上行/估值组合更好",
            "下行保护优先": "B现金流或防守性更强",
            "估值消化优先": "B估值消化难度更低",
            "近端催化优先": "B近端订单/产品节点更硬",
            "价格确认/动量": "B价格确认更强",
            "激进短线": "B高弹性叙事更适合进攻",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "成长、估值和防守互抵"
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
        + a["scores"]["下行保护优先"]
        + a["scores"]["估值消化优先"]
        - b["scores"]["NTM兑现优先"]
        - b["scores"]["风险调整收益"]
        - b["scores"]["下行保护优先"]
        - b["scores"]["估值消化优先"]
    )
    return "A" if key_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
            return "EQIX 的低IV、压力期韧性、互联粘性和AFFO底盘更适合防守配置。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "EQIX 的收入指引、MRR/bookings、EBITDA和AFFO兑现路径更清楚。"
        if a["scores"]["风险调整收益"] - b["scores"]["风险调整收益"] > 10:  # type: ignore[index,operator]
            return "EQIX 的上行不极端，但现金流、客户粘性和低波动让风险调整收益更均衡。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 8:  # type: ignore[index,operator]
            return "EQIX 的EBITDA/AFFO可见度更好，估值消化比B更可验证。"
        return "EQIX 在稳定兑现、防守质量和风险控制组合上略胜。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的高增长右尾和市值弹性明显强于 EQIX。"
    if b["scores"]["激进短线"] - a["scores"]["激进短线"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的高IV、短线叙事和事件弹性更适合进攻。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和资金偏好强于 EQIX。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化难度低于 EQIX，或增长足以覆盖当前倍数。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
        return f"{b['ticker']} 的收入/订单/利润兑现证据强于 EQIX。"
    return f"{b['ticker']} 在综合关键权重下略优于 EQIX，尤其能抵消EQIX的稳健兑现和防守优势。"


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
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["下行保护优先"] - x["b"]["scores"]["下行保护优先"]),  # type: ignore[index,operator]
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
        f"2026-06-22 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，P/S {fmt_num(fin.get('ps'))}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )
    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "2026Q1收入`24.44亿美元`、FY2026收入指引`101.44-102.44亿美元`、Q2收入指引`25.71-26.11亿美元`、MRR和bookings支撑",
            "增长主要是低双位数，新增容量还要经过上电、液冷/MEP、客户设备到货和验收",
        ),
        "右尾弹性优先": (
            "xScale美国JV最终`>1.5GW`、既有xScale full-buildout `>725MW`、atNorth `800MW`五年管线和AI Factory合作提供长期AI容量期权",
            "NTM收入基数大，xScale/atNorth多为权益或长期容量，不能直接并入近端并表收入",
        ),
        "风险调整收益": (
            "互联网络效应、经常性收入、EBITDA/AFFO可见度、低IV和压力窗口韧性让赔率较均衡",
            "2026-06-22 Forward PE`58.05`、P/S`11.55`且增长capex约`41亿美元`，估值和FCF after growth capex仍有压力",
        ),
        "下行保护优先": (
            "Call IV`30.5%`、三段SOXX压力窗口累计`-26.55%`、interconnection粘性和AFFO底盘强于多数AI高beta标的",
            "高估值、REIT利率敏感性、项目capex和电力交付延期仍限制其成为绝对防守资产",
        ),
        "估值消化优先": (
            "基准NTM收入`103.5-106.0亿美元`、调整后EBITDA`52.7-54.5亿美元`、AFFO`42.8-44.6亿美元`，业绩口径清楚",
            "当前P/S和Forward PE已经不低，收入增速低于NeoCloud/芯片/电力瓶颈公司，消化速度中等",
        ),
        "近端催化优先": (
            "Q2/Q3收入、MRR、gross bookings、presales/backlog、xScale lease closing、atNorth close和AI Factory客户案例都可跟踪",
            "多数催化是稳态验证而非爆发式订单；若上电或客户验收延迟，催化会后移",
        ),
        "价格确认/动量": (
            "2026-06-03两周`+1.12%`、一月`-0.74%`，2026-06-22价格高于6月初，趋势未明显破位",
            "动量显著弱于高beta AI云、光互联、电力设备和部分芯片股，资金进攻偏好不强",
        ),
        "激进短线": (
            "低IV和AI容量新闻可提供事件驱动，但主要适合作为稳健AI基础设施仓位",
            "低波动、成熟市值和低双位数增长使其短线爆发力弱于NeoCloud、光互联、AI芯片和电力小盘",
        ),
    }

    out: list[str] = []
    out += [
        "# EQIX 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：EQIX / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 EQIX vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。EQIX 的优势集中在经常性colocation/interconnection收入、EBITDA/AFFO可见度、低IV、SOXX压力窗口韧性、AI高密度容量和xScale/atNorth长期容量期权。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是低双位数增长、市值和收入基数大、Forward PE和P/S不低、增长capex前置，以及短线爆发力弱于NeoCloud、光互联、AI芯片和电力瓶颈标的。",
        "- A 最适合的投资者画像：想配置AI数据中心长期需求，但更重视收入/AFFO可见度、客户粘性、低波动和压力期韧性的中低beta资金。",
        "- A 最不适合的投资者画像：只追求极端收入上修、最高右尾、市值弹性、短线高IV或价格爆发力的进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在右尾弹性、近端催化、价格确认、估值消化或高增长收入兑现上压过EQIX。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：EQIX 是项目内“高质量、低波动、AI数据中心核心资产”而不是增长冠军；它在下行保护和稳健兑现中靠前，在右尾、动量和激进短线中靠后。",
        "- 后续最重要跟踪数据：Q2/Q3收入、MRR、gross bookings、annualized presales/backlog、colocation与interconnection增速、xScale lease closing、atNorth close/权益口径、AI Factory客户案例、Fabric capacity/net interconnections、growth capex、cash gross margin、调整后EBITDA率、AFFO、经营现金流和power/液冷/commissioning进度。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "EQIX"]),
        base.row(["公司名称", "Equinix, Inc."]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`103.5-106.0亿美元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}，但极度乐观在正式评估中下移为乐观上限/附录跟踪"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "`签约/预售 -> 上电 -> 液冷/MEP调试 -> 客户IT设备到货 -> 验收 -> MRR`，需求存在但NTM收入确认取决于物理交付。"]),
        base.row(["最大反证", "高密度/AI子集收入未披露，xScale/atNorth多为长期或权益口径，增长capex约`41亿美元`压制after-growth-capex FCF，当前估值不低。"]),
        base.row(["近端催化剂", "Q2/Q3收入与MRR、gross bookings、annualized presales、xScale lease closing、atNorth close、AI Factory客户案例、Fabric/net interconnections和AFFO/EBITDA率。"]),
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
        base.row(["直接同业", "同属数据中心、IDC、AI Factory或高密度容量运营商，优先比较上电容量、客户长约、RPO/backlog、AFFO/NOI、融资成本、利用率、收入确认和同业估值。", "DLR、APLD、IREN", "同业证据权重最高；若对方增长高但FCF/IV/压力期差，EQIX在风险调整和下行保护中可明显胜出。"]),
        base.row(["相邻替代", "同属云算力、NeoCloud、IDC、企业AI软件/平台或数据基础设施资金篮子，但收入模式不完全重叠。", "CRWV、NBIS、NTNX、PSTG、HPE、CRWD、ADBE", "重点回答资金只能买一个时，谁的增长质量、估值消化、风险调整和近端催化更好。"]),
        base.row(["上下游", "B 是 EQIX 的云客户、AI需求端、服务器/GPU/网络/电力/配电/冷却/MEP供应链或同一AI数据中心利润池中的上下游。", "AMZN、MSFT、GOOGL、META、ORCL、NVDA、ANET、VRT、ETN、CEG", "区分收入规模、利润捕获和议价权；不把云商capex或芯片收入机械等同为EQIX机会。"]),
        base.row(["跨赛道", "半导体材料、前道设备、封测、化学品、工业或其他与EQIX业务差异较大的公司，只作为资金配置替代。", "ASML、AMAT、LIN、TMO、RKLB、TSLA", "默认降低结论力度；除非增长质量、估值消化或防守性明显拉开，否则使用中性或微倾向。"]),
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
        need = "需要 EQIX 把高密度AI容量、xScale/atNorth和Fabric/AI Hub转成更高NTM收入增速、AFFO上修和价格确认。"
        if comparison["rel"] == "直接同业":
            need = "需要 EQIX 在同业中证明MRR/bookings、上电容量、AFFO/NOI、融资成本和压力期表现同时领先。"
        elif comparison["rel"] == "上下游":
            need = "需要 EQIX 证明其数据中心平台能捕获比上游芯片/网络/电力/冷却端更好的利润池和增长弹性。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 EQIX 用更高AFFO增长、估值消化或防守优势抵消跨赛道标的的增长和催化差距。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提高NTM订单/收入兑现、现金流质量、压力期韧性或估值消化证据。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要 B 把右尾叙事转成可确认收入、利润和现金流，并降低IV、估值或交付反证。"
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
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/云算力_IDC_AI软件平台/EQIX_Equinix_公司调研_2026-06-20.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI云算力外包和NeoCloud与AI数据中心运营商_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心土建、MEP与预制化交付_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_DCIM、能控与AI工厂数字孪生_2026-06-10.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AI Fabric网络操作系统与遥测软件_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_eqix_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+10%-12%` 做同号区间修正；对 EQIX 的收入/AFFO可见度、低IV、SOXX压力窗口、AI容量长期期权、增长capex、估值和低短线爆发力做人工校准后建档；未读取下游量化目录、备份、临时目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit(f"缺少目标公司正式评估：{TARGET}")
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
                "eqix_tiers": companies[TARGET]["tiers"],
                "eqix_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
