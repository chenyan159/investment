from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_pwr_company_comparison as calibrated


TARGET = "RKLB"
TARGET_NAME = "Rocket Lab"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "RKLB_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

SPACE_DEFENSE_ADJACENT = {
    "BWXT",
    "RYCEY",
    "TDY",
    "MSI",
    "OKLO",
    "SMR",
    "GEV",
    "CEG",
    "VST",
}

SPACE_SYSTEMS_COMPONENT_TOUCHPOINTS = {
    "ADI",
    "COHR",
    "LITE",
    "MTSI",
    "SITM",
    "VIAV",
    "VECO",
    "MTRN",
    "HOCPY",
    "ENTG",
    "MKSI",
    "TDKDY",
    "TTDKY",
}

AI_INFRA_CAPITAL_ALTERNATIVES = {
    "AAOI",
    "ALAB",
    "AMD",
    "AMZN",
    "ANET",
    "APLD",
    "ARM",
    "AVGO",
    "BE",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "CRWV",
    "DELL",
    "ETN",
    "FN",
    "GOOGL",
    "HPE",
    "IREN",
    "JBL",
    "META",
    "MRVL",
    "MSFT",
    "MU",
    "NBIS",
    "NVDA",
    "ORCL",
    "POET",
    "POWL",
    "SMCI",
    "SMTC",
    "VRT",
}

STABLE_QUALITY_ALTERNATIVES = {
    "LIN",
    "APD",
    "ECL",
    "TMO",
    "DHR",
    "MMM",
    "CAT",
    "PH",
    "JCI",
    "TT",
    "CARR",
    "NDSN",
    "FTV",
    "DOV",
}

