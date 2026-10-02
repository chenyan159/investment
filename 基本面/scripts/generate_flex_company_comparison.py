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


TARGET = "FLEX"
TARGET_NAME = "Flex Ltd"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "FLEX_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {"DELL", "HPE", "SMCI", "PENG", "JBL", "SANM", "CLS", "FN"}
SERVER_STORAGE_ADJACENT = {"NTAP", "PSTG", "STX", "WDC", "SNDK", "RMBS", "SIMO", "MRAM", "MU"}
UPSTREAM_CHIP_NETWORK = {
    "NVDA",
    "AMD",
    "AVGO",
    "MRVL",
    "INTC",
    "ARM",
    "QCOM",
    "ANET",
    "CSCO",
    "CIEN",
    "ALAB",
    "CRDO",
    "COHR",
    "LITE",
    "AAOI",
    "APH",
    "BDC",
    "BELFB",
    "MTSI",
    "SMTC",
    "TEL",
    "VIAV",
}
DOWNSTREAM_CLOUD = {
    "AMZN",
    "MSFT",
    "GOOGL",
    "META",
    "ORCL",
    "BABA",
    "IBM",
    "EQIX",
    "DLR",
    "CRWV",
    "APLD",
    "IREN",
    "NBIS",
    "NTNX",
    "ADBE",
    "CRWD",
}
POWER_COOLING_ADJACENT = {
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

# Keep peer-company calibrations from the existing comparison scripts so FLEX is
# judged against the same project-wide anchor set, then override FLEX itself.
EXTRA_SCORE_FLOORS = {
    **calibrated.SCORE_FLOORS,
    **cls_calibrated.EXTRA_SCORE_FLOORS,
    "CLS": cls_calibrated.CLS_SCORE_OVERRIDES,
    "DELL": {
        "NTM兑现优先": 86,
        "右尾弹性优先": 78,
        "风险调整收益": 68,
        "下行保护优先": 74,
        "估值消化优先": 82,
        "近端催化优先": 84,
        "价格确认/动量": 96,
        "激进短线": 88,
    },
    "CRWV": {
        "NTM兑现优先": 92,
        "右尾弹性优先": 100,
        "风险调整收益": 56,
        "下行保护优先": 35,
        "估值消化优先": 63,
        "近端催化优先": 86,
        "价格确认/动量": 60,
        "激进短线": 100,
    },
    "CSCO": {
        "NTM兑现优先": 72,
        "右尾弹性优先": 55,
        "风险调整收益": 82,
        "下行保护优先": 90,
        "估值消化优先": 64,
        "近端催化优先": 70,
        "价格确认/动量": 76,
        "激进短线": 66,
    },
    "CIEN": {
        "NTM兑现优先": 82,
        "右尾弹性优先": 78,
        "风险调整收益": 64,
        "下行保护优先": 58,
        "估值消化优先": 68,
        "近端催化优先": 84,
        "价格确认/动量": 74,
        "激进短线": 80,
    },
}

FLEX_OVERRIDES = {
    "NTM兑现优先": 76.0,
    "右尾弹性优先": 72.0,
    "风险调整收益": 68.0,
    "下行保护优先": 70.0,
    "估值消化优先": 74.0,
    "近端催化优先": 76.0,
    "价格确认/动量": 88.0,
    "激进短线": 82.0,
}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    calibrated.fix_growth_ranges(companies)  # type: ignore[arg-type]
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    for ticker, floors in EXTRA_SCORE_FLOORS.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[assignment]
            company["scores"][strategy] = max(float(current), float(floor))  # type: ignore[index]

    for strategy, score in FLEX_OVERRIDES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score  # type: ignore[index]

    calibrated.recompute_tiers(companies)  # type: ignore[arg-type]


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in SERVER_STORAGE_ADJACENT or category == "AI服务器_存储_EMS":
        return "相邻替代"
    if ticker in POWER_COOLING_ADJACENT or category in INFRA_CATS:
        return "相邻替代"
    if ticker in UPSTREAM_CHIP_NETWORK or ticker in DOWNSTREAM_CLOUD:
        return "上下游"
    if category in {"AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, winner: str, b: dict[str, object], rel: str) -> str:
    ticker = str(b["ticker"])
    category = str(b.get("category", ""))
    if winner == "A":
        return {
            "NTM兑现优先": "A有FY2027指引和CPI增长硬锚",
            "右尾弹性优先": "A的Power/液冷/整柜右尾可收入化",
            "风险调整收益": "A低P/S、FCF和CPI成长更均衡",
            "下行保护优先": "A有EMS/RMS底盘和FCF缓冲",
            "估值消化优先": "A用低P/S和FY2027增速消化估值",
            "近端催化优先": "A有Q1、SpinCo和CPI mix验证",
            "价格确认/动量": "A近月强涨已确认重估",
            "激进短线": "A高IV叠加电力/液冷/SpinCo事件",
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
        if ticker in POWER_COOLING_ADJACENT or category in INFRA_CATS:
            return {
                "NTM兑现优先": "B电力/冷却backlog兑现更清楚",
                "右尾弹性优先": "B设施瓶颈利润池右尾更直接",
                "风险调整收益": "B订单和现金流赔率更好",
                "下行保护优先": "B防御现金流或订单粘性更强",
                "估值消化优先": "B用订单兑现消化估值更容易",
                "近端催化优先": "B订单/产能/财报催化更近",
                "价格确认/动量": "B电气化价格趋势更强",
                "激进短线": "B电力瓶颈交易弹性更高",
            }[strategy]
        if ticker in UPSTREAM_CHIP_NETWORK or category in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链兑现或利润留存更强",
                "右尾弹性优先": "B上游瓶颈利润池右尾更大",
                "风险调整收益": "B上行更能覆盖执行风险",
                "下行保护优先": "B现金流/资产质量或波动更好",
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
        if float(a["scores"]["NTM兑现优先"]) - float(b["scores"]["NTM兑现优先"]) > 10:  # type: ignore[index]
            return "FLEX 的FY2027指引、CPI增长和Power/Cloud & Cooling收入锚让NTM兑现更硬。"
        if float(a["scores"]["估值消化优先"]) - float(b["scores"]["估值消化优先"]) > 10:  # type: ignore[index]
            return "FLEX 的低P/S、合理Forward PE和CPI成长让估值消化更顺。"
        if float(a["scores"]["近端催化优先"]) - float(b["scores"]["近端催化优先"]) > 10:  # type: ignore[index]
            return "FLEX 的SpinCo、CPI mix、Power和液冷验证更近。"
        return "FLEX 在收入兑现、估值消化、近端催化和动量组合上更均衡。"
    if float(b["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]) > 12:  # type: ignore[index]
        return f"{ticker} 的右尾或瓶颈利润池弹性明显大于 FLEX。"
    if float(b["scores"]["下行保护优先"]) - float(a["scores"]["下行保护优先"]) > 12:  # type: ignore[index]
        return f"{ticker} 的现金流、估值缓冲或压力期防守强于 FLEX。"
    if float(b["scores"]["风险调整收益"]) - float(a["scores"]["风险调整收益"]) > 10:  # type: ignore[index]
        return f"{ticker} 的上行/下行组合比 FLEX 的EMS与CPI成长组合更好。"
    if float(b["scores"]["NTM兑现优先"]) - float(a["scores"]["NTM兑现优先"]) > 10:  # type: ignore[index]
        return f"{ticker} 的NTM订单/收入兑现证据强于 FLEX。"
    return f"{ticker} 在多数投资思路下比 FLEX 更符合当前配置目标。"


def configure_helper() -> None:
    helper.TARGET = TARGET
    helper.TARGET_NAME = TARGET_NAME
    helper.OUT_PATH = OUT_PATH
    helper.DIRECT_PEERS = DIRECT_PEERS
    helper.SERVER_STORAGE_ADJACENT = SERVER_STORAGE_ADJACENT
    helper.UPSTREAM_CHIP_NETWORK = UPSTREAM_CHIP_NETWORK
    helper.DOWNSTREAM_CLOUD = DOWNSTREAM_CLOUD
    helper.POWER_COOLING_CHAIN = POWER_COOLING_ADJACENT
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
            float(a["scores"]["NTM兑现优先"]) + float(a["scores"]["估值消化优先"]) - float(x["b"]["scores"]["NTM兑现优先"]) - float(x["b"]["scores"]["估值消化优先"]),  # type: ignore[index]
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
    daily_snapshot = (
        f"2026-06-22 价格 {helper.fmt_num(fin.get('price'))} 美元，市值 {helper.fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {helper.fmt_num(fin.get('ttm_pe'))}，Forward PE {helper.fmt_num(fin.get('forward_pe'))}，P/S {helper.fmt_num(fin.get('ps'))}，"
        f"P/B {helper.fmt_num(fin.get('pb'))}，EV/EBITDA {helper.fmt_num(fin.get('ev_ebitda'))}，Call IV {helper.fmt_pct(fin.get('call_iv'))}，Put IV {helper.fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {helper.fmt_pct(mom2.get('mom2w'), True)}、过去1个月 {helper.fmt_pct(mom1.get('mom1m'), True)}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {helper.fmt_pct(soxx.get('soxx_cum'), True)}。"
    )
    products = [str(p[0]).split("：")[0] for p in a["products"][:7]]  # type: ignore[index]
    rank_text = {
        strategy: f"第 {a['ranks'][strategy]}/{n}，{a['tiers'][strategy]} 档"  # type: ignore[index]
        for strategy in STRATS
    }
    support = {
        "NTM兑现优先": (
            "FY2026收入279.14亿美元、FY2027收入指引323-338亿美元；CPI FY2026约66亿美元，FY2027目标同比+65%-75%，Cloud & Cooling和Power是硬锚",
            "收入兑现依赖Power/液冷/整柜集成产能、客户验收、组件供给和高增长业务的营运资本周转",
        ),
        "右尾弹性优先": (
            "乐观收入345-370亿美元、极度乐观390-430亿美元；Power shelf、BMR/BMR720、CESS、800VDC、JetCool和整柜集成为非线性上限",
            "FLEX仍有EMS/制造属性和较大收入基数，利润率不等同于芯片/软件瓶颈，右尾需要Power和液冷mix真正上升",
        ),
        "风险调整收益": (
            "2026-06-22 P/S约2.05、Forward PE约22.43，叠加FY2027收入中枢约+18%和FCF底盘，赔率较均衡",
            "TTM PE约66.87、Call IV约76.2%、SOXX压力窗口跌幅大，说明市场已重估且波动/执行风险不低",
        ),
        "下行保护优先": (
            "FY2026调整后经营利润率6.3%、FCF约10.60亿美元，RMS/ITS等非CPI业务提供一定底盘",
            "SOXX压力窗口累计约-58.62%、高IV和高P/B显示回撤弹性仍大，不是纯防守资产",
        ),
        "估值消化优先": (
            "低P/S、FY2027收入指引和CPI高增长让当前估值可由近端收入兑现消化；Forward PE约22.43未到极端透支",
            "若增量主要是低毛利pass-through、CapEx 14-16亿美元和营运资本吞噬FCF，则估值消化会失效",
        ),
        "近端催化优先": (
            "未来1-2季可跟踪Q1 FY2027收入、CPI收入/利润率、Cloud & Cooling vs Power mix、SpinCo Form 10和液冷/电源平台订单",
            "SpinCo、客户认证和产能放量均可能分阶段验证，单季若只看到收入而看不到margin/FCF，催化力度会打折",
        ),
        "价格确认/动量": (
            "截至2026-06-03过去两周+23.13%、过去1个月+76.60%；2026-06-22价格155.81美元仍接近6月初高位",
            "近月涨幅已大，后续必须由CPI增速、margin和FCF继续确认，不能只依赖AI电力/液冷主题延伸",
        ),
        "激进短线": (
            "高IV、强动量、SpinCo事件、AI电力/液冷/800VDC和CPI高增长叙事使短线弹性强于普通EMS",
            "爆发力仍弱于小基数光互联、NeoCloud或纯瓶颈芯片股，且高IV意味着方向错时损耗更大",
        ),
    }

    out: list[str] = [
        "# FLEX 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：FLEX / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 FLEX vs 公司 B 的二选一判断。未使用备份、临时目录、现成排序结论或下游量化资料作为判断依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{ranked_strategy_text(a_side, b_side, True)}。FLEX 的优势来自FY2027收入指引、CPI +65%-75%目标、Power/Cloud & Cooling/液冷/800VDC、较低P/S和近月价格重估。",
        f"- A 最吃亏的投资思路：{ranked_strategy_text(a_side, b_side, False)}。主要短板是制造/EMS属性限制利润率，右尾小基数不如光互联/NeoCloud/上游芯片，且高IV和压力窗口回撤削弱防守。",
        "- A 最适合的投资者画像：希望配置AI数据中心电力、冷却、整柜和EMS兑现链条，同时不愿支付纯芯片/高beta光互联高估值的中高风险资金。",
        "- A 最不适合的投资者画像：只追求纯软件/芯片毛利率、小市值极端右尾，或要求低波动、低回撤、现金流公用事业式防守的资金。",
        f"- 多数思路下最强反方公司：{'、'.join(str(x['ticker']) for x in strong_b[:12])}。这些公司通常在上游瓶颈利润、云平台现金流、数据中心电力订单或短线高beta上压过 FLEX。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：FLEX 对 {final_a}/{n - 1} 家公司多数思路占优，对 {final_b}/{n - 1} 家公司多数思路落后；属于全项目AI基础设施兑现、估值消化和近端催化的强势档，但不是全项目最稀缺利润池或最强防守资产。",
        "- 后续最重要跟踪数据：FY2027 Q1-Q2收入、CPI收入增速、Cloud & Cooling/Power mix、调整后经营利润率、FCF、CapEx、库存/应收/应付、SpinCo Form 10、客户集中度、液冷/电源平台订单、800VDC/Power shelf/JetCool认证和客户验收。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "FLEX"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(products)]),
        base.row(["NTM 基准收入", "FY2027收入指引323-338亿美元，中枢约330.5亿美元；FY2026收入279.14亿美元"]),
        base.row(["乐观/极度乐观收入", "乐观：345-370亿美元；极度乐观：390-430亿美元"]),
        base.row(["利润和现金流结论", "FY2026调整后经营利润率6.3%，FY2027指引7.0%-7.1%；FY2026 FCF约10.60亿美元，但FY2027 CapEx和营运资本敏感度上升。"]),
        base.row(["最大传导瓶颈", "不是AI需求本身，而是Power/液冷/整柜集成产能、客户认证与验收、组件供给、CapEx和高增长业务营运资本。"]),
        base.row(["最大反证", "若增量收入主要是低毛利compute/rack pass-through，或库存/应收扩大、FCF转换下降、CPI margin不升，则AI收入不能转化为更高质量利润。"]),
        base.row(["近端催化剂", "FY2027 Q1-Q2收入、CPI收入和margin、Cloud & Cooling vs Power mix、SpinCo Form 10、JetCool/SmartSense/SmartPlate、电源架构和800VDC订单。"]),
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
        base.row(["直接同业", "与 FLEX 在EMS/OEM/ODM、AI server/rack、电源/热管理集成、复杂系统制造或硬件交付收入池高度重叠，优先比较订单、收入兑现、margin、客户质量、营运资本和估值。", "DELL、HPE、SMCI、PENG、JBL、SANM、CLS、FN", "同业证据权重最高；若对手在订单、margin、现金流或价格确认明显胜出，可以给建议或强烈建议。"]),
        base.row(["相邻替代", "同属AI基础设施资金篮子但产品/利润池不完全重叠，重点比较增长质量、兑现确定性、估值消化、订单可见度和资金偏好。", "VRT、ETN、GEV、POWL、MOD、TT、MU、STX、WDC、PSTG", "保持中等力度；赛道更热不能自动胜出，必须由订单、backlog、收入或利润传导支撑。"]),
        base.row(["上下游", "B 是 FLEX 的芯片、网络、光/铜互联、连接器、云客户或IDC链条上下游，重点看谁捕获瓶颈利润和议价权。", "NVDA、AVGO、AMD、MRVL、ANET、CIEN、CRDO、COHR、MSFT、AMZN、GOOGL、META", "不把下游capex或上游供给稀缺直接等同于FLEX收入；比较利润捕获、客户验收、现金流和反证。"]),
        base.row(["跨赛道", "半导体设备/材料、工业、化工、生命科学工具等与 FLEX 业务差异大但可作为资金配置替代。", "ASML、AMAT、LIN、ECL、TMO、DHR、CAT", "默认降低结论力度；除非增长质量、估值消化或下行保护明显拉开，否则使用中性或微倾向。"]),
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
        need = "FLEX 需要证明CPI高增长可持续，Power/液冷/整柜mix提升，并把收入转化为更高margin和FCF。"
        if "右尾弹性优先" in wins:
            need = "FLEX 需要把Power shelf、800VDC、JetCool和液冷整柜从项目机会转成高毛利、可重复订单。"
        if "下行保护优先" in wins:
            need = "FLEX 需要降低IV和压力窗口回撤，证明CapEx、库存、应收和客户验收不会放大下行。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a, start=1):
        b = comparison["b"]
        wins = helper.win_strategies(comparison, "A")
        need = "B 需要拿出更硬的NTM订单/RPO、利润率、FCF和价格确认，或证明其右尾不只是叙事。"
        if "估值消化优先" in wins and "近端催化优先" in wins:
            need = "B 需要同时改善估值消化和近端催化，才能抵消FLEX的CPI收入锚、SpinCo事件和低P/S。"
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
        "- 其他主要项目来源：`公司调研/AI服务器_存储_EMS/FLEX_Flex_Ltd_公司调研_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_AI服务器整机与机架集成_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`；`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`；`行业调研/产业背景/AI产业链瓶颈与反证指标总表_2026-06-10.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 外部 sanity check：运行中查看了 Flex Investor Relations 最新季度/年度结果页，并用公开行情查询核对 FLEX 价格；仅用于确认本地评估所引用的FY2026/FY2027披露与最新市场语境仍匹配，主表不使用外部网页排序、券商评级或目标价。参考页：Flex IR <https://investors.flex.com/>；Flex FY2026 results <https://investors.flex.com/news/news-details/2026/FLEX-REPORTS-FOURTH-QUARTER-AND-FISCAL-2026-RESULTS/default.aspx>。",
        "- 自动化脚本：`scripts/generate_flex_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对 FLEX 的FY2027指引、CPI增长、Power/Cloud & Cooling、液冷/800VDC、SpinCo、估值、动量、高IV和压力窗口表现做人工校准后建档。",
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
                "flex_tiers": companies[TARGET]["tiers"],
                "flex_ranks": companies[TARGET]["ranks"],
                "flex_scores": {strategy: round(companies[TARGET]["scores"][strategy], 2) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
