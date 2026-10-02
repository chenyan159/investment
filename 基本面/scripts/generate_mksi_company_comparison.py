from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "MKSI"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MKSI_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_SUBSYSTEM_PEERS = {
    "AEIS",
    "ENTG",
    "ICHR",
    "Q",
    "UCTT",
}
WFE_OEM_PEERS = {
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
    "VECO",
}
MATERIALS_PACKAGING_ADJACENT = {
    "AJNMY",
    "AMKR",
    "ASMVY",
    "ASX",
    "BESIY",
    "CAMT",
    "COHU",
    "FORM",
    "HOCPY",
    "KEYS",
    "KLIC",
    "MICLF",
    "MTRN",
    "ONTO",
    "PLAB",
    "ROG",
    "SHECY",
    "TER",
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

    # MKSI calibration: MKS has a strong NTM bridge from Q2 2026 guidance,
    # VSD semiconductor subsystems, MSD/Atotech chemistry/equipment, ESI laser
    # drilling and service/consumables. The offsets are indirect AI exposure,
    # high IV, leverage/FCF timing and no formal bookings/backlog disclosure.
    a = companies[TARGET]
    overrides = {
        "NTM兑现优先": 76.0,
        "右尾弹性优先": 70.0,
        "风险调整收益": 52.0,
        "下行保护优先": 64.0,
        "估值消化优先": 64.0,
        "近端催化优先": 72.0,
        "价格确认/动量": 82.0,
        "激进短线": 88.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_SUBSYSTEM_PEERS:
        return "直接同业"
    if ticker in WFE_OEM_PEERS or ticker in FOUNDRY_MEMORY_CUSTOMERS or ticker in AI_DEMAND_CHAIN:
        return "上下游"
    if ticker in MATERIALS_PACKAGING_ADJACENT:
        return "相邻替代"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A Q2指引和三分部run-rate更清楚",
            "右尾弹性优先": "A封装基板/真空RF右尾更直接",
            "风险调整收益": "A增长和估值组合更均衡",
            "下行保护优先": "A服务耗材和化学品粘性更稳",
            "估值消化优先": "A收入增速可部分消化估值",
            "近端催化优先": "A Q2/Q3与订单措辞验证更近",
            "价格确认/动量": "A近期价格确认更强",
            "激进短线": "A高IV叠加设备链重定价更适合进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/RPO或订单兑现更硬",
            "右尾弹性优先": "B右尾更大或小基数更弹",
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
            return "MKSI 的Q2指引、VSD/MSD/PSD收入基数和服务耗材桥更清楚。"
        if a["scores"]["价格确认/动量"] - b["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
            return "MKSI 近期价格确认更强，且半导体子系统和E&P订单仍有财报验证窗口。"
        if a["scores"]["激进短线"] - b["scores"]["激进短线"] > 12:  # type: ignore[index,operator]
            return "MKSI 的高IV、强动量和先进封装/半导体设备链叙事更适合短线进攻。"
        return "MKSI 的制造端兑现质量和Atotech/ESI期权更好，B 的优势不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI收入、小基数或短线右尾明显强于 MKSI。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的当前估值更容易被NTM业绩消化。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的低波动、低估值或现金流防守属性更好。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/RPO/订单兑现证据更强。"
    return f"{b['ticker']} 在多数投资思路下比 MKSI 更符合项目内资金配置目标。"


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
        f"P/S {fmt_num(fin.get('ps'))}，Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:6]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "Q2 2026收入指引中位`12.00亿美元`，Semi/E&P/SI分别`5.50/3.50/3.00亿美元`，NTM基准`50.0-52.0亿美元`",
            "未披露标准bookings/backlog，订单转收入仍受OEM design-in、客户capex、交付验收和营运资本约束",
        ),
        "右尾弹性优先": (
            "VSD高端真空/RF/remote plasma、MSD/Atotech先进封装化学品与ESI激光钻孔共同提供上限",
            "AI暴露主要是制造端间接受益，TGV/glass/CPO等多为远期期权，不宜进入NTM基准",
        ),
        "风险调整收益": (
            "基准adjusted EBITDA `12.8-14.0亿美元`，consumables & service占Q1收入`40%`，利润质量有支撑",
            "2026-06-22 Forward PE `28.14`、P/S `6.97`、Call IV `69.2%`，净杠杆、FCF滞后和WFE/E&P周期反证仍重",
        ),
        "下行保护优先": (
            "服务耗材、化学品消耗和Specialty Industrial稳定项提供一定收入韧性",
            "SOXX压力窗口累计`-65.32%`，高IV、债务和半导体capex周期会放大回撤",
        ),
        "估值消化优先": (
            "若NTM收入`50.0-52.0亿美元`、毛利率`47%-48%`、EBITDA`12.8-14.0亿美元`兑现，可部分消化当前倍数",
            "估值已计入VSD/MSD复苏和先进封装期权，若Q2/Q3指引或FCF低于预期，消化会失败",
        ),
        "近端催化优先": (
            "Q2实际、Q3指引、Semi/E&P run-rate、VSD/MSD/PSD margin、remote plasma/chemistry equipment/laser drilling订单均在1-2季验证",
            "催化依赖订单转收入和化学品pull-through，不是单纯AI capex标题即可兑现",
        ),
        "价格确认/动量": (
            "2026-06-03两周`+7.59%`、一月`+19.96%`，2026-06-22价格升至`420.56`，6月内继续确认",
            "强价格确认叠加高IV意味着预期交易较充分，任何Q2/Q3失望都会放大回撤",
        ),
        "激进短线": (
            "高IV、强价格确认、WFE复苏、advanced packaging、Atotech/ESI订单和半导体子系统重定价适合短线进攻",
            "MKSI仍是间接受益制造链公司，爆发力低于小盘光互联、NeoCloud或直接AI芯片/云算力标的",
        ),
    }

    out: list[str] = []
    out += [
        "# MKSI 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：MKSI / MKS Inc",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 MKSI vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。MKSI 的优势来自 Q2 2026 明确指引、VSD/MSD/PSD三分部收入基数、服务耗材占比、Atotech/ESI先进封装订单线索和近期价格确认。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是AI收入传导偏间接、Forward PE `28.14`和P/S `6.97`已反映复苏，且SOXX压力窗口累计`-65.32%`、净杠杆、FCF滞后和未披露标准backlog仍是硬反证。",
        "- A 最适合的投资者画像：希望配置 AI 半导体制造上游中真空/RF/流体控制、先进PCB/封装化学品、电镀设备和激光钻孔的中高弹性设备材料复合标的，能接受半导体capex周期和高波动。",
        "- A 最不适合的投资者画像：只追求直接AI GPU/云算力收入、极端小基数右尾、最低估值防守，或不能承受高IV和设备周期回撤的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在直接AI收入、小基数右尾、估值消化、低波动防守或现金流质量上压过 MKSI。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：MKSI 是项目内半导体制造子系统和先进封装材料链的中上位置，NTM兑现、近端催化和价格确认较强；但风险调整收益和下行保护不如低波动现金流资产，右尾也弱于直接AI芯片、光互联、NeoCloud和部分小基数设备股。",
        "- 后续最重要跟踪数据：Q2 2026实际收入与Semi/E&P/SI拆分、Q3 2026指引、VSD/MSD/PSD收入和margin、consumables & service金额及占比、remote plasma/microwave/dissolved gas/chemistry equipment/laser drilling订单措辞、应收/库存/FCF/净杠杆、Atotech/ESI在高端PCB/封装基板/TGV/glass/CPO相关客户认证和量产证据。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "MKSI"]),
        base.row(["公司名称", "MKS Inc"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "50.0-52.0 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI需求不是直接进rack BOM，而是经WFE、HBM/DRAM、先进逻辑、先进封装、高层PCB/封装基板设备和耗材传导；关键在客户capex、OEM design-in、订单转收入、化学品/设备交付和Atotech/ESI能否进入AI package substrate。"]),
        base.row(["最大反证", "未披露标准backlog/book-to-bill；Q1 FCF偏低且营运资本占用；估值和价格已计入较强复苏；PSD/ESI订单可能偏消费电子flex而非AI高层PCB。"]),
        base.row(["近端催化剂", "Q2 2026实际收入和分终端市场、Q3指引、VSD/MSD/PSD margin、consumables & service金额、remote plasma/chemistry equipment/laser drilling订单措辞、H2 FCF和净杠杆。"]),
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
        base.row(["直接同业", "同属半导体设备子系统、工艺电源/RF、流体/气体控制、先进封装化学品或关键子组件资金池，优先看订单/指引、毛利率、客户认证、服务耗材粘性和同业估值。", "AEIS、ENTG、ICHR、Q、UCTT", "同业证据权重最高；若收入兑现、产品代际或估值差距大，结论力度可以上调。"]),
        base.row(["相邻替代", "同处AI半导体设备、封装测试、材料/基板、数据中心基础设施或AI资本开支受益篮子，但收入模式不完全相同。", "AMAT、LRCX、TER、ATEYY、BESIY、CAMT、VRT、ETN", "回答资金只能买一个时，谁的增长质量、订单可见度、估值消化和近端催化更好。"]),
        base.row(["上下游", "一方处在MKSI客户、供应商或终端需求链，重点看利润池位置、议价权、瓶颈稀缺性和收入确认链条。", "TSM、MU、INTC、NVDA、AVGO、MSFT、AMAT、LRCX、ASML", "不把下游AI收入规模直接等同MKSI机会，也不把上游子系统稀缺自动等同更好。"]),
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
        need = "需要 MKSI 证明Q2/Q3指引继续兑现或上修，VSD/MSD/ESI订单转收入与FCF同步改善，并降低高IV和净杠杆反证。"
        if comparison["rel"] == "直接同业":
            need = "需要 MKSI 在同业中证明VSD高端RF/真空、Atotech化学品和ESI激光钻孔能带来更强收入、GM、FCF和订单持续性。"
        elif comparison["rel"] == "上下游":
            need = "需要 MKSI 证明比该上下游公司更能捕获AI半导体制造利润池，而不是只承担capex周期beta。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 MKSI 用更强现金流、估值消化或防守表现抵消跨赛道标的的低波动/防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更强NTM收入利润兑现、或更低估值/更好现金流来抵消MKSI的半导体子系统与先进封装材料弹性。"
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
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 181 家；本次公司评估全集为 {n} 家，因此缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/晶圆制造_前道设备/MKSI_MKS_Inc_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体设备子系统与真空_RF_流体模块_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_AI芯片前道制造设备_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装湿化学与表面处理材料_2026-06-11.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 外部交叉核验：MKS Inc. Q1 2026 results release（https://investor.mks.com/news-releases/news-release-details/mks-inc-reports-first-quarter-2026-financial-results）、MKS Q1 2026 earnings presentation（https://investor.mks.com/static-files/382a3833-c6d9-47a6-9b39-bf4d1f1a2fce）和 MKS Q1 2026 net revenues by end market and division（https://investor.mks.com/static-files/e165cd1d-705c-4603-8f5d-a657872848f9）。",
        "- 自动化脚本：`scripts/generate_mksi_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间做同号区间修正后建档；未读取下游量化目录或现成排序结论。",
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
                "mksi_tiers": companies[TARGET]["tiers"],
                "mksi_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
