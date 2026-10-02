from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_nvt_company_comparison as nvt_ref


TARGET = "PSIX"
TARGET_NAME = "Power Solutions International"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "PSIX_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_POWER_SYSTEMS_PEERS = {"CAT", "CMI", "GEV", "GNRC", "RYCEY"}
POWER_AND_ELECTRICAL_ADJACENT = (
    set(getattr(nvt_ref, "POWER_ELECTRICAL_INFRA", set()))
    | {
        "AAON",
        "ABBNY",
        "AEIS",
        "ATKR",
        "BE",
        "BWXT",
        "CARR",
        "DOV",
        "EME",
        "ENS",
        "ENPH",
        "ETN",
        "FCEL",
        "FIX",
        "FLNC",
        "FTV",
        "HUBB",
        "IESC",
        "JCI",
        "MOD",
        "MYRG",
        "NVT",
        "OKLO",
        "PH",
        "PNR",
        "POWL",
        "PWR",
        "SMR",
        "TT",
        "VRT",
    }
)
UTILITY_AND_POWER_CUSTOMERS = set(getattr(nvt_ref, "UTILITY_AND_POWER_CUSTOMERS", set()))
DATA_CENTER_CUSTOMERS_AND_OPERATORS = set(getattr(nvt_ref, "DATA_CENTER_CUSTOMERS_AND_OPERATORS", set()))
SERVER_NETWORK_AND_AI_DEMAND_CHAIN = set(getattr(nvt_ref, "SERVER_NETWORK_AND_AI_DEMAND_CHAIN", set()))
SEMI_CHAIN = set(getattr(nvt_ref, "SEMI_CHAIN", set()))

PSIX_SCORES = {
    "NTM兑现优先": 58.0,
    "右尾弹性优先": 88.0,
    "风险调整收益": 52.0,
    "下行保护优先": 18.0,
    "估值消化优先": 78.0,
    "近端催化优先": 76.0,
    "价格确认/动量": 34.0,
    "激进短线": 100.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict]) -> None:
    nvt_ref.score_companies(companies)
    target = companies[TARGET]
    for strategy, score in PSIX_SCORES.items():
        target.setdefault("scores", {})[strategy] = score
    nvt_ref.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_POWER_SYSTEMS_PEERS:
        return "直接同业"
    if ticker in POWER_AND_ELECTRICAL_ADJACENT or category in {"电力_发电_能源_储能", "配电_电源_功率器件", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    if ticker in UTILITY_AND_POWER_CUSTOMERS or ticker in DATA_CENTER_CUSTOMERS_AND_OPERATORS:
        return "上下游"
    if ticker in SERVER_NETWORK_AND_AI_DEMAND_CHAIN or ticker in SEMI_CHAIN:
        return "上下游"
    if category in {
        "AI服务器_存储_EMS",
        "AI网络_光互联_连接器",
        "AI计算芯片_EDA_IP_custom_ASIC",
        "云算力_IDC_AI软件平台",
        "晶圆制造_前道设备",
        "封测_检测_计量_光罩",
    }:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        return "业务差异大且档位接近" if rel == "跨赛道" else "证据互有强弱且档位接近"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "PSIX有H2 Power Systems恢复锚",
            "右尾弹性优先": "PSIX小盘数据中心电力右尾更大",
            "风险调整收益": "PSIX低估值覆盖部分执行风险",
            "下行保护优先": "PSIX已有盈利和流动性支撑",
            "估值消化优先": "PSIX低PS/PE更易消化估值",
            "近端催化优先": "PSIX Q2/H2和MTL验证更近",
            "价格确认/动量": "PSIX高关注反弹交易更强",
            "激进短线": "PSIX高IV和小盘电力beta更高",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业订单或收入兑现更硬",
            "右尾弹性优先": f"{ticker}同业需求池或利润池更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}现金流和压力期表现更稳",
            "估值消化优先": f"{ticker}同业业绩更能覆盖估值",
            "近端催化优先": f"{ticker}订单/指引催化更明确",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业主题beta更高",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}订单/backlog或交付更清楚",
            "右尾弹性优先": f"{ticker}右尾或利润池弹性更直接",
            "风险调整收益": f"{ticker}增长与估值组合更优",
            "下行保护优先": f"{ticker}现金流或压力期表现更安全",
            "估值消化优先": f"{ticker}订单兑现更能消化估值",
            "近端催化优先": f"{ticker}近端订单或产能催化更强",
            "价格确认/动量": f"{ticker}趋势和资金偏好更强",
            "激进短线": f"{ticker}主题beta和波动更适合进攻",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}收入/RPO或客户兑现更短链",
            "右尾弹性优先": f"{ticker}AI主链或客户侧右尾更大",
            "风险调整收益": f"{ticker}上行和下行组合更优",
            "下行保护优先": f"{ticker}现金流或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更适合短线",
        }[strategy]

    if category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker}AI主链兑现证据更硬",
            "右尾弹性优先": f"{ticker}小基数或AI收入弹性更大",
            "风险调整收益": f"{ticker}增长赔率更能覆盖风险",
            "下行保护优先": f"{ticker}需求能见度或现金流更好",
            "估值消化优先": f"{ticker}高增速更能消化估值",
            "近端催化优先": f"{ticker}产品/订单催化更密集",
            "价格确认/动量": f"{ticker}价格趋势更强",
            "激进短线": f"{ticker}高波动更适合短线进攻",
        }[strategy]

    return {
        "NTM兑现优先": f"{ticker}未来12个月兑现证据更直接",
        "右尾弹性优先": f"{ticker}极端情景上行更大",
        "风险调整收益": f"{ticker}风险调整赔率更好",
        "下行保护优先": f"{ticker}估值或资产质量更安全",
        "估值消化优先": f"{ticker}当前估值更易消化",
        "近端催化优先": f"{ticker}未来两个季度催化更明确",
        "价格确认/动量": f"{ticker}价格行为更强",
        "激进短线": f"{ticker}短线关注度和波动更强",
    }[strategy]


