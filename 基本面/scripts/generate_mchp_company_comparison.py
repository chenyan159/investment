from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base
import generate_ceg_company_comparison as project_calibration
import generate_etn_company_comparison as etn_calibration
import generate_hubb_company_comparison as hubb_calibration


TARGET = "MCHP"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MCHP_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_MIXED_SIGNAL_PEERS = {
    "ADI",
    "ALAB",
    "AOSL",
    "AVGO",
    "DIOD",
    "IFNNY",
    "LFUS",
    "MPWR",
    "MRAAY",
    "MRVL",
    "MTSI",
    "MXL",
    "ON",
    "POWI",
    "RMBS",
    "SIMO",
    "SITM",
    "SMTC",
    "ST",
    "STM",
    "TTDKY",
    "TXN",
    "VICR",
    "VSH",
}

SEMI_ADJACENT = {
    "AMD",
    "ARM",
    "CDNS",
    "NVDA",
    "QCOM",
    "SNPS",
}

DATA_CENTER_DEMAND_CHAIN = {
    "AAOI",
    "ANET",
    "APH",
    "AMZN",
    "BDC",
    "BELFB",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "CSCO",
    "DELL",
    "DLR",
    "EQIX",
    "FLEX",
    "FN",
    "GOOGL",
    "HPE",
    "JBL",
    "LITE",
    "LWLG",
    "META",
    "MSFT",
    "MU",
    "NBIS",
    "NOK",
    "NTAP",
    "ORCL",
    "PENG",
    "POET",
    "PSTG",
    "SANM",
    "SMCI",
    "SNDK",
    "STX",
    "TEL",
    "VIAV",
    "VISN",
    "WDC",
}

FABS_EQUIPMENT_AND_MATERIALS = {
    "ACLS",
    "ACMR",
    "AMAT",
    "AMKR",
    "ASGLY",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "AXTI",
    "BESIY",
    "CAMT",
    "COHU",
    "DSCSY",
    "ENTG",
    "FORM",
    "GFS",
    "ICHR",
    "IMOS",
    "KEYS",
    "KLAC",
    "KLIC",
    "LRCX",
    "MICLF",
    "MKSI",
    "NVMI",
    "ONTO",
    "PLAB",
    "Q",
    "SHECY",
    "SOMMY",
    "TOELY",
    "TSEM",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
}

