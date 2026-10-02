from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_toely_company_comparison as template


ROOT = Path(r"D:\investment\基本面")
TARGET = "UMC"
TARGET_NAME = "United Microelectronics 联华电子"
REPORT_DATE = "2026-06-23"
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "UMC_逐家公司投资思路对比_2026-06-23.md"

base = template.base
template.TARGET = TARGET
template.REPORT_DATE = REPORT_DATE
template.OUT_PATH = OUT_PATH
base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH
base.FIN_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-23.md"
base.MOM2W_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去两周_2026-06-23.md"
base.MOM1M_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去1个月_2026-06-23.md"
base.SOXX_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md"

STRATS = template.STRATS
TAG_ORDER = template.TAG_ORDER
TIER_VAL = base.TIER_VAL

DIRECT_FOUNDRY_PEERS = {"GFS", "INTC", "TSM", "TSEM"}

FOUNDRY_SUPPLY_CHAIN = {
    "ACLS",
    "ACMR",
    "AEIS",
    "AMAT",
    "ASGLY",
    "ASMIY",
    "ASML",
    "AXTI",
    "ENTG",
    "HOCPY",
    "ICHR",
    "KLAC",
    "LRCX",
    "MKSI",
    "MTRN",
    "NVMI",
    "PLAB",
    "Q",
    "ROG",
    "SHECY",
    "TOELY",
    "UCTT",
    "VECO",
}

PACKAGING_TEST = {
    "AEHR",
    "AMKR",
    "ASMVY",
    "ASX",
    "ATEYY",
    "BESIY",
    "CAMT",
    "COHU",
    "FORM",
    "IMOS",
    "KEYS",
    "KLIC",
    "MICLF",
    "ONTO",
    "TER",
}

MATURE_ANALOG_POWER = {
    "ADI",
    "IFNNY",
    "MCHP",
    "MPWR",
    "ON",
    "POWI",
    "QCOM",
    "SIMO",
    "STM",
    "TXN",
    "VICR",
    "VSH",
}

