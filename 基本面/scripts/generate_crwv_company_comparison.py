from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import generate_alle_company_comparison as base
import generate_crwd_company_comparison as range_fix


TARGET = "CRWV"
TARGET_NAME = "CoreWeave"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "CRWV_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL

DIRECT_PEERS = {"AMZN", "MSFT", "GOOGL", "ORCL", "BABA", "NBIS", "APLD", "IREN"}
ADJACENT_PEERS = {"EQIX", "DLR", "IBM", "HPE", "NTNX", "PSTG", "CRWD", "ADBE"}
UPSTREAM_OR_CUSTOMER_CATS = {
    "AI服务器_存储_EMS",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "电力_发电_能源_储能",
    "机电_冷却_工程_水处理_边缘工业AI",
    "配电_电源_功率器件",
}
DISTANT_UPSTREAM_CATS = {
    "晶圆制造_前道设备",
    "封测_检测_计量_光罩",
    "半导体材料_化学品_基板",
}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    range_fix.fix_growth_ranges(companies)
    base.score_companies(companies)
    a = companies[TARGET]
    overrides = {
        # Manual calibration from the CRWV formal evaluation:
        # massive backlog/RPO and growth, but heavy CapEx, negative EPS/FCF,
        # high IV, high leverage, customer concentration, and poor pressure-window evidence.
        "NTM兑现优先": 92.0,
        "右尾弹性优先": 100.0,
        "风险调整收益": 56.0,
        "下行保护优先": 35.0,
        "估值消化优先": 63.0,
        "近端催化优先": 86.0,
        "价格确认/动量": 60.0,
        "激进短线": 100.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]
    range_fix.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in {"META", "NVDA", "AMD", "AVGO", "DELL", "SMCI", "PENG", "ANET", "VRT", "ETN", "CEG", "VST"}:
        return "上下游"
    if ticker in ADJACENT_PEERS or category == "云算力_IDC_AI软件平台":
        return "相邻替代"
    if category in UPSTREAM_OR_CUSTOMER_CATS:
        return "上下游"
    if category in DISTANT_UPSTREAM_CATS:
        return "跨赛道"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的backlog/RPO和指引更硬",
            "右尾弹性优先": "A的NeoCloud右尾更大",
            "风险调整收益": "A上行弹性可覆盖部分风险",
            "下行保护优先": "A合同可见度略强",
            "估值消化优先": "A高增速可消化部分P/S",
            "近端催化优先": "A有Q2/H2上电和Rubin节点",
            "价格确认/动量": "A近端AI云关注度更强",
            "激进短线": "A高IV和AI云叙事更进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B兑现更稳或利润留存更好",
            "右尾弹性优先": "B右尾更大或A执行链更重",
            "风险调整收益": "B估值/现金流组合更好",
            "下行保护优先": "B现金流和资产负债表更稳",
            "估值消化优先": "B利润和倍数更易消化",
            "近端催化优先": "B近端订单/产品催化更直接",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B短线资金偏好更高",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "成长与估值/防守互抵"
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
        + a["scores"]["近端催化优先"]
        + a["scores"]["风险调整收益"]
        - b["scores"]["NTM兑现优先"]
        - b["scores"]["右尾弹性优先"]
        - b["scores"]["近端催化优先"]
        - b["scores"]["风险调整收益"]
    )
    return "A" if key_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
            return "CRWV 的backlog/RPO、FY2026指引和客户合同让收入兑现更硬。"
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
            return "CRWV 的NeoCloud、AI factory和Rubin期权给出更大右尾。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 10:  # type: ignore[index,operator]
            return "CRWV 的Q2/H2收入、active power、客户上线和Rubin验证窗口更近。"
        return "CRWV 在增长、催化和短线弹性组合上略胜，但仍需盯紧现金流。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、资产负债表或压力期表现明显优于 CRWV。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 16:  # type: ignore[index,operator]
        return f"{b['ticker']} 的利润留存和估值消化压力明显小于 CRWV。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的上行/下行组合比 CRWV 的高杠杆模式更均衡。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和资金偏好强于 CRWV。"
    return f"{b['ticker']} 在多数投资思路下比 CRWV 更符合当前配置目标。"


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
        key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["下行保护优先"] - a["scores"]["下行保护优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            x["ac"] - x["bc"],
            a["scores"]["NTM兑现优先"] + a["scores"]["右尾弹性优先"] + a["scores"]["近端催化优先"] - x["b"]["scores"]["NTM兑现优先"] - x["b"]["scores"]["右尾弹性优先"] - x["b"]["scores"]["近端催化优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:45]  # type: ignore[operator]
    if not strong_b_rows:
        strong_b_rows = [x for x in strong_b if x["final"] == "B" and x["bc"] > x["ac"]][:45]  # type: ignore[operator]
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
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}，其中可用两段为 {fmt_pct(soxx.get('soxx2'))} / {fmt_pct(soxx.get('soxx3'))}。"
    )
    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "Q1收入`20.78亿美元`、FY2026收入指引`120-130亿美元`、backlog`994亿美元`、RPO`988亿美元`、active power`1GW+`",
            "收入确认仍依赖上电、GPU/rack到货、液冷/网络调试、客户验收和H2 ramp",
        ),
        "右尾弹性优先": (
            "基准NTM收入`150-180亿美元`、乐观`190-230亿美元`、极度乐观`240-300亿美元`，且有Rubin/推理/软件控制面期权",
            "极度乐观已被评估下移为乐观上沿，需多客户Rubin生产化和融资成本改善",
        ),
        "风险调整收益": (
            "客户合同、RPO/backlog和AI容量稀缺性给出大上行；P/S低于部分纯半导体高估值标的",
            "负EPS、负FCF、FY2026 CapEx`310-350亿美元`、高票息债和客户集中使风险调整只能中档",
        ),
        "下行保护优先": (
            "长期合同和客户预付款提供一定底部，Q1 OCF为正",
            "2026-06-04可用SOXX压力窗口为`-29.45%`/`-50.54%`，资产负债表高杠杆、净亏损和高IV使防守性很弱",
        ),
        "估值消化优先": (
            "2026-06-22 P/S`9.75`配合`+141%-189%`基准增速，收入层面有消化能力",
            "Forward PE缺失且forward EPS为负，EBITDA强不等于净利润/FCF，折旧利息会吞噬消化速度",
        ),
        "近端催化优先": (
            "Q2收入指引、H2上电、24个月backlog确认比例、Meta/Anthropic/Jane Street上线和Rubin验证都在1-2季可跟踪",
            "任何电力、变压器、液冷、网络、融资或客户验收延迟都会把催化推后",
        ),
        "价格确认/动量": (
            "2026-06-03两周上涨`+9.53%`，6月22日价格仍接近6月初水平，AI云关注度高",
            "过去一月`-6.79%`且SOXX压力窗口大幅回撤，价格确认不如AI服务器、存储和部分芯片/电力强势股",
        ),
        "激进短线": (
            "Call IV`88.4%`、纯AI云/NeoCloud标签、Rubin/客户合同/上电节点提供强事件弹性",
            "高波动来自真实融资和交付风险，不适合把短线弹性误读为下行保护",
        ),
    }

    out: list[str] = []
    out += [
        "# CRWV 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：CRWV / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 CRWV vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。CRWV 的优势集中在`994亿美元` backlog、`988亿美元` RPO、FY2026 指引、Meta/Anthropic/Jane Street 等客户合同、Rubin/GB300/推理右尾和高 IV 短线弹性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是负 EPS/Forward EPS、基准仍显著负 FCF、FY2026 CapEx `310-350亿美元`、高票息债、客户集中和压力窗口回撤大。",
        "- A 最适合的投资者画像：愿意承受高杠杆、高波动和交付风险，押注 AI 云容量稀缺、客户长约兑现、Rubin/推理放量和近端上电节点的进攻型资金。",
        "- A 最不适合的投资者画像：优先买低估值、可持续 FCF、压力期稳健、低 IV 或资产负债表强防守的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在现金流、防守质量、价格确认、利润留存或更低估值上压过 CRWV。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：CRWV 是项目内增长弹性和近端催化最突出的 AI 云容量标的之一，但不是风险调整、下行保护或利润/FCF 质量最好的公司；总体属于“高增长高风险的AI基础设施进攻核心”，而非稳健复利资产。",
        "- 后续最重要跟踪数据：季度收入、RPO/backlog、24个月内backlog确认比例、active power、contracted power、CapEx、interest expense、adjusted operating income margin、D&A、customer concentration、new customer commitments、GPU/reserved/spot pricing、Rubin production deployment、inference utilization、deferred revenue、OCF/FCF 和 data center delivery milestones。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "CRWV"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`150-180亿美元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}，但极度乐观在正式评估中下移为乐观上沿/跟踪"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "`backlog/RPO -> active power -> GPU/rack到货 -> 液冷/网络/电力调试 -> 客户验收 -> 收入确认`，需求不是唯一瓶颈。"]),
        base.row(["最大反证", "FY2026 CapEx`310-350亿美元`、负FCF、负EPS/Forward EPS、高票息债、客户集中、GPU残值/租价和SOXX压力窗口大回撤。"]),
        base.row(["近端催化剂", "Q2收入`24.5-26.0亿美元`、H2收入ramp、active power提升、24个月backlog确认比例、Meta/Anthropic/Jane Street上线、GB300/Rubin early deployment、融资成本变化。"]),
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
        base.row(["直接同业", "与 CRWV 在 AI 云、NeoCloud、AI factory、公有云/专用 GPU 容量或训练/推理云服务需求池中重叠，优先比较 RPO/backlog、active power、客户质量、融资成本、利用率和估值。", "AMZN、MSFT、GOOGL、ORCL、BABA、NBIS、APLD、IREN", "同业证据权重最高；若对手有更低资本成本或更稳利润，CRWV的增长优势需要被折扣。"]),
        base.row(["相邻替代", "同属云平台、IDC、数据平台、企业软件或 AI 软件/基础设施资金篮子，但收入模式不完全重叠。", "EQIX、DLR、IBM、HPE、NTNX、PSTG、CRWD、ADBE", "重点回答资金只能买一个时，谁的增长质量、估值消化和风险调整收益更好。"]),
        base.row(["上下游", "B 是 GPU/ASIC、服务器、网络、存储、电力、配电、液冷、MEP、客户侧 AI 需求或数据中心物理供给链，影响 CRWV 的收入兑现和利润池。", "NVDA、AMD、AVGO、DELL、SMCI、ANET、VRT、ETN、CEG、META", "区分上游利润捕获和CRWV服务收入，不把下游CapEx或上游芯片收入机械等同CRWV机会。"]),
        base.row(["跨赛道", "半导体材料、前道设备、封测、工业、化学品等与CRWV业务差异较大的标的，只作为资金配置替代。", "ASML、AMAT、LIN、TMO、RKLB、ALLE", "默认降低结论力度；除非增长质量、估值消化或防守性明显拉开，否则使用中性或微倾向。"]),
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
        need = "需要 CRWV 把backlog/RPO连续转成收入、经营利润和FCF，并降低客户集中、融资成本和交付延迟反证。"
        if "下行保护优先" in wins or "风险调整收益" in wins:
            need = "需要 CRWV 证明资产负债表、利息覆盖、OCF/FCF和压力期股价韧性已经改善。"
        if "估值消化优先" in wins:
            need = "需要 CRWV 证明P/S能由可持续经营利润和FCF消化，而不只是收入高增。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供同等硬度的订单/RPO、收入高增、近端催化或更强AI主链右尾，并避免估值或现金流反证扩大。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "需要 B 证明防守优势之外还有足够增长或近端重定价，不只是低风险低弹性。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖情况见金融资料；本次公司全集中缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/云算力_IDC_AI软件平台/CRWV_CoreWeave_公司调研_2026-06-11.md`、`行业调研/产业背景/全球AI需求与Token经济框架_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/产业背景/AI产业链瓶颈与反证指标总表_2026-06-10.md`、`行业调研/产业背景/AI产业链全局图谱与口径字典_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI云算力外包和NeoCloud与AI数据中心运营商_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 外部 sanity check：运行中对 CRWV 公开行情和 CoreWeave 官方新闻做了网页核对；主表不使用外部网页排序、券商评级或目标价。参考页：CoreWeave IR news <https://investors.coreweave.com/news/default.aspx>；CoreWeave stock info <https://investors.coreweave.com/stock-info/default.aspx>；MarketWatch CRWV quote <https://www.marketwatch.com/investing/stock/crwv>。",
        "- 自动化脚本：`scripts/generate_crwv_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+141%-189%` 做同号区间修正；对 CRWV 的 backlog/RPO、CapEx/负FCF、高IV、高杠杆、客户集中、SOXX压力窗口回撤和 Rubin/客户合同近端催化做人工校准后建档；未读取下游量化目录、备份、临时目录或现成排序结论。",
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
                "crwv_tiers": companies[TARGET]["tiers"],
                "crwv_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
