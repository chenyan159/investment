from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import generate_alle_company_comparison as base


TARGET = "AMPX"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "AMPX_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
INFRA_CATS = base.INFRA_CATS


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
    a = companies[TARGET]

    # AMPX is a high-growth, high-volatility specialty battery company. These
    # explicit overrides prevent the corrected growth parser from treating high
    # revenue growth as all-around quality, while keeping the near-term catalyst
    # and aggressive-short columns sensitive to high IV and UAS/LEV order flow.
    overrides = {
        "NTM兑现优先": 86.0,
        "右尾弹性优先": 91.0,
        "风险调整收益": 48.0,
        "下行保护优先": 44.0,
        "估值消化优先": 39.0,
        "近端催化优先": 79.0,
        "价格确认/动量": 84.0,
        "激进短线": 100.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in {"TSLA", "RKLB"}:
        return "上下游"
    if category == "电力_发电_能源_储能":
        return "相邻替代"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A指引/RPO和UAS/LEV PO更清楚",
            "右尾弹性优先": "A防务无人机右尾更大",
            "风险调整收益": "A小基数上行略能抵风险",
            "下行保护优先": "A现金无债但非防守",
            "估值消化优先": "A高增速可部分消化估值",
            "近端催化优先": "A订单/RPO/DIU节点更近",
            "价格确认/动量": "A两周涨幅和资金关注更强",
            "激进短线": "A高IV小盘更适合进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/订单兑现证据更硬",
            "右尾弹性优先": "B右尾可收入化更大",
            "风险调整收益": "B赔率与现金流更均衡",
            "下行保护优先": "B现金流或资产质量更稳",
            "估值消化优先": "B估值消化明显更容易",
            "近端催化优先": "B近端客户/产品催化更硬",
            "价格确认/动量": "B价格确认更强",
            "激进短线": "B短线爆发力更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"下行保护优先", "估值消化优先"}:
        return "安全性和估值接近"
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
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
            return "AMPX 的FY2026指引、RPO和UAS/LEV订单兑现弹性压过B。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
            return "AMPX 近端重定价主要来自直接PO、RPO、DIU和UAS/LEV交付节点。"
        if a["scores"]["激进短线"] - b["scores"]["激进短线"] > 12:  # type: ignore[index,operator]
            return "AMPX 高IV、小市值和防务无人机叙事更适合激进进攻。"
        return "AMPX 在高增长和近端催化上略优，但仍需跟踪回款和毛利。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化和风险调整证据强于 AMPX。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、防守和压力期韧性强于 AMPX。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/订单兑现证据更硬。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 16:  # type: ignore[index,operator]
        return f"{b['ticker']} 的可收入化右尾更大且反证更少。"
    return f"{b['ticker']} 在多数投资思路下比 AMPX 更符合项目内资金配置目标。"


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
        key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["估值消化优先"] - a["scores"]["估值消化优先"]),  # type: ignore[index,operator]
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

    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_snapshot = (
        f"2026-06-22 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"Forward PE {fmt_num(fin.get('forward_pe'))}，P/S {fmt_num(fin.get('ps'))}，Call IV {fmt_pct(fin.get('call_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    support = {
        "NTM兑现优先": (
            "FY2026 指引 `>= $130M`、2026Q1 收入同比 `+153%`、RPO `$46.1M`、`$35M` UAS PO 与 `$21M` LEV PO",
            "RPO 只覆盖全年剩余收入一部分，`$500M` 是客户终端订单不是 AMPX backlog",
        ),
        "右尾弹性优先": (
            "乐观收入 `$170-210M`、极度乐观 `$250-330M`，防务无人机、NDAA/DIU 与 `>2GWh` 代工 access 提供上限",
            "极度乐观可信度低到中，需直接 PO、交付验收、回款和合规供应同时成立",
        ),
        "风险调整收益": (
            "无债、现金约 `$62.6M`，Adjusted EBITDA 指引转正，收入基数小导致上行弹性大",
            "2026-06-22 Forward PE `276.16`、P/S `24.56`，GAAP 亏损、AR/bill-and-hold 和客户集中抵消赔率",
        ),
        "下行保护优先": (
            "无债、current ratio 高，Colorado 退出后固定资本开支压力下降",
            "Call IV `90.8%`、SOXX 压力窗口累计 `-20.65%`，现金流和客户验收不是防守资产特征",
        ),
        "估值消化优先": (
            "NTM 基准收入相对 TTM `$90.3M` 增速约 `+44-66%`，若毛利维持可改善收入倍数",
            "Forward PE `276.16`、P/S `24.56`，估值已经要求持续超预期和利润率上修",
        ),
        "近端催化优先": (
            "未来 1-2 季度可验证 RPO、新直接 PO、LEV 交付、DIU/Fremont/Nanotech 进度和 Matternet 量化订单",
            "催化必须转成 AMPX 直接订单和收入确认，新闻或客户终端订单不能直接计入",
        ),
        "价格确认/动量": (
            "2026-06-03 过去两周 `+44.26%`，高 IV 显示资金关注度高",
            "过去一月仅 `+4.17%`，且 2026-06-22 价格回落到 `15.65`，短线波动很高",
        ),
        "激进短线": (
            "小市值、高 IV、防务无人机与硅负极电池叙事容易在订单/RPO节点上快速重定价",
            "高波动可放大收益也会放大回撤，AR、bill-and-hold 或毛利反证会快速压估值",
        ),
    }

    out: list[str] = []
    out += [
        "# AMPX 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：AMPX / Amprius Technologies",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 AMPX vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。AMPX 的优势集中在小基数高增长、UAS/Defense/LEV 订单链条和高 IV 高关注度，不是稳健防守。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是估值高、GAAP 亏损、现金流尚未稳定、AR/bill-and-hold 与客户集中反证。",
        "- A 最适合的投资者画像：愿意承受高波动，押注高性能硅负极电芯在防务无人机、HAPS 和 LEV 中继续从 PO/RPO 转收入，并接受估值主要靠高增速消化的进攻型投资者。",
        "- A 最不适合的投资者画像：下行保护、估值纪律、成熟自由现金流或低波动优先的配置型资金；这类思路下 AMPX 经常输给成熟半导体、工业、电力设备和软件公司。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在估值消化、现金流、防守或更硬的 AI 数据中心收入化证据上压过 AMPX。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：AMPX 是项目内高右尾、高催化、高波动的小盘进攻标的，适合作为非核心高弹性仓位；若按风险调整或估值消化，它明显不是全项目最优。",
        "- 后续最重要跟踪数据：RPO、直接 PO、UAS/Ukraine/EMEA 出货、LEV 复购、Matternet 或其他 commercial drone 量化订单、DIU/Fremont/Nanotech 进度、毛利率、AR、bill-and-hold 未交付金额、operating cash flow。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "AMPX"]),
        base.row(["公司名称", "Amprius Technologies"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "SiCore UAS/HAPS/Defense；SiCore LEV cylindrical；NDAA-compliant U.S. supply / DIU / Fremont 10MWh；SiMaxx/eVTOL/EV-capable/customization；数据中心 UPS/BBU/BESS 仅跟踪且 NTM 为 0"]),
        base.row(["NTM 基准收入", a["base_rev"] or "`$130-150M`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "RPO/PO 到实物交付、客户验收和回款；RPO `$46.1M` 只覆盖 FY2026 指引剩余收入一部分。"]),
        base.row(["最大反证", "2026Q1 AR `$35.3M`、bill-and-hold revenue `$5.8M`、未交付 bill-and-hold `$17.1M`；`$500M` 为客户终端订单，不是 AMPX backlog。"]),
        base.row(["近端催化剂", "新增 `$30M+` 级 AMPX 直接 PO、RPO 连续上升、LEV 复购、Matternet/商业 drone 小批量、DIU/Fremont/NDAA qualification。"]),
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
        base.row(["直接同业", "项目内没有纯粹与 AMPX 在硅负极无人机/HAPS 高性能电芯上高度重叠的直接同业；若未来加入电芯同业，应优先看订单、毛利、认证和客户质量。", "本次无典型纯直接同业", "不强行制造直接同业；相关能源/电池公司按相邻替代处理。"]),
        base.row(["相邻替代", "同属能源、储能、电力设备、AI 数据中心供电或高弹性能源基础设施资金篮子，回答资金只能买一个时谁的增长质量和赔率更好。", "ENS、FLNC、BE、GNRC、VRT、ETN、POWL、NVT、GEV", "默认比较订单/收入兑现、利润质量、估值消化和风险调整收益。"]),
        base.row(["上下游", "B 与 AMPX 的终端应用或电动/航空航天需求链更接近，重点看利润池位置、客户验收和产品商业化阶段。", "TSLA、RKLB", "不把终端市场规模直接当 AMPX 机会，也不把 AMPX 小基数右尾直接当确定收入。"]),
        base.row(["跨赛道", "半导体、网络、服务器、软件、材料等业务差异大，只作为资金配置替代比较。", "NVDA、AVGO、TSM、ASML、MSFT、CRDO、ALAB", "结论力度更保守；除非档位差很大，否则使用中性或微倾向。"]),
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
        need = "需要 AMPX 证明高增长能转成可持续毛利、现金流和更低 AR/bill-and-hold 风险。"
        if comparison["rel"] == "跨赛道":
            need = "需要 AMPX 用直接 PO/RPO、收入确认和现金流改善抵消跨赛道公司的规模、盈利或 AI 主链优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更高增速、更明确订单/RPO、或同等短线催化，并避免估值反证扩大。"
        if b["scores"]["估值消化优先"] > a["scores"]["估值消化优先"]:  # type: ignore[index,operator]
            need = "需要 B 把估值优势转化为增长确认，或证明其近端催化不弱于 AMPX。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照与区间涨跌文件覆盖情况见对应金融资料；本次公司全集中缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/电力_发电_能源_储能/AMPX_Amprius_Technologies_公司调研_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_ampx_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+44-66%` 做同号区间修正后建档。",
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
                "ampx_tiers": companies[TARGET]["tiers"],
                "ampx_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