RKLB_SCORES = {
    "NTM兑现优先": 74.0,
    "右尾弹性优先": 85.0,
    "风险调整收益": 36.0,
    "下行保护优先": 24.0,
    "估值消化优先": 20.0,
    "近端催化优先": 78.0,
    "价格确认/动量": 55.0,
    "激进短线": 93.5,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def recompute_tiers(companies: dict[str, dict]) -> None:
    calibrated.nvt_ref.recompute_tiers(companies)


def score_companies(companies: dict[str, dict]) -> None:
    calibrated.score_companies(companies)
    target = companies[TARGET]
    for strategy, score in RKLB_SCORES.items():
        target.setdefault("scores", {})[strategy] = score
    recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in SPACE_SYSTEMS_COMPONENT_TOUCHPOINTS:
        return "上下游"
    if ticker in SPACE_DEFENSE_ADJACENT:
        return "相邻替代"
    if ticker in AI_INFRA_CAPITAL_ALTERNATIVES:
        return "相邻替代"
    if category in HIGH_GROWTH_CATS:
        return "相邻替代"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        return "业务差异大且档位接近" if rel == "跨赛道" else "证据互有强弱且档位接近"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "RKLB有Q2指引、backlog和12个月转化锚",
            "右尾弹性优先": "Neutron、SDA/HASTE和Space Systems右尾更大",
            "风险调整收益": "对手反证更重，RKLB增长赔率略占优",
            "下行保护优先": "对手更脆弱，RKLB订单池略有支撑",
            "估值消化优先": "对手估值兑现更难，RKLB高增速略胜",
            "近端催化优先": "Q2、HASTE、SDA和Neutron节点更近",
            "价格确认/动量": "航天主题和高波动仍有资金关注",
            "激进短线": "Neutron/HASTE/国防空间叙事更适合进攻",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}组件、设备或客户收入更短链",
            "右尾弹性优先": f"{ticker}空间/电子组件或AI链右尾更直接",
            "风险调整收益": f"{ticker}盈利质量和估值组合更好",
            "下行保护优先": f"{ticker}现金流、资产质量或估值更稳",
            "估值消化优先": f"{ticker}当前业绩更能覆盖估值",
            "近端催化优先": f"{ticker}订单、产品或财报催化更清楚",
            "价格确认/动量": f"{ticker}价格确认强于RKLB",
            "激进短线": f"{ticker}短线资金关注和波动更强",
        }[strategy]

    if rel == "相邻替代" or category in HIGH_GROWTH_CATS or category in INFRA_CATS:
        if category in {"AI计算芯片_EDA_IP_custom_ASIC", "AI网络_光互联_连接器", "AI服务器_存储_EMS", "云算力_IDC_AI软件平台"}:
            return {
                "NTM兑现优先": f"{ticker} AI主链收入兑现更硬",
                "右尾弹性优先": f"{ticker} AI数据中心右尾更直接",
                "风险调整收益": f"{ticker} 增长质量更能覆盖风险",
                "下行保护优先": f"{ticker} 现金流或需求能见度更好",
                "估值消化优先": f"{ticker} AI收入更能消化估值",
                "近端催化优先": f"{ticker} 产品/订单催化更密集",
                "价格确认/动量": f"{ticker} 价格趋势确认更强",
                "激进短线": f"{ticker} AI beta更适合短线进攻",
            }[strategy]
        if category in INFRA_CATS:
            return {
                "NTM兑现优先": f"{ticker} 订单/backlog或交付更清楚",
                "右尾弹性优先": f"{ticker} AI电力/设备利润池更直接",
                "风险调整收益": f"{ticker} 增长与估值组合更优",
                "下行保护优先": f"{ticker} 现金流或压力期表现更安全",
                "估值消化优先": f"{ticker} 业绩更能消化当前估值",
                "近端催化优先": f"{ticker} 近端订单或产能催化更强",
                "价格确认/动量": f"{ticker} 趋势和资金偏好更强",
                "激进短线": f"{ticker} 主题beta和波动更适合进攻",
            }[strategy]
        return {
            "NTM兑现优先": f"{ticker} 未来12个月收入证据更直接",
            "右尾弹性优先": f"{ticker} 极端情景上行更大",
            "风险调整收益": f"{ticker} 风险调整赔率更好",
            "下行保护优先": f"{ticker} 资产质量或估值更安全",
            "估值消化优先": f"{ticker} 当前估值更容易消化",
            "近端催化优先": f"{ticker} 未来两个季度催化更明确",
            "价格确认/动量": f"{ticker} 价格行为更强",
            "激进短线": f"{ticker} 短线关注度和波动更强",
        }[strategy]

    if ticker in STABLE_QUALITY_ALTERNATIVES:
        return {
            "NTM兑现优先": f"{ticker}经营兑现更成熟",
            "右尾弹性优先": f"{ticker}右尾虽小但质量更可验证",
            "风险调整收益": f"{ticker}现金流和估值组合更稳",
            "下行保护优先": f"{ticker}盈利稳定性和低IV更强",
            "估值消化优先": f"{ticker}成熟利润更能消化估值",
            "近端催化优先": f"{ticker}财报兑现比RKLB更清楚",
            "价格确认/动量": f"{ticker}价格趋势更健康",
            "激进短线": f"{ticker}短线赔率更不依赖Neutron",
        }[strategy]

    return {
        "NTM兑现优先": f"{ticker}NTM利润或收入兑现更稳",
        "右尾弹性优先": f"{ticker}极端情景或估值空间更优",
        "风险调整收益": f"{ticker}上行下行组合更好",
        "下行保护优先": f"{ticker}现金流、估值或资产质量更安全",
        "估值消化优先": f"{ticker}当前估值更容易消化",
        "近端催化优先": f"{ticker}近端事件更容易重定价",
        "价格确认/动量": f"{ticker}价格行为更强",
        "激进短线": f"{ticker}短线弹性更清晰",
    }[strategy]


def label_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    at = a.get("tiers", {}).get(strategy, "资料不足")
    bt = b.get("tiers", {}).get(strategy, "资料不足")
    if "资料不足" in (at, bt):
        if at == bt:
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    diff = float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0))
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


def tag_in_cell(cell: str) -> str:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return "中性"


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in row_obj[strategy])
    b_count = sum(1 for strategy in STRATS if "投B" in row_obj[strategy])
    return a_count, b_count, 8 - a_count - b_count