def label_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    at = a.get("tiers", {}).get(strategy, "资料不足")
    bt = b.get("tiers", {}).get(strategy, "资料不足")
    if "资料不足" in (at, bt):
        if at == bt:
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    diff = a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0)
    tier_gap = tier_value(at) - tier_value(bt)
    abs_diff = abs(diff)
    if abs_diff < 4:
        return "中性"

    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 28, 13, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 24, 11, 4
    else:
        strong_cut, suggest_cut, micro_cut = 21, 10, 4

    if diff > 0:
        if tier_gap >= 2 and abs_diff >= strong_cut:
            return "强烈建议投A"
        if tier_gap >= 1 and abs_diff >= suggest_cut:
            return "建议投A"
        if abs_diff >= micro_cut:
            return "微倾向投A"
    else:
        if tier_gap <= -2 and abs_diff >= strong_cut:
            return "强烈建议投B"
        if tier_gap <= -1 and abs_diff >= suggest_cut:
            return "建议投B"
        if abs_diff >= micro_cut:
            return "微倾向投B"
    return "中性"


def cell_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    label = label_for(strategy, a, b, rel)
    return f"{label}：{reason_for(strategy, label, b, rel)}"


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in row_obj[strategy])
    b_count = sum(1 for strategy in STRATS if "投B" in row_obj[strategy])
    neutral = 8 - a_count - b_count
    return a_count, b_count, neutral


