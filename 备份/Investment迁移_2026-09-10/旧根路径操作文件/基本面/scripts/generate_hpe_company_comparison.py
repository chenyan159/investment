from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated
import generate_cls_company_comparison as cls_calibrated


TARGET = "HPE"
TARGET_NAME = "惠普企业"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "HPE_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_SYSTEM_PEERS = {
    "DELL",
    "SMCI",
    "PENG",
    "JBL",
    "FLEX",
    "SANM",
    "CLS",
    "FN",
    "NTAP",
    "PSTG",
}

DIRECT_NETWORK_PEERS = {"ANET", "CSCO", "CIEN", "NOK", "VISN"}

SERVER_STORAGE_ADJACENT = {
    "MRAM",
    "RMBS",
    "SIMO",
    "SNDK",
    "STX",
    "WDC",
    "MU",
}

UPSTREAM_CHIP_NETWORK = {
    "AAOI",
    "ADI",
    "ALAB",
    "AMD",
    "APH",
    "ARM",
    "AVGO",
    "BDC",
    "BELFB",
    "CDNS",
    "COHR",
    "CRDO",
    "GLW",
    "INTC",
    "LITE",
    "LWLG",
    "MCHP",
    "MRVL",
    "MTSI",
    "MXL",
    "NVDA",
    "ON",
    "POET",
    "QCOM",
    "SITM",
    "SMTC",
    "SNPS",
    "STM",
    "TEL",
    "TXN",
    "VIAV",
}

DOWNSTREAM_CLOUD = {
    "ADBE",
    "AMZN",
    "APLD",
    "BABA",
    "CRWD",
    "CRWV",
    "DLR",
    "EQIX",
    "GOOGL",
    "IBM",
    "IREN",
    "META",
    "MSFT",
    "NBIS",
    "NTNX",
    "ORCL",
}

POWER_COOLING_CHAIN = {
    "AAON",
    "ABBNY",
    "AEIS",
    "AEP",
    "BE",
    "BWXT",
    "CARR",
    "CEG",
    "CMI",
    "DTE",
    "EME",
    "ENS",
    "ET",
    "ETN",
    "ETR",
    "FIX",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "IESC",
    "JCI",
    "MOD",
    "MYRG",
    "NVT",
    "OKLO",
    "POWI",
    "POWL",
    "PSIX",
    "PWR",
    "SMR",
    "TT",
    "VICR",
    "VRT",
    "VST",
}

EXTRA_SCORE_FLOORS = {
    **cls_calibrated.EXTRA_SCORE_FLOORS,
    "ANET": {
        "NTM兑现优先": 88,
        "右尾弹性优先": 86,
        "风险调整收益": 64,
        "下行保护优先": 72,
        "估值消化优先": 60,
        "近端催化优先": 76,
        "价格确认/动量": 76,
        "激进短线": 84,
    },
    "CSCO": {
        "NTM兑现优先": 72,
        "右尾弹性优先": 55,
        "风险调整收益": 82,
        "下行保护优先": 90,
        "估值消化优先": 64,
        "近端催化优先": 70,
        "价格确认/动量": 76,
        "激进短线": 66,
    },
    "CIEN": {
        "NTM兑现优先": 82,
        "右尾弹性优先": 78,
        "风险调整收益": 64,
        "下行保护优先": 58,
        "估值消化优先": 68,
        "近端催化优先": 84,
        "价格确认/动量": 74,
        "激进短线": 80,
    },
    "CRWV": {
        "NTM兑现优先": 92,
        "右尾弹性优先": 100,
        "风险调整收益": 56,
        "下行保护优先": 35,
        "估值消化优先": 63,
        "近端催化优先": 86,
        "价格确认/动量": 60,
        "激进短线": 100,
    },
    "DELL": {
        "NTM兑现优先": 86,
        "右尾弹性优先": 78,
        "风险调整收益": 68,
        "下行保护优先": 74,
        "估值消化优先": 82,
        "近端催化优先": 84,
        "价格确认/动量": 96,
        "激进短线": 88,
    },
    "SMCI": {
        "NTM兑现优先": 76,
        "右尾弹性优先": 76,
        "风险调整收益": 55,
        "估值消化优先": 82,
        "近端催化优先": 74,
        "激进短线": 78,
    },
    "JBL": {
        "NTM兑现优先": 78,
        "右尾弹性优先": 70,
        "风险调整收益": 64,
        "估值消化优先": 68,
        "近端催化优先": 72,
        "价格确认/动量": 78,
        "激进短线": 76,
    },
    "NTAP": {
        "NTM兑现优先": 70,
        "风险调整收益": 64,
        "下行保护优先": 72,
        "估值消化优先": 66,
    },
}

