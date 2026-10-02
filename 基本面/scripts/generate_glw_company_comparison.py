from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated
import generate_dell_company_comparison as helper
import generate_cls_company_comparison as cls_calibrated
import generate_flex_company_comparison as flex_calibrated


TARGET = "GLW"
TARGET_NAME = "Corning"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "GLW_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {"APH", "BDC", "BELFB", "TEL", "SMTOY"}
OPTICAL_CHAIN = {
    "AAOI",
    "ALAB",
    "ANET",
    "APH",
    "AVGO",
    "BDC",
    "BELFB",
    "CIEN",
    "COHR",
    "CRDO",
    "CSCO",
    "FN",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "NOK",
    "POET",
    "SITM",
    "SMTC",
    "SMTOY",
    "TEL",
    "VIAV",
    "VISN",
}
SERVER_CLOUD_CUSTOMERS = {
    "ADBE",
    "AMZN",
    "APLD",
    "BABA",
    "CRWD",
    "CRWV",
    "DELL",
    "DLR",
    "EQIX",
    "FLEX",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "JBL",
    "META",
    "MSFT",
    "NBIS",
    "NTNX",
    "ORCL",
    "PENG",
    "SANM",
    "SMCI",
}
AI_COMPUTE_UPSTREAM = {
    "ADI",
    "AMD",
    "ARM",
    "AVGO",
    "CDNS",
    "INTC",
    "MCHP",
    "MXL",
    "NVDA",
    "ON",
    "QCOM",
    "SNPS",
    "STM",
    "TXN",
}
POWER_COOLING_CHAIN = {
    "AAON",
    "ABBNY",
    "AEIS",
    "AEP",
    "BE",
    "BWXT",
    "CARR",
    "CEG",
    "CMI",
    "DKILY",
    "DTE",
    "EME",
    "ENS",
    "ET",
    "ETN",
    "ETR",
    "FCEL",
    "FIX",
    "FLNC",
    "GEV",
    "GNRC",
    "HTHIY",
    "HUBB",
    "IESC",
    "IFNNY",
    "JCI",
    "MIELY",
    "MOD",
    "MRAAY",
    "MYRG",
    "NVT",
    "OKLO",
    "POWI",
    "POWL",
    "PSIX",
    "PWR",
    "SMR",
    "TT",
    "TTDKY",
    "VICR",
    "VRT",
    "VST",
}

EXTRA_SCORE_FLOORS = {
    **calibrated.SCORE_FLOORS,
    **helper.EXTRA_SCORE_FLOORS,
    **cls_calibrated.EXTRA_SCORE_FLOORS,
    "CLS": cls_calibrated.CLS_SCORE_OVERRIDES,
    "DELL": helper.DELL_OVERRIDES,
    "FLEX": flex_calibrated.FLEX_OVERRIDES,
    "FN": {
        "NTM兑现优先": 78,
        "右尾弹性优先": 82,
        "风险调整收益": 54,
        "下行保护优先": 58,
        "估值消化优先": 66,
        "近端催化优先": 76,
        "价格确认/动量": 66,
        "激进短线": 84,
    },
    "CRDO": {
        "NTM兑现优先": 88,
        "右尾弹性优先": 98,
        "风险调整收益": 62,
        "下行保护优先": 48,
        "估值消化优先": 72,
        "近端催化优先": 86,
        "价格确认/动量": 78,
        "激进短线": 98,
    },
    "COHR": {
        "NTM兑现优先": 82,
        "右尾弹性优先": 100,
        "风险调整收益": 54,
        "下行保护优先": 48,
        "估值消化优先": 55,
        "近端催化优先": 78,
        "价格确认/动量": 82,
        "激进短线": 100,
    },
    "AAOI": {
        "NTM兑现优先": 75,
        "右尾弹性优先": 94,
        "风险调整收益": 50,
        "下行保护优先": 38,
        "估值消化优先": 58,
        "近端催化优先": 78,
        "激进短线": 96,
    },
    "LITE": {
        "NTM兑现优先": 78,
        "右尾弹性优先": 86,
        "风险调整收益": 48,
        "下行保护优先": 45,
        "估值消化优先": 48,
        "近端催化优先": 72,
        "激进短线": 86,
    },
    "POET": {
        "右尾弹性优先": 90,
        "下行保护优先": 30,
        "激进短线": 98,
    },
    "LWLG": {
        "右尾弹性优先": 88,
        "下行保护优先": 32,
        "激进短线": 96,
    },
}

