from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_nvt_company_comparison as nvt_ref


TARGET = "PWR"
TARGET_NAME = "Quanta Services"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "PWR_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_ENGINEERING_PEERS = {
    "EME",
    "FIX",
    "IESC",
    "MYRG",
}

UPSTREAM_EQUIPMENT = {
    "ABBNY",
    "AEIS",
    "ATKR",
    "ETN",
    "GEV",
    "HUBB",
    "HTHIY",
    "IFNNY",
    "LFUS",
    "MIELY",
    "MRAAY",
    "NVT",
    "POWL",
    "ST",
    "TTDKY",
    "VICR",
    "VRT",
    "VSH",
}

FACILITY_INFRA_ADJACENT = {
    "AAON",
    "ALLE",
    "AMPX",
    "BE",
    "BWXT",
    "CARR",
    "CAT",
    "CEG",
    "CMI",
    "DCI",
    "DD",
    "DHR",
    "DKILY",
    "DOV",
    "ECL",
    "ENS",
    "ENPH",
    "FCEL",
    "FLNC",
    "FTV",
    "GNRC",
    "JCI",
    "MOD",
    "MMM",
    "MSI",
    "NDSN",
    "OKLO",
    "PH",
    "PNR",
    "PSIX",
    "RYCEY",
    "SMR",
    "TDY",
    "TMO",
    "TT",
    "VST",
}

UTILITY_AND_POWER_CUSTOMERS = set(getattr(nvt_ref, "UTILITY_AND_POWER_CUSTOMERS", set())) | {
    "AEP",
    "DTE",
    "ET",
    "ETR",
}
DATA_CENTER_CUSTOMERS_AND_OPERATORS = set(getattr(nvt_ref, "DATA_CENTER_CUSTOMERS_AND_OPERATORS", set()))
SERVER_NETWORK_AND_AI_DEMAND_CHAIN = set(getattr(nvt_ref, "SERVER_NETWORK_AND_AI_DEMAND_CHAIN", set()))
SEMI_CHAIN = set(getattr(nvt_ref, "SEMI_CHAIN", set()))