def final_choice(row_obj: dict) -> str:
    weights = {
        "NTM兑现优先": 1.10,
        "风险调整收益": 1.25,
        "估值消化优先": 1.20,
        "下行保护优先": 1.10,
        "近端催化优先": 0.90,
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
        score += weights[strategy] * label_score.get(tag_in_cell(row_obj[strategy]), 0.0)
    return "A" if score > 0.15 else "B" if score < -0.15 else "中性"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    ticker = str(b["ticker"])
    category = str(b.get("category", ""))
    diffs = {strategy: float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0)) for strategy in STRATS}
    if choice == "中性":
        return "RKLB的航天右尾与对手的兑现、估值或防守优势未拉开强判差距。"

    if choice == "A":
        if diffs["右尾弹性优先"] > 15:
            return "RKLB的Space Systems、Electron/HASTE、Neutron和国防空间订单提供更大的非线性右尾。"
        if diffs["近端催化优先"] > 12:
            return "RKLB的Q2收入、backlog转化、HASTE执行、SDA里程碑和Neutron首飞节点更近端可验证。"
        if diffs["NTM兑现优先"] > 10:
            return "RKLB有FY2026 Q2指引、22.20亿美元backlog和约36%十二个月转化池支撑收入兑现。"
        if diffs["激进短线"] > 12:
            return "RKLB高IV、航天稀缺性和Neutron/HASTE叙事更适合激进进攻。"
        return "RKLB在增长弹性和近端航天催化上更清楚，对手缺少足够兑现或右尾证据。"

    if category in {"AI计算芯片_EDA_IP_custom_ASIC", "AI网络_光互联_连接器", "AI服务器_存储_EMS", "云算力_IDC_AI软件平台"}:
        return f"{ticker}拥有更直接的AI数据中心收入、利润池或客户capex传导，RKLB当前AI数据中心收入按0处理。"
    if diffs["估值消化优先"] < -18:
        return f"{ticker}的当前利润、现金流或估值消化能力明显强于RKLB。"
    if diffs["下行保护优先"] < -18:
        return f"{ticker}的现金流、资产质量、IV或压力期表现明显强于RKLB。"
    if diffs["风险调整收益"] < -14:
        return f"{ticker}的上行和下行组合优于高估值、负FCF的RKLB。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker}的收入/利润兑现证据比仍处亏损和项目制执行风险的RKLB更硬。"
    if diffs["价格确认/动量"] < -12:
        return f"{ticker}的价格确认和短线资金偏好明显强于RKLB。"
    return f"{ticker}在多数投资思路下比RKLB更符合项目内资金配置目标。"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong = [strategy.replace("优先", "") for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) > tier_value(b.get("tiers", {}).get(strategy))]
    b_strong = [strategy.replace("优先", "") for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) < tier_value(b.get("tiers", {}).get(strategy))]
    close = [strategy.replace("优先", "") for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) == tier_value(b.get("tiers", {}).get(strategy))]

    def joined(items: list[str]) -> str:
        return "无" if not items else "、".join(items[:3]) + ("等" if len(items) > 3 else "")

    return f"A强：{joined(a_strong)}；B强：{joined(b_strong)}；接近：{joined(close)}"


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
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {fmt_num(fin.get('call_iv'), 1)}%，"
        f"Put IV {fmt_num(fin.get('put_iv'), 1)}%；2026-06-03 过去两周 {fmt_pct(m2w.get('mom2w'))}，"
        f"过去一月 {fmt_pct(m1m.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
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
    strong_b_names = "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]]) or "无明显集中反方"

    support = {
        "NTM兑现优先": (
            "全项目强势成长档",
            "FY2026 Q1收入200.3M美元、Q2指引225-240M美元，Q1末backlog 2.220B美元且约36%预计12个月内确认，Space Systems与Launch均有正式订单锚",
            "利润仍亏损，固定价Space Systems项目、HASTE/Electron cadence、Neutron进度和并购整合会影响收入转利润质量",
        ),
        "右尾弹性优先": (
            "全项目强势右尾档",
            "Neutron中型火箭、SDA/USSF国防卫星prime、HASTE高超声速测试、Mynaric/Gauss/Motiv组件化和轨道数据中心远期期权共同构成非线性右尾",
            "当前AI数据中心可确认收入为0；Neutron未商业首飞，极度乐观情景必须等待飞行、客户和收入确认",
        ),
        "风险调整收益": (
            "偏弱风险调整档",
            "收入增长和订单池真实，商业航天稀缺性高，若Neutron或国防空间新增合同兑现，上行足够大",
            f"2026-06-22 P/S {fmt_num(fin.get('ps'), 2)}、Forward PE不适用、EV/EBITDA为负，基准FCF仍为负，压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}",
        ),
        "下行保护优先": (
            "弱势防守档",
            "backlog和政府/国防项目提供一定收入可见度，公司不是单纯无收入早期题材",
            f"TTM EPS为负、Forward EPS为负、Call IV {fmt_num(fin.get('call_iv'), 1)}%，2026-06-04三段SOXX压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}，安全边际弱",
        ),
        "估值消化优先": (
            "全项目弱势估值消化档",
            "NTM基准收入980M-1.08B美元，若乐观收入和毛利率改善兑现，收入增速可以部分缓冲高倍数",
            f"市值约 {fmt_b(fin.get('market_cap_b'))}，P/S约 {fmt_num(fin.get('ps'), 2)}，TTM/Forward PE均不适用，基准调整后EBITDA仍可能为负",
        ),
        "近端催化优先": (
            "全项目顶层催化档",
            "Q2 2026收入和毛利率、backlog 12个月转化、SDA/SSC里程碑、HASTE发射节奏、Neutron首飞/发动机/LC-3、Mynaric/Gauss/Motiv订单均是1-2季度可验证点",
            "催化强但也容易变反证；任一关键节点延迟会直接伤害估值消化和短线价格",
        ),
        "价格确认/动量": (
            "中性偏弱动量档",
            f"2026-06-03过去1个月上涨 {fmt_pct(m1m.get('mom1m'))}，说明题材资金曾明显确认",
            f"2026-06-03过去两周 {fmt_pct(m2w.get('mom2w'))}，且2026-06-22收盘价100.29低于2026-06-03的114.70，短期动量已回落",
        ),
        "激进短线": (
            "全项目强势短线进攻档",
            f"航天稀缺性、Neutron/HASTE/SDA/Golden Dome叙事、约90%近月IV、近期财报和发射节点使RKLB适合高风险短线进攻",
            "高IV和高估值会吞噬赔率；若Neutron或Q2交付不及预期，短线回撤会很快",
        ),
    }

    product_names = [
        "Space Systems国防整星/卫星平台",
        "Space Systems组件与子系统",
        "Electron与HASTE发射服务",
        "Neutron中型可复用火箭",
        "Mynaric激光光通信",
        "Gauss电推进",
        "Motiv空间机器人/精密机构",
        "轨道数据中心远期期权",
    ]

    lines: list[str] = [
        "# RKLB 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：RKLB / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 RKLB vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。RKLB 的优势集中在商业航天稀缺性、Space Systems国防订单、Electron/HASTE发射底盘、Neutron右尾、Q2/backlog转化和高波动短线关注。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是当前估值已反映Neutron成功和国防空间持续追加，TTM/Forward PE不适用，FCF仍为负，SOXX压力窗口回撤极大。",
        "- A 最适合的投资者画像：愿意承担高波动和高估值，押注商业航天第二供应商、美国国防低轨星座、HASTE高超声速测试和Neutron商业化的激进成长资金。",
        "- A 最不适合的投资者画像：要求成熟盈利、估值可由NTM利润迅速消化、压力期防守或低IV稳定回撤的质量/防守资金。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常拥有更直接的AI数据中心收入、成熟利润/现金流、估值消化能力、下行保护或更健康价格确认。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：RKLB 最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它是项目内极强右尾/短线航天期权，但不是风险调整、估值消化或下行保护维度的核心配置答案。",
        "- 后续最重要跟踪数据：Q2 2026收入和毛利率、backlog总额和12个月转化比例、Space Systems项目毛利、SDA/SSC里程碑、HASTE发射节奏、Neutron首飞/发动机/LC-3、Mynaric/Gauss/Motiv客户订单、contract liabilities、应收/库存/OCF/FCF、任何轨道数据中心或空间AI正式合同。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "RKLB"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "机电_冷却_工程_水处理_边缘工业AI")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "980M-1.08B 美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev') or '1.12-1.25B 美元'}；极度乐观：{a.get('extreme_rev') or '1.32-1.50B 美元'}"]),
        base.row(["利润和现金流结论", "基准调整后EBITDA约 -70M 至 -20M 美元，GAAP净利润大概率仍为负；基准FCF约 -250M 至 -150M 美元，乐观情景才可能接近现金流改善拐点。"]),
        base.row(["最大传导瓶颈", "backlog按期确认、Space Systems固定价项目控本、HASTE/Electron cadence、Neutron首飞和可重复商业发射、Mynaric/Gauss/Motiv整合。"]),
        base.row(["最大反证", "2026-06-22 P/S约92，TTM/Forward PE不适用，FCF仍为负；AI数据中心当前可确认收入为0，Neutron仍未商业首飞。"]),
        base.row(["近端催化剂", "Q2 2026收入/毛利率、backlog转化、SDA/SSC里程碑、HASTE任务节奏、Neutron首飞/发动机/LC-3、组件新品客户订单和现金流数据。"]),
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
        base.row(["直接同业", "项目内没有纯商业航天发射/卫星prime公司，因此本报告没有把任何B强行列为直接同业；若后续纳入ASTS、LUNR、PL、SPIR或传统卫星prime，可单独重跑。", "本次无典型直接同业", "避免误把AI电力、芯片、云或工业公司硬套成火箭/卫星同业；同业证据不足时不放大结论力度。"]),
        base.row(["相邻替代", "同属高增长、硬科技、国防/空间、AI基础设施或物理基础设施资金篮子，资金可能在RKLB与这些公司之间二选一。", "NVDA、AVGO、CRWV、VRT、ETN、POWL、OKLO、SMR、BWXT、RYCEY、TDY", "默认比较增长质量、右尾、估值消化、近端催化和风险调整收益；不因航天叙事稀缺就自动胜出。"]),
        base.row(["上下游", "可能与RKLB的卫星组件、光通信、射频/电源/测试、空间材料或客户需求链有局部触点，但不是地面AI数据中心链条。", "COHR、LITE、VIAV、MTSI、SITM、VECO、MTRN、ADI", "只在产品/组件/客户触点上加权，不把AI光模块或半导体需求直接等同RKLB收入。"]),
        base.row(["跨赛道", "业务差异较大，但作为项目内资金配置替代仍比较增长质量、估值消化、下行保护和催化可见度。", "LIN、APD、ECL、TMO、DHR、MMM、CAT、PH等", "默认降低结论力度；若证据互有强弱，优先使用中性或微倾向。"]),
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
        catchup = "RKLB需要证明Q2/Q3收入和毛利率高于指引、backlog转化加快、Neutron首飞成功且订单转收入，同时FCF消耗和估值压力下降。"
        if row_obj["relationship"] == "相邻替代" and any(cat in row_obj["classification"] for cat in ["AI计算", "AI网络", "AI服务器", "云算力"]):
            catchup = "RKLB需要拿出可确认的AI/空间数据合同，或证明国防空间收入和Neutron商业化能提供不弱于AI主链的利润池。"
        elif row_obj["relationship"] == "上下游":
            catchup = "RKLB需要把组件/光通信/卫星平台触点转成外部收入、毛利率和现金流，而不是只停留在技术入口。"
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
        if "右尾弹性优先" in wins or "激进短线" in wins:
            catchup = "B需要证明自己的右尾可收入化程度、近端催化或短线资金关注不弱于RKLB的Neutron/HASTE/国防空间叙事。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/机电_冷却_工程_水处理_边缘工业AI/RKLB_Rocket_Lab_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/产业背景/AI产业链全局图谱与口径字典_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI云算力外包和NeoCloud与AI数据中心运营商_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- RKLB 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_rklb_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台/冷却标的沿用既有正式脚本的最低分校准，对RKLB的Q2指引、backlog、Space Systems、Electron/HASTE、Neutron、Mynaric/Gauss/Motiv、AI数据中心当前收入为0、估值、IV、价格确认和压力窗口做目标公司校准后建档；未读取下游量化目录、现成排序结论或既有公司对比成品。",
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
        raise SystemExit("缺少 RKLB 正式评估文件")
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
                "rklb_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "rklb_scores": {strategy: round(float(a.get("scores", {}).get(strategy, 0)), 2) for strategy in STRATS},
                "rklb_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
