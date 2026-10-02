from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated
import generate_cls_company_comparison as cls_calibrated


TARGET = "IBM"
TARGET_NAME = "International Business Machines"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "IBM_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_SOFTWARE_PEERS = {
    "MSFT",
    "ORCL",
    "NTNX",
}

ADJACENT_SOFTWARE_PLATFORM = {
    "ADBE",
    "AMZN",
    "BABA",
    "CRWD",
    "GOOGL",
    "META",
}

UPSTREAM_DOWNSTREAM = {
    "AAOI",
    "ADI",
    "ALAB",
    "AMD",
    "ANET",
    "ARM",
    "AVGO",
    "CDNS",
    "CIEN",
    "COHR",
    "CRDO",
    "CRWV",
    "CSCO",
    "DELL",
    "DLR",
    "EQIX",
    "HPE",
    "INTC",
    "IREN",
    "MRVL",
    "NBIS",
    "NVDA",
    "PSTG",
    "QCOM",
    "SMCI",
    "SNPS",
    "TSM",
}

POWER_COOLING_CHAIN = {
    "AAON",
    "ABBNY",
    "AEIS",
    "AEP",
    "APLD",
    "BE",
    "BWXT",
    "CARR",
    "CEG",
    "DTE",
    "EME",
    "ETN",
    "ETR",
    "FIX",
    "FLNC",
    "GEV",
    "HUBB",
    "IESC",
    "JCI",
    "MOD",
    "MYRG",
    "NVT",
    "OKLO",
    "PWR",
    "SMR",
    "TT",
    "VRT",
    "VST",
}

# IBM's formal evaluation describes mid-single-digit NTM revenue growth,
# strong FCF, and moderate AI software optionality. The generic regex reads
# "+5-7%" as a negative range, so these overrides anchor IBM's project-relative
# tiers to the evaluated business profile rather than the parser miss.
IBM_SCORE_OVERRIDES = {
    "NTM兑现优先": 66.0,
    "右尾弹性优先": 54.0,
    "风险调整收益": 62.0,
    "下行保护优先": 90.0,
    "估值消化优先": 62.0,
    "近端催化优先": 64.0,
    # 2026-06-03 interval momentum was strong, but the 2026-06-22 close
    # materially retraced from the 6/3 close. Treat momentum as stale/faded.
    "价格确认/动量": 55.0,
    "激进短线": 72.0,
}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    calibrated.fix_growth_ranges(companies)
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    for floorset in (calibrated.SCORE_FLOORS, cls_calibrated.EXTRA_SCORE_FLOORS):
        for ticker, floors in floorset.items():
            company = companies.get(ticker)
            if not company:
                continue
            for strategy, floor in floors.items():
                current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[assignment]
                company["scores"][strategy] = max(float(current), float(floor))  # type: ignore[index]

    for strategy, score in IBM_SCORE_OVERRIDES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score  # type: ignore[index]
    calibrated.recompute_tiers(companies)


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_SOFTWARE_PEERS:
        return "直接同业"
    if ticker in ADJACENT_SOFTWARE_PLATFORM or category == "云算力_IDC_AI软件平台":
        return "相邻替代"
    if ticker in UPSTREAM_DOWNSTREAM or ticker in POWER_COOLING_CHAIN:
        return "上下游"
    if category in {"AI计算芯片_EDA_IP_custom_ASIC", "AI网络_光互联_连接器", "AI服务器_存储_EMS"}:
        return "上下游"
    if category in INFRA_CATS:
        return "上下游"
    return "跨赛道"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong: list[str] = []
    b_strong: list[str] = []
    close: list[str] = []
    for strategy in STRATS:
        av = tier_value(a["tiers"].get(strategy))  # type: ignore[union-attr]
        bv = tier_value(b["tiers"].get(strategy))  # type: ignore[union-attr]
        diff = av - bv
        if diff >= 1:
            a_strong.append(strategy.replace("优先", ""))
        elif diff <= -1:
            b_strong.append(strategy.replace("优先", ""))
        else:
            close.append(strategy.replace("优先", ""))
    return f"A强：{'、'.join(a_strong[:3]) or '无'}；B强：{'、'.join(b_strong[:3]) or '无'}；接近：{'、'.join(close[:3]) or '无'}"