def final_choice(row_obj: dict) -> str:
    weights = {
        "NTM兑现优先": 1.15,
        "风险调整收益": 1.20,
        "估值消化优先": 1.15,
        "下行保护优先": 1.05,
        "近端催化优先": 0.85,
        "右尾弹性优先": 0.80,
        "价格确认/动量": 0.45,
        "激进短线": 0.45,
    }
    label_score = {
        "强烈建议投A": 2.0,
        "建议投A": 1.35,
        "微倾向投A": 0.55,
        "中性": 0.0,
        "微倾向投B": -0.55,
        "建议投B": -1.35,
        "强烈建议投B": -2.0,
    }
    score = 0.0
    for strategy in STRATS:
        score += weights[strategy] * label_score.get(tag_in_cell(row_obj[strategy]) or "中性", 0.0)
    return "A" if score > 0.15 else "B" if score < -0.15 else "中性"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    ticker = str(b["ticker"])
    if choice == "中性":
        return "PSIX的右尾、估值和短线弹性与对手兑现、现金流或防守优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["估值消化优先"] > 12:
            return "PSIX的低P/S、低PE和基准盈利情景比对手更容易消化当前估值。"
        if diffs["右尾弹性优先"] > 14:
            return "PSIX的小盘数据中心电力、genset enclosure和power package右尾更大。"
        if diffs["近端催化优先"] > 12:
            return "PSIX的Q2/H2 Power Systems、MTL效率和订单可见度验证更近。"
        if diffs["激进短线"] > 15:
            return "PSIX的高IV、小盘电力题材和数据中心自备电力叙事更适合进攻。"
        return "PSIX在低估值、数据中心电力右尾和近端交付验证之间的组合更好。"

    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、资产质量或压力窗口表现明显强于PSIX。"
    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的订单、RPO、backlog或指引比PSIX更能支撑NTM兑现。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量、估值消化和下行组合优于PSIX。"
    if diffs["价格确认/动量"] < -12:
        return f"{ticker}的价格确认和资金偏好明显强于PSIX。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比PSIX更直接。"
    if diffs["右尾弹性优先"] < -16:
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于PSIX。"
    return f"{ticker}在多数投资思路下比PSIX更符合项目内资金配置目标。"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong = [strategy for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) > tier_value(b.get("tiers", {}).get(strategy))]
    b_strong = [strategy for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) < tier_value(b.get("tiers", {}).get(strategy))]
    close = [strategy for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) == tier_value(b.get("tiers", {}).get(strategy))]
    parts = []
    if a_strong:
        parts.append("A强:" + "、".join(a_strong[:3]))
    if b_strong:
        parts.append("B强:" + "、".join(b_strong[:3]))
    if close:
        parts.append("接近:" + "、".join(close[:2]))
    return "；".join(parts) if parts else "档位接近"


def comparison_sort_key(row_obj: dict) -> tuple[int, str, str]:
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return (rel_order.get(row_obj["relationship"], 9), row_obj["classification"], row_obj["ticker"])


def build_comparisons(companies: dict[str, dict]) -> list[dict]:
    a = companies[TARGET]
    rows = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        row_obj = {
            "ticker": ticker,
            "name": b["name"],
            "classification": base.category_short(str(b.get("category", ""))),
            "relationship": rel,
            "grade_diff": grade_diff_summary(a, b),
        }
        for strategy in STRATS:
            row_obj[strategy] = cell_for(strategy, a, b, rel)
        ac, bc, nc = direction_counts(row_obj)
        row_obj["majority"] = f"A {ac} / B {bc} / 中性 {nc}"
        row_obj["ac"] = ac
        row_obj["bc"] = bc
        row_obj["nc"] = nc
        row_obj["final_choice"] = final_choice(row_obj)
        row_obj["key_reason"] = key_reason(a, b, row_obj, row_obj["final_choice"])
        rows.append(row_obj)
    return sorted(rows, key=comparison_sort_key)


def fmt_num(value, decimals: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{decimals}f}"
    except Exception:
        return "缺失"


def fmt_b(value) -> str:
    if value is None:
        return "缺失"
    try:
        return f"${float(value):.2f}B"
    except Exception:
        return "缺失"


def fmt_pct(value) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):+.2f}%"
    except Exception:
        return "缺失"


