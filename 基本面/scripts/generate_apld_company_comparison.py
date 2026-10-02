from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "APLD"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "APLD_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {"IREN", "DLR", "EQIX"}
NEOCLOUD_ADJACENT = {"CRWV", "NBIS"}
HYPERSCALER_CUSTOMERS = {"AMZN", "MSFT", "GOOGL", "META", "ORCL", "BABA", "IBM"}
SERVER_NETWORK_UPSTREAM = {
    "AAOI",
    "ALAB",
    "ANET",
    "APH",
    "AVGO",
    "BDC",
    "BELFB",
    "COHR",
    "CRDO",
    "DELL",
    "FN",
    "FLEX",
    "GLW",
    "HPE",
    "JBL",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "NTAP",
    "PENG",
    "POET",
    "PSTG",
    "SANM",
    "SITM",
    "SMCI",
    "SMTC",
    "STX",
    "TEL",
    "VIAV",
    "WDC",
}
POWER_MEP_UPSTREAM_CATS = {
    "电力_发电_能源_储能",
    "机电_冷却_工程_水处理_边缘工业AI",
    "配电_电源_功率器件",
}
SEMI_CHAIN_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "晶圆制造_前道设备",
    "封测_检测_计量_光罩",
    "半导体材料_化学品_基板",
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

    # APLD needs manual calibration: the generic scoring correctly identifies
    # the large NTM/right-tail ramp, but over-rewards valuation digestion and
    # under-penalizes high IV, negative EPS, construction capex, and RFS risk.
    a = companies[TARGET]
    overrides = {
        "NTM兑现优先": 88.0,
        "右尾弹性优先": 100.0,
        "风险调整收益": 48.0,
        "下行保护优先": 34.0,
        "估值消化优先": 48.0,
        "近端催化优先": 78.0,
        "价格确认/动量": 79.0,
        "激进短线": 100.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in NEOCLOUD_ADJACENT or category == "云算力_IDC_AI软件平台":
        return "相邻替代"
    if ticker in HYPERSCALER_CUSTOMERS or ticker in SERVER_NETWORK_UPSTREAM:
        return "上下游"
    if category in POWER_MEP_UPSTREAM_CATS or category in SEMI_CHAIN_CATS:
        return "上下游"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A已签MW和PF1收入表更硬",
            "右尾弹性优先": "A的1.4GW/$36B右尾更大",
            "风险调整收益": "A上行和合同证据略优",
            "下行保护优先": "A长约/融资证据相对更强",
            "估值消化优先": "A收入跃迁可部分消化估值",
            "近端催化优先": "A有RFS/验收/融资节点",
            "价格确认/动量": "A价格确认和关注度更强",
            "激进短线": "A高IV和AI Factory弹性更强",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/利润兑现更稳",
            "右尾弹性优先": "B右尾证据或市值弹性更强",
            "风险调整收益": "B估值/现金流反证组合更好",
            "下行保护优先": "B低IV、现金流或压力期更稳",
            "估值消化优先": "B估值消化难度更低",
            "近端催化优先": "B近端订单/产品节点更硬",
            "价格确认/动量": "B趋势更强或未明显过热",
            "激进短线": "B短线爆发力更高",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"下行保护优先", "估值消化优先", "风险调整收益"}:
        return "上行与风险互相抵消"
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
        + a["scores"]["右尾弹性优先"]
        + a["scores"]["风险调整收益"]
        + a["scores"]["估值消化优先"]
        + a["scores"]["近端催化优先"]
        - b["scores"]["NTM兑现优先"]
        - b["scores"]["右尾弹性优先"]
        - b["scores"]["风险调整收益"]
        - b["scores"]["估值消化优先"]
        - b["scores"]["近端催化优先"]
    )
    return "A" if key_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 16:  # type: ignore[index,operator]
            return "APLD 的1.4GW已签容量和长期租约右尾更大。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
            return "APLD 的PF1/PF2租约、项目融资和收入化路径更硬。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
            return "APLD 的RFS、验收、HPC租金拆分和项目融资节点更近。"
        if a["scores"]["激进短线"] - b["scores"]["激进短线"] > 14:  # type: ignore[index,operator]
            return "APLD 的高IV、AI Factory叙事和价格关注度更适合进攻。"
        return "APLD 在合同右尾、NTM兑现和近端催化组合上略胜。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、低IV或压力期韧性明显强于 APLD。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的估值消化难度低于 APLD。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的上行/下行综合赔率更好。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 15:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和短线资金偏好强于 APLD。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的收入和利润兑现证据更稳。"
    return f"{b['ticker']} 在多数投资思路下比 APLD 更符合当前项目内配置目标。"


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
        key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["下行保护优先"] - a["scores"]["下行保护优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["右尾弹性优先"] - x["b"]["scores"]["右尾弹性优先"]),  # type: ignore[index,operator]
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

    product_names = []
    for product in a["products"][:7]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    support = {
        "NTM兑现优先": (
            "PF1 100MW已完整季度运行，PF1 400MW CoreWeave约`$11B`长约，PF2 200MW约`$5B`租约和`$2.15B`项目债支撑NTM收入化",
            "收入确认仍取决于RFS、tenant fit-out、客户验收和MEP/电气设备交付；净利润和FCF不稳",
        ),
        "右尾弹性优先": (
            "截至2026-06-08约`1.4GW` contracted critical IT load、约`2.15GW` utility power、约`$36B` 15年base-term leases，续约期权潜在约`$86B`",
            "PF3/DF2主要在NTM之后，长期合同不能直接等同短期收入；项目融资和建设执行是硬约束",
        ),
        "风险调整收益": (
            "小收入基数叠加已签MW带来高上行，PF1/PF2有收入表、租约和融资证据",
            "2026-06-22 P/S `40.46`、EV/EBITDA `1107.32`、EPS为负、Call IV `98.3%`，建设CapEx和FCF压力大",
        ),
        "下行保护优先": (
            "长约和项目融资降低需求消失风险，legacy hosting提供部分现金流",
            "SOXX三段压力窗口累计`-117.36%`、IV接近100%、无PE/FwdPE、FCF仍可能为负，压力期很脆弱",
        ),
        "估值消化优先": (
            "NTM基准收入`$700-950M`相对TTM约`$319M`有2-3倍收入跃迁，若PF1/PF2兑现可快速降低远期P/S",
            "当前价格已要求乐观兑现；基准Adj. EBITDA`$250-420M`仍难完全解释市值，任何RFS/验收延迟都会放大估值压力",
        ),
        "近端催化优先": (
            "未来1-2季可验证PF1后续150MW RFS、PF2施工/验收、HPC base rent/fit-out/power拆分、`$550M` revolver和项目债使用节奏",
            "多项大租约已经公告，新增定价需要收入表和NOI/MW确认；负面延迟同样会迅速重定价",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周`+13.13%`、过去一月`+33.26%`，2026-06-22收盘`45.20`高于6月初，价格已确认右尾叙事",
            "强动量伴随高IV和过热风险，历史压力窗口回撤大，不能当作下行保护",
        ),
        "激进短线": (
            "高IV、高关注度、AI Factory长约、CoreWeave/投资级hyperscaler叙事和RFS节点带来短线进攻弹性",
            "短线容错低；融资成本、客户验收、construction或fit-out延迟会直接打击高估值和高beta",
        ),
    }

    out: list[str] = []
    out += [
        "# APLD 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：APLD / Applied Digital",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 APLD vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。APLD 的核心优势是已签AI Factory容量、小收入基数、长约右尾、RFS/验收催化和高beta短线弹性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是高P/S、高IV、负EPS、自由现金流/建设CapEx压力，以及SOXX压力窗口回撤明显。",
        "- A 最适合的投资者画像：愿意承担高波动和建设/融资执行风险、追求AI数据中心长约右尾、NTM收入跃迁和短期事件重定价的进攻型资金。",
        "- A 最不适合的投资者画像：优先看低IV、稳定FCF、净利润、估值缓冲和压力期防守的资金；这类资金更适合成熟云、数据中心REIT、公用事业或现金流型设备公司。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在收入兑现、估值消化、风险调整、价格确认或盈利质量的组合上压过APLD。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：APLD 是项目内高右尾、高催化、高短线弹性的前排标的，但不是全能型好公司；在下行保护和估值消化优先的资金框架下明显靠后。",
        "- 后续最重要跟踪数据：PF1第二/第三150MW RFS日期、PF2施工与full-capacity进度、DF1项目融资、季度HPC Hosting base rent/fit-out/power拆分、NOI/MW、Adj. EBITDA margin、cash/restricted cash、项目债成本、completion guarantee、客户acceptance和1.7GW+ marketed power转签约率。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "APLD"]),
        base.row(["公司名称", "Applied Digital Corporation"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`$700-950M`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "已签MW转RFS、tenant fit-out、customer acceptance、base rent/NOI的交付链；电气设备、MEP、液冷可靠性、项目融资和客户验收任一环节延迟都会把合同推到远期。"]),
        base.row(["最大反证", "当前P/S约`40.46`、EV/EBITDA异常高、EPS为负、自由现金流仍受建设CapEx和项目债约束，且SOXX压力窗口累计回撤约`-117.36%`。"]),
        base.row(["近端催化剂", "PF1后续RFS/验收、PF2施工和客户接收、Q4/FY2027早期HPC rent拆分、NOI/MW、项目融资成本和新增lease/客户披露。"]),
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
        base.row(["直接同业", "同为数据中心/AI基础设施容量运营商或IDC租赁模式，优先比较已签容量、RFS、租约质量、NOI/MW、融资和估值。", "IREN、DLR、EQIX", "同业证据权重最高；若对方现金流/估值/压力期显著更好，会压低APLD的风险调整和下行保护结论。"]),
        base.row(["相邻替代", "同属云算力、NeoCloud、IDC或AI基础设施资金篮子，但收入模式不同；回答资金只能买一个时谁的增长质量和赔率更好。", "CRWV、NBIS、AMZN、MSFT、ORCL", "默认同时看右尾、收入兑现、利润质量和估值消化，避免只因AI叙事更热就胜出。"]),
        base.row(["上下游", "一方是APLD园区建设、服务器、芯片、网络、电力、配电、冷却或云客户链条上的上游/下游。", "VRT、ETN、GEV、NVDA、AVGO、SMCI、DELL、ANET", "重点看利润池和瓶颈稀缺性，不把客户GPU/服务器CapEx直接算成APLD收入。"]),
        base.row(["跨赛道", "业务差异大，但仍作为项目内资金配置替代比较增长质量、风险调整收益、估值消化和催化。", "RKLB、TSLA、TMO、CAT、MMM", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要 APLD 把PF1/PF2按期转成可验证base rent/NOI，并用现金流和估值消化抵消高IV。"
        if comparison["rel"] == "直接同业":
            need = "需要 APLD 在RFS、NOI/MW、项目融资成本和客户验收上明显优于同业，并降低FCF/估值反证。"
        elif comparison["rel"] == "上下游":
            need = "需要 APLD 证明AI Factory租金利润池比上游设备/电力/芯片端更稀缺、更可持续。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 APLD 用更硬收入兑现和现金流改善抵消跨赛道标的的防守或盈利质量优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提高NTM收入/订单兑现和近端催化强度，或证明右尾能转成可确认利润。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "需要 B 在保持防守优势的同时，拿出足够高的收入上修、订单或价格确认来压过APLD右尾。"
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
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/云算力_IDC_AI软件平台/APLD_Applied_Digital_公司调研_2026-06-12.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI云算力外包和NeoCloud与AI数据中心运营商_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心开关设备与变压器_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心土建、MEP与预制化交付_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_apld_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对APLD的高增长、高估值、高波动和建设执行风险做人工校准后建档。",
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
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "apld_tiers": companies[TARGET]["tiers"],
        "apld_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
