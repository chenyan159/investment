from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_nvt_company_comparison as framework


TARGET = "TXN"
TARGET_NAME = "德州仪器"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "TXN_逐家公司投资思路对比_2026-06-23.md"

base.FIN_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-23.md"
base.MOM2W_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去两周_2026-06-23.md"
base.MOM1M_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去1个月_2026-06-23.md"
base.SOXX_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md"
base.TARGET = TARGET

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_ANALOG_POWER_PEERS = {
    "ADI",
    "AOSL",
    "DIOD",
    "IFNNY",
    "LFUS",
    "MCHP",
    "MPWR",
    "MRAAY",
    "ON",
    "POWI",
    "STM",
    "TTDKY",
    "VICR",
    "VSH",
}

ADJACENT_AI_SEMI = {
    "ALAB",
    "AMD",
    "ARM",
    "AVGO",
    "CDNS",
    "INTC",
    "MRVL",
    "MTSI",
    "MXL",
    "NVDA",
    "QCOM",
    "RMBS",
    "SIMO",
    "SITM",
    "SMTC",
    "SNPS",
}

AI_POWER_ELECTRICAL_ADJACENT = {
    "ABBNY",
    "AEIS",
    "ATKR",
    "BE",
    "ENS",
    "ENPH",
    "ETN",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "MIELY",
    "NVT",
    "NVTS",
    "POWL",
    "PSIX",
    "ST",
    "WOLF",
}

DATA_CENTER_INFRA_ADJACENT = {
    "AAON",
    "CARR",
    "CEG",
    "DKILY",
    "EME",
    "FIX",
    "JCI",
    "MOD",
    "MYRG",
    "PWR",
    "TT",
    "VRT",
    "VST",
}

SERVER_NETWORK_STORAGE_CHAIN = {
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
    "MU",
    "NOK",
    "NTAP",
    "PENG",
    "POET",
    "PSTG",
    "SANM",
    "SMCI",
    "SNDK",
    "STX",
    "TEL",
    "VIAV",
    "VISN",
    "WDC",
}

FABS_EQUIPMENT_MATERIALS_CHAIN = {
    "ACLS",
    "ACMR",
    "AEHR",
    "AMAT",
    "AMKR",
    "ASGLY",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "AXTI",
    "BESIY",
    "CAMT",
    "COHU",
    "DSCSY",
    "ENTG",
    "FORM",
    "GFS",
    "HOCPY",
    "ICHR",
    "IMOS",
    "KEYS",
    "KLAC",
    "KLIC",
    "LIN",
    "LRCX",
    "MICLF",
    "MKSI",
    "NVMI",
    "ONTO",
    "PLAB",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
    "TER",
    "TOELY",
    "TSEM",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
}

