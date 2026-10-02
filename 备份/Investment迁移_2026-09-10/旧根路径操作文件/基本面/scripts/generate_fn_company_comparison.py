from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated
import generate_cls_company_comparison as cls_calibrated
import generate_dell_company_comparison as helper
import generate_flex_company_comparison as flex_calibrated


TARGET = "FN"
TARGET_NAME = "Fabrinet"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "FN_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {"DELL", "HPE", "SMCI", "PENG", "JBL", "FLEX", "SANM", "CLS"}
SERVER_STORAGE_ADJACENT = {"NTAP", "PSTG", "STX", "WDC", "SNDK", "RMBS", "SIMO", "MRAM", "MU"}
AI_NETWORK_UPDOWN = {
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
    "GLW",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "NOK",
    "POET",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}
AI_COMPUTE_UPSTREAM = {
    "ADI",
    "AMD",
    "ARM",
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
DOWNSTREAM_CLOUD = {
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
POWER_COOLING_CHAIN = {
    "VRT",
    "ETN",
    "GEV",
    "CEG",
    "VST",
    "AEP",
    "DTE",
    "ETR",
    "PWR",
    "EME",
    "FIX",
    "IESC",
    "MYRG",
    "AAON",
    "TT",
    "MOD",
    "CARR",
    "JCI",
    "DKILY",
    "POWL",
    "HUBB",
    "NVT",
    "ABBNY",
    "AEIS",
    "POWI",
    "VICR",
    "BE",
    "ENS",
    "FLNC",
    "GNRC",
    "HTHIY",
    "TTDKY",
    "MRAAY",
    "MIELY",
    "IFNNY",
}

EXTRA_SCORE_FLOORS = {
    **helper.EXTRA_SCORE_FLOORS,
    **cls_calibrated.EXTRA_SCORE_FLOORS,
    "CLS": cls_calibrated.CLS_SCORE_OVERRIDES,
    "DELL": helper.DELL_OVERRIDES,
    "FLEX": flex_calibrated.FLEX_OVERRIDES,
}

FN_OVERRIDES = {
    "NTM兑现优先": 78.0,
    "右尾弹性优先": 82.0,
    "风险调整收益": 54.0,
    "下行保护优先": 58.0,
    "估值消化优先": 66.0,
    "近端催化优先": 76.0,
    "价格确认/动量": 66.0,
    "激进短线": 84.0,
}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    calibrated.fix_growth_ranges(companies)  # type: ignore[arg-type]
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

    for strategy, score in FN_OVERRIDES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score  # type: ignore[index]

    calibrated.recompute_tiers(companies)  # type: ignore[arg-type]


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in SERVER_STORAGE_ADJACENT or category == "AI服务器_存储_EMS":
        return "相邻替代"
    if ticker in AI_NETWORK_UPDOWN or ticker in AI_COMPUTE_UPSTREAM:
        return "上下游"
    if ticker in DOWNSTREAM_CLOUD:
        return "上下游"
    if ticker in POWER_COOLING_CHAIN or category in INFRA_CATS:
        return "相邻替代"
    if category in {"AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, winner: str, b: dict[str, object], rel: str) -> str:
    ticker = str(b["ticker"])
    category = str(b.get("category", ""))
    if winner == "A":
        return {
            "NTM兑现优先": "A有Q4指引、DCI/HPC和datacom收入锚",
            "右尾弹性优先": "A的1.6T/DCI/HPC/CPO上限更集中",
            "风险调整收益": "A增长、估值与盈利底盘更均衡",
            "下行保护优先": "A有盈利和传统通信制造底盘",
            "估值消化优先": "A可用NTM高增长消化5.2x P/S",
            "近端催化优先": "A有Q4、DCI、HPC和Building 10验证",
            "价格确认/动量": "A前期价格已有基本面确认",
            "激进短线": "A高IV叠加AI光互联/HPC催化",
        }[strategy]
    if winner == "B":
        if ticker in DIRECT_PEERS or category == "AI服务器_存储_EMS":
            return {
                "NTM兑现优先": "B同业订单或利润兑现更直接",
                "右尾弹性优先": "B同业小基数或利润弹性更大",
                "风险调整收益": "B同业估值/现金流组合更优",
                "下行保护优先": "B同业波动或压力期更稳",
                "估值消化优先": "B同业倍数更易被业绩消化",
                "近端催化优先": "B同业订单/财报催化更近",
                "价格确认/动量": "B同业价格趋势更强",
                "激进短线": "B同业短线弹性更高",
            }[strategy]
        if ticker in AI_NETWORK_UPDOWN or ticker in AI_COMPUTE_UPSTREAM or category in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B上游AI主链兑现或利润留存更强",
                "右尾弹性优先": "B瓶颈利润池或小基数右尾更大",
                "风险调整收益": "B上行更能覆盖执行和估值风险",
                "下行保护优先": "B现金流、规模或波动更好",
                "估值消化优先": "B利润弹性更能消化估值",
                "近端催化优先": "B产品/订单催化更密集",
                "价格确认/动量": "B价格趋势和资金偏好更强",
                "激进短线": "B高beta叙事更适合进攻",
            }[strategy]
        if ticker in DOWNSTREAM_CLOUD:
            return {
                "NTM兑现优先": "B云/软件收入确认更稳",
                "右尾弹性优先": "B平台扩张或AI云右尾更大",
                "风险调整收益": "B盈利质量和资本结构更好",
                "下行保护优先": "B现金流、客户粘性或规模更稳",
                "估值消化优先": "B利润留存更能支撑估值",
                "近端催化优先": "B云订单或AI产品催化更近",
                "价格确认/动量": "B价格确认更强",
                "激进短线": "B市场关注或波动更集中",
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
            return "FN 的AI光互联、DCI和HPC已收入化，NTM兑现证据更硬。"
        if float(a["scores"]["近端催化优先"]) - float(b["scores"]["近端催化优先"]) > 10:
            return "FN 的Q4指引、DCI/HPC爬坡和Building 10验证更近。"
        if float(a["scores"]["估值消化优先"]) - float(b["scores"]["估值消化优先"]) > 10:
            return "FN 的NTM收入增长可部分消化当前P/S和Forward PE。"
        return "FN 在AI光互联收入化、右尾和近端催化组合上更均衡。"
    if float(b["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]) > 12:
        return f"{ticker} 的右尾或瓶颈利润池弹性明显大于 FN。"
    if float(b["scores"]["下行保护优先"]) - float(a["scores"]["下行保护优先"]) > 12:
        return f"{ticker} 的现金流、估值缓冲或压力期防守强于 FN。"
    if float(b["scores"]["风险调整收益"]) - float(a["scores"]["风险调整收益"]) > 10:
        return f"{ticker} 的上行/下行组合比 FN 的EMS制造和高IV组合更好。"
    if float(b["scores"]["NTM兑现优先"]) - float(a["scores"]["NTM兑现优先"]) > 10:
        return f"{ticker} 的NTM订单/收入兑现证据强于 FN。"
    return f"{ticker} 在多数投资思路下比 FN 更符合当前配置目标。"


def configure_helper() -> None:
    helper.TARGET = TARGET
    helper.TARGET_NAME = TARGET_NAME
    helper.OUT_PATH = OUT_PATH
    helper.DIRECT_PEERS = DIRECT_PEERS
    helper.SERVER_STORAGE_ADJACENT = SERVER_STORAGE_ADJACENT
    helper.UPSTREAM_CHIP_NETWORK = AI_NETWORK_UPDOWN | AI_COMPUTE_UPSTREAM
    helper.DOWNSTREAM_CLOUD = DOWNSTREAM_CLOUD
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
    missing_fin = sorted(
        ticker
        for ticker, company in companies.items()
        if not company.get("fin") or not company["fin"].get("price")  # type: ignore[union-attr]
    )
    file_list = "；".join(f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies))  # type: ignore[union-attr]

    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    latest_vs_june3 = ""
    try:
        latest_vs_june3 = f"，且6/22价格较6/3收盘约{(float(fin.get('price')) / float(mom2.get('latest_close')) - 1) * 100:+.2f}%"
    except Exception:
        latest_vs_june3 = ""
    daily_snapshot = (
        f"2026-06-22 价格 {helper.fmt_num(fin.get('price'))} 美元，市值 {helper.fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {helper.fmt_num(fin.get('ttm_pe'))}，Forward PE {helper.fmt_num(fin.get('forward_pe'))}，P/S {helper.fmt_num(fin.get('ps'))}，"
        f"P/B {helper.fmt_num(fin.get('pb'))}，EV/EBITDA {helper.fmt_num(fin.get('ev_ebitda'))}，Call IV {helper.fmt_pct(fin.get('call_iv'))}，Put IV {helper.fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {helper.fmt_pct(mom2.get('mom2w'), True)}、过去1个月 {helper.fmt_pct(mom1.get('mom1m'), True)}{latest_vs_june3}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {helper.fmt_pct(soxx.get('soxx_cum'), True)}。"
    )
    products = [str(p[0]).split("：")[0] for p in a["products"][:7]]  # type: ignore[index]
    rank_text = {
        strategy: f"第 {a['ranks'][strategy]}/{n}，{a['tiers'][strategy]} 档"  # type: ignore[index]
        for strategy in STRATS
    }
    support = {
        "NTM兑现优先": (
            "FY2026Q3收入12.143亿美元、同比+39.3%；FY2026Q4指引12.50-12.90亿美元；NTM基准56-62亿美元，DCI和HPC已进收入表",
            "Datacom仍受laser/memory/ASIC供给、客户认证和测试产能约束，HPC里程碑曾推迟约一季",
        ),
        "右尾弹性优先": (
            "乐观65-73亿美元、极度乐观78-88亿美元；1.6T、800ZR/1.6T ZR、HPC follow-on、CPO/ELS/OCS和Building 10构成上限",
            "FN仍是EMS/精密制造平台，利润率不能按光芯片/IP或模块品牌商处理，CPO/OCS缺量产金额和时间表",
        ),
        "风险调整收益": (
            "NTM基准增速约+22%-+35%，P/S 5.22仍可被高收入增速部分消化，且公司已有盈利和正FCF潜力",
            "Forward PE 35.74、EV/EBITDA 40.89、IV 80%+和压力窗口回撤使风险调整不如低倍数/强现金流公司",
        ),
        "下行保护优先": (
            "Telecom ex-DCI、Automotive、Industrial/Other提供收入底座，基准情景仍有经营利润和FCF转正路径",
            "SOXX三段压力窗口累计-57.48%、高IV、客户集中、库存/应收和扩产CapEx削弱防守属性",
        ),
        "估值消化优先": (
            "如果NTM收入56-62亿美元、净利润5.6-6.7亿美元兑现，5.22x P/S和35.74x Forward PE可被高增速摊薄",
            "估值已经要求datacom供给缓解、DCI/HPC延续和利润率不被pass-through稀释；若只是收入增长而非利润/FCF增长，消化失败",
        ),
        "近端催化优先": (
            "未来1-2季可验证FY2026Q4实际收入/毛利率、Datacom供应缓解、DCI收入、HPC是否越过150M美元/季、Building 10投产",
            "催化主要是经营兑现而非已公告大额订单；若Q4或下一季只兑现收入不兑现毛利/现金流，重定价力度会被削弱",
        ),
        "价格确认/动量": (
            "2026-06-03两周+9.48%、一月+2.61%，基本面强度曾推动价格确认",
            "2026-06-22价格617.09已低于6/3的725.00，高IV和回撤说明动量不再是无瑕强项",
        ),
        "激进短线": (
            "Call IV 85.0%、AI光互联/1.6T/DCI/HPC/CPO叙事集中，若Q4超预期可有短线进攻弹性",
            "市值和EMS属性使爆发力弱于CRDO、AAOI、POET、LWLG等小基数/高beta光互联标的，方向错时损耗也高",
        ),
    }

    out: list[str] = [
        "# FN 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：FN / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 FN vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{ranked_strategy_text(a_side, b_side, True)}。FN 的优势来自已经收入化的AI光互联/DCI/HPC制造、Q4指引、NTM 56-62亿美元基准收入、1.6T/800ZR/HPC/CPO远期上限和较清楚的近端验证点。",
        f"- A 最吃亏的投资思路：{ranked_strategy_text(a_side, b_side, False)}。主要短板是EMS/精密制造利润率属性、高IV、SOXX压力期大回撤、库存/应收/扩产CapEx和2026-06-22价格较6/3明显回落。",
        "- A 最适合的投资者画像：愿意买AI光互联与复杂系统制造收入兑现链条、重视NTM收入可见度和1.6T/DCI/HPC/capacity上修的中高风险资金。",
        "- A 最不适合的投资者画像：要求低波动、强防守、低估值现金流，或只追求芯片/IP/小市值光互联极端右尾和短线爆发的资金。",
        f"- 多数思路下最强反方公司：{'、'.join(str(x['ticker']) for x in strong_b[:12])}。这些公司通常在上游瓶颈利润、云平台现金流、数据中心电力订单、低估值防守或高beta短线弹性上压过 FN。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：FN 对 {final_a}/{n - 1} 家公司多数思路占优，对 {final_b}/{n - 1} 家公司多数思路落后；属于全项目AI光互联制造兑现和近端催化强势档，但不是全项目最强防守资产，也不是利润池最稀缺的上游芯片/IP公司。",
        "- 后续最重要跟踪数据：FY2026Q4实际收入和毛利率、Datacom供应约束、DCI收入、HPC是否越过150M美元/季、direct hyperscale/merchant programs、Building 10投产、库存/应收/经营现金流、CPO/ELS/OCS是否从项目变为可量化收入。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "FN"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(products)]),
        base.row(["NTM 基准收入", a["base_rev"] or "56-62亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；净利润/EBITDA：{a['base_profit']}；现金流：{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "Datacom 从需求到收入的瓶颈不是需求池，而是EML/CW laser、memory、certain ASICs、客户认证、测试和产能排程。"]),
        base.row(["最大反证", "若Datacom连续低于需求、DCI环比下滑、HPC停在1.0-1.2亿美元/季、库存继续上升但收入不加速，或毛利率跌破11.5%且FCF持续为负。"]),
        base.row(["近端催化剂", "FY2026Q4实际收入/毛利率、Datacom供应约束缓解、DCI revenue、HPC revenue越过150M美元/季、direct hyperscale/merchant programs、Building 10、库存/应收/经营现金流。"]),
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
        base.row(["直接同业", "与 FN 在EMS/OEM/ODM、AI server/rack、光通信/复杂系统制造或硬件交付收入池高度重叠，优先比较收入兑现、订单、客户项目、毛利率、营运资本和估值。", "DELL、HPE、SMCI、PENG、JBL、FLEX、SANM、CLS", "同业证据权重最高；若对手在订单、margin、现金流或价格确认明显胜出，可以给建议或强烈建议。"]),
        base.row(["相邻替代", "同属AI服务器/存储/数据中心基础设施资金篮子但产品/利润池不完全重叠，重点比较增长质量、兑现确定性、估值消化、订单可见度和资金偏好。", "MU、STX、WDC、PSTG、VRT、ETN、GEV、MOD、TT、POWL", "保持中等力度；赛道更热不能自动胜出，必须由订单、backlog、收入或利润传导支撑。"]),
        base.row(["上下游", "B 是 FN 的光互联、网络、芯片、云客户或IDC链条上下游，重点看谁捕获瓶颈利润和议价权。", "CRDO、COHR、LITE、CIEN、NVDA、AVGO、AMD、ANET、MSFT、AMZN、GOOGL、META", "不把下游capex或上游供给稀缺直接等同于FN收入；比较利润捕获、客户验收、现金流和反证。"]),
        base.row(["跨赛道", "半导体设备/材料、工业、化工、生命科学工具等与 FN 业务差异大但可作为资金配置替代。", "ASML、AMAT、LIN、ECL、TMO、DHR、CAT", "默认降低结论力度；除非增长质量、估值消化或下行保护明显拉开，否则使用中性或微倾向。"]),
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
        need = "FN 需要证明Datacom供给缓解、DCI/HPC继续爬坡，且收入增长能转化为毛利率和FCF。"
        if "下行保护优先" in wins:
            need = "FN 需要降低IV和压力窗口回撤，证明库存、应收、Building 10 CapEx和客户验收不会放大下行。"
        if "右尾弹性优先" in wins:
            need = "FN 需要把1.6T、CPO/ELS/OCS和HPC follow-on从项目机会转成可量化高质量收入。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a, start=1):
        b = comparison["b"]
        wins = helper.win_strategies(comparison, "A")
        need = "B 需要拿出更硬的NTM订单/RPO、利润率、FCF和价格确认，或证明其右尾不只是叙事。"
        if "估值消化优先" in wins and "近端催化优先" in wins:
            need = "B 需要同时改善估值消化和近端催化，才能抵消FN的AI光互联收入锚和Q4/HPC/DCI验证点。"
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
        "- 其他主要项目来源：`公司调研/AI服务器_存储_EMS/FN_Fabrinet_公司调研_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_AI服务器整机与机架集成_2026-06-10.md`；`行业调研/AI网络_光互联_铜互联/行业调研_LPO_LRO线性光模块_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_CPO／NPO与交换侧光引擎_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_光DSP、TIA与CDR芯片_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_激光器、EML与光器件_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_fn_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对 FN 的FY2026Q4指引、DCI/HPC、Datacom供给约束、1.6T/CPO/OCS期权、Building 10、估值、高IV、压力窗口和6/22价格回落做人工校准后建档。",
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
                "fn_tiers": companies[TARGET]["tiers"],
                "fn_ranks": companies[TARGET]["ranks"],
                "fn_scores": {strategy: round(companies[TARGET]["scores"][strategy], 2) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
