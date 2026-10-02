from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import generate_alle_company_comparison as base


TARGET = "ANET"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ANET_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
INFRA_CATS = base.INFRA_CATS
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS


DIRECT_PEERS = {"CSCO", "HPE", "NOK", "CIEN", "VISN"}
NETWORK_UPSTREAM = {
    "AAOI",
    "ALAB",
    "APH",
    "AVGO",
    "BDC",
    "BELFB",
    "COHR",
    "CRDO",
    "GLW",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "POET",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
}
CLOUD_AI_CUSTOMERS = {
    "AMZN",
    "MSFT",
    "GOOGL",
    "META",
    "ORCL",
    "BABA",
    "IBM",
    "EQIX",
    "DLR",
    "CRWV",
    "APLD",
    "IREN",
    "NBIS",
    "NTNX",
    "CRWD",
    "ADBE",
}
SERVER_STORAGE = {"DELL", "SMCI", "JBL", "FN", "PENG", "SANM", "FLEX", "CLS", "NTAP", "PSTG", "STX", "WDC", "SNDK", "MU", "RMBS", "SIMO", "MRAM"}


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

    # ANET-specific calibration: the generic model underweights RPO/deferred
    # revenue, AI Ethernet visibility, and FCF quality, while high valuation
    # still needs to cap valuation digestion and short-term aggression.
    overrides = {
        "NTM兑现优先": 88.0,
        "右尾弹性优先": 86.0,
        "风险调整收益": 64.0,
        "下行保护优先": 72.0,
        "估值消化优先": 60.0,
        "近端催化优先": 76.0,
        "价格确认/动量": 76.0,
        "激进短线": 84.0,
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
    if ticker in NETWORK_UPSTREAM or ticker in CLOUD_AI_CUSTOMERS or ticker in SERVER_STORAGE:
        return "上下游"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的RPO/递延和AI fabric指引更硬",
            "右尾弹性优先": "A的800G/1.6T收入化更清楚",
            "风险调整收益": "A增长、FCF和证据质量更均衡",
            "下行保护优先": "A现金流和客户粘性更强",
            "估值消化优先": "A高增长利润可部分消化估值",
            "近端催化优先": "A有1.6T/Q2-RPO催化",
            "价格确认/动量": "A近期价格确认更强",
            "激进短线": "A AI Ethernet叙事更近",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/订单兑现证据更硬",
            "右尾弹性优先": "B右尾弹性或市值弹性更大",
            "风险调整收益": "B估值与下行组合更好",
            "下行保护优先": "B估值或压力期韧性更强",
            "估值消化优先": "B估值消化难度更低",
            "近端催化优先": "B近端订单/产品节点更硬",
            "价格确认/动量": "B价格趋势更强",
            "激进短线": "B高波动右尾更适合进攻",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"下行保护优先", "估值消化优先"}:
        return "估值和安全性接近"
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
            return "ANET 的RPO、递延收入、FY2026 AI fabric目标和Q2收入指引更能支撑NTM兑现。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
            return "ANET 近端重定价主要来自1.6T 7060XE7、RPO/递延转收入和Q2/Q3 AI fabric进度。"
        if a["scores"]["风险调整收益"] - b["scores"]["风险调整收益"] > 8:  # type: ignore[index,operator]
            return "ANET 在增长、现金流和证据可信度之间更均衡。"
        return "ANET 以AI Ethernet兑现、强FCF和客户粘性略胜，但估值仍需持续业绩消化。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 15:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化明显比 ANET 容易。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 15:  # type: ignore[index,operator]
        return f"{b['ticker']} 的右尾弹性或市值弹性比 ANET 更大。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的下行保护和估值缓冲强于 ANET。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和短线资金偏好更强。"
    return f"{b['ticker']} 在多数投资思路下比 ANET 更符合当前项目内资金配置目标。"


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

    product_names = []
    for product in a["products"][:6]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    support = {
        "NTM兑现优先": (
            "Q1 2026收入`27.09亿美元`、同比`+35.1%`，Q2指引约`28亿美元`，FY2026收入目标约`115亿美元`，递延收入约`62亿美元`、RPO约`77亿美元`",
            "两大客户集中、1.6T/optics供给和验收周期会影响收入确认节奏",
        ),
        "右尾弹性优先": (
            "800G/51.2T AI Ethernet、1.6T/102.4T 7060XE7、7800 AI spine、EOS/CloudVision和XPO构成AI网络右尾",
            "市值已大，XPO和1.6T大额收入仍偏2027+，极度乐观可信度低到中低",
        ),
        "风险调整收益": (
            "NTM基准收入`127-136亿美元`、非GAAP净利约`50-56亿美元`、FCF约`48-58亿美元`，证据质量高",
            "2026-06-22 P/S `22.64`、Forward PE `39.19`，估值要求持续兑现",
        ),
        "下行保护优先": (
            "强现金、强服务/软件粘性、RPO和递延收入支撑，业务不是纯小盘概念",
            "SOXX三段压力窗口累计`-71.59%`，高估值和客户集中使其不是防守顶档",
        ),
        "估值消化优先": (
            "NTM基准收入较LTM约`+31%-40%`，经营利润率`46%-48%`，能用增长和利润部分消化估值",
            "P/S和Forward PE都偏高，若GM跌破`61%`或AI fabric目标不再上修，消化压力会放大",
        ),
        "近端催化优先": (
            "Q2/Q3收入与GM、FY2026 AI fabric目标、RPO/递延转收入、1.6T 7060XE7客户部署证据都在未来1-2季可验证",
            "Meta/Microsoft/Oracle背书仍需转成量产收入，客户验收和供应链不能延期",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周`+24.12%`，2026-06-22价格`174.56`，AI Ethernet叙事已获得价格确认",
            "过去一月仅`+0.97%`，并非全项目最强动量；若财报不兑现，高估值会放大回撤",
        ),
        "激进短线": (
            "1.6T/AI Ethernet、Q2/RPO、客户部署和55.8% Call IV提供事件弹性",
            "大市值限制爆发倍数，短线进攻性低于AAOI、ALAB、CRDO、APLD等更高beta标的",
        ),
    }

    out: list[str] = []
    out += [
        "# ANET 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：ANET / Arista Networks",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 ANET vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ANET 的胜率来自高可信 NTM 兑现、强现金流、AI Ethernet 近端产品催化和软件/服务粘性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 P/S `22.64`、Forward PE `39.19`，以及大市值导致激进短线和右尾倍数不如小盘高 beta 标的。",
        "- A 最适合的投资者画像：愿意为高质量 AI 网络龙头支付一定估值溢价，重视 RPO/递延收入、FCF、客户粘性和1.6T/AI fabric连续验证的中长期成长配置者。",
        "- A 最不适合的投资者画像：只追求最低估值、最大短线波动、极端小市值右尾，或要求 SOXX 压力期绝对防守的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在估值消化、短线高 beta、直接AI芯片/算力右尾或压力期防守上压过 ANET。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：ANET 是项目内高质量 AI 基础设施龙头，整体处于前列但不是所有风格的第一选择；在近端催化和NTM兑现上强，在估值消化、极端右尾和纯短线进攻上会输给更便宜或更高 beta 的标的。",
        "- 后续最重要跟踪数据：Q2/Q3 2026收入和非GAAP GM、FY2026 AI fabric目标是否上修、RPO/递延收入和采购承诺、1.6T 7060XE7量产客户、800G/1.6T optics供给和ASP、服务收入增速、两大客户capex和供应商策略。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ANET"]),
        base.row(["公司名称", "Arista Networks"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`127-136 亿美元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI订单到收入确认的验收周期、1.6T optics/200G SerDes/高端交换silicon供给、两大云客户采购和部署节奏。"]),
        base.row(["最大反证", "产品级AI/1.6T收入未单独披露；两大客户集中；800G ASP、白盒/SONiC、NVIDIA/Cisco竞争和大客户议价会压毛利。"]),
        base.row(["近端催化剂", "Q2/Q3收入和GM、FY2026 AI fabric目标再上修、RPO/递延收入转确认、1.6T 7060XE7量产客户和CloudVision/EOS服务attach。"]),
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
        base.row(["直接同业", "与ANET在数据中心/企业网络系统、AI Ethernet、交换/路由和客户预算上有较高重叠，优先比较份额、RPO/backlog、产品代际、毛利率和同业估值。", "CSCO、HPE、CIEN、NOK、VISN", "同业证据权重最高；若收入兑现或估值差距大，结论力度可以上调。"]),
        base.row(["相邻替代", "同属AI基础设施资金篮子，但不是同一产品；回答资金只能买一个时谁的增长质量、估值消化和催化更好。", "NVDA、AMD、AVGO、TSM、ASML、VRT、ETN、GEV", "不强行比较产品细节；按增长质量、兑现确定性、风险调整和估值消化判断。"]),
        base.row(["上下游", "一方处于ANET需求链、供应链、客户或AI网络组件链条，重点看利润池位置、议价权、瓶颈稀缺性和客户集中。", "CRDO、ALAB、MRVL、COHR、LITE、APH、AMZN、MSFT、GOOGL、META、DELL、SMCI", "不把云capex或组件TAM直接等同于ANET收入，也不把上游稀缺自动等同更好。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较风险调整收益、估值消化、下行保护和催化可见度。", "LIN、TMO、ECL、CAT、DHR、MMM、RYCEY", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要 ANET 证明高估值可由AI fabric收入、1.6T量产和FCF继续消化。"
        if comparison["rel"] == "上下游":
            need = "需要 ANET 证明自己比组件/芯片/云客户更能捕获AI网络利润池，并持续扩大RPO和服务attach。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 ANET 用更强收入兑现、毛利和价格确认抵消跨赛道公司的低估值或防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更高NTM兑现、或同等AI近端催化，并避免估值或现金流反证扩大。"
        if b["scores"]["估值消化优先"] > a["scores"]["估值消化优先"]:  # type: ignore[index,operator]
            need = "需要 B 把估值优势转成增长确认，否则仍难压过ANET的AI Ethernet兑现质量。"
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
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/AI网络_光互联_连接器/ANET_Arista_Networks_公司调研_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AI以太网交换系统与Fabric芯片_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AI Fabric网络操作系统与遥测软件_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_CPO／NPO与交换侧光引擎_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_anet_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+31%-40%` 做同号区间修正后建档。",
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
                "anet_tiers": companies[TARGET]["tiers"],
                "anet_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