AI_OPTICAL_SERVER = {
    "AAOI",
    "ALAB",
    "AMD",
    "ANET",
    "APH",
    "AVGO",
    "BDC",
    "BELFB",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "DELL",
    "FLEX",
    "FN",
    "GLW",
    "HPE",
    "JBL",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "NVDA",
    "PENG",
    "POET",
    "RMBS",
    "SANM",
    "SITM",
    "SMCI",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    template.fix_growth_ranges(companies)
    base.score_companies(companies)

    # UMC calibration: the base parser underweights UMC because it has no RPO,
    # bookings or product backlog table. The formal assessment provides hard
    # Q2 shipment/ASP/GM/utilization guidance and April-May sales evidence, so
    # NTM and near-term visibility should not be treated as bottom-tier. Offsets
    # are mature-node price pressure, indirect AI exposure, high listed IV after
    # a sharp price move, and weak evidence for SiPh/TFLN/12nm revenue in NTM.
    a = companies[TARGET]
    overrides = {
        "NTM兑现优先": 74.0,
        "右尾弹性优先": 63.0,
        "风险调整收益": 55.0,
        "下行保护优先": 84.0,
        "估值消化优先": 60.0,
        "近端催化优先": 66.0,
        "价格确认/动量": 97.0,
        "激进短线": 92.5,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]

    template.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_FOUNDRY_PEERS:
        return "直接同业"
    if ticker in FOUNDRY_SUPPLY_CHAIN or ticker in PACKAGING_TEST:
        return "上下游"
    if ticker in MATURE_ANALOG_POWER or ticker in AI_OPTICAL_SERVER:
        return "相邻替代"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    if category in base.HIGH_GROWTH_CATS or category in base.INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A有Q2指引和4-5月销售锚",
            "右尾弹性优先": "A有BCD/SiPh/22nm恢复期权",
            "风险调整收益": "A现金流和压力窗口更均衡",
            "下行保护优先": "A压力窗口回撤小且FCF正向",
            "估值消化优先": "A恢复型收入可部分消化估值",
            "近端催化优先": "A六月销售和Q2财报验证近",
            "价格确认/动量": "A两周和一月价格确认最强",
            "激进短线": "A高IV叠加强动量适合进攻",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入/RPO或订单兑现更硬",
            "右尾弹性优先": "B直接AI或小基数右尾更大",
            "风险调整收益": "B上行与估值组合更优",
            "下行保护优先": "B现金流/低IV/低估值更防守",
            "估值消化优先": "B估值消化压力更低",
            "近端催化优先": "B近端订单或产品催化更强",
            "价格确认/动量": "B价格趋势确认更稳或更强",
            "激进短线": "B短线beta和叙事更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "估值和安全边际接近"
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
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 12:  # type: ignore[index,operator]
            return "UMC 的压力窗口回撤、成熟节点现金流和低capex提供更好防守底盘。"
        if a["scores"]["价格确认/动量"] - b["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
            return "UMC 过去两周和一月价格确认显著强于 B。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 8:  # type: ignore[index,operator]
            return "UMC 的Q2指引和4-5月销售让近端收入兑现更清楚。"
        return "UMC 的成熟特色制程恢复、防守和动量组合更好，B 的优势不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI收入、小基数或非线性右尾明显强于 UMC。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/RPO/订单兑现证据更强。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的当前估值更容易被NTM业绩消化。"
    if b["scores"]["风险调整收益"] - a["scores"]["风险调整收益"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的上行空间、估值和现金流组合优于 UMC。"
    return f"{b['ticker']} 在多数投资思路下比 UMC 更符合项目内资金配置目标。"


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
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["下行保护优先"] - x["b"]["scores"]["下行保护优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:45]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:45]  # type: ignore[operator]
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker]["fin"] or not companies[ticker]["fin"].get("price")  # type: ignore[union-attr]
    ]

    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_snapshot = (
        f"2026-06-23 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}（USD/TWD币种错配，日度文件标为bad，不直接作为估值优势），"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-23 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-23 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "2026Q1收入NT$61.04B，Q2指引出货高个位数增长、ASP低个位数增长、GM约30%，4-5月销售NT$45.61B",
            "NTM基准增速12%-18%，缺backlog/bookings/RPO，主要是恢复型兑现而非高订单爆发",
        ),
        "右尾弹性优先": (
            "BCD/Smart Power、22nm specialty、SiPh/iSiPP300/TFLN、28nm eNVM和12nm/14nm远期期权提供上限",
            "AI主die、HBM和高端CoWoS不由UMC主导；SiPh/TFLN和12nm缺订单、客户名和量产收入",
        ),
        "风险调整收益": (
            "基准GM 29.5%-31.5%、OPM 18.5%-21%、净利润NT$48-58B，2026 capex US$1.5B后仍应正FCF",
            "Forward PE 32.17且股价一月+44.02%，成熟节点价格竞争和高IV降低赔率质量",
        ),
        "下行保护优先": (
            "三段SOXX压力窗口累计-28.61%，明显好于多数半导体高beta；成熟特色制程和正FCF提供底盘",
            "Call/Put IV约91%，估值不低；若利用率回到70%区间或ASP下行，防守结论会削弱",
        ),
        "估值消化优先": (
            "NTM基准收入NT$270-285B、净利润NT$48-58B，若Q2/Q3兑现可部分支撑恢复定价",
            "Forward PE 32.17高于成熟代工通常舒适区，且P/S因币种错配不可用于证明便宜",
        ),
        "近端催化优先": (
            "2026年6月销售、Q2实际、Q3指引、利用率、ASP、22nm tape-out转量产和BCD/SiPh订单均在1-2季验证",
            "近端催化多为验证恢复和产品认证，不是高端AI订单或大额RPO重估",
        ),
        "价格确认/动量": (
            "过去两周+31.99%、过去一月+44.02%，2026-06-23日度区间涨幅处于项目前列",
            "价格已很强，需防范短线过热；上涨必须由Q2、月销售和毛利率继续确认",
        ),
        "激进短线": (
            "91%左右IV、强两周/一月动量、成熟代工恢复和AI power/optical叙事可支持短线进攻",
            "市值约658亿美元且右尾间接，短线爆发性弱于小基数光互联、NeoCloud、存储和核能/电力链",
        ),
    }

    out: list[str] = []
    out += [
        "# UMC 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：UMC / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-23；过去两周和过去1个月区间涨跌为 2026-06-23；SOXX 三段压力窗口为 2026-06-23",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 UMC vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。UMC 的比较优势集中在价格确认/动量、下行保护和NTM兑现：过去两周+31.99%、过去一月+44.02%、三段SOXX压力窗口累计-28.61%，同时Q2指引和4-5月销售给恢复型收入提供证据。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。UMC 的短板是估值消化、右尾弹性和激进短线：AI暴露多为BCD/Smart Power、硅光/TFLN和控制器等间接传导，Forward PE 32.17且IV约91%，不能按先进逻辑、AI主芯片或小基数高beta资产定价。",
        "- A 最适合的投资者画像：想买成熟/特色代工周期恢复、重视压力窗口回撤和价格确认、愿意用较高IV承受短线进攻的资金。",
        "- A 最不适合的投资者画像：只追求最强AI直接收入、最大非线性右尾、最硬RPO/backlog、最低估值或要求长期利润池处在先进逻辑/AI主芯片核心的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常在直接AI收入、小基数右尾、订单/RPO、估值消化或风险调整收益上压过 UMC。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：UMC 不是全项目高增长核心，更像成熟特色代工恢复叠加强价格确认的交易型标的；在防守和动量列很有竞争力，但在长期增长质量、右尾和估值消化上落后于多数AI核心链公司。",
        "- 后续最重要跟踪数据：2026年6月销售、2026Q2收入/GM/OPM/利用率、Q3出货与ASP指引、22nm tape-out转量产、BCD/Smart Power客户订单或价格、SiPh/TFLN模块级认证、12nm/14nm是否出现客户pilot、capex是否维持US$1.5B、成熟节点ASP与中国供给压力。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "UMC"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "NT$270-285B"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI数据中心需求主要通过BCD/Smart Power、SiPh/TFLN、控制器和eNVM间接传导；GPU/ASIC主die、HBM和高端CoWoS不由UMC主导。"]),
        base.row(["最大反证", "成熟节点供给过剩和价格竞争、22nm tape-out未转量产、SiPh/TFLN缺客户量产收入、14nm/12nm当前收入为0、无backlog/bookings披露。"]),
        base.row(["近端催化剂", "2026年6月销售、Q2实际收入/GM/利用率、Q3指引、22nm转量产、55nm BCD/Smart Power客户订单、SiPh/TFLN认证。"]),
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
        base.row(["直接同业", "同属晶圆代工/IDM foundry替代资金池，优先看制程代际、利用率、ASP、成熟节点价格、客户质量、毛利率、capex效率和同业估值。", "TSM、GFS、TSEM、INTC", "同业证据权重最高；UMC在成熟特色制程与防守性上可胜，但遇到先进逻辑或AI制造硬证据时结论力度向B倾斜。"]),
        base.row(["相邻替代", "同属半导体、AI硬件、模拟/功率/光互联或AI基础设施资金篮子，但收入模式不完全重叠。", "ON、TXN、MPWR、NVDA、AVGO、CRDO、ANET、DELL", "重点回答资金只能买一个时，谁的增长质量、估值消化、右尾和近端催化更好；档位接近时保守使用微倾向。"]),
        base.row(["上下游", "一方处在UMC设备、材料、封测、客户或需求链，重点看利润池位置、议价权、瓶颈稀缺性和收入确认链条。", "AMAT、ASML、TOELY、LRCX、AMKR、ASX、ENTG、KLAC、TER", "不把上游设备景气或下游AI收入自动等同胜出；必须看谁能捕获利润并消化估值。"]),
        base.row(["跨赛道", "业务差异大但作为项目内资金配置替代，比较风险调整收益、下行保护、估值消化和催化可见度。", "LIN、TMO、DHR、CAT、MSI、RYCEY", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        need = "需要 UMC 证明Q2/Q3收入、利用率、ASP和毛利率持续上修，并把BCD/SiPh/22nm机会转成客户订单和收入。"
        if comparison["rel"] == "直接同业":
            need = "需要 UMC 证明成熟特色制程、价格纪律、FCF和防守性足以抵消该同业的先进制程或增长优势。"
        elif comparison["rel"] == "上下游":
            need = "需要 UMC 证明比该上下游公司更能捕获AI半导体利润池，而不只是间接受益。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 UMC 用更强现金流、估值消化或压力期表现抵消跨赛道标的的低波动/防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更强NTM收入利润兑现、或更低估值/更好现金流来抵消UMC的防守和价格确认。"
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
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-23.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md`。",
        f"- 日度金融数据覆盖：2026-06-23 金融快照覆盖 189 家；本次公司评估全集为 {n} 家，因此缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot} 备注：UMC 行内 `交易货币/财报货币不一致: USD/TWD`、`P/S:bad(currency_mismatch)`，因此估值消化列主要参考Forward PE、利润增长、现金流和价格透支，不直接使用P/S强行比较。",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/晶圆制造_前道设备/UMC_United Microelectronics 联华电子_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_特种晶圆代工_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_先进逻辑晶圆代工和封装_2026-06-11.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 自动化脚本：`scripts/generate_umc_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对UMC的Q2指引、4-5月销售、成熟特色制程、BCD/SiPh间接AI暴露、压力窗口、估值错配和价格动量做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
                "umc_tiers": companies[TARGET]["tiers"],
                "umc_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