AI_INFRA_ADJACENT = {
    "AAON",
    "ABBNY",
    "AEIS",
    "ALLE",
    "APLD",
    "ATKR",
    "BABA",
    "BE",
    "BWXT",
    "CARR",
    "CEG",
    "CMI",
    "CRWD",
    "CRWV",
    "EME",
    "ENS",
    "ETN",
    "FIX",
    "FLNC",
    "GEV",
    "HUBB",
    "HTHIY",
    "IBM",
    "IESC",
    "IREN",
    "JCI",
    "MOD",
    "MYRG",
    "NVT",
    "NTNX",
    "OKLO",
    "POWL",
    "PSIX",
    "PWR",
    "SMR",
    "TT",
    "VRT",
    "VST",
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

    for floorset in (project_calibration.SCORE_FLOORS, etn_calibration.LOCAL_SCORE_FLOORS):
        for ticker, floors in floorset.items():
            company = companies.get(ticker)
            if not company:
                continue
            for strategy, floor in floors.items():
                company["scores"][strategy] = max(company["scores"].get(strategy, 0), floor)  # type: ignore[index,union-attr]
    if "ETN" in companies:
        companies["ETN"]["scores"].update(etn_calibration.ETN_SCORES)  # type: ignore[index,union-attr]
    if "HUBB" in companies:
        companies["HUBB"]["scores"].update(hubb_calibration.HUBB_SCORES)  # type: ignore[index,union-attr]

    # MCHP-specific calibration:
    # - The generic parser reads ranges like "+23%-34%" as a mixed positive/negative
    #   range. MCHP is therefore anchored manually to the formal evaluation:
    #   FY2027 Q1 guide, NTM base revenue $5.8-6.3B, DCS CY2026 target near $0.5B,
    #   Non-GAAP OM 31-34%, and FCF re-covering dividend/deleveraging.
    # - Right-tail and short-line scores are capped because DCS is still a subsegment,
    #   customer/backlog detail is not disclosed, momentum is modest, IV is high,
    #   and the SOXX stress-window drawdown was severe.
    mchp = companies[TARGET]
    overrides = {
        "NTM兑现优先": 68.5,
        "右尾弹性优先": 66.0,
        "风险调整收益": 51.0,
        "下行保护优先": 58.0,
        "估值消化优先": 58.5,
        "近端催化优先": 64.0,
        "价格确认/动量": 58.5,
        "激进短线": 79.0,
    }
    for strategy, score in overrides.items():
        mchp["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_MIXED_SIGNAL_PEERS:
        return "直接同业"
    if ticker in SEMI_ADJACENT:
        return "相邻替代"
    if ticker in DATA_CENTER_DEMAND_CHAIN or ticker in FABS_EQUIPMENT_AND_MATERIALS:
        return "上下游"
    if ticker in AI_INFRA_ADJACENT:
        return "相邻替代"
    if category == "AI计算芯片_EDA_IP_custom_ASIC":
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI网络_光互联_连接器", "云算力_IDC_AI软件平台", "晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
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
            "NTM兑现优先": "A指引、库存正常化和DCS目标更可兑现",
            "右尾弹性优先": "A有PCIe/CXL/DCS与周期修复右尾",
            "风险调整收益": "A增长、FCF和估值组合更均衡",
            "下行保护优先": "A MCU/Analog底盘和FCF修复更稳",
            "估值消化优先": "A利润率恢复更能消化估值",
            "近端催化优先": "A有Q1兑现、DCS和Gen6/CXL验证",
            "价格确认/动量": "A价格确认略优且未极端透支",
            "激进短线": "A高IV和DCS重估适合事件交易",
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
            return "MCHP 的 FY2027 Q1 指引、库存正常化和 DCS 目标让 NTM 修复路径更清楚。"
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 10:  # type: ignore[index,operator]
            return "MCHP 的 MCU/Analog 基本盘和 FCF 修复给组合提供更好缓冲。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 8:  # type: ignore[index,operator]
            return "MCHP 的基准收入增长、Non-GAAP OM 和 FCF 修复更能支撑当前估值。"
        return "MCHP 的经营修复和现金流质量略好，B 的上行证据不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接 AI 收入、订单/RPO 或小基数右尾明显强于 MCHP。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/订单兑现证据更硬。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 10:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、防守属性或压力期表现更好。"
    if b["scores"]["近端催化优先"] - a["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
        return f"{b['ticker']} 的近端订单、产品或财报催化更可见。"
    return f"{b['ticker']} 在多数投资思路下比 MCHP 更符合项目内资金配置目标。"


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
        f"TTM PE `{fin.get('ttm_pe')}`，Forward PE `{fin.get('forward_pe')}`，P/S `{fin.get('ps')}`，"
        f"EV/EBITDA `{fin.get('ev_ebitda')}`，Call IV `{fin.get('call_iv')}%`，Put IV `{fin.get('put_iv')}%`；"
        f"2026-06-03 过去两周 `{mom2.get('mom2w')}%`、过去一月 `{mom1.get('mom1m')}%`；"
        f"2026-06-04 三段 SOXX 压力窗口累计 `{soxx.get('soxx_cum')}%`。"
    )
    support = {
        "NTM兑现优先": (
            "FY2027 Q1指引中点`14.56亿美元`、NTM基准`58-63亿美元`、DCS CY2026约`5亿美元`，库存正常化和传统MCU/Analog修复有收入表支撑",
            "Q1之后仍需订单延续；DCS客户名、平台backlog和产品级利润未披露，不能把广义Datacenter & Compute 18%全部当AI收入",
        ),
        "右尾弹性优先": (
            "乐观/极度乐观收入`66-71/75-82亿美元`；DCS PCIe/CXL/storage/retimer、Switchtec Gen6、XpressConnect和传统周期复苏提供非线性上限",
            "DCS仍是子业务，CXL/Gen6平台认证和客户份额未完全公开；Astera/Broadcom/Marvell/NVIDIA/AMD生态竞争强",
        ),
        "风险调整收益": (
            "基准Non-GAAP OM`31%-34%`、operating income`18-21亿美元`、FCF重回覆盖股息和去杠杆，提供可计算赔率",
            "2026-06-22 TTM PE`466.86`、P/S`11.81`、EV/EBITDA`48.79`且IV约60%，估值和波动会吃掉部分上行",
        ),
        "下行保护优先": (
            "MCU/Analog长生命周期、工业/汽车/通信分散需求和FCF修复有一定底盘",
            "SOXX三段压力窗口累计`-87.08%`，Call/Put IV约`60%`，高债务和股息分配压力使其不是防守顶档",
        ),
        "估值消化优先": (
            "FY2026收入`47.131亿美元`到NTM基准`58-63亿美元`，若毛利率稳定在`61.5%-63%`、OM回到`31%-34%`，可部分消化Forward PE",
            "P/S`11.81`和EV/EBITDA`48.79`已经要求DCS和传统恢复兑现；若Q2/Q3订单转弱，估值消化会迅速变差",
        ),
        "近端催化优先": (
            "FY2027 Q1实际收入/GM/OM、DCS是否继续兑现CY2026约`5亿美元`、Switchtec Gen6/XpressConnect qualification、选择性涨价和库存天数均是近端验证点",
            "缺少产品级订单/RPO和客户名；催化强度弱于AI GPU、光互联、NeoCloud和电力设备订单龙头",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周`+2.69%`、过去一月`+2.77%`，2026-06-22收盘`102.71`高于6月初`96.55`",
            "涨幅温和，价格没有给出强趋势确认；相对AI主链、光互联、核能/电力高beta标的动量偏弱",
        ),
        "激进短线": (
            "Call/Put IV约`60%`、DCS高速I/O/CXL叙事和FY2027 Q1兑现可支持事件交易",
            "公司市值约`556亿美元`且DCS占比仍有限，短线爆发力弱于小基数光互联、NeoCloud、内存和核能开发标的",
        ),
    }

    out: list[str] = []
    out += [
        "# MCHP 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：MCHP / Microchip Technology",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 MCHP vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。MCHP 正式评估中的增速区间含 `+23%-34%` 一类写法，通用解析器会误读为负值，因此本脚本按正式评估中的 FY2027 Q1 指引、DCS 目标、利润率、FCF、估值和价格数据对目标公司做专门档位校准。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。MCHP 的强项是 FY2027 Q1 指引、库存正常化、传统 MCU/Analog 修复、DCS CY2026 目标、Non-GAAP 利润率恢复和 FCF 回补，而不是纯 AI 高 beta。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 DCS 客户/backlog/份额未披露，P/S 和 EV/EBITDA 不低，IV约60%，SOXX压力窗口历史回撤大，价格确认只有温和修复。",
        "- A 最适合的投资者画像：愿意买成熟 MCU/Analog 周期修复，同时保留 PCIe/CXL/storage/retimer DCS 右尾的中期基本面资金；更适合 NTM兑现和估值消化，不适合把它当AI核心算力股。",
        "- A 最不适合的投资者画像：只追求最高右尾、最强价格动量、最厚下行保护或最明确AI订单/RPO的资金。前者通常更偏 NVDA/AVGO/MRVL/ALAB/CRDO/MU/NBIS/CRWV/OKLO，后者通常更偏公用事业、云平台或低IV现金流资产。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在直接 AI 收入、订单/RPO、右尾弹性、近端催化、估值消化或压力期防守上压过 MCHP。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：MCHP 是全项目中上偏周期修复的成熟半导体标的；相对弱周期/无现金流/无收入锚公司有优势，但面对AI主链、光互联、内存、NeoCloud、电力设备和订单高确定性的公司，经常只能按思路拆分甚至让位。",
        "- 后续最重要跟踪数据：FY2027 Q1实际收入和Non-GAAP GM/OM、DCS是否继续披露并兑现CY2026约5亿美元目标、Switchtec Gen6和XpressConnect客户qualification、渠道库存天数、DOI、book-to-bill、选择性涨价接受度、FCF、普通股股息覆盖和净债务变化。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "MCHP"]),
        base.row(["公司名称", "Microchip Technology"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["scenarios"]["base"].get("NTM 公司收入", "缺失")]),  # type: ignore[index]
        base.row(["乐观/极度乐观收入", f"{a['scenarios']['bull'].get('NTM 公司收入', '缺失')} / {a['scenarios']['extreme'].get('NTM 公司收入', '缺失')}"]),  # type: ignore[index]
        base.row(["利润和现金流结论", f"{a['scenarios']['base'].get('EBITDA/净利润', '')}；{a['scenarios']['base'].get('自由现金流方向', '')}"]),  # type: ignore[index]
        base.row(["最大传导瓶颈", "DCS 从 PCIe/CXL/AI rack 需求转成可确认收入需要客户平台认证、量产排产、CXL软件互操作和在Astera/Broadcom/Marvell/NVIDIA/AMD生态中的份额稳定。"]),
        base.row(["最大反证", "Q1 FY2027指引兑现后Q2/Q3订单转弱；DCS无法兑现CY2026约5亿美元；CXL/PCIe Gen6认证延迟；通用MCU/Analog价格下行；FCF无法覆盖股息和去杠杆。"]),
        base.row(["近端催化剂", "FY2027 Q1实际收入和Non-GAAP GM/OM、DCS收入披露、Switchtec Gen6/XpressConnect qualification、渠道库存、book-to-bill、选择性涨价、FCF和净债务。"]),
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
        base.row(["直接同业", "与MCHP在MCU、模拟/电源/接口、车规/工业半导体、高速I/O、PCIe/CXL/retimer/storage controller或数据中心控制面有产品、客户或需求池重叠。", "ADI、TXN、ON、STM、IFNNY、MPWR、ALAB、MRVL、AVGO、MXL、SMTC、MTSI、RMBS", "优先看同一需求池中的收入兑现、客户认证、产品代际、毛利率、DCS/高速I/O份额和同业估值消化。"]),
        base.row(["相邻替代", "同属AI半导体或AI基础设施资金篮子，但不是直接替代；资金可能在成熟半导体周期修复与AI主链/电力设备之间二选一。", "NVDA、AMD、ARM、QCOM、ETN、VRT、GEV、POWL、HUBB、APLD、CRWV", "默认按档位判断；只有增长质量、订单可见度、估值消化或风险收益明显拉开时才给建议级结论。"]),
        base.row(["上下游", "云厂、服务器、网络、存储、晶圆制造、封测、材料、设备等处在MCHP DCS、MCU/Analog或制造供给链的需求端或供给端。", "MSFT、AMZN、GOOGL、DELL、SMCI、ANET、CRDO、TSM、ASML、AMAT、TER", "不把下游AI capex或上游设备订单直接等同于MCHP收入，重点看利润池位置、议价权、订单/RPO和收入确认链条。"]),
        base.row(["跨赛道", "软件、材料、医疗工具、普通工业、化工和业务差异较大的公司，仍作为项目资金配置替代比较。", "ADBE、TMO、DHR、ECL、LIN、CAT、RKLB", "默认降低结论力度；若证据互有强弱，优先中性或微倾向。"]),
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
                    "MCHP" if comparison["final"] == "A" else b["ticker"],
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
        need = "需要 MCHP 披露更清晰的 DCS 客户/平台/backlog、Q2/Q3订单延续、DCS收入继续高增，并证明MCU/Analog修复能转成FCF。"
        if comparison["rel"] == "直接同业":
            need = "需要 MCHP 在同业中证明PCIe/CXL/retimer、MCU/Analog或电源/接口产品份额、毛利和估值消化强于对手。"
        elif comparison["rel"] == "上下游":
            need = "需要 MCHP 证明下游AI capex能持续转成自己的DCS和控制/模拟收入，而不是停留在系统或客户预算层。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 MCHP 用更强增长、现金流或估值消化抵消跨赛道标的的订单、防守或右尾优势。"
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
        need = "需要 B 提供更硬订单/RPO、更强NTM收入利润兑现，或证明估值/现金流反证低于 MCHP。"
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
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/AI计算芯片_EDA_IP_custom_ASIC/MCHP_Microchip_Technology_公司调研_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_PCIe_CXL高速IO交换与Retimer_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_CXL内存扩展与内存池化_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_服务器BMC、MCU与嵌入式控制_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_mchp_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对 MCHP 的增速解析、DCS目标、利润率、FCF、估值、压力窗口和IV做专门档位校准；未读取下游量化目录或现成排序结论。",
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
        "mchp_tiers": companies[TARGET]["tiers"],
        "mchp_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
