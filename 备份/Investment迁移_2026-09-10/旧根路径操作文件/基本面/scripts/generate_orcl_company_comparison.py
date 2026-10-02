from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base
import generate_amzn_company_comparison as cloud_helper


TARGET = "ORCL"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ORCL_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL

DIRECT_PEERS = {"AMZN", "MSFT", "GOOGL", "BABA", "IBM", "CRWV", "NBIS", "APLD", "IREN"}
ADJACENT_PEERS = {"META", "ADBE", "CRWD", "NTNX", "EQIX", "DLR"}
UPSTREAM_CATS = {
    "AI服务器_存储_EMS",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "电力_发电_能源_储能",
    "机电_冷却_工程_水处理_边缘工业AI",
    "配电_电源_功率器件",
    "晶圆制造_前道设备",
    "封测_检测_计量_光罩",
    "半导体材料_化学品_基板",
}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    cloud_helper.fix_growth_ranges(companies)
    base.score_companies(companies)
    a = companies[TARGET]

    # ORCL is now a high-growth OCI/AI infrastructure story with unusually hard
    # RPO and FY2027 revenue anchors, but it is not a clean software cash-flow
    # compounder while AI data center capex and customer concentration dominate
    # free cash flow and downside protection.
    overrides = {
        "NTM兑现优先": 92.0,
        "右尾弹性优先": 92.0,
        "风险调整收益": 64.0,
        "下行保护优先": 60.0,
        "估值消化优先": 80.0,
        "近端催化优先": 81.0,
        "价格确认/动量": 52.0,
        "激进短线": 84.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]
    cloud_helper.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in ADJACENT_PEERS or category == "云算力_IDC_AI软件平台":
        return "相邻替代"
    if category in UPSTREAM_CATS:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的FY2027指引和RPO兑现锚更硬",
            "右尾弹性优先": "A有OCI/GW交付和Stargate右尾",
            "风险调整收益": "A高增速与Forward PE组合较优",
            "下行保护优先": "A有软件support和大客户RPO底座",
            "估值消化优先": "A约16倍Forward PE可被NTM高增消化",
            "近端催化优先": "A的Q1云增速/RPO/交付GW节点近",
            "价格确认/动量": "A的AI云关注度仍有交易确认",
            "激进短线": "A的OCI、RPO和Stargate叙事可进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/订单兑现更清楚",
            "右尾弹性优先": "B小基数或硬件右尾更大",
            "风险调整收益": "B上行下行组合更优",
            "下行保护优先": "B现金流、估值或压力期更稳",
            "估值消化优先": "B业绩增速更能覆盖估值",
            "近端催化优先": "B订单/产品/财报催化更强",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B短线波动和资金偏好更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"价格确认/动量", "激进短线"}:
        return "动量或短线弹性接近"
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
        + a["scores"]["估值消化优先"]
        - b["scores"]["NTM兑现优先"]
        - b["scores"]["风险调整收益"]
        - b["scores"]["估值消化优先"]
    )
    return "A" if key_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    ticker = str(b["ticker"])
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
            return "ORCL的FY2027收入指引、6380亿美元RPO和OCI交付路径更清楚。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
            return "ORCL约16倍Forward PE配合NTM高增速，估值消化更有支撑。"
        if a["scores"]["近端催化优先"] - b["scores"]["近端催化优先"] > 12:  # type: ignore[index,operator]
            return "ORCL的Q1 FY2027云收入、RPO顺序变化和交付GW是更近的重定价节点。"
        return "ORCL在OCI收入兑现、右尾和估值消化的组合上略胜。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{ticker}现金流、估值缓冲或压力期表现强于ORCL。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 18:  # type: ignore[index,operator]
        return f"{ticker}价格趋势和资金确认明显强于ORCL。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 16:  # type: ignore[index,operator]
        return f"{ticker}小基数、订单或硬件右尾比ORCL更大。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 12:  # type: ignore[index,operator]
        return f"{ticker}的增长、估值和下行组合优于ORCL。"
    return f"{ticker}在多数投资思路下比ORCL更符合当前配置目标。"


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
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return sorted(output, key=lambda x: (rel_order.get(str(x["rel"]), 9), str(x["b"]["category"]), str(x["ticker"])))  # type: ignore[index]


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
    strong_b_rows = [
        x for x in sorted(comparisons, key=lambda x: (x["bc"] - x["ac"], x["bc"]), reverse=True)  # type: ignore[operator]
        if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3  # type: ignore[operator]
    ][:45]
    strong_a_rows = [
        x for x in sorted(comparisons, key=lambda x: (x["ac"] - x["bc"], x["ac"]), reverse=True)  # type: ignore[operator]
        if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3  # type: ignore[operator]
    ][:45]
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
    for product in a["products"][:7]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    support = {
        "NTM兑现优先": (
            "FY2027收入指引900亿美元、RPO 6380亿美元、Q1 FY2027收入+27-29%且cloud +58-64%，OCI/IaaS是明确收入主通道",
            "RPO不能线性转收入，仍受已上电MW、GPU/rack/液冷/网络验收、客户使用和revenue recognition限制",
        ),
        "右尾弹性优先": (
            "乐观/极度乐观收入960-1050亿/1080-1220亿美元，Stargate、OCI GPU Supercluster、Database@Hyperscaler和客户预付形成大右尾",
            "极度乐观需要5GW+交付、多客户扩散、OCI margin改善和融资顺利同时成立，可信度低于收入基准",
        ),
        "风险调整收益": (
            "Forward PE约16.04，NTM收入+31-37%，软件support现金牛与OCI高增长形成较高赔率",
            "FY2026 FCF -237亿美元，资本开支、折旧、融资成本和客户集中削弱下行边界",
        ),
        "下行保护优先": (
            "Software support/license、Cloud Applications SaaS和数据库锁定提供利润底座，客户预付/供硬件缓解部分现金压力",
            "SOXX压力窗口累计-58.88%，OCI资本强度和自由现金流为负使防守属性弱于公用事业、现金牛软件和低估值工业",
        ),
        "估值消化优先": (
            "16倍左右Forward PE与FY2027 900亿美元收入、non-GAAP EPS 8.05美元指引匹配，若OCI兑现可较快消化估值",
            "估值消化依赖Q1/Q2云收入、RPO转收入和OCI margin验证；若capex同步上修，FCF仍难同步改善",
        ),
        "近端催化优先": (
            "FY2027 Q1 cloud/IaaS、RPO顺序变化、新AI contracts、交付MW/GW、GPU utilization和OCI margin均是1-2季关键节点",
            "大部分催化仍要转成上电、验收、收入确认和毛利率，不是单一公告即可闭环",
        ),
        "价格确认/动量": (
            "2026-06-03前两周+22.41%、一月+34.05%，说明FY2026 Q4/RPO主题曾有强价格确认",
            "2026-06-22价格175.07美元显著低于2026-06-03的230.33美元，最新价格确认已弱化，不能给高档",
        ),
        "激进短线": (
            "Call IV 53.6%，OCI/RPO/Stargate/OpenAI credits和FY2027 Q1验证仍具进攻交易性",
            "大市值、近期回落、FCF为负和OCI交付反证限制短线强度，弱于高IV小盘、光互联、NeoCloud和电力链",
        ),
    }

    out: list[str] = [
        "# ORCL 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：ORCL / Oracle Corporation",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 ORCL vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ORCL 的优势集中在FY2027收入指引、RPO、OCI交付链和估值消化；近端催化尤其依赖Q1 FY2027 cloud/IaaS、RPO顺序变化和交付GW。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是FCF仍为负、AI data center资本强度高、客户集中、SOXX压力窗口表现弱和最新价格从高位回落。",
        "- A 最适合的投资者画像：愿意押注OCI从软件公司转向AI基础设施运营商、重视RPO到收入兑现和估值消化的中高风险配置者。",
        "- A 最不适合的投资者画像：只追求低波动下行保护、稳定FCF、最强短线动量或小市值右尾弹性的投资者。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]]) or '无明显集中反方'}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：ORCL 对 {sum(1 for x in comparisons if x['final'] == 'A')}/{n - 1} 家公司多数思路占优，对 {sum(1 for x in comparisons if x['final'] == 'B')}/{n - 1} 家公司多数思路落后；它是全项目AI云/OCI兑现和估值消化的强势标的，但不是最强防守、最强价格确认或最高小基数右尾资产。",
        "- 后续最重要跟踪数据：FY2027 Q1 revenue/cloud/IaaS、RPO顺序变化、新签AI contracts客户分散度、交付MW/GW、客户预付/客户供硬件余额、GPU renewal/utilization、OCI margin、capex/net cash outlay、Multicloud AI Database增速、Universal Credits真实usage。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ORCL"]),
        base.row(["公司名称", "Oracle Corporation"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "$88-92B"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润：{a['base_profit']}；现金流：{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "不是需求，而是RPO -> 已上电MW -> GPU/rack/液冷/网络验收 -> 客户使用 -> revenue recognition的交付链。"]),
        base.row(["最大反证", "FY2027 Q1 cloud growth低于50%、RPO顺序停滞、GPU utilization跌破80%、关键站点延至2028、OCI gross margin或FCF显著低于可接受路径。"]),
        base.row(["近端催化剂", "FY2027 Q1 revenue/cloud/IaaS、RPO顺序变化、新AI contracts、交付MW/GW、客户预付/供硬件余额、GPU utilization、OCI margin和capex。"]),
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
        base.row(["直接同业", "与ORCL在云基础设施、AI云、NeoCloud、企业云资源或数据库/AI平台预算中高度重叠，优先比较OCI/AWS/Azure/GCP/NeoCloud收入、RPO/backlog、客户质量、利润率、资本强度和同业估值消化。", "AMZN、MSFT、GOOGL、BABA、IBM、CRWV、NBIS、APLD、IREN", "同档或相邻档时，RPO、云收入、客户集中、capex/FCF和同业估值证据可放大到建议级别。"]),
        base.row(["相邻替代", "不完全同业，但同属AI平台、企业软件、安全、IDC/REIT或云资源配置替代。", "META、ADBE、CRWD、NTNX、EQIX、DLR", "默认看增长质量、估值消化、近端催化和风险调整，不只看业务热度。"]),
        base.row(["上下游", "B是ORCL OCI AI data center建设和云收入链条中的芯片、服务器、网络、电力、冷却、配电、晶圆、材料、封测或工程供应商。", "NVDA、AMD、AVGO、TSM、MU、SMCI、ANET、VRT、ETN、CEG、PWR", "不把ORCL下游收入规模或上游瓶颈稀缺自动等同胜出；关键看利润捕获、交付瓶颈、估值消化和现金流。"]),
        base.row(["跨赛道", "业务差异较大，只作为资金配置替代比较。", "RKLB、TSLA、部分材料/工业/医疗仪器公司", "结论力度最保守；除非增长质量、估值消化或风险调整明显拉开，否则使用中性或微倾向。"]),
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
        need = "需要ORCL证明RPO能高质量转收入、OCI margin改善、FCF压力下降，并重新获得价格确认。"
        if comparison["rel"] == "上下游":
            need = "需要ORCL证明下游AI云利润捕获强于上游硬件/电力订单弹性，并让capex不吞噬FCF。"
        if "下行保护优先" in wins:
            need = "需要ORCL把客户预付、数据库support和OCI利用率转成更清楚的FCF与资产负债表缓冲。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B提供更硬的NTM订单/收入、利润质量、估值消化和近端价格确认。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要B把右尾叙事转成可确认收入、利润和现金流，并降低估值或执行反证。"
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
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/云算力_IDC_AI软件平台/ORCL_Oracle Corporation_公司调研_2026-06-20.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI云算力外包和NeoCloud与AI数据中心运营商_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI集群调度与推理运行时_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_orcl_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对百分比区间如 `+31%-37%` 做同号区间修正，并对ORCL的OCI/RPO/FY2027指引、FCF压力、估值消化、下行保护和价格确认做公司专属校准后建档；未读取下游量化目录或现成排序结论。",
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
                "orcl_tiers": companies[TARGET]["tiers"],
                "orcl_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
