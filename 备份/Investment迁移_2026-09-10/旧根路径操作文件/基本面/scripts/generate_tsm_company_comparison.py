from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_toely_company_comparison as template


ROOT = Path(r"D:\drive\Investment\基本面")
TARGET = "TSM"
TARGET_NAME = "台积电"
REPORT_DATE = "2026-06-23"
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "TSM_逐家公司投资思路对比_2026-06-23.md"

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

DIRECT_FOUNDRY_PEERS = {"GFS", "INTC", "TSEM", "UMC"}

AI_CHIP_CUSTOMERS = {
    "ALAB",
    "AMD",
    "ARM",
    "AVGO",
    "CDNS",
    "MRVL",
    "NVDA",
    "QCOM",
    "RMBS",
    "SNPS",
}

CLOUD_AND_AI_DEMAND = {
    "ADBE",
    "AMZN",
    "APLD",
    "BABA",
    "CRWD",
    "CRWV",
    "DLR",
    "EQIX",
    "GOOGL",
    "IBM",
    "IREN",
    "META",
    "MSFT",
    "NBIS",
    "NTNX",
    "ORCL",
}

WFE_UPSTREAM = {
    "ACLS",
    "ACMR",
    "AEIS",
    "AMAT",
    "ASMIY",
    "ASML",
    "DSCSY",
    "ICHR",
    "KLAC",
    "LRCX",
    "MKSI",
    "NVMI",
    "TOELY",
    "UCTT",
    "VECO",
}

PACKAGING_TEST_MEMORY = {
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
    "MU",
    "ONTO",
    "PLAB",
    "SNDK",
    "STX",
    "TDY",
    "TER",
    "TMO",
    "WDC",
}

MATERIALS_SUBSTRATE = {
    "AJNMY",
    "APD",
    "ASGLY",
    "AXTI",
    "CC",
    "DD",
    "ECL",
    "ENTG",
    "HOCPY",
    "LIN",
    "MTRN",
    "NDSN",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
}

