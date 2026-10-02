from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base
import generate_amzn_company_comparison as helper


TARGET = "MSFT"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MSFT_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL

DIRECT_PEERS = {"AMZN", "GOOGL", "ORCL", "BABA", "IBM", "CRWV", "NBIS"}
ADJACENT_PEERS = {"META", "ADBE", "CRWD", "NTNX", "APLD", "IREN", "EQIX", "DLR"}
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
    helper.fix_growth_ranges(companies)
    base.score_companies(companies)
    a = companies[TARGET]

    # MSFT is a high-confidence Azure + enterprise SaaS platform. The overrides
    # intentionally keep it top-tier in NTM, downside protection, valuation
    # digestion, and risk-adjusted return, while not treating Copilot, Maia, or
    # long-dated capacity projects as small-cap-like right-tail or momentum.
    overrides = {
        "NTM兑现优先": 84.0,
        "右尾弹性优先": 72.0,
        "风险调整收益": 74.0,
        "下行保护优先": 80.0,
        "估值消化优先": 82.0,
        "近端催化优先": 74.0,
        "价格确认/动量": 42.0,
        "激进短线": 66.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]
    helper.recompute_tiers(companies)


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
            "NTM兑现优先": "A的Azure/RPO/M365兑现更硬",
            "右尾弹性优先": "A有Azure/Copilot/GitHub右尾",
            "风险调整收益": "A增长、现金流和估值更均衡",
            "下行保护优先": "A客户粘性和低IV更强",
            "估值消化优先": "A高利润与Forward PE更匹配",
            "近端催化优先": "A的Azure/Copilot验证点更近",
            "价格确认/动量": "A价格确认略稳且IV较低",
            "激进短线": "A大盘AI平台仍具交易性",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B订单或收入兑现更清楚",
            "右尾弹性优先": "B小基数或硬件右尾更大",
            "风险调整收益": "B赔率或反证组合更好",
            "下行保护优先": "B压力期或现金流更稳",
            "估值消化优先": "B估值更易被业绩消化",
            "近端催化优先": "B订单/产品催化更强",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B短线爆发力更高",
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
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
            return "MSFT的Azure、commercial RPO和M365收入兑现更清楚。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
            return "MSFT的Forward PE、净利润和企业SaaS质量更能消化估值。"
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 12:  # type: ignore[index,operator]
            return "MSFT的现金流、客户粘性和压力期表现更稳。"
        return "MSFT在兑现、风险调整和估值消化的组合上略胜。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']}的小基数、订单或硬件右尾明显强于MSFT。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']}的价格确认和短线资金偏好明显强于MSFT。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']}的估值消化或赔率更好，MSFT短期受AI CapEx压制。"
    return f"{b['ticker']}在多数投资思路下比MSFT更符合当前配置目标。"


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
        key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["估值消化优先"] - x["b"]["scores"]["估值消化优先"]),  # type: ignore[index,operator]
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
    for product in a["products"][:7]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    support = {
        "NTM兑现优先": (
            "FY2026 Q3收入828.86亿美元、Azure CC +39%-40% Q4指引、commercial RPO 6270亿美元、AI business ARR >370亿美元",
            "Azure需求强但可售容量、并网、GPU/ASIC/HBM/网络和revenue-ready周期仍是收入确认约束",
        ),
        "右尾弹性优先": (
            "Azure AI、M365 Copilot、GitHub Copilot、Security/Dynamics agents和Maia/Cobalt形成多条AI右尾",
            "公司体量巨大，极度乐观需要Azure 50%+、Copilot 9000万+ seats、Maia降本和容量上线同时成立",
        ),
        "风险调整收益": (
            "Forward PE 18.99、P/S 8.57，基准收入3780-3920亿美元、净利润1380-1510亿美元，质量高于多数高beta标的",
            "FY2026前九个月新增PP&E 801.46亿美元，AI CapEx前置使FCF低于传统软件模型",
        ),
        "下行保护优先": (
            "企业SaaS续费、Azure RPO、净现金/强OCF、Call IV 34.4%和SOXX压力窗口-36.85%提供防守质量",
            "Microsoft Cloud毛利率受AI折旧、电力、模型推理成本压制，OpenAI集中度和监管仍是尾部风险",
        ),
        "估值消化优先": (
            "18.99倍Forward PE对应Azure/PBP双引擎和高净利率，业绩兑现更容易消化估值",
            "P/S 8.57并不低，估值消化依赖Azure AI容量转收入和AI推理毛利不继续恶化",
        ),
        "近端催化优先": (
            "Q4 Azure +39%-40%、Q4 CapEx超400亿美元、RPO确认、AI ARR、Copilot seats和GitHub usage billing均可在1-2季验证",
            "多数催化是收入/毛利逐季验证，不如小盘订单或产品认证的单点重定价剧烈",
        ),
        "价格确认/动量": (
            "两周+1.49%、一月+3.11%，低IV和完整金融数据使价格确认可跟踪",
            "2026-06-22价格367.34美元低于2026-06-03收盘427.34美元，近期趋势并不强",
        ),
        "激进短线": (
            "Azure/Copilot/GitHub/OpenAI/Maia仍是市场高关注AI平台叙事，财报前后有交易性",
            "Call IV 34.4%、大市值和低beta属性限制短线爆发，弱于高IV小盘和直接硬件订单股",
        ),
    }

    out: list[str] = []
    out += [
        "# MSFT 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：MSFT / 微软",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 MSFT vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。MSFT 的优势集中在估值消化、下行保护、NTM兑现和风险调整，核心是 Azure/PBP 双引擎、commercial RPO、AI ARR、Copilot seats 和较低Forward PE同时存在。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是价格确认不强、短线爆发力不如高IV小盘/硬件/电力链，且AI CapEx前置压低传统软件式FCF。",
        "- A 最适合的投资者画像：希望持有大市值AI云和企业SaaS核心仓位、看重收入兑现、估值消化、客户粘性和下行保护的中长期配置者。",
        "- A 最不适合的投资者画像：只追求小基数收入爆发、极端短线动量、期权高波动或上游硬件订单弹性的进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在右尾弹性、价格确认、激进短线或更直接AI硬件/电力订单上压过MSFT。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：MSFT 对 {sum(1 for x in comparisons if x['final'] == 'A')}/{n - 1} 家公司多数思路占优，对 {sum(1 for x in comparisons if x['final'] == 'B')}/{n - 1} 家公司多数思路落后；它是全项目最强的均衡型AI平台之一，但不是最高弹性或最强短线动量资产。",
        "- 后续最重要跟踪数据：Azure增速、commercial RPO剔除OpenAI增速、25%未来12个月确认比例、AI ARR、M365 Copilot paid seats/active usage、GitHub usage billing接受度、Microsoft Cloud毛利率、FY2026 Q4和CY2026 CapEx、Maia/Cobalt迁移、OpenAI集中度、FCF转化率。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "MSFT"]),
        base.row(["公司名称", "微软"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "3780-3920 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "Azure AI不是需求不足，而是可售容量、并网/数据中心交付、GPU/ASIC/HBM/网络和revenue-ready周期。"]),
        base.row(["最大反证", "若Azure低于35%、commercial RPO剔除OpenAI低于20%、Microsoft Cloud毛利率跌破62%、Copilot活跃/ARPU不及预期或AI CapEx继续吞噬FCF，MSFT的估值消化和风险调整会下修。"]),
        base.row(["近端催化剂", "FY2026 Q4 Azure +39%-40%指引兑现、RPO确认、AI ARR、M365 Copilot seats、GitHub用量计费、Microsoft Cloud毛利率、Q4 CapEx超过400亿美元和Maia/Cobalt部署。"]),
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
        base.row(["直接同业", "与MSFT在云基础设施、AI云、企业软件、开发者平台或云资源采购中高度重叠，优先比较Azure/AWS/GCP/OCI收入、RPO、AI收入、利润率、客户质量和同业估值消化。", "AMZN、GOOGL、ORCL、BABA、IBM、CRWV、NBIS", "同档或相邻档时，RPO、云利润率、企业客户粘性和AI收入证据可放大到建议级别。"]),
        base.row(["相邻替代", "不完全同业，但同属大市值AI平台、AI软件、安全、IDC/NeoCloud或AI资源配置替代。", "META、ADBE、CRWD、NTNX、APLD、IREN、EQIX、DLR", "默认看增长质量、估值消化、近端催化和风险调整，不只看业务热度。"]),
        base.row(["上下游", "B是MSFT AI CapEx和Azure云收入链条中的芯片、服务器、网络、电力、冷却、设备、材料或能源供应商。", "NVDA、AMD、AVGO、TSM、VRT、ETN、PWR、CEG、MU、SMCI", "不把MSFT下游收入规模直接等同于更好，也不把上游瓶颈稀缺自动当胜出；看利润捕获和估值消化。"]),
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
        need = "需要MSFT证明Azure/RPO/Copilot继续上修，并让AI CapEx不再持续压低FCF转化。"
        if "价格确认/动量" in wins or "激进短线" in wins:
            need = "需要MSFT出现更强价格确认，或用Azure AI、Copilot和GitHub数据触发短线重定价。"
        if comparison["rel"] == "上下游":
            need = "需要MSFT证明下游AI平台利润捕获强于上游硬件订单弹性，并改善云毛利率。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B提供更硬的收入/订单兑现、利润质量、估值消化和价格确认。"
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
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/云算力_IDC_AI软件平台/MSFT_微软_公司调研_2026-06-20.md`、`行业调研/AI服务器_存储_芯片/行业调研_云厂自研AI ASIC_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI集群调度与推理运行时_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI云算力外包和NeoCloud与AI数据中心运营商_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AI以太网交换系统与Fabric芯片_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_msft_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对百分比区间如 `+14%-18%` 做同号区间修正，并对MSFT的Azure/RPO/Copilot、AI CapEx、估值消化、下行保护和价格确认做公司专属校准后建档；未读取下游量化目录或现成排序结论。",
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
                "msft_tiers": companies[TARGET]["tiers"],
                "msft_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