AI_CUSTOMERS_AND_OPERATORS = {
    "AMZN",
    "APLD",
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

CROSS_SECTOR = {
    "ADBE",
    "AJNMY",
    "ALLE",
    "AMPX",
    "APD",
    "BABA",
    "BWXT",
    "CAT",
    "CC",
    "CMI",
    "CRWD",
    "DCI",
    "DD",
    "DHR",
    "DOV",
    "DTE",
    "ECL",
    "ET",
    "ETR",
    "FCEL",
    "FTV",
    "HTHIY",
    "IESC",
    "MMM",
    "MSI",
    "MTRN",
    "NDSN",
    "OKLO",
    "PH",
    "PNR",
    "RKLB",
    "RYCEY",
    "SMR",
    "TDY",
    "TMO",
    "TSLA",
}

TXN_SCORES = {
    "NTM兑现优先": 68.0,
    "右尾弹性优先": 60.0,
    "风险调整收益": 50.0,
    "下行保护优先": 78.0,
    "估值消化优先": 54.0,
    "近端催化优先": 66.0,
    "价格确认/动量": 55.0,
    "激进短线": 75.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def patch_txn_growth_fields(companies: dict[str, dict]) -> None:
    txn = companies.get(TARGET)
    if not txn:
        return
    txn["bear_growth"] = 9.0
    txn["base_growth"] = 20.0
    txn["bull_growth"] = 33.0
    txn["extreme_growth"] = 49.5


def score_companies(companies: dict[str, dict]) -> None:
    patch_txn_growth_fields(companies)
    framework.score_companies(companies)
    for strategy, score in TXN_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score
    framework.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_ANALOG_POWER_PEERS:
        return "直接同业"
    if ticker in ADJACENT_AI_SEMI or ticker in AI_POWER_ELECTRICAL_ADJACENT or ticker in DATA_CENTER_INFRA_ADJACENT:
        return "相邻替代"
    if ticker in SERVER_NETWORK_STORAGE_CHAIN or ticker in FABS_EQUIPMENT_MATERIALS_CHAIN or ticker in AI_CUSTOMERS_AND_OPERATORS:
        return "上下游"
    if ticker in CROSS_SECTOR:
        return "跨赛道"
    if category == "AI计算芯片_EDA_IP_custom_ASIC":
        return "相邻替代"
    if category in {"配电_电源_功率器件", "电力_发电_能源_储能", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI网络_光互联_连接器", "云算力_IDC_AI软件平台", "晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "直接同业":
            return "模拟/功率同业证据接近"
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，增长与估值互抵"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "TXN Q2指引、工业恢复和数据中心增速更清楚",
            "右尾弹性优先": "TXN 48V/800V电源链期权更直接",
            "风险调整收益": "TXN现金流和成熟模拟底盘更均衡",
            "下行保护优先": "TXN FCF、资产质量和压力期表现更稳",
            "估值消化优先": "TXN基准恢复可部分消化估值",
            "近端催化优先": "TXN Q2/Q3、数据中心和800V节点更近",
            "价格确认/动量": "TXN两周价格确认强于对手",
            "激进短线": "TXN AI电源叙事和IV提供短攻弹性",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业订单或收入兑现更硬",
            "右尾弹性优先": f"{ticker}在AI电源/功率器件右尾更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或估值缓冲更厚",
            "估值消化优先": f"{ticker}收入增速更能覆盖估值",
            "近端催化优先": f"{ticker}同业产品/订单催化更近",
            "价格确认/动量": f"{ticker}同业价格趋势更强",
            "激进短线": f"{ticker}同业beta和关注度更适合短攻",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}订单、RPO或收入确认链更硬",
            "右尾弹性优先": f"{ticker}AI主链或瓶颈利润池更大",
            "风险调整收益": f"{ticker}上行与下行组合更优",
            "下行保护优先": f"{ticker}现金流、规模或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更适合短线",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}收入、订单或交付可见度更强",
            "右尾弹性优先": f"{ticker}右尾或利润池弹性更直接",
            "风险调整收益": f"{ticker}增长与估值组合更好",
            "下行保护优先": f"{ticker}现金流或压力期表现更安全",
            "估值消化优先": f"{ticker}订单兑现更能消化估值",
            "近端催化优先": f"{ticker}近端订单或产品催化更强",
            "价格确认/动量": f"{ticker}趋势和资金偏好更强",
            "激进短线": f"{ticker}主题beta和波动更适合进攻",
        }[strategy]

    if category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker}的AI链兑现证据更硬",
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
    elif rel == "直接同业":
        strong_cut, suggest_cut, micro_cut = 20, 9, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 24, 11, 4
    else:
        strong_cut, suggest_cut, micro_cut = 22, 10, 4

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
        return "TXN的模拟现金流/数据中心电源期权与对手增长、估值或防守优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["NTM兑现优先"] > 10:
            return "TXN有Q1实际、Q2收入指引、工业恢复和data center终端市场增速支撑NTM兑现。"
        if diffs["下行保护优先"] > 10:
            return "TXN的成熟模拟底盘、FCF恢复和SOXX压力窗口相对韧性更强。"
        if diffs["近端催化优先"] > 10:
            return "TXN未来1-2季可用Q2/Q3、data center增速、800V架构和Silicon Labs交易连续验证。"
        if diffs["风险调整收益"] > 10:
            return "TXN在现金流、模拟周期恢复和估值风险之间的组合优于对手。"
        return "TXN在NTM兑现、下行保护和近端验证之间的组合略优。"

    if diffs["右尾弹性优先"] < -16:
        return f"{ticker}的AI主链、小基数或电力设备右尾明显大于TXN。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}的业绩增速或估值组合比TXN更容易消化。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量、估值消化和下行组合优于TXN。"
    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、估值缓冲或防御属性明显强于TXN。"
    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的订单/RPO/backlog或收入兑现比TXN更硬。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比TXN更直接。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和短线资金偏好明显强于TXN。"
    return f"{ticker}在多数投资思路下比TXN更符合项目内资金配置目标。"


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
    missing_price = sorted([ticker for ticker, company in companies.items() if not company.get("fin", {}).get("price")])
    fin = a.get("fin", {})
    m2w = a.get("mom2", {})
    m1m = a.get("mom1", {})
    soxx = a.get("soxx", {})
    daily_snapshot = (
        f"2026-06-23 最新价格 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {fmt_num(fin.get('call_iv'), 1)}%，"
        f"Put IV {fmt_num(fin.get('put_iv'), 1)}%；过去两周 {fmt_pct(m2w.get('mom2w'))}，"
        f"过去1个月 {fmt_pct(m1m.get('mom1m'))}；三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
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
    strong_b_names = "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]]) or "无"

    support = {
        "NTM兑现优先": (
            "A档",
            "2026Q1收入48.25亿美元、同比+19%、环比+9%；2026Q2指引50.0-54.0亿美元；工业Q1约+30%、data center约+90%，NTM基准收入206-218亿美元。",
            "无backlog/bookings披露，lead time短且订单条款客户友好，Q2后若只是补库则兑现强度会下移。",
        ),
        "右尾弹性优先": (
            "B档",
            "48V/54V电源、hot-swap/eFuse、current sense、隔离、GaN、800VDC两级架构和NVIDIA参考设计提供右尾。",
            "2025 data center终端市场仅约15亿美元、约9%收入；800V/6V量产、客户和socket份额缺硬证据，右尾低于AI主链和高beta电源公司。",
        ),
        "风险调整收益": (
            "B档",
            "基准净利润约64-71亿美元、FCF约50-65亿美元，300mm产能和CHIPS/ITC缓冲支持中期现金流恢复。",
            "2026-06-23 Forward PE约31.60、P/S约14.93、EV/EBITDA约35.93，估值不便宜且需要工业和data center同时兑现。",
        ),
        "下行保护优先": (
            "B档",
            "成熟Analog/Embedded底盘、FCF恢复和SOXX三段压力窗口累计-45.58%，在半导体内相对稳健。",
            "高估值、库存天数约209天、300mm折旧吸收和模拟周期波动仍会放大需求失速时的下行。",
        ),
        "估值消化优先": (
            "C档",
            "若NTM基准收入206-218亿美元和利润率38%-40%兑现，能部分解释当前溢价。",
            "P/S约14.93和Forward PE约31.60要求较高，TXN不是NVDA/AVGO式AI主链高增，估值消化空间受限。",
        ),
        "近端催化优先": (
            "A档",
            "Q2实际/Q3指引、data center终端市场绝对收入、Analog/Embedded margin、库存天数、800V/NVIDIA进展和Silicon Labs审批均可在1-2季验证。",
            "多数催化需要从参考架构或终端市场增速转成产品级订单、收入和利润，不能只按主题定价。",
        ),
        "价格确认/动量": (
            "C档",
            "2026-06-23过去两周上涨+4.78%，说明短期已有一定价格确认。",
            "过去1个月下跌-2.20%，动量不如AI设备、电力设备、存储、光互联和部分小盘高beta标的。",
        ),
        "激进短线": (
            "C档",
            "Call IV约64.5%，AI电源、800V架构和Q2/Q3节点提供短线题材。",
            "公司市值约2753亿美元、data center收入占比仍小，短线爆发力低于NVTS、AOSL、ALAB、CRDO、BE、VRT等高beta标的。",
        ),
    }

    lines: list[str] = [
        "# TXN 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：TXN / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV、过去两周/过去1个月区间涨跌、SOXX三段压力窗口均为 2026-06-23。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 TXN vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。TXN 的强项不是最大右尾，而是 Q2 指引、工业恢复、data center 电源链增长和成熟模拟现金流共同支撑的 NTM 兑现、近端验证和下行韧性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。TXN 对 AI 数据中心有真实但仍偏小的电源/保护/信号链暴露，右尾和激进短线通常弱于AI芯片、HBM/存储、光互联、NeoCloud、高beta电源器件和数据中心电力设备。",
        "- A 最适合的投资者画像：愿意用较成熟、现金流更强的模拟半导体底盘，配置工业周期恢复和AI机柜电源升级期权的资金；更适合风险调整、兑现和防守组合，而不是纯追最高AI beta。",
        "- A 最不适合的投资者画像：只追求项目内最高NTM收入增速、最硬AI订单/RPO、最大右尾弹性或最强短线爆发力的资金；这些资金通常会优先选择NVDA/AVGO/MRVL/ALAB/MU/CRDO/AAOI、VRT/ETN/HUBB/POWL/NVT/BE或高波动小盘电源器件。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常在AI主链收入、订单/backlog、估值消化、价格确认、短线高beta或电力基础设施利润池上压过TXN。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：TXN 是项目内中上但非顶尖的稳健AI电源链/模拟半导体标的，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它能明显压过大量缺现金流、缺兑现或防守弱的公司，但面对AI主链、存储/光互联、电力设备和部分低估值高FCF公司时需要按投资思路拆开。",
        "- 后续最重要跟踪数据：2026Q2实际收入是否落在50.0-54.0亿美元指引内；data center终端市场绝对收入、YoY和QoQ；Analog/Embedded分部收入和经营利润率；库存天数、CapEx和FCF；lead time和价格表述；800V/NVIDIA架构是否披露客户、量产时间表或产品收入；Silicon Labs交易审批和closing；MPS/Infineon/Vicor/ADI/Renesas在AI power socket的竞争证据。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "TXN"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "")]),
        base.row(["重要产品/业务线", "Analog电源管理/信号链/接口/隔离/传感；Data center电源/保护/信号链；Embedded Processing MCU/C2000/Sitara；Other DLP/定制；Silicon Labs低功耗无线连接收购"]),
        base.row(["NTM 基准收入", a.get("base_rev") or a["scenarios"]["base"].get("NTM 公司收入", "缺失")]),
        base.row(["乐观/极度乐观收入", f"{a.get('bull_rev') or a['scenarios']['bull'].get('NTM 公司收入', '缺失')} / {a.get('extreme_rev') or a['scenarios']['extreme'].get('NTM 公司收入', '缺失')}"]),
        base.row(["利润和现金流结论", f"{a.get('base_profit', '')}；{a.get('base_cash', '')}"]),
        base.row(["最大传导瓶颈", "公司不披露backlog/bookings，lead time短且订单条款较客户友好；收入传导必须用Q2指引、终端市场增速、库存天数、产能和产品认证路径校准。"]),
        base.row(["最大反证", "Q2后工业订单减速或只是补库；data center环比增速从Q1的>25%快速回落；价格压力重现；800V架构停留参考设计；高价值AI power socket被MPS/Infineon/Vicor/ADI等拿走。"]),
        base.row(["近端催化剂", "Q2实际/Q3指引、data center终端市场披露、Analog/Embedded margin、库存/CapEx/FCF、800V/NVIDIA架构进展、Silicon Labs交易审批。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        rank = a.get("ranks", {}).get(strategy)
        total = a.get("rank_total", {}).get(strategy) or len(companies)
        lines.append(base.row([strategy, a["tiers"][strategy], f"第 {rank}/{total}，{support[strategy][0]}", support[strategy][1], support[strategy][2]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与TXN在模拟、嵌入式、功率器件、电源管理、信号链或AI机柜电源socket上高度重叠。", "ADI、MCHP、ON、STM、IFNNY、MPWR、POWI、VICR、MRAAY", "优先比较分部收入、指引、利润率、产品代际、客户/socket、估值和AI power收入确认；直接同业证据强时结论力度上调。"]),
        base.row(["相邻替代", "同属AI半导体、AI电力、数据中心电源/配电/冷却或高端工业资金篮子，但产品不一一替代。", "NVDA、AVGO、MRVL、ALAB、QCOM、ETN、HUBB、NVT、VRT、BE", "重点回答资金只能买一个时，谁的增长质量、右尾、估值消化、近端催化和风险调整更好。"]),
        base.row(["上下游", "B 是TXN数据中心、服务器、云客户、网络/存储、晶圆制造、封测、设备或材料链条上的需求或供给环节。", "MSFT、AMZN、GOOGL、META、DELL、ANET、MU、TSM、ASML、AMAT、ENTG", "不把下游capex或上游设备收入直接等同TXN收入，重点看利润池位置、议价权、瓶颈稀缺性和收入确认链条。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "TMO、DHR、LIN、CAT、RKLB、CRWD、ADBE", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
        base.row(["序号", "公司B", "公司B分类", "可比关系", "档位差摘要", *STRATS, "多数思路方向", "最终更值得投", "最关键理由"]),
        base.row(["---:", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(comparisons, start=1):
        lines.append(
            base.row(
                [
                    index,
                    f"{row_obj['ticker']} / {row_obj['name']}",
                    row_obj["classification"],
                    row_obj["relationship"],
                    row_obj["grade_diff"],
                    *[row_obj[strategy] for strategy in STRATS],
                    row_obj["majority"],
                    "TXN" if row_obj["final_choice"] == "A" else row_obj["ticker"] if row_obj["final_choice"] == "B" else "中性",
                    row_obj["key_reason"],
                ]
            )
        )

    lines += [
        "",
        "## 6. 投资思路统计",
        "",
        base.row(["投资思路", *TAG_ORDER, "A侧合计", "B侧合计"]),
        base.row(["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]),
    ]
    for strategy in STRATS:
        lines.append(base.row([strategy, *[stats[strategy][tag] for tag in TAG_ORDER], a_side[strategy], b_side[strategy]]))

    lines += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(strong_b, start=1):
        wins = [strategy for strategy in STRATS if "投B" in row_obj[strategy]]
        need = "TXN需要披露更硬的data center产品级收入、订单/socket、利润率和800V量产时间表，同时证明工业恢复不是补库。"
        if row_obj["relationship"] == "直接同业":
            need = "TXN需要在模拟/功率同业中证明data center power收入、margin、客户socket和估值消化强于B。"
        elif row_obj["relationship"] == "上下游":
            need = "TXN需要证明云厂AI capex、服务器/网络/存储增长或晶圆制造周期能明确落到自己的模拟/嵌入式收入和利润。"
        lines.append(base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], need]))

    lines += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(strong_a, start=1):
        b = companies[row_obj["ticker"]]
        wins = [strategy for strategy in STRATS if "投A" in row_obj[strategy]]
        need = "B需要拿出更硬订单/RPO、更强NTM收入利润兑现，或证明估值、现金流和执行反证低于TXN。"
        if b.get("scores", {}).get("右尾弹性优先", 0) > a.get("scores", {}).get("右尾弹性优先", 0):
            need = "B需要把右尾叙事转成可确认收入、利润和现金流，并证明估值与执行反证可控。"
        lines.append(base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], need]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/AI计算芯片_EDA_IP_custom_ASIC/TXN_德州仪器_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未使用备份、临时结果、现成排序或下游量化结论。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家；缺少日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}；价格缺失或不可用公司为：{('、'.join(missing_price) if missing_price else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-23.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-23.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_服务器BMC、MCU与嵌入式控制_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI边缘推理芯片_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_精密时钟与同步芯片_2026-06-10.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/产业背景/AI产业链全局图谱与口径字典_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- TXN 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_txn_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台/冷却标的使用项目内脚本校准函数，对TXN的2026Q1/Q2指引、NTM收入四情景、data center电源链、800V/NVIDIA、Silicon Labs、估值、IV、区间涨跌和SOXX压力窗口做目标公司校准后建档；未读取下游量化目录、现成排序结论、临时结果、备份结论或既有公司对比成品。",
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
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 TXN 正式评估文件")
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
                "txn_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "txn_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "txn_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