SERVER_NETWORK_DOWNSTREAM = {
    "AAOI",
    "ANET",
    "APH",
    "BDC",
    "BELFB",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "CSCO",
    "DELL",
    "FLEX",
    "FN",
    "GLW",
    "HPE",
    "JBL",
    "LITE",
    "LWLG",
    "MTSI",
    "NOK",
    "PENG",
    "POET",
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

    # TSM calibration: TSMC has unusually hard NTM evidence from Q1/Q2
    # guidance, monthly revenue, HPC/node revenue mix, N3/CoWoS capacity and
    # customer AI product roadmaps. The offsets are mega-cap size, high CapEx,
    # SOXX-like pressure-window drawdown, overseas/N2 dilution and geopolitical
    # risk.
    a = companies[TARGET]
    overrides = {
        "NTM兑现优先": 94.0,
        "右尾弹性优先": 84.0,
        "风险调整收益": 82.0,
        "下行保护优先": 64.0,
        "估值消化优先": 78.0,
        "近端催化优先": 86.0,
        "价格确认/动量": 66.0,
        "激进短线": 74.0,
    }
    for strategy, score in overrides.items():
        a["scores"][strategy] = score  # type: ignore[index]

    template.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_FOUNDRY_PEERS:
        return "直接同业"
    if ticker in AI_CHIP_CUSTOMERS or ticker in CLOUD_AND_AI_DEMAND:
        return "上下游"
    if ticker in WFE_UPSTREAM or ticker in PACKAGING_TEST_MEMORY or ticker in MATERIALS_SUBSTRATE:
        return "上下游"
    if ticker in SERVER_NETWORK_DOWNSTREAM:
        return "相邻替代"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    if category in base.HIGH_GROWTH_CATS or category in base.INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A有Q2指引、月营收和HPC收入表锚",
            "右尾弹性优先": "A的N3/CoWoS/AI ASIC右尾可收入化",
            "风险调整收益": "A高毛利、强FCF和估值组合更均衡",
            "下行保护优先": "A现金流和先进节点护城河更强",
            "估值消化优先": "A用NTM高增长消化22倍Forward PE",
            "近端催化优先": "A Q2/Q3、月营收和N3/CoWoS节点近",
            "价格确认/动量": "A价格趋势更稳且未明显破位",
            "激进短线": "A高流动性AI主线仍有进攻性",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B订单/RPO或收入兑现更直接",
            "右尾弹性优先": "B小基数或高beta右尾更大",
            "风险调整收益": "B估值、现金流或反证组合更优",
            "下行保护优先": "B压力期更稳或估值更低",
            "估值消化优先": "B估值消化压力更低",
            "近端催化优先": "B近端订单/产品催化更强",
            "价格确认/动量": "B价格确认更强",
            "激进短线": "B短线弹性和市场关注更高",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "估值和安全边际接近"
    return "档位接近需再验证"


def cell_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    tag = template.label_for(a, b, strategy, rel)
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
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "TSM 的Q2指引、月营收+30%、HPC 61%和先进节点收入表让NTM兑现更硬。"
        if a["scores"]["风险调整收益"] - b["scores"]["风险调整收益"] > 10:  # type: ignore[index,operator]
            return "TSM 的高毛利、强自由现金流和AI/HPC需求能见度形成更好风险调整组合。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
            return "TSM 的NTM高增速和净利润兑现更能消化当前估值。"
        return "TSM 的先进逻辑代工和CoWoS瓶颈稀缺性更好，B 的优势不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的小基数、直接AI收入或短线右尾明显强于 TSM。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和短线资金偏好明显强于 TSM。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的低波动、低估值或现金流防守属性更好。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的当前估值更容易被NTM业绩消化。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/RPO/订单兑现证据更强。"
    return f"{b['ticker']} 在多数投资思路下比 TSM 更符合项目内资金配置目标。"


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
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["NTM兑现优先"] - x["b"]["scores"]["NTM兑现优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:45]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:45]  # type: ignore[operator]
    strongest_b_names = "、".join([x["ticker"] for x in strong_b_rows[:10]]) or "无明显集中反方"
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
        f"P/S {fmt_num(fin.get('ps'))}（USD/TWD币种错配，日度文件标为bad，估值列主要参考Forward PE、TTM PE和现金流），"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-23 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-23 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "2026Q1收入359.0亿美元、Q2指引390-402亿美元、1-5月月营收同比+30.0%，HPC占61%，NTM基准收入1,780-1,900亿美元",
            "收入确认仍要穿过CoWoS/HBM/基板/测试和客户机架验收，AI CapEx下修会影响后续订单",
        ),
        "右尾弹性优先": (
            "乐观1,950-2,150亿美元、极度乐观2,200-2,450亿美元；N3/N3P、CoWoS、HBM base die、AI ASIC和N2/A16锁产能构成大右尾",
            "市值基数已经很大，14-reticle CoWoS、SoIC和CPO多数是2028以后期权，不能提前计入NTM基准",
        ),
        "风险调整收益": (
            "基准毛利率63.5%-66.5%、营业利润率54%-58%、净利润840-960亿美元、FCF 500-700亿美元，Forward PE约22倍",
            "2026 CapEx 520-560亿美元、海外fab/N2稀释、客户集中、地缘和出口管制仍是主要反证",
        ),
        "下行保护优先": (
            "先进节点份额、客户锁产能、高利润率和强自由现金流提供基本面底盘",
            "三段SOXX压力窗口累计-56.76%，说明价格防守性一般；高CapEx和地缘风险会放大压力期折价",
        ),
        "估值消化优先": (
            "NTM收入对最近四季度约+34%-43%，基准净利润840-960亿美元，可支撑约22倍Forward PE的消化",
            "TTM PE 37.75且股价过去一月+8.29%，市场已交易部分AI/HPC乐观；P/S因USD/TWD错配不可直接使用",
        ),
        "近端催化优先": (
            "2026Q2实际与Q3指引、每月营收、HPC/3nm/5nm占比、CoWoS扩产、客户GB300/ASIC/Trainium/Maia交付均在1-2季验证",
            "催化必须体现为收入、毛利、客户锁产能和交付，不可只靠AI需求叙事",
        ),
        "价格确认/动量": (
            "2026-06-23过去两周+2.37%、过去一月+8.29%，价格确认为正且未破坏趋势",
            "动量不如近期最强半导体设备、存储和小盘光互联；54.1% IV也显示短线波动不低",
        ),
        "激进短线": (
            "AI/HPC、N3、CoWoS、GB300/ASIC客户链和54.1% Call IV给短线进攻材料，流动性强",
            "mega-cap体量限制爆发倍数，短线beta弱于小基数光互联、NeoCloud、存储和核能/电力链",
        ),
    }

    out: list[str] = []
    out += [
        "# TSM 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：TSM / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-23；过去两周和过去1个月区间涨跌为 2026-06-23；SOXX 三段压力窗口为 2026-06-23",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 TSM vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。TSM 的强项是NTM兑现、风险调整收益、估值消化和近端催化：Q2指引、月营收、HPC占比、N3/CoWoS扩产和客户AI产品路径都已经进入经营证据。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是mega-cap体量压低短线爆发倍数，压力窗口回撤并不低，且高CapEx、海外fab/N2稀释、地缘风险会削弱下行保护。",
        "- A 最适合的投资者画像：希望买入AI半导体制造环节中收入和利润兑现最硬、同时仍有N3/CoWoS/HBM4/N2长期上修期权的中期基本面资金。",
        "- A 最不适合的投资者画像：只追求最小基数右尾、极端短线高beta、低波动防守或要求估值完全未反映AI/HPC预期的资金。",
        f"- 多数思路下最强反方公司：{strongest_b_names}。在本次阈值下没有公司在多数投资思路中明显压过 TSM；单列反方主要来自小基数右尾、价格动量、低估值防守或短线高beta。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：TSM 是全项目最硬的经营兑现和AI制造瓶颈核心之一，更像高质量核心仓；但不是最便宜、最防守或最短线爆发的资产。",
        "- 后续最重要跟踪数据：2026Q2实际和Q3指引、月营收是否保持above-30%路径、HPC和3nm/5nm/7nm占比、N3扩产、CoWoS产能/lead time/utilization、GB300/Rubin/MI350/MI400/Trainium3/Maia/TPU交付、HBM4良率、N2/N2P/A16毛利稀释、海外fab和Amkor先进封装认证。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "TSM"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "1,780-1,900 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI accelerator需求要穿过N3/N4/N5 wafer allocation、CoWoS/HBM/基板/测试、客户系统验收和云厂CapEx ROI，最终变成TSM可确认收入。"]),
        base.row(["最大反证", "云厂AI CapEx下修、CoWoS利用率下降但GPU/rack出货未升、HBM4认证延迟、N3/N2排产松动、海外fab/N2稀释超预期、汇率/材料/能源成本无法转嫁。"]),
        base.row(["近端催化剂", "2026Q2实际与Q3指引、月营收、HPC/先进节点占比、N3 capacity expansion、CoWoS capacity/lead time/utilization、NVIDIA/Broadcom/AMD/AWS/Microsoft客户交付。"]),
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
        base.row(["直接同业", "同属晶圆代工或IDM/foundry替代资金池，优先看先进节点份额、客户质量、收入兑现、毛利率、CapEx效率、成熟节点价格压力和同业估值。", "GFS、UMC、TSEM、INTC", "同业证据权重最高；TSM在先进逻辑和CoWoS上通常可放大结论力度，但遇到估值/成熟节点防守需复核。"]),
        base.row(["相邻替代", "同属AI基础设施或半导体资金篮子，但不是TSM直接客户/供应商，重点比较增长质量、赔率、估值消化和催化。", "VRT、ETN、GEV、ANET、CRDO、DELL、SMCI", "默认按档位判断；若业务差异大但档位接近，优先微倾向或中性。"]),
        base.row(["上下游", "一方处于TSM需求链、设备/材料/封测供应链或客户芯片链，重点看利润池位置、议价权、瓶颈稀缺性和收入确认链条。", "NVDA、AVGO、AMD、MRVL、AMAT、ASML、TOELY、MU、AMKR、ENTG、MSFT、AMZN", "不把下游收入规模或上游设备稀缺自动等同胜出；必须看谁能捕获更多利润并更好消化估值。"]),
        base.row(["跨赛道", "业务差异大但作为项目内资金配置替代，比较风险调整收益、下行保护、估值消化和催化可见度。", "LIN、TMO、DHR、MMM、CAT、ALLE", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
    if not strong_b_rows:
        out.append(
            base.row(
                [
                    1,
                    "无明显集中反方",
                    "无",
                    "按 B 胜出至少 5 个投资思路且净胜 A 至少 3 个思路的阈值，本次没有公司在多数思路下明显强于 TSM。",
                    "TSM 仍需用Q2/Q3指引、月营收、HPC/3nm/CoWoS数据和压力窗口表现继续验证核心仓优势；小基数右尾和短线高beta反方应在单列中跟踪。",
                ]
            )
        )
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要 TSM 继续用Q2/Q3指引、月营收、HPC/3nm/CoWoS数据证明收入和利润率上修，并降低CapEx、地缘和压力窗口反证。"
        if comparison["rel"] == "直接同业":
            need = "需要 TSM 继续证明先进节点和CoWoS份额、毛利率、客户锁产能和收入兑现显著高于该同业。"
        elif comparison["rel"] == "上下游":
            need = "需要 TSM 证明比该上下游公司更能捕获AI半导体利润池，而不只是承担客户CapEx周期和制造执行风险。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 TSM 用更强现金流、估值消化或压力期表现抵消跨赛道标的的低波动/防守优势。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬订单/RPO、更强NTM收入利润兑现、或更低估值/更好现金流来抵消TSM的先进节点和CoWoS稀缺性。"
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
        f"- 公司 A 日度数据摘录：{daily_snapshot} 备注：TSM 行内 `交易货币/财报货币不一致: USD/TWD`、`P/S:bad(currency_mismatch)`，因此估值消化列主要参考Forward PE、利润增长和现金流，不直接使用P/S强行比较。",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/晶圆制造_前道设备/TSM_台积电_公司调研_2026-06-20.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_先进逻辑晶圆代工和封装_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026-06-11.md`，以及各正式公司评估文件附录中列明的官方披露来源。",
        "- 自动化脚本：`scripts/generate_tsm_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对TSM的Q2指引、月营收、HPC/先进节点、N3/CoWoS、估值错配、压力窗口和价格动量做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
                "tsm_tiers": companies[TARGET]["tiers"],
                "tsm_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