def tag_from_diff(score_diff: float, tier_diff: int, rel: str) -> str:
    adiff = abs(score_diff)
    atier = abs(tier_diff)
    if adiff < 5 and atier == 0:
        return "中性"
    if adiff < 9 and atier <= 1:
        base_tag = "微倾向"
    elif adiff < 20 and atier <= 2:
        base_tag = "建议"
    else:
        base_tag = "强烈建议"

    if rel == "跨赛道" and base_tag == "强烈建议" and not (adiff >= 30 or atier >= 3):
        base_tag = "建议"
    if rel in {"相邻替代", "上下游"} and base_tag == "强烈建议" and not (adiff >= 26 or atier >= 3):
        base_tag = "建议"
    side = "A" if score_diff > 0 else "B"
    return f"{base_tag}投{side}"


def label_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    score_diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
    tier_diff = tier_value(a["tiers"].get(strategy)) - tier_value(b["tiers"].get(strategy))  # type: ignore[union-attr]
    tag = tag_from_diff(score_diff, tier_diff, rel)
    if tag == "中性":
        return tag
    if rel == "直接同业" and tag.startswith("建议") and abs(score_diff) >= 18:
        return "强烈" + tag
    return tag


def neutral_reason(rel: str) -> str:
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if rel == "直接同业":
        return "同档需等收入和订单验证"
    return "档位接近需再验证"


def reason_for(strategy: str, tag: str, b: dict[str, object], rel: str) -> str:
    if tag == "中性":
        return neutral_reason(rel)
    winner = "A" if tag.endswith("投A") else "B"
    if winner == "A":
        return {
            "NTM兑现优先": "A有FY2026指引、软件收入和FCF硬锚",
            "右尾弹性优先": "A企业AI软件和主机期权更可收入化",
            "风险调整收益": "A现金流、估值和反证组合更稳",
            "下行保护优先": "A企业客户粘性和FCF底座更强",
            "估值消化优先": "A用18.75x远期PE和FCF消化估值",
            "近端催化优先": "A有Q2财报、z17和并购整合验证",
            "价格确认/动量": "A旧窗口确认更强但仍需看回撤修复",
            "激进短线": "A有企业AI事件和IV弹性可交易",
        }[strategy]

    return {
        "NTM兑现优先": "B收入/订单兑现增速更高",
        "右尾弹性优先": "B右尾增长和市值弹性更大",
        "风险调整收益": "B上行、估值和反证组合更好",
        "下行保护优先": "B低IV、现金流或压力期更稳",
        "估值消化优先": "B业绩增速或估值消化更好",
        "近端催化优先": "B近端订单/财报/产能催化更强",
        "价格确认/动量": "B趋势更强且IBM六月回撤",
        "激进短线": "B短线弹性和市场关注度更高",
    }[strategy]