def majority_rows(rows: list[dict], final: str, limit: int = 45) -> list[dict]:
    selected = [row for row in rows if row["final_choice"] == final]
    if final == "B":
        selected.sort(key=lambda x: (x["bc"] - x["ac"], x["bc"], -x["nc"]), reverse=True)
    else:
        selected.sort(key=lambda x: (x["ac"] - x["bc"], x["ac"], -x["nc"]), reverse=True)
    return selected[:limit]


def render_report(companies: dict[str, dict], comparisons: list[dict]) -> str:
    a = companies[TARGET]
    latest_dates = sorted({company["date"] for company in companies.values() if company.get("date")})
    date_range = f"{latest_dates[0]} 至 {latest_dates[-1]}" if latest_dates else "缺失"
    missing_fin = sorted([ticker for ticker, company in companies.items() if not company.get("fin")])
    fin = a.get("fin", {})
    m2w = a.get("mom2", {})
    m1m = a.get("mom1", {})
    soxx = a.get("soxx", {})
    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，"
        f"Call IV {fmt_num(fin.get('call_iv'), 1)}%，Put IV {fmt_num(fin.get('put_iv'), 1)}%；"
        f"2026-06-03 过去两周 {fmt_pct(m2w.get('mom2w'))}，过去一月 {fmt_pct(m1m.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    stats: dict[str, Counter] = {strategy: Counter() for strategy in STRATS}
    for row_obj in comparisons:
        for strategy in STRATS:
            stats[strategy][tag_in_cell(row_obj[strategy])] += 1

    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b = majority_rows(comparisons, "B", 45)
    strong_a = majority_rows(comparisons, "A", 45)
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "B")
    final_neutral = len(comparisons) - final_a - final_b
    strong_b_names = "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]])

    support = {
        "NTM兑现优先": (
            "中性偏弱",
            "NTM基准收入650-720百万美元，Q2大体与Q1持平、H2随larger Power Systems orders投产改善，Power Systems仍是主收入池",
            "2026Q1收入同比下降、管理层无正式FY2026指引，数据中心收入和backlog不单列，H2兑现依赖客户排程和MTL/Wisconsin throughput",
        ),
        "右尾弹性优先": (
            "全项目强档",
            "乐观收入800-900百万美元、极度乐观1.0-1.2十亿美元；小市值叠加数据中心custom genset enclosures、integrated packages、5MW平台和microgrid期权",
            "极度乐观可信度低，数据中心细分是研究估算而非公司披露，不能把行业TAM直接映射为PSIX收入",
        ),
        "风险调整收益": (
            "中上档",
            "低估值、已有盈利和基准EBITDA/净利润75-105百万/45-70百万美元给上行赔率提供底盘",
            "Call IV 103.8%、Put IV 81.8%，Q1下滑、oil & gas软、客户延期和高波动削弱风险调整分",
        ),
        "下行保护优先": (
            "全项目弱档",
            "公司仍有盈利、Power Systems需求池和客户预付款/合同负债潜在支撑",
            "2026-06-04三段SOXX压力窗口累计-130.28%，过去一月-42.67%，小盘项目制收入在压力期防守性很弱",
        ),
        "估值消化优先": (
            "全项目顶档",
            "2026-06-22 Forward PE 11.78、P/S 1.26、EV/EBITDA 10.29；若基准EBITDA和净利润兑现，当前估值可被NTM业绩消化",
            "估值便宜建立在H2恢复、GM回到23%-25%和MTL整合不拖累上；若Q2/H2低于路径会变成价值陷阱",
        ),
        "近端催化优先": (
            "强势档",
            "Q2是否不低于Q1、H2 larger Power Systems orders投产、MTL lead time/效率、contract liabilities和5MW/1.5MW产品更新都在1-2季度可验证",
            "催化多为执行验证而非已披露大额backlog，若数据中心客户/订单仍不透明，催化力度会折扣",
        ),
        "价格确认/动量": (
            "弱势档",
            "过去两周到2026-06-03反弹+9.36%，高IV和数据中心电力关注度使交易弹性仍在",
            "过去一月-42.67%、SOXX压力窗口表现最弱之一，2026-06-22本地收盘价39.11美元仍未形成可靠趋势确认",
        ),
        "激进短线": (
            "全项目顶档",
            "Call IV 103.8%、Put IV 81.8%，小盘数据中心电力、备用/过渡供电、microgrid和power package叙事具备短线高beta",
            "激进短线可容忍高风险，但Q2 miss、H2延期或GM未修复会快速反杀",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "数据中心custom genset enclosures/integrated packages",
            "1MW-1.25MW standby/continuous engines和power systems",
            "microgrid/demand response/onsite prime power",
            "oil & gas power products",
            "Industrial/Transportation power systems",
        ]

    lines: list[str] = [
        "# PSIX 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：PSIX / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 PSIX vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。PSIX 的优势集中在低估值消化、小盘数据中心电力右尾、近端Q2/H2执行验证和极高IV带来的短线进攻弹性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是NTM收入仍接近低增长/恢复型路径、数据中心收入和backlog不单列、过去一月和SOXX压力窗口价格表现很弱。",
        "- A 最适合的投资者画像：愿意承受小盘高波动、看重数据中心备用/过渡供电和power package右尾，同时要求估值不能已经透支的进攻型或事件驱动资金。",
        "- A 最不适合的投资者画像：优先追求明确NTM订单/RPO/backlog、低波动下行保护、已验证价格趋势或大市值高确定性复利的资金。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常拥有更硬的订单/RPO/backlog、更直接AI主链收入、更强价格确认或更好的防守属性。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：PSIX 是项目内高右尾、低估值、高短线beta的电力小盘标的，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它不是全项目NTM兑现和下行保护冠军，但在估值消化、右尾弹性和激进短线口径下明显有竞争力。",
        "- 后续最重要跟踪数据：2026Q2收入是否不低于Q1、2026H2 Power Systems订单转收入、数据中心客户/订单/backlog首次披露、MTL lead time和效率、Wisconsin产能吞吐、GM是否回到23%-25%、contract liabilities/客户预付款、oil & gas是否继续拖累、FCF和库存周转。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "PSIX"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "电力_发电_能源_储能")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "$650-720M"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev') or '$800-900M'}；极度乐观：{a.get('extreme_rev') or '$1.0-1.2B'}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a.get('base_margin') or '8-12%'}；利润/现金流：{a.get('base_profit') or 'EBITDA $75-105M，净利润 $45-70M'}；{a.get('base_cash') or '小幅正，取决于客户预付款和扩产周转'}"]),
        base.row(["最大传导瓶颈", "数据中心收入不单列，订单/客户排程可见度不足；H2大型Power Systems订单、Wisconsin/MTL制造throughput和客户验收决定收入确认。"]),
        base.row(["最大反证", "2026Q1收入同比下降、Power Systems仍同比下滑，管理层不给FY2026正式指引；若Q2低于Q1、H2延迟或GM停留在21%-23%，基准路径失效。"]),
        base.row(["近端催化剂", "Q2收入、H2 Power Systems恢复、MTL效率、contract liabilities/客户预付款、数据中心订单/客户可见度、5MW标准化package和1.5MW gas engine进展。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]

    for strategy in STRATS:
        tier = a.get("tiers", {}).get(strategy, "资料不足")
        position = f"{support[strategy][0]}；评分排名 {a.get('ranks', {}).get(strategy)}/{a.get('rank_total', {}).get(strategy)}"
        lines.append(base.row([strategy, tier, position, support[strategy][1], support[strategy][2]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与PSIX在发动机、genset、power systems、备用/过渡供电、数据中心电力包或发电设备需求池高度重叠；优先比较订单/backlog、收入兑现、产品代际、毛利率、客户质量和同业估值。", "CAT、CMI、GEV、GNRC、RYCEY", "判断力度最高；若同业在订单、规模、现金流或压力期表现更强，可压过PSIX的低估值和小盘右尾。"]),
        base.row(["相邻替代", "同属AI园区电力、配电、冷却、储能、核能、工程建设或工业基础设施资金篮子，但产品不完全重叠。", "ETN、HUBB、NVT、POWL、VRT、MOD、JCI、PWR、EME、FIX、BE、SMR、OKLO", "重点回答资金只能买一个时，谁的增长质量、估值消化、现金流和近端催化更好。"]),
        base.row(["上下游", "B位于PSIX需求链上下游，如云厂、IDC、NeoCloud、服务器、芯片、网络、半导体设备材料、公用事业和电力客户。", "MSFT、AMZN、GOOGL、META、ORCL、EQIX、DLR、CRWV、NVDA、DELL、ANET、TSM、ASML、AEP、CEG、VST", "不把下游capex直接等同PSIX收入；若对方拥有更直接AI收入、RPO或价格确认，可在右尾、催化和动量列胜出。"]),
        base.row(["跨赛道", "业务差异较大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "部分材料、化学品、软件、生命科学和航天公司", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]

    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    lines.append(base.row(headers))
    lines.append(base.row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for idx, row_obj in enumerate(comparisons, 1):
        cells = [
            idx,
            f"{row_obj['ticker']} / {row_obj['name']}",
            row_obj["classification"],
            row_obj["relationship"],
            row_obj["grade_diff"],
        ] + [row_obj[strategy] for strategy in STRATS] + [
            row_obj["majority"],
            row_obj["final_choice"],
            row_obj["key_reason"],
        ]
        lines.append(base.row(cells))

    lines += [
        "",
        "## 6. 投资思路统计",
        "",
        base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]),
        base.row(["---"] + ["---:"] * 9),
    ]
    for strategy in STRATS:
        c = stats[strategy]
        lines.append(base.row([strategy] + [c[tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    lines += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for idx, row_obj in enumerate(strong_b, 1):
        wins = [strategy for strategy in STRATS if "投B" in row_obj[strategy]]
        catchup = "PSIX需要证明Q2/H2收入转化、数据中心订单/backlog、GM修复和FCF能同步兑现，并改善压力期价格表现。"
        if row_obj["relationship"] == "直接同业":
            catchup = "PSIX需要在直接同业中证明数据中心电力包订单、交付速度、毛利率和客户可见度强于B。"
        elif row_obj["relationship"] == "上下游":
            catchup = "PSIX需要证明云厂/AI主链capex能持续落到其power systems收入和利润，而不是只停留在行业TAM。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for idx, row_obj in enumerate(strong_a, 1):
        wins = [strategy for strategy in STRATS if "投A" in row_obj[strategy]]
        catchup = "B需要拿出更清晰的NTM收入/利润兑现、订单或客户合同，并证明估值、现金流和压力窗口能承受波动。"
        if "估值消化优先" in wins and row_obj["final_choice"] == "A":
            catchup = "B需要把增长叙事转成可确认收入、利润和现金流，并降低估值透支或融资反证。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/电力_发电_能源_储能/PSIX_Power_Solutions_International_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心发电机组与燃气轮机_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与BESS_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心中压配电、switchgear与变压器_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心土建、MEP与预制化交付_2026-06-10.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- PSIX 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_psix_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台/冷却标的使用既有正式脚本的最低分校准，对PSIX的NTM恢复路径、数据中心电力右尾、低估值、高IV、Q2/H2催化、价格破位和压力窗口反证做目标公司校准后建档；未读取下游量化目录、现成排序结论或既有公司对比成品。",
        "",
        "### 公司全集最新正式评估文件清单",
        "",
        base.row(["股票代号", "公司名称", "评估日期", "正式评估文件"]),
        base.row(["---", "---", "---", "---"]),
    ]
    for ticker in sorted(companies):
        company = companies[ticker]
        lines.append(base.row([ticker, company["name"], company["date"], f"`分析报告/公司评估/结果/{Path(company['path']).name}`"]))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 PSIX 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    a = companies[TARGET]
    print(
        json.dumps(
            {
                "target": TARGET,
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "psix_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "psix_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "psix_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
