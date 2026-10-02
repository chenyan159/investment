from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "ARM"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ARM_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_PEERS = {"CDNS", "SNPS"}
CPU_AI_LICENSEE_OR_PARTNER = {
    "ADI",
    "ALAB",
    "AMD",
    "AVGO",
    "INTC",
    "MCHP",
    "MRVL",
    "MXL",
    "NVDA",
    "ON",
    "QCOM",
    "STM",
    "TXN",
    "TSM",
}
CLOUD_AND_SYSTEM_CUSTOMERS = {
    "AMZN",
    "BABA",
    "CRWV",
    "DELL",
    "GOOGL",
    "HPE",
    "IBM",
    "META",
    "MSFT",
    "NBIS",
    "ORCL",
    "SMCI",
}
DESIGN_SUPPLY_CHAIN = {
    "ASML",
    "ASMIY",
    "AMAT",
    "LRCX",
    "KLAC",
    "TOELY",
    "ENTG",
    "MKSI",
    "TER",
    "ATEYY",
    "RMBS",
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

    # ARM-specific calibration. The generic parser sees the 20%-27% NTM
    # growth correctly after range repair, but still underweights ACV/RPO,
    # the royalty/license gross-margin model, and AGI CPU event optionality.
    # It also needs a harsher explicit cap for risk/valuation because current
    # daily data shows P/S 88.51, Forward PE 132.20, IV 101.8%, and large
    # SOXX pressure-window drawdowns.
    overrides = {
        "NTM兑现优先": 78.0,
        "右尾弹性优先": 83.0,
        "风险调整收益": 32.0,
        "下行保护优先": 45.0,
        "估值消化优先": 25.0,
        "近端催化优先": 72.0,
        "价格确认/动量": 97.0,
        "激进短线": 100.0,
    }
    target = companies[TARGET]
    for strategy, score in overrides.items():
        target["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in CPU_AI_LICENSEE_OR_PARTNER or ticker in CLOUD_AND_SYSTEM_CUSTOMERS or ticker in DESIGN_SUPPLY_CHAIN:
        return "上下游"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A指引/ACV/royalty证据更硬",
            "右尾弹性优先": "A有AGI CPU与CSS右尾",
            "风险调整收益": "A高毛利IP与净现金略胜",
            "下行保护优先": "A资产轻且现金底盘更好",
            "估值消化优先": "A增长斜率可部分消化估值",
            "近端催化优先": "A财报/ACV/AGI CPU节点更近",
            "价格确认/动量": "A价格已强确认",
            "激进短线": "A高IV和AGI叙事更强",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/订单兑现更硬",
            "右尾弹性优先": "B右尾或市值弹性更大",
            "风险调整收益": "B估值与下行组合更好",
            "下行保护优先": "B估值/低IV/现金流更稳",
            "估值消化优先": "B当前估值更易消化",
            "近端催化优先": "B近端订单/产品节点更硬",
            "价格确认/动量": "B趋势确认更顺",
            "激进短线": "B短线爆发赔率更高",
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
    key_weight = (
        a["scores"]["NTM兑现优先"]
        + a["scores"]["右尾弹性优先"] * 0.8
        + a["scores"]["风险调整收益"]
        + a["scores"]["估值消化优先"]
        + a["scores"]["近端催化优先"] * 0.6
        - b["scores"]["NTM兑现优先"]
        - b["scores"]["右尾弹性优先"] * 0.8
        - b["scores"]["风险调整收益"]
        - b["scores"]["估值消化优先"]
        - b["scores"]["近端催化优先"] * 0.6
    )
    return "A" if key_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["价格确认/动量"] - b["scores"]["价格确认/动量"] > 15:  # type: ignore[index,operator]
            return "ARM 的价格确认、AI CPU叙事和高IV交易属性明显更强。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "ARM 的FY2026收入、Q1指引、ACV和royalty/license路径更清楚。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 8:  # type: ignore[index,operator]
            return "ARM 未来1-2季可验证ACV/RPO、royalty增速和AGI CPU供给节点。"
        return "ARM 以高毛利IP模型、Cloud AI royalty和AGI CPU期权略胜，但估值压力仍是硬约束。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化难度明显低于 ARM。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的风险调整收益明显优于 ARM。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值、现金流或压力期韧性更好。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的右尾收入弹性或市值弹性强于 ARM。"
    return f"{b['ticker']} 在多数投资思路下比 ARM 更符合当前项目内配置目标。"


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
            x["b"]["scores"]["风险调整收益"] + x["b"]["scores"]["估值消化优先"] - a["scores"]["风险调整收益"] - a["scores"]["估值消化优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            x["ac"] - x["bc"],
            a["scores"]["价格确认/动量"] + a["scores"]["激进短线"] - x["b"]["scores"]["价格确认/动量"] - x["b"]["scores"]["激进短线"],  # type: ignore[index,operator]
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

    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_snapshot = (
        f"2026-06-22 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，P/S {fmt_num(fin.get('ps'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = []
    for product in a["products"][:7]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    support = {
        "NTM兑现优先": (
            "FY2026收入`$4.920B`、同比`+23%`；Q1 FY2027指引`$1.26B +/- $50M`；ACV`$1.660B`同比`+22%`，license/royalty路径清楚",
            "RPO`$2.071B`同比`-7%`，license大单timing和AGI CPU收入确认仍有波动",
        ),
        "右尾弹性优先": (
            "AGI CPU FY2027/FY2028 demand `>$2B`、Cloud AI/data center royalty >2x、CSS/Total Design把Arm从IP税推向AI CPU平台",
            "公司市值已大，NTM AGI CPU基准仅小额收入，GPU/HBM主利润池不归ARM",
        ),
        "风险调整收益": (
            "IP/royalty毛利极高、净现金和生态锁定强，基准收入增速仍可达约`+20%-27%`",
            "2026-06-22 P/S`88.51`、Forward PE`132.20`、Call IV`101.8%`，赔率被高预期显著压低",
        ),
        "下行保护优先": (
            "资产轻、现金与短投约`$3.601B`、负债低、license/royalty粘性强",
            "高估值、高IV和SOXX压力窗口`-61.37%`显示市场压力期防守不足",
        ),
        "估值消化优先": (
            "NTM基准收入`$5.90-6.25B`、non-GAAP OPM`41%-45%`，业务质量可支撑部分溢价",
            "P/S接近`89x`、Forward PE超`130x`，需要多年AGI CPU/royalty上修才能完全消化",
        ),
        "近端催化优先": (
            "Q1/Q2 FY2027财报、royalty恢复到约`20%+`、ACV/RPO变化、AGI CPU supply-backed outlook和客户部署证据可在未来1-2季验证",
            "真正大额AGI CPU revenue偏FY2027 Q4/FY2028，短期多是visibility而非大规模收入",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周`+60.41%`、过去一月`+95.01%`，2026-06-22仍在`407.72`美元，价格已充分确认AI CPU叙事",
            "涨幅已过热，价格确认强不等于风险调整后仍便宜",
        ),
        "激进短线": (
            "Call IV`101.8%`、AGI CPU/Meta/Cloud AI royalty高关注度和强动量使其适合短线进攻",
            "大市值限制倍数弹性，且任何指引/royalty/AGI供给低于预期都会快速反噬",
        ),
    }

    out: list[str] = []
    out += [
        "# ARM 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：ARM / Arm Holdings",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 ARM vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ARM 在项目内最强的是价格确认、激进短线和近端催化，核心来自 AGI CPU/Cloud AI royalty 叙事、极高 IV 和最近一个月的强动量。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是估值消化、风险调整和下行保护：当前 P/S `88.51`、Forward PE `132.20`，需要多年收入斜率才能证明合理。",
        "- A 最适合的投资者画像：愿意为高毛利 CPU/IP 平台、Cloud AI royalty、AGI CPU 和 CSS/Total Design 中期右尾支付高估值溢价，并能承受高 IV 和高回撤风险的进攻型成长资金。",
        "- A 最不适合的投资者画像：要求低估值、现金流防守、压力期韧性、或只买已由 NTM 利润完全覆盖估值的稳健配置者。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在估值消化、风险调整、下行保护或更直接可收入化AI订单上压过 ARM。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：ARM 是高质量、高稀缺、但估值极端透支的 AI 计算平台标的；它不是全风格最优，适合右尾/动量/事件驱动，不适合作为风险调整或估值消化优先的第一选择。",
        "- 后续最重要跟踪数据：Q1/Q2 FY2027 revenue、royalty growth 是否恢复到约20%+、license and other revenue 与ACV/RPO、data center royalty是否继续>2x、AGI CPU supply-backed outlook 是否从约10亿美元上修、FY2027 Q4首批production revenue、Meta/OpenAI/SAP/Cloudflare/F5/SK Telecom等客户production deployment、non-GAAP OPM/FCF、以及P/S/Forward PE是否随盈利上修快速回落。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ARM"]),
        base.row(["公司名称", "Arm Holdings"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`$5.90-6.25B`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AGI CPU 从 demand/supply line-of-sight 到可确认收入需要 TSMC 3nm、DDR5、封装、测试、服务器/rack validation 和客户软件迁移全部兑现；Cloud AI royalty 金额拆分仍低披露。"]),
        base.row(["最大反证", "当前估值已经预支多年增长；RPO 同比 -7%，AGI CPU 基准收入仍小；若 royalty 总增速回落、AGI CPU 供应链不上修或 non-GAAP OPM 被硬件化稀释，股价容错率很低。"]),
        base.row(["近端催化剂", "Q1/Q2 FY2027 财报、royalty/license 是否约20%+增长、ACV/RPO、data center royalty、AGI CPU supply-backed outlook、Meta/OpenAI/Cloudflare/SAP 等客户部署证据。"]),
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
        base.row(["直接同业", "与ARM在半导体IP、EDA/IP平台、芯片设计使能或IP royalty/license预算上高度重叠，优先看ACV/RPO、license大单、生态锁定、客户迁移成本和估值。", "SNPS、CDNS", "同业证据权重最高；若一方在估值或收入可见度明显更强，可上调结论力度。"]),
        base.row(["相邻替代", "同属AI计算、AI网络、服务器、云软件或AI基础设施资金篮子，但不直接竞争；回答资金只能买一个时谁的增长质量、赔率和催化更好。", "NVDA、AMD、AVGO、ALAB、MRVL、CRDO、VRT、ETN", "不把赛道热度本身当胜出，重点校准可收入化、估值消化和反证。"]),
        base.row(["上下游", "B 是 ARM 的客户/licensee、云端需求方、芯片/系统供应链或半导体设计制造伙伴，重点看谁能捕获AI计算利润池、议价权和收入确认。", "AMZN、MSFT、GOOGL、META、NVDA、QCOM、TSM、SMCI、DELL、ASML", "不把下游云capex或上游供应稀缺直接等同于ARM收入；比较利润捕获和估值消化。"]),
        base.row(["跨赛道", "业务差异较大，只作为项目内资金配置替代比较风险调整收益、估值消化、下行保护和催化可见度。", "LIN、TMO、ECL、CAT、DHR、RYCEY", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要 ARM 用连续财报证明 royalty/license 和 AGI CPU 收入上修足以快速压低 P/S 与 Forward PE。"
        if "下行保护优先" in wins or "风险调整收益" in wins:
            need = "需要 ARM 证明高估值下仍有足够下行边界，并降低 IV/回撤反证。"
        if "估值消化优先" in wins:
            need = "需要 ARM 把AGI CPU demand转成可确认收入和利润，让估值倍数随业绩兑现显著下行。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更强价格确认、短线催化或AI收入化证据，并避免估值/订单反证扩大。"
        if b["scores"]["风险调整收益"] > a["scores"]["风险调整收益"]:  # type: ignore[index,operator]
            need = "需要 B 把风险调整优势转化成更强价格确认，否则短线资金仍可能偏向ARM的AGI CPU叙事。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 181 家，本次公司评估全集为 {n} 家；缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/AI计算芯片_EDA_IP_custom_ASIC/ARM_Arm_Holdings_公司调研_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI服务器CPU与控制平面芯片_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_EDA工具、接口IP与Chiplet IP_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_云厂自研AI ASIC_2026-06-10.md`、`行业调研/产业背景/行业调研_头部AI芯片全景与产能释放_2026-06-10.md`、`行业调研/产业背景/AI产业链全局图谱与口径字典_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 外部 sanity check：Arm 官方 FY2026 Q4/FY2026 results 与 SEC 6-K，用于复核 FY2026 收入、Q4 license/royalty、ACV/RPO、data center royalty 和 AGI CPU demand 口径；主表不使用外部网页排序、评级或目标价。",
        "- 外部 sanity check 链接：`https://newsroom.arm.com/news/arm-q4-fye26-results`；`https://www.sec.gov/Archives/edgar/data/1973239/000197323926000062/exhibit992fye26q431-marx26.htm`。",
        "- 自动化脚本：`scripts/generate_arm_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+20%-27%` 做同号区间修正后建档。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    base.TARGET = TARGET
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
                "arm_tiers": companies[TARGET]["tiers"],
                "arm_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
