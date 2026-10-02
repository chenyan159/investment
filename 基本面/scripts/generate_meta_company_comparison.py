from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base
import generate_amzn_company_comparison as helper


TARGET = "META"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "META_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL

DIRECT_PEERS = {"GOOGL", "AMZN", "MSFT", "BABA", "ADBE"}
ADJACENT_PEERS = {"ORCL", "IBM", "CRWD", "NTNX", "CRWV", "NBIS", "APLD", "IREN", "EQIX", "DLR"}
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

    # META is a large profitable advertising/AI platform. The project-wide
    # adjustment keeps the strong NTM and valuation digestion evidence, while
    # not treating internal AI CapEx, MTIA, or AI glasses as hard external
    # revenue in right-tail, momentum, or short-term attack columns.
    overrides = {
        "NTM兑现优先": 82.0,
        "右尾弹性优先": 70.0,
        "风险调整收益": 66.0,
        "下行保护优先": 74.0,
        "估值消化优先": 82.0,
        "近端催化优先": 67.0,
        "价格确认/动量": 42.0,
        "激进短线": 84.0,
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
            "NTM兑现优先": "A广告收入和Q2指引更硬",
            "右尾弹性优先": "A广告AI/WhatsApp仍有右尾",
            "风险调整收益": "A增长与低Forward PE更均衡",
            "下行保护优先": "A利润和现金流底盘更厚",
            "估值消化优先": "A高增长更能消化低PE",
            "近端催化优先": "A财报量价和CapEx节点更近",
            "价格确认/动量": "A价格确认略好且未缺数据",
            "激进短线": "A大盘AI关注度仍可交易",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B订单或收入兑现更清楚",
            "右尾弹性优先": "B小基数或硬件右尾更大",
            "风险调整收益": "B赔率/反证组合更好",
            "下行保护优先": "B压力期或现金流更稳",
            "估值消化优先": "B估值更易被业绩消化",
            "近端催化优先": "B近端订单/产品催化更强",
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
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
            return "META 的广告利润和低Forward PE让估值消化更占优。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
            return "META 的广告收入、Q2指引和利润兑现比 B 更清楚。"
        return "META 在兑现、估值消化和风险调整的组合上略胜。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的小基数右尾或硬件订单弹性明显强于 META。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和短线资金偏好明显强于 META。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的防守、现金流或压力期表现更适合该思路。"
    return f"{b['ticker']} 在多数投资思路下比 META 更符合当前配置目标。"


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
            "2026Q1收入 `$56.3B`、广告 `$55.0B`、展示 +19%、价格 +12%，Q2收入指引 `$58B-$61B`",
            "NTM仍依赖广告量价持续强势，监管和预算周期会影响兑现斜率",
        ),
        "右尾弹性优先": (
            "AI广告、WhatsApp商业消息、Meta AI、MTIA降本和AI glasses形成多条期权",
            "Meta AI/MTIA/RL在NTM内多数是成本或间接贡献，不是硬收入右尾",
        ),
        "风险调整收益": (
            "Forward PE `15.56`、基准收入增速约 +21%-+26%，FoA利润池足以覆盖多数执行误差",
            "CapEx `$125B-$145B`、RL亏损、监管和AI折旧压制FCF与估值弹性",
        ),
        "下行保护优先": (
            "FoA现金流、广告主粘性和大市值流动性提供基本盘，Call IV `36.7%`不极端",
            "SOXX压力窗口累计 `-66.11%`，广告周期和高CapEx使其不是最强防守资产",
        ),
        "估值消化优先": (
            "低Forward PE叠加20%以上NTM收入增长，广告利润留存有能力消化估值",
            "P/S `6.66`不低，估值消化取决于AI基建投入能否不继续吞噬FCF",
        ),
        "近端催化优先": (
            "Q2收入、广告展示/价格、FoA Other、CapEx/MTIA commentary和RL亏损均可在1-2季验证",
            "缺少像硬件链大额订单、RPO或客户认证那样的单一重定价催化",
        ),
        "价格确认/动量": (
            "2026-06-03 两周 +2.96%、一月 +2.34%，基础价格数据完整",
            "2026-06-22 价格已低于6月3日收盘，短期价格确认不如强动量硬件/电力链",
        ),
        "激进短线": (
            "广告AI、Meta AI、AI眼镜、MTIA和大盘高关注度仍有财报交易性",
            "公司体量过大且右尾多为间接变现，爆发力弱于小基数高IV标的",
        ),
    }

    out: list[str] = []
    out += [
        "# META 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：META / Meta Platforms",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 META vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。META 的优势集中在估值消化、NTM兑现和风险调整，核心是广告收入高可见、利润池厚、Forward PE 明显低于多数高增长AI标的。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是价格确认一般、激进短线弹性不如小基数硬件/电力/NeoCloud，且AI CapEx和Reality Labs会压制FCF。",
        "- A 最适合的投资者画像：重视大市值AI平台、广告现金牛、低PE估值消化和可验证收入利润的人；适合作为AI组合里偏核心、偏风险调整的配置候选。",
        "- A 最不适合的投资者画像：只追求订单爆发、小基数收入右尾、短线高IV和价格动量的进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在右尾弹性、价格确认、激进短线或更直接AI硬件/电力订单上压过META。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：META 对 {sum(1 for x in comparisons if x['final'] == 'A')}/{n - 1} 家公司多数思路占优，对 {sum(1 for x in comparisons if x['final'] == 'B')}/{n - 1} 家公司多数思路落后；它是全项目强估值消化/强兑现的大盘AI平台，不是最强硬件右尾或最强短线动量资产。",
        "- 后续最重要跟踪数据：广告展示量、平均广告价格、Q2/Q3收入指引、FoA Other收入、FoA经营利润率、2026费用与CapEx指引、PP&E和折旧、OCF/FCF、MTIA生产负载、AMD/Broadcom协议交付、数据中心上电、Reality Labs收入与亏损、AI glasses销量和监管进展。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "META"]),
        base.row(["公司名称", "Meta Platforms"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`2600-2700 亿美元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "广告需求和广告价格能否持续快于AI基建折旧、第三方云、能源、网络、数据中心运营和AI人才成本；AI数据中心投入本身不是META外部收入。"]),
        base.row(["最大反证", "若广告平均价格转弱、2026费用/CapEx继续上修且收入不跟、监管削弱个性化广告、MTIA/GPU上电延迟或Reality Labs亏损扩大，则估值消化和风险调整会下修。"]),
        base.row(["近端催化剂", "Q2收入兑现、广告展示/价格、FoA Other、CapEx和费用指引、MTIA/AMD/Broadcom进展、Reality Labs亏损、AI glasses和Meta AI货币化披露。"]),
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
        base.row(["直接同业", "同属大市值广告、云、AI平台或数字内容/企业软件资金篮子，优先比较广告/云收入兑现、利润质量、AI产品代际、用户/客户质量和同业估值。", "GOOGL、AMZN、MSFT、BABA、ADBE", "同档或相邻档时，广告现金流、云/RPO、AI产品变现和估值消化可放大到建议级别。"]),
        base.row(["相邻替代", "不直接竞争，但同属AI平台、AI软件、IDC/AI云运营或云资源配置替代。", "ORCL、IBM、CRWD、NTNX、CRWV、NBIS、APLD、IREN、EQIX、DLR", "默认看增长质量、估值消化、近端催化和风险调整，不只看业务热度。"]),
        base.row(["上下游", "B 是 META AI CapEx、数据中心、芯片、服务器、网络、电力、冷却、设备、材料或能源供应链参与者。", "NVDA、AMD、AVGO、TSM、VRT、ETN、PWR、CEG、MU、SMCI", "不把META下游收入规模直接等同于更好，也不把上游瓶颈稀缺自动当胜出；看利润捕获和估值消化。"]),
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
        need = "需要 META 证明广告量价和FoA利润继续上修，同时让AI CapEx不再持续吞噬FCF。"
        if "价格确认/动量" in wins or "激进短线" in wins:
            need = "需要 META 出现更强价格确认，或用广告AI/MTIA/AI眼镜数据触发短线重定价。"
        if comparison["rel"] == "上下游":
            need = "需要 META 证明下游广告/AI平台利润捕获强于上游硬件订单弹性，且CapEx转化效率改善。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬的收入/订单兑现、利润质量和估值消化证据。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要 B 把右尾叙事转成可确认收入、利润和现金流，并降低估值或执行反证。"
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
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/云算力_IDC_AI软件平台/META_Meta Platforms_公司调研_2026-06-20.md`、`行业调研/产业背景/AI产业链全局图谱与口径字典_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_云厂自研AI ASIC_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI集群调度与推理运行时_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_meta_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对百分比区间如 `+14%-18%` 做同号区间修正，并对META的广告收入、AI CapEx、MTIA、Reality Labs、估值和价格确认做公司专属校准后建档；未读取下游量化目录或现成排序结论。",
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
                "meta_tiers": companies[TARGET]["tiers"],
                "meta_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