def cell_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    tag = label_for(a, b, strategy, rel)
    return f"{tag}：{reason_for(strategy, tag, b, rel)}"


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
        if float(a["scores"]["下行保护优先"]) - float(b["scores"]["下行保护优先"]) > 14:  # type: ignore[index]
            return "IBM 的自由现金流、企业客户粘性和主机/软件底盘提供更强下行保护。"
        if float(a["scores"]["风险调整收益"]) - float(b["scores"]["风险调整收益"]) > 10:  # type: ignore[index]
            return "IBM 的上行虽不极端，但估值、现金流和反证组合更均衡。"
        if float(a["scores"]["NTM兑现优先"]) - float(b["scores"]["NTM兑现优先"]) > 8:  # type: ignore[index]
            return "IBM 的FY2026指引、Software/Consulting证据和FCF兑现路径更清楚。"
        return "IBM 更适合作为企业AI软件和现金流防守型配置，B 的右尾不足以覆盖风险差距。"

    if float(b["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]) > 16:  # type: ignore[index]
        return f"{b['ticker']} 的高增长右尾和重定价弹性明显强于 IBM。"
    if float(b["scores"]["NTM兑现优先"]) - float(a["scores"]["NTM兑现优先"]) > 12:  # type: ignore[index]
        return f"{b['ticker']} 的 NTM 收入/订单兑现证据比 IBM 更强。"
    if float(b["scores"]["价格确认/动量"]) - float(a["scores"]["价格确认/动量"]) > 14:  # type: ignore[index]
        return f"{b['ticker']} 的价格趋势更强，IBM 6 月旧动量已经回撤。"
    if float(b["scores"]["估值消化优先"]) - float(a["scores"]["估值消化优先"]) > 12:  # type: ignore[index]
        return f"{b['ticker']} 的业绩增速或估值消化空间优于 IBM。"
    return f"{b['ticker']} 在多数投资思路下比 IBM 更符合项目内增长配置目标。"


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    rows: list[dict[str, object]] = []
    for ticker in sorted(companies):
        if ticker == TARGET:
            continue
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(a, b, strategy, rel) for strategy in STRATS]
        a_count, b_count, neutral = direction_counts(cells)
        final = final_choice(a, b, cells)
        rows.append(
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
    return rows


def majority_text(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def fmt_num(value: object, decimals: int = 2) -> str:
    if value is None or value == "":
        return "缺失"
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return str(value)


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"${float(value):.2f}B"
    except (TypeError, ValueError):
        return str(value)


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return str(value)


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
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["下行保护优先"] - x["b"]["scores"]["下行保护优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:45]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:45]  # type: ignore[operator]
    missing_fin = [ticker for ticker in sorted(companies) if not companies[ticker]["fin"]]

    fin = a["fin"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    product_names = [str(product[0]).split("：")[0] for product in a["products"][:6]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]

    support = {
        "NTM兑现优先": ("FY2026固定汇率收入+5%+、Software/Red Hat、GenAI Consulting backlog和FCF指引支撑", "公司层增长仅中个位数，传统咨询和Infrastructure仍会抵消成长业务"),
        "右尾弹性优先": ("Confluent/Data、Red Hat AI、HashiCorp、z17和ServiceNow数据织物提供软件右尾", "IBM不是GPU/HBM/光模块/NeoCloud，极度乐观收入仍需ARR、订单和客户证据"),
        "风险调整收益": ("2026-06-22 Forward PE 18.75、P/S 3.44，NTM FCF 153-160亿美元且业务粘性高", "上行弹性不如AI主链，Confluent/HashiCorp整合和咨询交付仍有反证"),
        "下行保护优先": ("企业软件、主机TP、咨询客户粘性和150亿美元级FCF提供防守底盘", "Call IV 56.0%，且6/22价格已较6/03明显回撤"),
        "估值消化优先": ("估值低于多数高成长软件和AI硬件，FCF可支撑估值", "收入增速偏中低，若Software mix或并购协同不兑现，消化速度有限"),
        "近端催化优先": ("Q2财报、Software/Data/Automation增速、z17周期、Confluent/HashiCorp并表和ServiceNow 2026H2方案可验证", "缺少单一大额订单或产能放量，催化更偏稳态验证"),
        "价格确认/动量": ("2026-06-03过去两周+35.84%、过去一月+31.62%，曾有明显资金确认", "2026-06-22收盘252.22低于6/03的305.63，旧动量已被回撤削弱"),
        "激进短线": ("56.0% Call IV和企业AI/并购/财报事件仍有可交易波动", "大市值、低右尾、近期回撤，不适合追求最激进短线爆发"),
    }

    out: list[str] = []
    out += [
        "# IBM 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：IBM / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 IBM vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。IBM 的 `+5-7%` NTM 增速和 2026-06-22 价格回撤已做人工校准，避免通用解析器误读为负增长或机械沿用 6/03 旧动量。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。IBM 最强的是自由现金流、企业客户粘性、主机/软件高续约底盘和相对可消化估值，而不是 AI 主链最高收入弹性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 NTM 公司层增长只有中个位数、右尾收入需要产品/客户/ARR继续验证，且 6 月下旬价格已从 6 月初强动量回撤。",
        "- A 最适合的投资者画像：重视现金流、企业软件/主机粘性、稳态 AI 生产化收入和估值纪律的风险调整型资金；适合作为 AI 软件/混合云主题里的防守型核心，而不是高 beta 冲锋仓位。",
        "- A 最不适合的投资者画像：只追求 GPU/HBM/光互联/NeoCloud 级别非线性右尾，或只做短期价格爆发和高动量延续的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常拥有更高 NTM 收入增速、更直接 AI 基础设施收入化、更强订单/RPO或更明确价格动量。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：IBM 位于项目内中上游偏防守位置；它强于大量现金流弱、估值难消化或收入兑现不足的公司，但面对 NVDA、AVGO、MU、CRWV、ORCL、HPE/DELL 等高成长或更直接 AI 基建受益标的时，不是多数思路的最优解。",
        "- 后续最重要跟踪数据：2026Q2 Software/Data/Automation/Red Hat 增速、OpenShift ARR、Consulting GenAI revenue/backlog/signings、Confluent 并表和联合客户、HashiCorp incremental ARR、IBM Z/z17与Transaction Processing、segment margin、FCF、融资应收、ServiceNow 2026H2客户证据，以及 6/22 后价格能否修复 6 月回撤。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "IBM"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "725-740 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润：{a['base_profit']}；现金流：{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI 需求必须转成 IBM 软件订阅、咨询合同、数据平台合同或主机升级；企业AI预算/GPU CapEx不能直接算作 IBM 收入。"]),
        base.row(["最大反证", "公司层增长只有中个位数；Confluent/HashiCorp交叉销售、GenAI咨询验收、z17周期和Software margin都需要继续验证。"]),
        base.row(["近端催化剂", "2026Q2财报、Software/Data/Automation/Red Hat增速、OpenShift ARR、GenAI Consulting backlog、z17周期、Confluent/HashiCorp并表、ServiceNow方案客户证据。"]),
        base.row(["日度市场数据", f"2026-06-22 收盘 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，P/S {fmt_num(fin.get('ps'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"]),
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
        base.row(["直接同业", "与 IBM 在企业软件、混合云、数据库/数据平台、企业AI平台或IT自动化预算中高度重叠，优先比较软件ARR、RPO/backlog、客户迁移、利润率和估值。", "MSFT、ORCL、NTNX", "同业证据权重最高；若一方在ARR/收入兑现、利润质量或估值消化明显胜出，结论力度可上调。"]),
        base.row(["相邻替代", "同属企业AI软件、云平台、SaaS或安全软件资金篮子，但产品和收入模式不完全重叠。", "GOOGL、AMZN、META、ADBE、CRWD、BABA", "重点回答资金只能买一个时，谁的增长质量、估值和风险调整收益更好。"]),
        base.row(["上下游", "一方处在 IBM 企业AI/混合云需求链、算力/数据中心供应链或云客户/基础设施位置，比较利润捕获、议价权和兑现时间。", "NVDA、AVGO、DELL、HPE、SMCI、EQIX、VRT、ETN", "不把上游稀缺或下游收入规模机械等同为更好，必须看收入化、估值和反证。"]),
        base.row(["跨赛道", "半导体设备、材料、工业、公用事业等与 IBM 业务差异大但可作为项目内资金配置替代。", "ASML、TSM、LIN、TMO、ECL、CAT", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
                    majority_text(comparison["ac"], comparison["bc"], comparison["nc"]),  # type: ignore[arg-type]
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
        need = "需要 IBM 披露更高的 Software/Red Hat/Data/Automation ARR、GenAI咨询收入转化和并购交叉销售订单，并修复6月价格回撤。"
        if comparison["rel"] == "跨赛道":
            need = "需要 IBM 用更强现金流、估值和可见催化抵消该跨赛道标的的增长或价格优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提高收入确认可信度、现金流质量和估值消化能力，或出现明确订单/指引上修。"
        if float(b["scores"]["右尾弹性优先"]) > float(a["scores"]["右尾弹性优先"]):  # type: ignore[index]
            need = "需要 B 把右尾叙事转成可确认收入/利润，并降低估值、IV或现金流反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：从 `分析报告/公司评估/结果/` 根层读取 `*_收入传导估值评估_*.md`，同一 Ticker 取文件名日期最新版本；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        "- 公司 A 日度数据摘录：2026-06-22 收盘价 `252.22` 美元，市值 `$237.06B`，TTM PE `22.30`，Forward PE `18.75`，P/S `3.44`，EV/EBITDA `17.59`，Call IV `56.0%`，Put IV `50.9%`；2026-06-03 过去两周 `+35.84%`、过去一月 `+31.62%`；2026-06-04 三段 SOXX 压力窗口累计 `-22.41%`；另按 2026-06-22 收盘相对 2026-06-03 收盘 `305.63` 计算，6月中下旬回撤约 `-17.48%`，因此价格确认/动量列对 6/03 旧动量做保守折扣。",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/云算力_IDC_AI软件平台/IBM_International Business Machines_公司调研_2026-06-12.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。IBM 评估附录主要外部来源包括 IBM 1Q 2026 earnings、IBM 4Q 2025 earnings、IBM 2025 Annual Report、Confluent/HashiCorp/DataStax/Red Hat AI/ServiceNow/z17 官方公告。",
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
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "ibm_tiers": companies[TARGET]["tiers"],
        "ibm_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
