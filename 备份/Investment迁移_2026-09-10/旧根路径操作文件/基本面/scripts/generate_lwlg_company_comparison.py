from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import generate_alle_company_comparison as base


TARGET = "LWLG"
TARGET_NAME = "Lightwave Logic"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "LWLG_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {
    "AAOI",
    "COHR",
    "LITE",
    "MTSI",
    "POET",
}

OPTICAL_VALUE_CHAIN = {
    "ALAB",
    "ANET",
    "APH",
    "AVGO",
    "BDC",
    "BELFB",
    "CIEN",
    "CRDO",
    "CSCO",
    "FN",
    "GLW",
    "MRVL",
    "NOK",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}

FOUNDRY_AND_ENABLEMENT = {
    "ASML",
    "AMAT",
    "ENTG",
    "GFS",
    "KLAC",
    "LRCX",
    "MKSI",
    "TSEM",
    "TSM",
    "UMC",
}

AI_DEMAND_OR_PLATFORM = {
    "AMD",
    "AMZN",
    "BABA",
    "CRWV",
    "DELL",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "META",
    "MSFT",
    "NBIS",
    "NVDA",
    "ORCL",
    "SMCI",
}


def mid_growth(value: object) -> float | None:
    text = str(value).replace("−", "-").replace("～", "-").replace("—", "-").replace("–", "-")
    ranged = re.search(
        r"([+-]?)\s*(\d+(?:\.\d+)?)\s*%\s*(?:至|到|-)\s*([+-]?)\s*(\d+(?:\.\d+)?)\s*%",
        text,
    )
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

    # LWLG-specific calibration. Its percentage growth is mathematically huge
    # because TTM revenue is only about $0.24m, so the target must be anchored
    # to revenue quality, order evidence, cash burn, valuation and catalyst
    # visibility rather than raw growth percentages.
    lwlg = companies[TARGET]
    overrides = {
        "NTM兑现优先": 34.0,
        "右尾弹性优先": 76.5,
        "风险调整收益": 36.0,
        "下行保护优先": 34.5,
        "估值消化优先": 14.0,
        "近端催化优先": 64.5,
        "价格确认/动量": 34.0,
        "激进短线": 89.5,
    }
    for strategy, score in overrides.items():
        lwlg["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in OPTICAL_VALUE_CHAIN or ticker in FOUNDRY_AND_ENABLEMENT or ticker in AI_DEMAND_OR_PLATFORM:
        return "上下游"
    if category == "AI网络_光互联_连接器":
        return "相邻替代"
    if category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A至少有小额授权/NRE路径",
            "右尾弹性优先": "A的EO polymer右尾更非线性",
            "风险调整收益": "B反证更重且A有现金缓冲",
            "下行保护优先": "A现金无债且B更弱",
            "估值消化优先": "A虽高估但B消化证据更弱",
            "近端催化优先": "A有Stage3/PDK/客户协议催化",
            "价格确认/动量": "A高波动反弹弹性略强",
            "激进短线": "A高IV和光I/O叙事更适合进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/订单兑现更硬",
            "右尾弹性优先": "B右尾证据更可收入化",
            "风险调整收益": "B赔率与下行组合更均衡",
            "下行保护优先": "B现金流/估值防守更强",
            "估值消化优先": "B业绩更能消化估值",
            "近端催化优先": "B近端订单/财报催化更明确",
            "价格确认/动量": "B价格确认更强",
            "激进短线": "B短线资金偏好更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "估值消化优先", "下行保护优先"}:
        return "成长/估值/防守互抵"
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
    return "A" if a["scores"]["右尾弹性优先"] + a["scores"]["激进短线"] >= b["scores"]["右尾弹性优先"] + b["scores"]["激进短线"] else "B"  # type: ignore[index,operator]


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["右尾弹性优先"] - b["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
            return f"LWLG 的 EO polymer、PDK 和 400G/lane 技术期权比 {b['ticker']} 更非线性。"
        if a["scores"]["激进短线"] - b["scores"]["激进短线"] > 16:  # type: ignore[index,operator]
            return "LWLG 的高IV、Stage3/PDK窗口和光I/O叙事更适合激进进攻。"
        return "LWLG 在右尾和近端技术催化上略优，但仍需客户合同和Stage4验证。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入、订单或利润兑现证据明显强于 LWLG。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 更能用当前业绩消化估值，LWLG 当前仍是高PS期权。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的现金流、盈利或估值防守强于 LWLG。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和趋势强于 LWLG。"
    return f"{b['ticker']} 在多数投资思路下比 LWLG 更符合项目内资金配置目标。"


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


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def fmt_num(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return str(value)


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return str(value)


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        v = float(value)
    except (TypeError, ValueError):
        return str(value)
    if abs(v) >= 1000:
        return f"${v / 1000:.2f}T"
    if abs(v) >= 1:
        return f"${v:.2f}B"
    return f"${v * 1000:.2f}M"


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
        key=lambda x: (
            x["bc"] - x["ac"],
            x["b"]["scores"]["NTM兑现优先"] + x["b"]["scores"]["估值消化优先"] - a["scores"]["NTM兑现优先"] - a["scores"]["估值消化优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            x["ac"] - x["bc"],
            a["scores"]["右尾弹性优先"] + a["scores"]["激进短线"] - x["b"]["scores"]["右尾弹性优先"] - x["b"]["scores"]["激进短线"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:70]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:70]  # type: ignore[operator]
    relative_b_rows = [x for x in strong_b if x["final"] == "B"][:12]
    if strong_b_rows:
        b_opposition_text = f"{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在可确认收入、订单/backlog、利润现金流、估值消化或价格确认上压过 LWLG。"
    elif relative_b_rows:
        b_opposition_text = (
            "无达到“B胜出至少5列且净胜3列”的显著强反方；相对压制或最终偏B的公司包括 "
            f"{'、'.join([x['ticker'] for x in relative_b_rows])}。"
        )
    else:
        b_opposition_text = "无显著强反方；LWLG在多数公司对比中主要输在兑现、估值和防守单列。"

    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker]["fin"] or not companies[ticker]["fin"].get("price")  # type: ignore[union-attr]
    ]

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]

    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_snapshot = (
        f"2026-06-22 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    support = {
        "NTM兑现优先": (
            "2026Q1收入2.92万美元、TTM约24.31万美元，现有材料/授权协议和小额NRE可形成最低收入锚",
            "无正式收入指引、无backlog/bookings、2026Q1 NRE为0，Stage3/PDK不是订单",
        ),
        "右尾弹性优先": (
            "4个Stage3客户、200G/400G per lane、Tower/GF/SilTerra PDK和EO polymer若被采用可形成高毛利royalty",
            "缺少Stage4、客户名、最低采购、royalty rate和量产良率，极度乐观仍是低可信期权",
        ),
        "风险调整收益": (
            "现金约7510万美元、无债务，技术路线若通过客户qualification有非线性上行",
            "2026-06-22 P/S 6357x、Forward PE缺失、经营亏损和客户验证失败风险很高",
        ),
        "下行保护优先": (
            "资产负债表短期安全，现金可支撑研发和客户支持，不存在近端债务压力",
            "股票Call IV 132.9%、Put IV 123.8%，收入极小且估值依赖技术期权，防守性弱",
        ),
        "估值消化优先": (
            "只有出现带金额的upfront、milestone、minimum royalty或Stage4订单，估值消化才会开始有路径",
            "TTM收入约24.31万美元对1.55B美元市值，当前业绩无法消化估值",
        ),
        "近端催化优先": (
            "2026H2 PDK v1.1 high-volume foundry transfer、Tower/GF/SilTerra tape-out、Stage3推进和新授权协议谈判可验证",
            "催化大多是技术和商业谈判节点，若没有金额/客户/验收披露，重定价持续性有限",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+5.13%，高波动使利好披露能迅速反映到价格",
            "2026-06-03过去一月-24.46%，2026-06-22价格10.03低于6月3日12.29，趋势未确认",
        ),
        "激进短线": (
            "Call IV 132.9%、AI光互联、CPO/光I/O、400G/lane和客户Stage3叙事具备进攻弹性",
            "高IV意味着期权已很贵，任何无订单、无Stage4或验证延迟都会放大回撤",
        ),
    }

    out: list[str] = []
    out += [
        "# LWLG 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：LWLG / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 LWLG vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。LWLG 的优势主要在右尾弹性和激进短线，原因是 EO polymer、200G/400G per lane、PDK/foundry导入和Stage3客户若转为Stage4，收入基数极小会带来非线性上修。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是当前收入只有几十万美元级、无backlog/订单金额、2026Q1 NRE为0、Forward PE缺失、P/S约 `6357x`、经营仍大幅亏损。",
        "- A 最适合的投资者画像：接受高波动、高验证风险，愿意为 AI 光互联材料/IP 期权和客户验证突破付费的激进成长或事件驱动资金。",
        "- A 最不适合的投资者画像：要求未来12个月收入利润可兑现、低估值、强现金流、低IV或防守回撤的稳健资金。",
        f"- 多数思路下最强反方公司：{b_opposition_text}",
        "- 如果只追求更高增长、更好公司，A 的总体位置：LWLG 是项目内高右尾小基数技术期权，不是当前更高质量的已收入化 AI 主链公司；总体更适合作为小仓位进攻期权，而不是核心配置。",
        "- 后续最重要跟踪数据：Q2/Q3 2026 net sales和NRE、新材料供应/授权协议金额、Stage3到Stage4、Tower/GF/SilTerra 200G/400G lane测试、PDK v1.1 foundry transfer、客户qualification、良率、封装可靠性、现金消耗和股权融资。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "LWLG"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "30-140 万美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "Stage3/PDK/tape-out 转为可确认收入；客户qualification、可靠性、良率、封装、foundry transfer、合同金额和收入确认条款。"]),
        base.row(["最大反证", "无backlog/bookings/客户采购金额/量产合同；Q1 2026 NRE为0；成熟InP/SiPh/TFLN/BTO和大厂内部方案仍可替代。"]),
        base.row(["近端催化剂", "2026H2 PDK v1.1向高产量foundry转移、Tower/GF/SilTerra tape-out、Stage3客户推进、新材料/授权/NRE/milestone协议。"]),
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
        base.row(["直接同业", "同属AI光互联器件、光模块、光引擎、调制器材料/IP或高速光电转换需求池，优先比较客户项目阶段、收入兑现、订单、良率、产品代际和估值。", "LITE、COHR、AAOI、MTSI、POET", "同业证据权重最高；LWLG若只有Stage3/PDK而对手已有量产收入，兑现/估值列倾向对手。"]),
        base.row(["相邻替代", "同处AI网络、AI芯片、服务器、数据中心基础设施资金篮子，但不是同一产品或收入模式。", "ALAB、ANET、VRT、ETN、SMCI、DELL、GEV", "回答资金只能买一个时，谁的增长质量、估值消化和催化更好；LWLG右尾强但兑现弱。"]),
        base.row(["上下游", "一方是LWLG的潜在foundry、PIC/模块/系统、交换芯片、云/AI集群需求端或供应链使能方。", "TSEM、GFS、TSM、MRVL、AVGO、CIEN、CSCO、NVDA、MSFT", "强调利润捕获和议价权，不把下游AI收入规模直接等同于LWLG收入，也不把上游技术稀缺直接等同订单。"]),
        base.row(["跨赛道", "半导体材料、前道设备、封测、工业、化工、公用事业等与LWLG业务差异大，但作为项目内资金配置替代仍可比较。", "ASML、LIN、TMO、AEP、CAT、DHR", "默认降低结论力度；只有成长、估值、现金流或下行保护明显拉开时才给建议/强烈建议。"]),
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
        need = "需要 LWLG 披露带金额的新材料/授权/NRE/milestone协议、至少一个Stage3进入Stage4、客户名或最低采购/royalty，并证明现金消耗可控。"
        if comparison["rel"] == "直接同业":
            need = "需要 LWLG 在同业中证明200G/400G lane客户qualification、量产良率、收入确认和royalty经济性足以压过已量产对手。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 LWLG 用更硬合同和收入兑现抵消跨赛道标的的现金流、估值或防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更大的非线性右尾、明确AI主线催化或更强短线资金偏好，否则难以压过LWLG的技术期权。"
        if b["scores"]["NTM兑现优先"] > a["scores"]["NTM兑现优先"]:  # type: ignore[index,operator]
            need = "需要 B 把兑现优势和现金流优势延续到更高成长，否则在右尾/激进短线上仍可能输给LWLG。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少可用价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/AI网络_光互联_连接器/LWLG_Lightwave_Logic_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_硅光材料、光子材料与电光聚合物_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_CPO／NPO与交换侧光引擎_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_Optical Interposer与新型光引擎_2026-06-11.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 自动化脚本：`scripts/generate_lwlg_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对 LWLG 做目标公司专属校准；未读取下游量化目录、备份、临时目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 LWLG 正式评估文件")
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
                "lwlg_tiers": companies[TARGET]["tiers"],
                "lwlg_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
                "lwlg_ranks": companies[TARGET]["ranks"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