HPE_SCORE_OVERRIDES = {
    "NTM兑现优先": 84.0,
    "右尾弹性优先": 78.0,
    "风险调整收益": 68.0,
    "下行保护优先": 62.0,
    "估值消化优先": 86.0,
    "近端催化优先": 86.0,
    "价格确认/动量": 96.0,
    "激进短线": 90.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    calibrated.fix_growth_ranges(companies)
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    for ticker, floors in {**calibrated.SCORE_FLOORS, **EXTRA_SCORE_FLOORS}.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[assignment]
            company["scores"][strategy] = max(float(current), float(floor))  # type: ignore[index]

    for strategy, score in HPE_SCORE_OVERRIDES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score  # type: ignore[index]
    calibrated.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_SYSTEM_PEERS or ticker in DIRECT_NETWORK_PEERS:
        return "直接同业"
    if ticker in SERVER_STORAGE_ADJACENT:
        return "相邻替代"
    if ticker in UPSTREAM_CHIP_NETWORK or ticker in DOWNSTREAM_CLOUD or ticker in POWER_COOLING_CHAIN:
        return "上下游"
    if category in {"AI服务器_存储_EMS", "AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    if category in INFRA_CATS:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A有FY2026高增指引和AI backlog",
            "右尾弹性优先": "A有AI Systems和AI网络双右尾",
            "风险调整收益": "A估值、增长和现金流较均衡",
            "下行保护优先": "A低P/S和企业客户底盘支撑",
            "估值消化优先": "A低P/S和高增速更易消化估值",
            "近端催化优先": "A有Q3指引、订单和交付催化",
            "价格确认/动量": "A近月价格确认显著更强",
            "激进短线": "A高IV叠加AI订单叙事更进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/订单兑现证据更硬",
            "右尾弹性优先": "B右尾收入弹性更大",
            "风险调整收益": "B上行下行组合更好",
            "下行保护优先": "B现金流或防御属性更强",
            "估值消化优先": "B业绩或估值消化更顺",
            "近端催化优先": "B近端重定价事件更清楚",
            "价格确认/动量": "B价格趋势或强度更好",
            "激进短线": "B短线爆发力和关注度更强",
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

    score_diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
    tier_diff = tier_value(str(at)) - tier_value(str(bt))
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
        if tag == "强烈建议投A" and abs(score_diff) < 38 and abs(tier_diff) < 4:
            tag = "建议投A"
        elif tag == "强烈建议投B" and abs(score_diff) < 38 and abs(tier_diff) < 4:
            tag = "建议投B"
        elif tag == "建议投A" and abs(score_diff) < 18 and abs(tier_diff) < 2:
            tag = "微倾向投A"
        elif tag == "建议投B" and abs(score_diff) < 18 and abs(tier_diff) < 2:
            tag = "微倾向投B"
    if rel == "直接同业" and abs(score_diff) >= 20 and tag.startswith("建议"):
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
    a_core = (
        float(a["scores"]["NTM兑现优先"])
        + float(a["scores"]["右尾弹性优先"])
        + float(a["scores"]["风险调整收益"])
        + float(a["scores"]["估值消化优先"])
        + float(a["scores"]["近端催化优先"])
    )
    b_core = (
        float(b["scores"]["NTM兑现优先"])
        + float(b["scores"]["右尾弹性优先"])
        + float(b["scores"]["风险调整收益"])
        + float(b["scores"]["估值消化优先"])
        + float(b["scores"]["近端催化优先"])
    )
    return "A" if a_core >= b_core else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if float(a["scores"]["估值消化优先"]) - float(b["scores"]["估值消化优先"]) > 12:  # type: ignore[index]
            return "HPE 的低 P/S、低远期 PE 和 FY2026 增长指引使估值消化更有利。"
        if float(a["scores"]["近端催化优先"]) - float(b["scores"]["近端催化优先"]) > 12:  # type: ignore[index]
            return "HPE 的 AI backlog、Q3/Q4 指引和 Juniper 网络收入化更接近重定价窗口。"
        if float(a["scores"]["价格确认/动量"]) - float(b["scores"]["价格确认/动量"]) > 12:  # type: ignore[index]
            return "HPE 已经有更强价格确认，且基本面上有订单和指引配合。"
        return "HPE 在兑现、估值和近端催化上更均衡，B 的优势不足以覆盖差距。"
    if float(b["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]) > 12:  # type: ignore[index]
        return f"{b['ticker']} 的非线性右尾和重定价弹性明显强于 HPE。"
    if float(b["scores"]["下行保护优先"]) - float(a["scores"]["下行保护优先"]) > 12:  # type: ignore[index]
        return f"{b['ticker']} 的现金流、防御性或压力窗口表现优于 HPE。"
    if float(b["scores"]["NTM兑现优先"]) - float(a["scores"]["NTM兑现优先"]) > 10:  # type: ignore[index]
        return f"{b['ticker']} 的 NTM 收入/订单兑现证据更强。"
    if float(b["scores"]["风险调整收益"]) - float(a["scores"]["风险调整收益"]) > 10:  # type: ignore[index]
        return f"{b['ticker']} 的风险调整赔率比 HPE 更好。"
    return f"{b['ticker']} 在多数投资思路下比 HPE 更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong: list[str] = []
    b_strong: list[str] = []
    close: list[str] = []
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


def category_short(category: str) -> str:
    return category.replace("_", "/") if category else "未分类"


def short_name(company: dict[str, object]) -> str:
    return f"{company['ticker']} / {company['name']}"


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    output: list[dict[str, object]] = []
    for ticker in sorted(t for t in companies if t != TARGET):
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


def win_strategies(comparison: dict[str, object], side: str) -> list[str]:
    suffix = "投A" if side == "A" else "投B"
    return [
        strategy
        for strategy, cell in zip(STRATS, comparison["cells"])  # type: ignore[arg-type]
        if (base.tag_in_cell(cell) or "").endswith(suffix)
    ]


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
        key=lambda x: (
            int(x["bc"]) - int(x["ac"]),
            int(x["bc"]),
            float(x["b"]["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]),  # type: ignore[index]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            int(x["ac"]) - int(x["bc"]),
            int(x["ac"]),
            float(a["scores"]["估值消化优先"]) + float(a["scores"]["近端催化优先"]) - float(x["b"]["scores"]["估值消化优先"]) - float(x["b"]["scores"]["近端催化优先"]),  # type: ignore[index]
        ),
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if int(x["bc"]) >= 5 and int(x["bc"]) - int(x["ac"]) >= 3][:45]
    strong_a_rows = [x for x in strong_a if int(x["ac"]) >= 5 and int(x["ac"]) - int(x["bc"]) >= 3][:45]
    final_b_rows = [x for x in strong_b if x["final"] == "B"]
    strong_b_phrase = "、".join([x["ticker"] for x in strong_b_rows[:12]]) if strong_b_rows else "无"
    final_b_phrase = "、".join([x["ticker"] for x in final_b_rows[:12]]) if final_b_rows else "无"
    missing_fin = [ticker for ticker in sorted(companies) if not companies[ticker]["fin"]]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    file_list = "；".join(f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies))  # type: ignore[union-attr]

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]  # type: ignore[index]
    support = {
        "NTM兑现优先": ("Q2 FY2026 收入 +40%，FY2026 指引 +29%-+33%，AI backlog 59 亿美元", "AI Systems backlog 到收入仍受供应、现场和验收约束"),
        "右尾弹性优先": ("AI Systems、Networks for AI、Alletra/GreenLake 同时提供上行情景", "Helios、Rubin、1.6T 和软件 attach 很多偏 2027+ 或缺独立收入拆分"),
        "风险调整收益": ("2026-06-22 P/S 1.65、Forward PE 12.11，基准 FCF 至少 35 亿美元", "Call IV 66.2%，库存和低毛利 GPU/内存透传会放大利润/现金流波动"),
        "下行保护优先": ("企业/主权客户、Networking 高毛利 mix 和低销售倍数提供缓冲", "SOXX 三段压力窗口累计 -50.37%，不如公用事业/高现金流防御股"),
        "估值消化优先": ("低 P/S、低远期 PE 和 25%-30% NTM 基准收入增速组合稀缺", "若 AI Systems 低毛利透传或验收延迟，估值消化会转慢"),
        "近端催化优先": ("Q3 FY2026 115-121 亿美元收入指引、FY2026 H2 backlog 转收入、Networks for AI 订单", "需要看到 backlog 转收入而不是库存继续堆高"),
        "价格确认/动量": ("2026-06-03 过去两周 +63.17%、过去一月 +93.03%，价格已验证叙事", "2026-06-22 已回落至 48.40，短线过热后容易震荡"),
        "激进短线": ("高 IV、强动量和 AI server/network 重定价叙事适合进攻", "激进交易对订单取消、交付延期和组件成本高度敏感"),
    }

    out: list[str] = []
    out += [
        "# HPE 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：HPE / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 HPE vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。HPE 最强的是低估值消化、近端订单/指引催化和已经发生的价格确认，而不是绝对最高的长期平台右尾。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。在下行保护上，HPE 的 IV 和历史压力窗口弱于公用事业、成熟工业和现金流防御股；在右尾上又弱于少数 AI 芯片、HBM、NeoCloud 和高弹性网络标的。",
        "- A 最适合的投资者画像：愿意承担 AI server 交付和库存波动、但希望用较低 P/S/远期 PE 押注 FY2026 H2 backlog 转收入、Juniper 网络利润 mix 和企业/主权 AI 工厂订单的进攻型价值成长资金。",
        "- A 最不适合的投资者画像：只要最低波动、最强现金流下行保护，或只追求最极端 AI 右尾和高 beta 短线爆发的资金。",
        f"- 多数思路下最强反方公司：{strong_b_phrase}。最终选择为 B 的主要公司包括 {final_b_phrase}，它们通常在高确定性订单/RPO、极端右尾、现金流防御或更清楚的同业产品代际上超过 HPE。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：HPE 位于项目内中上游，强于大量传统工业、材料、低增长零部件和小型反证较重公司；但面对 {final_b_phrase} 这类右尾或同业强证据标的时，不是多数思路的最优解。",
        "- 后续最重要跟踪数据：Q3/Q4 FY2026 revenue vs Q3 115-121 亿美元指引和 FY2026 +29%-+33% 指引；AI Systems backlog、orders、cancelations 和 revenue conversion；Networks for AI 订单与收入确认；Networking normalized growth 和 margin；Storage/Alletra/X10000、GreenLake ARR、inventory、purchase commitments、FCF、net leverage。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "HPE"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "485-505 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润：{a['base_profit']}；现金流：{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI Systems backlog 从订单到收入确认的交付链条，尤其是 GPU/加速器、DRAM/NAND、网络组件、液冷/电力现场、客户验收和营运资本占用。"]),
        base.row(["最大反证", "AI Systems 直接收入未单列，backlog 不等于 NTM 收入；低毛利 GPU/内存透传、库存上升和客户验收延期可能吞噬收入上修。"]),
        base.row(["近端催化剂", "Q3/Q4 FY2026 收入兑现、AI Systems orders/backlog 转收入、Networks for AI 订单确认、Juniper normalized growth/margin、Alletra/GreenLake attach 和 FCF 改善。"]),
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
        base.row(["直接同业", "与 HPE 在 AI server、企业服务器、存储、网络系统、EMS/OEM 交付或企业/数据中心网络需求池高度重叠，优先比较订单/backlog、收入确认、产品代际、毛利率、客户质量和同业估值。", "DELL、SMCI、PENG、JBL、FLEX、SANM、CLS、FN、NTAP、PSTG、ANET、CSCO、CIEN、NOK", "同业证据权重最高；若一方在收入兑现、产品代际或估值消化明显胜出，结论力度可上调。"]),
        base.row(["相邻替代", "同属 AI server/storage/存储器/高速接口资金篮子，但收入模式或利润池不完全重叠。", "MU、WDC、STX、SNDK、RMBS、SIMO、MRAM", "重点看资金只能买一个时的增长质量、估值消化、右尾和库存/周期风险。"]),
        base.row(["上下游", "一方是 HPE 的芯片/光互联/电力冷却/云客户/IDC 需求链或供应链位置，比较利润捕获、议价权和催化时间。", "NVDA、AMD、AVGO、MRVL、MSFT、AMZN、GOOGL、EQIX、VRT、ETN、GEV、PWR", "不能把上游稀缺或下游收入规模机械等同为更好，必须看利润池、估值和兑现可见度。"]),
        base.row(["跨赛道", "半导体材料、前道设备、封测、工业、化工等与 HPE 业务差异大但可作为项目内资金配置替代。", "ASML、TSM、LIN、TMO、ECL、CAT、DHR、MMM", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
                    short_name(b),  # type: ignore[arg-type]
                    category_short(str(b["category"])),  # type: ignore[index]
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],  # type: ignore[list-item]
                    majority(int(comparison["ac"]), int(comparison["bc"]), int(comparison["nc"])),
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
        need = "需要 HPE 把 AI backlog 稳定转成收入和 FCF，并证明 Juniper/GreenLake 高毛利 mix 能抵消服务器透传毛利压力。"
        if comparison["rel"] == "跨赛道":
            need = "需要 HPE 证明其风险调整收益能接近该跨赛道标的，或用更强估值消化和近端订单兑现抵消业务差异。"
        out.append(base.row([index, short_name(b), "、".join(win_strategies(comparison, "B")), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        need = "需要 B 提高 NTM 收入/利润兑现可信度、降低估值或披露更硬订单/backlog。"
        if float(b["scores"]["右尾弹性优先"]) > float(a["scores"]["右尾弹性优先"]):  # type: ignore[index]
            need = "需要 B 把右尾叙事转成可确认收入和现金流，并降低估值/波动反证。"
        out.append(base.row([index, short_name(b), "、".join(win_strategies(comparison, "A")), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层全部 `*_收入传导估值评估_*.md` 正式文件；同一 Ticker 取文件名日期最新一份；本次得到 `{n}` 家，日期范围 `{date_range}`。未读取 `分析报告/公司评估/结果/备份/`、`分析报告/备份/`、`分析报告/tmp/`、`分析报告/公司排序/`、`分析报告/简单排序/` 或 `特征量化/` 作为决策依据。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 `{n - len(missing_fin)}/{n}` 家；缺少当日价格/估值/IV 的公司为 `{('、'.join(missing_fin) if missing_fin else '无')}`，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        "- 公司 A 日度数据摘录：2026-06-22 最新价格 `48.40`，市值 `$64.09B`，TTM PE `45.23`，Forward PE `12.11`，P/S `1.65`，P/B `2.53`，EV/EBITDA `14.00`，Call IV `66.2%`，Put IV `70.6%`；2026-06-03 过去两周 `+63.17%`、过去一月 `+93.03%`；2026-06-04 三段 SOXX 压力窗口累计 `-50.37%`。",
        "- 其他主要来源：`公司调研/公司索引.md`、HPE 公司调研 `公司调研/AI服务器_存储_EMS/HPE_惠普企业_公司调研_2026-06-20.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研、IR、SEC、产品公告和财报来源。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    base.TARGET = TARGET
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
                "hpe_tiers": companies[TARGET]["tiers"],
                "hpe_ranks": companies[TARGET]["ranks"],
                "hpe_scores": {strategy: round(float(companies[TARGET]["scores"][strategy]), 2) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