GLW_OVERRIDES = {
    "NTM兑现优先": 78.0,
    "右尾弹性优先": 78.0,
    "风险调整收益": 52.0,
    "下行保护优先": 56.0,
    "估值消化优先": 54.0,
    "近端催化优先": 78.0,
    "价格确认/动量": 76.0,
    "激进短线": 84.0,
}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    calibrated.fix_growth_ranges(companies)
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    for ticker, floors in EXTRA_SCORE_FLOORS.items():
        company = companies.get(ticker)
        if not company or ticker == TARGET:
            continue
        for strategy, floor in floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[assignment]
            company["scores"][strategy] = max(float(current), float(floor))  # type: ignore[index]

    for strategy, score in GLW_OVERRIDES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score  # type: ignore[index]

    calibrated.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in OPTICAL_CHAIN or category == "AI网络_光互联_连接器":
        return "相邻替代"
    if ticker in AI_COMPUTE_UPSTREAM or ticker in SERVER_CLOUD_CUSTOMERS or category in {"AI计算芯片_EDA_IP_custom_ASIC", "AI服务器_存储_EMS", "云算力_IDC_AI软件平台"}:
        return "上下游"
    if ticker in POWER_COOLING_CHAIN or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, winner: str, b: dict[str, object], rel: str) -> str:
    ticker = str(b["ticker"])
    category = str(b.get("category", ""))
    if winner == "A":
        return {
            "NTM兑现优先": "A有多家hyperscaler长协和Optical收入锚",
            "右尾弹性优先": "A的AI光纤/CPO/高密度连接上限更直接",
            "风险调整收益": "A成长与多业务底盘更均衡",
            "下行保护优先": "A有Glass/Auto利润底座和长协支撑",
            "估值消化优先": "A可用Optical高增和利润率改善消化估值",
            "近端催化优先": "A有Amazon/Meta/NVIDIA和Q2-Q3验证",
            "价格确认/动量": "A价格已确认光纤瓶颈重估",
            "激进短线": "A高IV叠加光纤瓶颈交易",
        }[strategy]
    if winner == "B":
        if ticker in DIRECT_PEERS or category == "AI网络_光互联_连接器":
            return {
                "NTM兑现优先": "B同业订单或利润兑现更硬",
                "右尾弹性优先": "B同业小基数或利润池更弹",
                "风险调整收益": "B同业赔率或估值组合更好",
                "下行保护优先": "B同业现金流/估值/波动更稳",
                "估值消化优先": "B同业倍数更容易被业绩消化",
                "近端催化优先": "B同业产品/订单催化更密集",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业短线爆发力更高",
            }[strategy]
        if ticker in AI_COMPUTE_UPSTREAM or category in {"AI计算芯片_EDA_IP_custom_ASIC"}:
            return {
                "NTM兑现优先": "B上游AI主链收入兑现更硬",
                "右尾弹性优先": "B芯片/IP瓶颈利润右尾更大",
                "风险调整收益": "B利润留存覆盖执行风险更好",
                "下行保护优先": "B现金流或规模防守更强",
                "估值消化优先": "B利润弹性更能消化估值",
                "近端催化优先": "B产品/订单催化更直接",
                "价格确认/动量": "B价格趋势和资金偏好更强",
                "激进短线": "B高beta AI主线更适合进攻",
            }[strategy]
        if ticker in SERVER_CLOUD_CUSTOMERS or category in {"AI服务器_存储_EMS", "云算力_IDC_AI软件平台"}:
            return {
                "NTM兑现优先": "B云/服务器收入确认更直接",
                "右尾弹性优先": "B平台或AI云右尾更大",
                "风险调整收益": "B盈利质量或资本结构更好",
                "下行保护优先": "B现金流、规模或客户粘性更稳",
                "估值消化优先": "B利润留存更能支撑估值",
                "近端催化优先": "B云订单或AI交付催化更近",
                "价格确认/动量": "B价格确认更强",
                "激进短线": "B市场关注和波动更集中",
            }[strategy]
        if ticker in POWER_COOLING_CHAIN or category in INFRA_CATS:
            return {
                "NTM兑现优先": "B电力/机电backlog兑现更清楚",
                "右尾弹性优先": "B设施瓶颈右尾更直接",
                "风险调整收益": "B订单和现金流赔率更好",
                "下行保护优先": "B防御现金流或订单粘性更强",
                "估值消化优先": "B用订单兑现消化估值更容易",
                "近端催化优先": "B订单/产能/财报催化更近",
                "价格确认/动量": "B价格趋势更强",
                "激进短线": "B电气化交易弹性更高",
            }[strategy]
        return {
            "NTM兑现优先": "B未来12个月兑现证据更直接",
            "右尾弹性优先": "B极端情景上行更大",
            "风险调整收益": "B上行和下行组合更好",
            "下行保护优先": "B资产质量或估值缓冲更好",
            "估值消化优先": "B当前估值更容易被业绩消化",
            "近端催化优先": "B未来两个季度催化更明确",
            "价格确认/动量": "B价格行为更强",
            "激进短线": "B短线波动和关注度更适合进攻",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "增长与估值/防守互抵"
    return "档位接近需再验证"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    ticker = str(b["ticker"])
    if final == "A":
        if float(a["scores"]["NTM兑现优先"]) - float(b["scores"]["NTM兑现优先"]) > 10:
            return "GLW 的Meta/Amazon/NVIDIA长协和Optical收入锚让NTM兑现更硬。"
        if float(a["scores"]["近端催化优先"]) - float(b["scores"]["近端催化优先"]) > 10:
            return "GLW 的Amazon新增长协、光纤涨价/交期信号和Q2-Q3验证更近。"
        if float(a["scores"]["右尾弹性优先"]) - float(b["scores"]["右尾弹性优先"]) > 10:
            return "GLW 的AI结构化光纤、高密度连接和CPO被动光学右尾更直接。"
        return "GLW 在AI光互联收入化、长协可见度和近端催化组合上更均衡。"
    if float(b["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]) > 12:
        return f"{ticker} 的右尾或瓶颈利润池弹性明显大于 GLW。"
    if float(b["scores"]["下行保护优先"]) - float(a["scores"]["下行保护优先"]) > 12:
        return f"{ticker} 的现金流、估值缓冲或压力期防守强于 GLW。"
    if float(b["scores"]["估值消化优先"]) - float(a["scores"]["估值消化优先"]) > 10:
        return f"{ticker} 的估值消化压力低于 GLW 的高倍数材料股重估。"
    if float(b["scores"]["NTM兑现优先"]) - float(a["scores"]["NTM兑现优先"]) > 10:
        return f"{ticker} 的NTM订单/收入兑现证据强于 GLW。"
    return f"{ticker} 在多数投资思路下比 GLW 更符合当前配置目标。"


def configure_helper() -> None:
    helper.TARGET = TARGET
    helper.TARGET_NAME = TARGET_NAME
    helper.OUT_PATH = OUT_PATH
    helper.DIRECT_PEERS = DIRECT_PEERS
    helper.SERVER_STORAGE_ADJACENT = set()
    helper.UPSTREAM_CHIP_NETWORK = OPTICAL_CHAIN | AI_COMPUTE_UPSTREAM
    helper.DOWNSTREAM_CLOUD = SERVER_CLOUD_CUSTOMERS
    helper.POWER_COOLING_CHAIN = POWER_COOLING_CHAIN
    helper.relationship = relationship
    helper.reason_for = reason_for
    helper.key_reason = key_reason


def ranked_strategy_text(a_side: dict[str, int], b_side: dict[str, int], reverse: bool) -> str:
    ordered = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=reverse)[:3]
    return "、".join(ordered)


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    date_range = f"{min(str(c['date']) for c in companies.values())} 至 {max(str(c['date']) for c in companies.values())}"
    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][base.tag_in_cell(str(cell))] += 1
    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}

    strong_b = sorted(
        [c for c in comparisons if c["final"] == "B"],
        key=lambda x: (
            int(x["bc"]) - int(x["ac"]),
            int(x["bc"]),
            float(x["b"]["scores"]["风险调整收益"]) - float(a["scores"]["风险调整收益"]),  # type: ignore[index]
        ),
        reverse=True,
    )[:45]
    strong_a = sorted(
        [c for c in comparisons if c["final"] == "A"],
        key=lambda x: (
            int(x["ac"]) - int(x["bc"]),
            int(x["ac"]),
            float(a["scores"]["NTM兑现优先"]) + float(a["scores"]["近端催化优先"]) - float(x["b"]["scores"]["NTM兑现优先"]) - float(x["b"]["scores"]["近端催化优先"]),  # type: ignore[index]
        ),
        reverse=True,
    )[:45]
    final_a = sum(1 for c in comparisons if c["final"] == "A")
    final_b = sum(1 for c in comparisons if c["final"] == "B")
    missing_fin = sorted(ticker for ticker, company in companies.items() if not company.get("fin") or not company["fin"].get("price"))  # type: ignore[union-attr]
    file_list = "；".join(f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies))  # type: ignore[union-attr]

    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    latest_vs_june3 = ""
    try:
        latest_vs_june3 = f"，且6/22价格较6/3收盘约{(float(fin.get('price')) / float(mom2.get('latest_close')) - 1) * 100:+.2f}%"
    except Exception:
        pass
    daily_snapshot = (
        f"2026-06-22 价格 {helper.fmt_num(fin.get('price'))} 美元，市值 {helper.fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {helper.fmt_num(fin.get('ttm_pe'))}，Forward PE {helper.fmt_num(fin.get('forward_pe'))}，P/S {helper.fmt_num(fin.get('ps'))}，"
        f"P/B {helper.fmt_num(fin.get('pb'))}，EV/EBITDA {helper.fmt_num(fin.get('ev_ebitda'))}，Call IV {helper.fmt_pct(fin.get('call_iv'))}，Put IV {helper.fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {helper.fmt_pct(mom2.get('mom2w'), True)}、过去1个月 {helper.fmt_pct(mom1.get('mom1m'), True)}{latest_vs_june3}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {helper.fmt_pct(soxx.get('soxx_cum'), True)}。"
    )
    products = [str(p[0]).split("：")[0] for p in a["products"][:8]]  # type: ignore[index]
    rank_text = {strategy: f"第 {a['ranks'][strategy]}/{n}，{a['tiers'][strategy]} 档" for strategy in STRATS}  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "Q1 2026 core sales 43.45亿美元、Optical 18.46亿美元同比+36%；Q2指引约46亿美元；Meta/Amazon/NVIDIA和未披露客户长协给收入锚",
            "收入确认仍按多年交付和客户施工/验收节奏折扣，Solar低利润和扩产成本会稀释利润质量",
        ),
        "右尾弹性优先": (
            "极度乐观NTM 235-260亿美元；AI结构化光纤、高密度连接、multicore、CPO/Photonics和本土产能紧缺构成右尾",
            "公司基数已大，CPO/玻璃基板多数仍是2027+或更远期权，普通fiber/cable多供可能压价",
        ),
        "风险调整收益": (
            "Optical和Glass利润底座较硬，多客户长协降低扩产空转风险，基准core net income 27-32亿美元",
            "2026-06-22 Forward PE 49.92、P/S 11.06、Call IV 80.7%，估值已经显著前置AI光互联重估",
        ),
        "下行保护优先": (
            "Glass Innovations、Automotive和部分Carrier业务提供非AI底盘，长债期限和客户deposit改善扩产风险",
            "SOXX三段压力窗口累计-57.92%、高IV和高倍数削弱防守；Q1 adjusted FCF仅1.88亿美元且2026 capex约17亿美元",
        ),
        "估值消化优先": (
            "若Optical继续高增且core OM维持20%+，NTM利润上修可部分消化高倍数",
            "当前估值需要乐观路径持续兑现，Solar低毛利、扩产营运资本和CPO量产不确定使估值容错较低",
        ),
        "近端催化优先": (
            "未来1-2季可验证Q2/Q3 Optical收入利润、Amazon新增协议、Meta/NVIDIA扩产节点、Fujikura式光纤涨价/交期信号",
            "很多催化已被股价预期吸收；若财报只兑现收入、不兑现毛利/FCF，重定价力度会下降",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+11.11%、过去1个月+26.85%，6/22价格较6/3继续约+4.52%，价格已确认光纤瓶颈",
            "高IV和估值拥挤意味着趋势对任何订单延迟、毛利率或FCF反证很敏感",
        ),
        "激进短线": (
            "Call IV 80.7%、AI光纤线缆瓶颈新闻、Amazon/Meta/NVIDIA长协和CPO/Photonics叙事适合事件进攻",
            "短线爆发力弱于CRDO、AAOI、POET、COHR等小基数光互联标的，且材料股高倍数回撤风险大",
        ),
    }

    out: list[str] = [
        "# GLW 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：GLW / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 GLW vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{ranked_strategy_text(a_side, b_side, True)}。GLW 的优势来自 AI 数据中心结构化光纤/光缆/连接系统已经进入收入表，Meta、Amazon、NVIDIA 和未披露 hyperscaler 长协给 NTM 兑现和近端催化较硬支撑。",
        f"- A 最吃亏的投资思路：{ranked_strategy_text(a_side, b_side, False)}。主要短板是 Forward PE `49.92`、P/S `11.06`、Call IV `80.7%`、SOXX 压力窗口 `-57.92%`，以及 capex/营运资本导致 FCF 不如收入线性。",
        "- A 最适合的投资者画像：愿意买 AI 光互联中低调但订单硬的结构化光纤/布线瓶颈，接受材料股高倍数和扩产现金流波动的成长配置资金。",
        "- A 最不适合的投资者画像：优先要求低估值、低波动、强自由现金流防守，或只追求光芯片/IP/小市值光模块那类极端短线 beta 的资金。",
        f"- 多数思路下最强反方公司：{'、'.join(str(x['ticker']) for x in strong_b[:12])}。这些公司通常在芯片/IP瓶颈利润、云平台现金流、电力/液冷订单、估值消化或小基数短线弹性上压过 GLW。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：GLW 对 {final_a}/{n - 1} 家公司多数思路占优，对 {final_b}/{n - 1} 家公司多数思路落后；它是全项目 AI 光纤/布线收入兑现和近端催化强势档，但不是估值消化、下行保护或极端短线弹性的最优。",
        "- 后续最重要跟踪数据：Optical Communications季度收入和分部利润率、Enterprise/Carrier拆分、Meta/Amazon/NVIDIA交付和扩产里程碑、customer deposits/deferred revenue、core GM/OM、capex/库存/adjusted FCF、PRIZM/MMC/multicore客户标准化、CPO design win和field deployment。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "GLW"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(products)]),
        base.row(["NTM 基准收入", a["base_rev"] or "192-204 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "Meta/Amazon/NVIDIA/未披露 hyperscaler 长协在 NTM 内的交付节奏、美国光纤与 connectivity 产能爬坡、客户施工/验收窗口、普通 fiber/cable 多供压价。"]),
        base.row(["最大反证", "Backlog 和单客户年度收入未披露；CPO/Photonics 和 glass substrate 的 NTM 量产收入证据不足；Solar 低利润、capex 与营运资本可能使FCF低于收入增长。"]),
        base.row(["近端催化剂", "Q2/Q3 Optical收入和利润率、Amazon协议落地、Meta/NVIDIA相关产能建设、美国 optical connectivity 10x 与 fiber +50%扩产、PRIZM/MMC/multicore采用、CPO design win。"]),
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
        base.row(["直接同业", "与 GLW 在光纤、光缆、结构化布线、连接器或数据中心物理连接需求池高度重叠，优先比较订单/长协、产品代际、利润率、产能和估值。", "APH、BDC、BELFB、TEL、SMTOY", "同业证据权重最高；若对手在同一需求池内利润留存、价格确认或估值消化明显更强，结论力度可上调。"]),
        base.row(["相邻替代", "同属 AI 网络、光互联、数据中心电力/冷却或基础设施资金篮子，但产品和利润池不完全重叠。", "COHR、CRDO、CIEN、LITE、AAOI、VRT、ETN、GEV", "重点回答资金只能买一个时，谁的增长质量、估值消化、右尾和近端催化更好。"]),
        base.row(["上下游", "B 是 GLW 的客户、平台、服务器/云需求端或芯片/交换/模块上游瓶颈，重点看谁捕获更稀缺利润池和议价权。", "NVDA、AVGO、MRVL、ANET、CSCO、MSFT、AMZN、META、DELL、HPE", "不把下游 capex 或上游稀缺直接等同于 GLW 收入；比较收入确认、利润留存、客户验收和估值反证。"]),
        base.row(["跨赛道", "半导体设备/材料、工业、化工、生命科学、公用事业等与 GLW 业务差异大，但作为项目内配置替代仍可比较。", "ASML、AMAT、LIN、ECL、TMO、DHR、CAT", "默认降低结论力度；若成长、估值或防守证据互有强弱，优先中性或微倾向。"]),
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
                    helper.majority(int(comparison["ac"]), int(comparison["bc"]), int(comparison["nc"])),
                    comparison["final"],
                    comparison["reason"],
                ]
            )
        )

    out += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        out.append(base.row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_b, start=1):
        b = comparison["b"]
        wins = helper.win_strategies(comparison, "B")
        need = "GLW 需要证明Optical高增可持续、长协转收入和毛利率改善能覆盖高估值，并让FCF同步改善。"
        if "右尾弹性优先" in wins:
            need = "GLW 需要把高密度连接、multicore、CPO/Photonics从期权转成可量化客户订单和NTM收入。"
        if "估值消化优先" in wins or "下行保护优先" in wins:
            need = "GLW 需要降低估值压力、IV和压力窗口回撤，并用core OM/FCF证明高倍数有业绩支撑。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a, start=1):
        b = comparison["b"]
        wins = helper.win_strategies(comparison, "A")
        need = "B 需要拿出更硬的NTM订单/RPO、利润率、FCF或同等AI光互联右尾，才能压过GLW的长协和Optical兑现。"
        if "下行保护优先" in wins:
            need = "B 需要把防守优势转化为更高增长和更清楚催化，否则难以压过GLW的AI光纤收入锚。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未使用备份、临时目录、现成排序结论或下游量化资料作为判断依据。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 公司索引来源：`公司调研/公司索引.md`，用于公司名称和分类目录校验。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖情况见金融资料；本次公司全集中缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要项目来源：`公司调研/AI网络_光互联_连接器/GLW_Corning_公司调研_2026-06-11.md`；`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_高速连接器、背板与结构化布线_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_CPO／NPO与交换侧光引擎_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_玻璃基板、TGV与玻璃检测_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 当前性校验补充：运行时核对了 Corning/Meta 官方 up-to-$6B 数据中心协议 `https://investor.corning.com/news-and-events/news/news-details/2026/Corning-and-Meta-Announce-Multiyear-up-to-6-Billion-Agreement-to-Accelerate-US-Data-Center-Buildout/default.aspx`、Amazon 官方 multiyear multibillion-dollar 光纤协议 `https://www.aboutamazon.com/news/company-news/amazon-corning-fiber-optics-1000-jobs-north-carolina`、Corning OFC 2026 AI fiber/cable/connectivity 新闻 `https://investor.corning.com/news-and-events/news/news-details/2026/Corning-To-Launch-AI-Innovations-in-Fiber-Cable-and-Connectivity-at-OFC-2026/default.aspx` 和 NVIDIA/Corning 合作新闻 `https://nvidianews.nvidia.com/news/nvidia-and-corning-announce-long-term-partnership-to-strengthen-us-manufacturing-for-ai-infrastructure`；正式价格、估值、IV和涨跌幅仍以项目内 `金融资料` 为准。",
        "- 自动化脚本：`scripts/generate_glw_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对 GLW 的 AI optical 长协、Optical分部收入利润、CPO/Photonics期权、估值、高IV、压力窗口、capex/FCF约束和6月光纤线缆瓶颈信号做目标公司校准后建档。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    configure_helper()
    base.TARGET = TARGET
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit(f"缺少目标公司正式评估：{TARGET}")
    score_companies(companies)
    comparisons = helper.build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "target": TARGET,
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "size": OUT_PATH.stat().st_size,
                "glw_tiers": companies[TARGET]["tiers"],
                "glw_ranks": companies[TARGET]["ranks"],
                "glw_scores": {strategy: round(companies[TARGET]["scores"][strategy], 2) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