PWR_SCORES = {
    "NTM兑现优先": 86.0,
    "右尾弹性优先": 74.0,
    "风险调整收益": 66.0,
    "下行保护优先": 84.0,
    "估值消化优先": 62.0,
    "近端催化优先": 79.0,
    "价格确认/动量": 48.0,
    "激进短线": 68.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict]) -> None:
    nvt_ref.score_companies(companies)
    target = companies[TARGET]
    for strategy, score in PWR_SCORES.items():
        target.setdefault("scores", {})[strategy] = score
    nvt_ref.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_ENGINEERING_PEERS:
        return "直接同业"
    if ticker in UPSTREAM_EQUIPMENT or ticker in UTILITY_AND_POWER_CUSTOMERS or ticker in DATA_CENTER_CUSTOMERS_AND_OPERATORS:
        return "上下游"
    if ticker in SERVER_NETWORK_AND_AI_DEMAND_CHAIN or ticker in SEMI_CHAIN:
        return "上下游"
    if ticker in FACILITY_INFRA_ADJACENT:
        return "相邻替代"
    if category in {"电力_发电_能源_储能", "配电_电源_功率器件", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
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
            "NTM兑现优先": "PWR有FY2026指引、12个月backlog和RPO硬锚",
            "右尾弹性优先": "PWR大负荷电力/数据中心电气右尾可兑现",
            "风险调整收益": "PWR订单、FCF和工程执行质量更均衡",
            "下行保护优先": "PWR backlog/FCF和压力期韧性更强",
            "估值消化优先": "PWR用backlog转收入更能消化估值",
            "近端催化优先": "PWR Q2/Q3 backlog和NiSource节点更近",
            "价格确认/动量": "PWR压力期韧性和AI电力资金偏好更好",
            "激进短线": "PWR AI电力工程主题仍有短线弹性",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业收入或backlog兑现更硬",
            "右尾弹性优先": f"{ticker}同业小基数或利润弹性更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}现金流和压力期表现更稳",
            "估值消化优先": f"{ticker}同业业绩更能覆盖估值",
            "近端催化优先": f"{ticker}订单/RPO或指引催化更明确",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业主题beta更高",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}订单/RPO或客户兑现更短链",
            "右尾弹性优先": f"{ticker}AI主链或设备利润池右尾更大",
            "风险调整收益": f"{ticker}上行和下行组合更优",
            "下行保护优先": f"{ticker}现金流或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更适合短线",
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
        return "PWR的工程兑现、下行韧性与对手增长、估值或右尾优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["NTM兑现优先"] > 10:
            return "PWR有FY2026收入指引347-352亿美元、484.71亿美元backlog、262.42亿美元RPO和282.33亿美元12个月backlog支撑兑现。"
        if diffs["下行保护优先"] > 12:
            return "PWR的backlog、FCF路径和SOXX压力窗口韧性使其下行保护优于对手。"
        if diffs["风险调整收益"] > 10:
            return "PWR在AI电力需求、工程执行、现金流和估值消化之间的风险调整组合更均衡。"
        if diffs["近端催化优先"] > 10:
            return "PWR的Q2/Q3 revenue、Electric backlog、RPO、NiSource节点和CEI/DSI/Tri-City整合更近端可验证。"
        if diffs["估值消化优先"] > 10:
            return "PWR可用高覆盖backlog和Electric收入兑现来消化当前估值。"
        return "PWR拥有真实电力/数据中心工程需求、backlog和现金流底盘，对手证据不足以压过。"

    if diffs["右尾弹性优先"] < -18:
        return f"{ticker}的AI主链、小基数或设备利润池右尾明显大于PWR。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和短线资金偏好明显强于PWR。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比PWR更直接。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker}的订单/RPO/backlog或收入确认证据比PWR更硬。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量、估值消化和下行组合优于PWR。"
    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、估值缓冲或防御属性明显强于PWR。"
    return f"{ticker}在多数投资思路下比PWR更符合项目内资金配置目标。"


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
    strong_b_names = "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]])

    support = {
        "NTM兑现优先": (
            "全项目强档",
            "2026Q1收入78.75亿美元，FY2026收入指引347.0-352.0亿美元；总backlog 484.71亿美元、RPO 262.42亿美元、12个月backlog 282.33亿美元覆盖FY2026中点约80.8%",
            "backlog转收入仍受项目NTP、许可、OEM设备交期、劳动力、commissioning、客户验收和营运资本节奏约束",
        ),
        "右尾弹性优先": (
            "强势但非顶档",
            "数据中心园区电气、低压系统、预制电力模块、机械/process piping、液冷设施侧集成、发电+BESS/microgrid和NiSource 3GW提供右尾",
            "PWR不是GPU、UPS、变压器、PDU或燃机OEM，硬件ASP和垄断利润主要留给设备商；公司基数大，非线性弱于小盘AI主链",
        ),
        "风险调整收益": (
            "全项目顶档",
            "收入能见度、Electric backlog、FCF路径和工程执行能力较强，AI电力建设需求与传统公用事业维护需求形成双底盘",
            f"估值已反映较多AI电力预期；2026-06-22 Forward PE {fmt_num(fin.get('forward_pe'), 2)}、P/S {fmt_num(fin.get('ps'), 2)}、EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}",
        ),
        "下行保护优先": (
            "强势防守档",
            f"backlog、RPO、FCF和公用事业客户粘性提供缓冲，三段SOXX压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}",
            "工程承包仍有项目制营运资本、合同资产、设备延迟、固定价格/变更单和客户验收风险",
        ),
        "估值消化优先": (
            "中上档",
            "基准收入365-380亿美元、adjusted EBITDA 38-41亿美元和FCF 18-23亿美元可用backlog转收入消化估值",
            "若Electric margin、工作资本或大项目现金回收低于预期，估值消化会明显放慢；当前价格已包含AI电力瓶颈溢价",
        ),
        "近端催化优先": (
            "强势档",
            "Q2/Q3收入、Electric/Underground backlog、RPO、NiSource 3GW项目NTP/backlog、CEI/DSI/Tri-City整合、FCF和合同资产都是1-2季度可验证点",
            "催化更多来自财报和backlog验证，不是单一新品发布；NiSource等大项目若只停留在合作框架，短期重定价会受限",
        ),
        "价格确认/动量": (
            "中性偏弱",
            f"压力窗口韧性较好，但2026-06-03过去两周 {fmt_pct(m2w.get('mom2w'))}、过去一月 {fmt_pct(m1m.get('mom1m'))}，短期价格确认不如AI主链和高beta设备股",
            "若价格继续横盘或工程/现金流数据低于预期，基本面优势不会自动转成动量优势",
        ),
        "激进短线": (
            "弱势短线档",
            f"AI电力工程、time-to-power、NiSource、CEI/DSI/Tri-City和Call IV {fmt_num(fin.get('call_iv'), 1)}%提供一定进攻性",
            "大市值工程服务属性使爆发力弱于光互联、NeoCloud、核能开发、小盘电力设备和高IV AI芯片链",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "输电、变电、配电、公用事业互联",
            "数据中心园区电气与预制化电力模块",
            "机械/process piping与液冷设施侧集成",
            "发电、BESS、microgrid和大负荷供电协调",
            "可再生能源+BESS EPC",
            "地下公用事业、通信、管线和维护",
        ]

    lines: list[str] = [
        "# PWR 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：PWR / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 PWR vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。PWR 的优势集中在FY2026收入指引、12个月backlog/RPO覆盖、Electric Segment backlog、AI数据中心time-to-power/园区电气施工需求、FCF路径和压力窗口韧性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是PWR不是硬件OEM，不能直接捕获GPU、UPS、变压器、PDU、燃机等设备利润池；工程服务基数大、利润率非线性有限，短线动量也弱于更高beta AI主链。",
        "- A 最适合的投资者画像：想配置AI数据中心电力和大负荷并网的物理执行端，且更看重真实backlog、收入兑现、现金流和下行韧性，而不是追求最高短线爆发的中期成长/质量资金。",
        "- A 最不适合的投资者画像：只追求最大右尾、小基数非线性、高IV短线进攻、AI芯片/内存/光互联或设备ASP弹性的资金；这类资金通常会偏向NVDA、AVGO、MU、ALAB、CRDO、VRT、POWL、OKLO、SMR等。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常拥有更直接AI主链收入、更高设备利润池、更大右尾弹性、更强近端产品/订单催化或更明显价格确认。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：PWR 是项目内偏强的AI电力/工程执行平台，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它明显强于许多低兑现、弱现金流或估值难消化标的，但面对顶级AI主链、电气设备OEM、小盘核能/电力高beta和部分云/平台龙头时需要按投资思路拆分。",
        "- 后续最重要跟踪数据：Q2/Q3 revenue、Electric/Underground segment margin、total backlog、RPO、12个月backlog、NiSource 3GW项目NTP/backlog、CEI/DSI/Tri-City整合、OCF/FCF、contract assets/AR、transformer/switchgear/gas turbine交期、hyperscaler/NeoCloud电力需求和BTM许可/设备PO。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "PWR"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "电力_发电_能源_储能")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "365-380 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev') or '390-415 亿美元'}；极度乐观：{a.get('extreme_rev') or '425-465 亿美元'}"]),
        base.row(["利润和现金流结论", "基准 adjusted EBITDA 38-41亿美元、GAAP净利润15-18亿美元、FCF 18-23亿美元；乐观/极度乐观情景有利润杠杆，但大项目工作资本会放大现金流波动。"]),
        base.row(["最大传导瓶颈", "项目NTP、许可、OEM设备交期、utility interconnection、合格劳动力、prefab产能、commissioning和客户验收，而不是单纯需求不足。"]),
        base.row(["最大反证", "数据中心AI-only收入、客户项目金额和产品级margin未完全披露；PWR不卖GPU/UPS/变压器/PDU/燃机，硬件利润池不归PWR。"]),
        base.row(["近端催化剂", "Q2/Q3收入、Electric/Underground margin、total/RPO/12个月backlog、NiSource 3GW项目NTP/backlog、CEI/DSI/Tri-City整合、OCF/FCF和working capital。"]),
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
        base.row(["直接同业", "与PWR在数据中心/公用事业电气工程、MEP、EPC、prefab、commissioning或大型项目交付需求池高度重叠；优先比较收入、RPO/backlog、margin、项目执行、现金流和同业估值。", "EME、FIX、IESC、MYRG", "判断力度最高；同档或相邻档时必须复核谁更能把订单转成高质量收入和FCF。"]),
        base.row(["相邻替代", "同属AI园区电力、冷却、发电、储能、核能、工业基础设施或物理AI基础设施资金篮子，但产品或收入模式不完全相同。", "VRT、GEV、JCI、MOD、TT、BE、GNRC、PSIX、OKLO、SMR、CEG、VST", "回答资金只能买一个时，谁的增长质量、估值消化、现金流和近端催化更好；不因赛道更热自动胜出。"]),
        base.row(["上下游", "B是PWR交付链的设备供应商、客户/负载侧、云厂/IDC/服务器/芯片/网络/半导体制造链或公用事业需求端。", "ETN、HUBB、NVT、POWL、ABBNY、MSFT、AMZN、GOOGL、META、ORCL、NVDA、DELL、ANET、AEP、ETR", "不把客户capex直接等同PWR利润，也不把设备ASP直接等同PWR机会；核心看利润捕获、议价权、订单硬度和反证。"]),
        base.row(["跨赛道", "业务差异较大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "材料、化学品、软件、生命科学、航天和部分平台公司", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
        catchup = "PWR需要继续证明backlog/RPO高质量转收入，Electric margin、FCF和NiSource/数据中心项目落地同步兑现，并降低估值透支风险。"
        if row_obj["relationship"] == "直接同业":
            catchup = "PWR需要在直接工程同业中证明Electric backlog、数据中心电气/MEP交付、margin和现金流明显强于B。"
        elif row_obj["relationship"] == "上下游":
            catchup = "PWR需要证明云厂/AI主链capex和设备交付瓶颈能持续落到其工程收入和利润，而不是只停留在行业TAM。"
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
        if "右尾弹性优先" in wins and row_obj["final_choice"] == "A":
            catchup = "B需要把右尾叙事转成可确认收入、利润和现金流，并降低估值或融资反证。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/电力_发电_能源_储能/PWR_Quanta Services_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心土建、MEP与预制化交付_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心开关设备与变压器_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心低压配电、PDU与母线槽_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- PWR 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_pwr_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台/冷却标的使用既有正式脚本的最低分校准，对PWR的FY2026指引、backlog/RPO、Electric Segment、数据中心园区电气、NiSource 3GW、CEI/DSI/Tri-City、估值、IV、价格确认和工程服务利润池限制做目标公司校准后建档；未读取下游量化目录、现成排序结论或既有公司对比成品。",
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
        raise SystemExit("缺少 PWR 正式评估文件")
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
                "pwr_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "pwr_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "pwr_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
