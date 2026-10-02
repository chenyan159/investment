from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as project_calibration
import generate_etn_company_comparison as etn_calibration
import generate_hubb_company_comparison as hubb_calibration


TARGET = "MRAAY"
TARGET_NAME = "Murata Manufacturing"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MRAAY_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_COMPONENT_PEERS = {
    "TTDKY",
    "VSH",
    "LFUS",
    "BELFB",
    "IFNNY",
    "MPWR",
    "MCHP",
    "ON",
    "STM",
    "TXN",
    "POWI",
    "NVTS",
    "VICR",
    "WOLF",
    "AOSL",
    "DIOD",
    "ST",
}

OPTICAL_AND_BOARD_POWER_ALTS = {
    "AAOI",
    "APH",
    "AVGO",
    "BDC",
    "COHR",
    "CRDO",
    "GLW",
    "LITE",
    "LWLG",
    "MTSI",
    "POET",
    "QCOM",
    "RMBS",
    "SIMO",
    "SITM",
    "SMTC",
    "SMTOY",
    "TEL",
    "VIAV",
    "VISN",
}

ELECTRICAL_AND_POWER_ALTS = {
    "ABBNY",
    "AEIS",
    "ALAB",
    "ETN",
    "GEV",
    "HUBB",
    "HTHIY",
    "MIELY",
    "NVT",
    "POWL",
}

MEP_COOLING_AND_INFRA_ALTS = {
    "AAON",
    "ATKR",
    "BE",
    "CARR",
    "CAT",
    "CMI",
    "DKILY",
    "DOV",
    "EME",
    "ENS",
    "FIX",
    "FLNC",
    "FTV",
    "GNRC",
    "IESC",
    "JCI",
    "MOD",
    "MYRG",
    "PH",
    "PNR",
    "PWR",
    "RYCEY",
    "TT",
    "VRT",
}

AI_COMPUTE_AND_SERVER_DEMAND = {
    "ADBE",
    "AMD",
    "AMZN",
    "ANET",
    "APLD",
    "ARM",
    "BABA",
    "CIEN",
    "CLS",
    "CRWD",
    "CRWV",
    "CSCO",
    "DELL",
    "DLR",
    "EQIX",
    "FLEX",
    "FN",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "JBL",
    "META",
    "MRVL",
    "MSFT",
    "MU",
    "NBIS",
    "NOK",
    "NTAP",
    "NTNX",
    "NVDA",
    "ORCL",
    "PENG",
    "PSTG",
    "SANM",
    "SMCI",
    "SNDK",
    "STX",
    "WDC",
}

SEMICONDUCTOR_EQUIPMENT_AND_MATERIALS = {
    "ACLS",
    "ACMR",
    "AJNMY",
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
    "CDNS",
    "COHU",
    "DD",
    "DHR",
    "DSCSY",
    "ENTG",
    "FORM",
    "GFS",
    "HOCPY",
    "ICHR",
    "IMOS",
    "INTC",
    "KEYS",
    "KLAC",
    "KLIC",
    "LIN",
    "LRCX",
    "MICLF",
    "MKSI",
    "MTRN",
    "NVMI",
    "ONTO",
    "PLAB",
    "Q",
    "ROG",
    "SHECY",
    "SOMMY",
    "TER",
    "TMO",
    "TOELY",
    "TSEM",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
}

UTILITY_AND_POWER_CUSTOMERS = {
    "AEP",
    "BWXT",
    "CEG",
    "DTE",
    "ET",
    "ETR",
    "FCEL",
    "OKLO",
    "PSIX",
    "SMR",
    "TSLA",
    "VST",
}

MRAAY_MARKET_SNAPSHOT = {
    "category": "配电_电源_功率器件",
    "name": TARGET_NAME,
    "price_date": "2026-06-23 10:44 EDT delayed quote",
    "price": 33.94,
    "market_cap_b": 140.06,
    "ttm_pe": 80.43,
    "forward_pe": 68.0,
    "ps": 11.0,
    "pb": None,
    "ev_ebitda": None,
    "eps": 0.42,
    "call_iv": None,
    "put_iv": None,
    "currency": "USD",
    "financial_currency": "JPY",
    "source_timestamp": "MarketWatch delayed quote, 2026-06-23 10:44 EDT",
    "notes": "本地每日金融数据缺少MRAAY；使用MarketWatch和公司调研中6/22-6/23行情快照作目标公司价格/估值校准；OTC ADR且ADR比例/日元口径需确认；未取得干净期权IV。",
}

MRAAY_SCORES = {
    "NTM兑现优先": 72.0,
    "右尾弹性优先": 73.0,
    "风险调整收益": 58.0,
    "下行保护优先": 78.0,
    "估值消化优先": 45.0,
    "近端催化优先": 72.0,
    "价格确认/动量": 82.0,
    "激进短线": 74.0,
}


def inject_mraay_market_data(companies: dict[str, dict]) -> None:
    company = companies.get(TARGET)
    if not company:
        return
    company["fin"] = dict(MRAAY_MARKET_SNAPSHOT)
    company["mom2"] = {
        "category": "配电_电源_功率器件",
        "latest_trade_date": "2026-06-23",
        "base_trade_date": "MarketWatch 5D",
        "mom2w": 3.46,
        "notes": "本地两周区间缺失；外部5D表现仅用于目标公司动量校准。",
    }
    company["mom1"] = {
        "category": "配电_电源_功率器件",
        "latest_trade_date": "2026-06-23",
        "base_trade_date": "MarketWatch 1M",
        "mom1m": 31.96,
        "notes": "本地一月区间缺失；外部1M表现用于目标公司动量校准。",
    }
    company["soxx"] = {
        "category": "配电_电源_功率器件",
        "soxx_cum": None,
        "notes": "本地SOXX三段压力窗口缺少MRAAY。",
    }


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def recompute_tiers(companies: dict[str, dict]) -> None:
    for strategy in STRATS:
        scored = [
            company.get("scores", {}).get(strategy)
            for company in companies.values()
            if company.get("scores", {}).get(strategy) is not None
        ]
        scored.sort(reverse=True)
        total = len(scored)
        if not total:
            continue
        cuts = {
            "S": scored[max(0, int(total * 0.07) - 1)],
            "A": scored[max(0, int(total * 0.25) - 1)],
            "B": scored[max(0, int(total * 0.55) - 1)],
            "C": scored[max(0, int(total * 0.85) - 1)],
        }
        for company in companies.values():
            score = company.get("scores", {}).get(strategy)
            if score is None:
                tier = "资料不足"
                rank = None
            elif score >= cuts["S"]:
                tier = "S"
                rank = sum(1 for value in scored if value > score) + 1
            elif score >= cuts["A"]:
                tier = "A"
                rank = sum(1 for value in scored if value > score) + 1
            elif score >= cuts["B"]:
                tier = "B"
                rank = sum(1 for value in scored if value > score) + 1
            elif score >= cuts["C"]:
                tier = "C"
                rank = sum(1 for value in scored if value > score) + 1
            else:
                tier = "D"
                rank = sum(1 for value in scored if value > score) + 1
            company.setdefault("tiers", {})[strategy] = tier
            company.setdefault("ranks", {})[strategy] = rank
            company.setdefault("rank_total", {})[strategy] = total

    for company in companies.values():
        if not company.get("fin", {}).get("price"):
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"
                company.setdefault("ranks", {})[strategy] = None


def score_companies(companies: dict[str, dict]) -> None:
    inject_mraay_market_data(companies)
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target
    inject_mraay_market_data(companies)

    floors: dict[str, dict[str, float]] = {}
    floors.update(getattr(project_calibration, "SCORE_FLOORS", {}))
    floors.update(getattr(etn_calibration, "LOCAL_SCORE_FLOORS", {}))
    floors["ETN"] = getattr(etn_calibration, "ETN_SCORES", {})
    floors["HUBB"] = getattr(hubb_calibration, "HUBB_SCORES", {})

    for ticker, strategy_floors in floors.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in strategy_floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)
            company["scores"][strategy] = max(current, floor)

    for strategy, score in MRAAY_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score

    recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_COMPONENT_PEERS:
        return "直接同业"
    if ticker in OPTICAL_AND_BOARD_POWER_ALTS or ticker in ELECTRICAL_AND_POWER_ALTS:
        return "相邻替代"
    if ticker in MEP_COOLING_AND_INFRA_ALTS:
        return "相邻替代"
    if ticker in AI_COMPUTE_AND_SERVER_DEMAND or ticker in UTILITY_AND_POWER_CUSTOMERS:
        return "上下游"
    if ticker in SEMICONDUCTOR_EQUIPMENT_AND_MATERIALS:
        return "跨赛道"
    if category in {"配电_电源_功率器件", "AI网络_光互联_连接器", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台", "电力_发电_能源_储能"}:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "跨赛道":
            return "业务差异大且证据接近"
        return "档位接近且证据互有强弱"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "A有FY2026指引、B2B和backlog硬锚",
            "右尾弹性优先": "A数据中心电容收入和MLCC供需右尾更直接",
            "风险调整收益": "A净现金、FCF和AI增量组合更均衡",
            "下行保护优先": "A资产负债表强且业务分散更防守",
            "估值消化优先": "A利润率改善可部分消化高估值",
            "近端催化优先": "A订单、ASP和server capacitor验证更近",
            "价格确认/动量": "A近月价格重估强且AI MLCC被确认",
            "激进短线": "A AI MLCC重估和资金关注度更适合进攻",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业收入/订单兑现更硬",
            "右尾弹性优先": f"{ticker}同业小基数或产品弹性更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或估值缓冲更好",
            "估值消化优先": f"{ticker}同业估值更易被业绩消化",
            "近端催化优先": f"{ticker}同业订单/产品催化更近",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业波动和主题beta更高",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}收入/RPO或客户兑现更短链",
            "右尾弹性优先": f"{ticker}AI主链或需求端右尾更大",
            "风险调整收益": f"{ticker}上行和下行组合更优",
            "下行保护优先": f"{ticker}现金流或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更适合短线",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS or category in HIGH_GROWTH_CATS:
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
        "估值消化优先": 1.10,
        "下行保护优先": 1.05,
        "右尾弹性优先": 0.90,
        "近端催化优先": 0.85,
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


def key_reason(a: dict, b: dict, choice: str) -> str:
    ticker = str(b["ticker"])
    if choice == "中性":
        return "MRAAY的高端MLCC兑现与对手增长、估值或催化优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["NTM兑现优先"] > 12:
            return "MRAAY有FY2026收入/利润指引、Q4 B2B 1.24和backlog 4462亿日元支撑NTM兑现。"
        if diffs["右尾弹性优先"] > 12:
            return "MRAAY的数据中心相关收入+83.9%、server capacitor +85%-90%让右尾更可收入化。"
        if diffs["下行保护优先"] > 12:
            return "MRAAY净现金、权益比率85%和多元终端底盘提供更好下行保护。"
        if diffs["近端催化优先"] > 10:
            return "MRAAY的订单、ASP、数据中心电容capex和下一次财报验证更近。"
        return "MRAAY在AI MLCC增量、净现金和经营可见度之间更均衡。"

    if diffs["估值消化优先"] < -12:
        return f"{ticker}的估值更容易被NTM业绩消化，MRAAY已包含较强AI MLCC重估。"
    if diffs["右尾弹性优先"] < -14:
        return f"{ticker}的AI主链、小基数或高beta右尾明显大于MRAAY。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker}的订单/RPO/backlog或收入确认证据比MRAAY更硬。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比MRAAY更直接。"
    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、估值或压力期韧性强于MRAAY。"
    if diffs["价格确认/动量"] < -12:
        return f"{ticker}价格确认和资金偏好强于MRAAY。"
    return f"{ticker}在多数投资思路下比MRAAY更符合项目内资金配置目标。"


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
        row_obj["key_reason"] = key_reason(a, b, row_obj["final_choice"])
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


def market_snapshot_text(a: dict) -> str:
    fin = a.get("fin", {})
    return (
        f"本地 `每日金融数据_2026-06-22.md`、两周/一月区间涨跌和SOXX压力窗口均无 MRAAY 行；"
        f"目标公司使用外部交叉检查：MarketWatch 2026-06-23 10:44 EDT 延时报价 {fmt_num(fin.get('price'), 2)} 美元，"
        f"前收 38.27 美元，市值 {fmt_b(fin.get('market_cap_b'))}，TTM P/E {fmt_num(fin.get('ttm_pe'), 2)}；"
        "公司调研中以2026-06-22收盘价38.27美元和FY2026指引估算Forward P/E约68x、Forward P/S约11x；"
        "MarketWatch显示5日+3.46%、1个月+31.96%、3个月+203.84%、YTD+230.68%，但6/23盘中曾较前收大幅回撤；干净期权IV缺失。"
    )


def render_report(companies: dict[str, dict], comparisons: list[dict]) -> str:
    a = companies[TARGET]
    latest_dates = sorted({company["date"] for company in companies.values() if company.get("date")})
    date_range = f"{latest_dates[0]} 至 {latest_dates[-1]}" if latest_dates else "缺失"
    missing_fin = sorted([ticker for ticker, company in companies.items() if not company.get("fin", {}).get("price") and ticker != TARGET])

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
            "强势档",
            "FY2026收入指引1.960万亿日元、OP 3800亿日元；Q4订单5707亿日元、B2B 1.24、backlog 4462亿日元",
            "公司总收入基准仅+7.1%，通信、家电和普通周期业务抵消AI增量",
        ),
        "右尾弹性优先": (
            "强势档",
            "data-center-related收入从1767亿到3250亿日元，server-related capacitor sales +85%-90%，ASP +5%-10%",
            "体量大且SiCap/VPD/800V等仍是远期期权，不能与小盘AI主链同等放大",
        ),
        "风险调整收益": (
            "强势档",
            "净现金、权益比率85%、FY2025 FCF 2314亿日元，AI MLCC增量已进入收入表",
            "高估值、手机/RF拖累、数据中心产品拆分为模型估算，赔率被估值部分抵消",
        ),
        "下行保护优先": (
            "中上档",
            "资产负债表极强、现金充足、汽车/工业/通信多元底盘和电容龙头地位提供防守",
            "本地SOXX压力窗口缺失；6/23盘中大幅回撤提醒价格防守不能只看资产质量",
        ),
        "估值消化优先": (
            "中性偏弱",
            "FY2026经营利润指引+34.8%、净利+25.3%，AI高端mix提升可帮助消化部分高倍数",
            "Forward P/E约68x、Forward P/S约11x，已经提前计入强AI MLCC重估",
        ),
        "近端催化优先": (
            "强势档",
            "下一次财报可验证order/B2B/backlog、data-center revenue、server capacitor销售、ASP与capex爬坡",
            "催化偏经营验证，不像AI芯片、HBM或光模块订单那样单一事件驱动",
        ),
        "价格确认/动量": (
            "强势档",
            "外部行情显示1个月+31.96%、3个月+203.84%、YTD+230.68%，价格已明显确认AI MLCC重估",
            "本地日度区间缺失，且6/23延时报价较前收大幅下跌，过热和回撤风险高",
        ),
        "激进短线": (
            "中性偏弱档",
            "高端AI MLCC重估、强近月动量、数据中心收入上修和高估值敏感度带来短线进攻性",
            "OTC ADR、IV缺失、业务仍分散，短线弹性弱于小盘光互联、NeoCloud和高beta电力设备",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "高容量小型化AI MLCC",
            "低ESL/三端/高耐压AI电源链MLCC",
            "数据中心电源模块",
            "SiCap/iPaS/embedded passives/VPD",
            "Mobility汽车高可靠元件",
            "高频通信/RF/手机模块",
        ]

    lines: list[str] = [
        "# MRAAY 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：MRAAY / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：B公司价格/估值/IV为项目内 `金融资料/每日金融数据/每日金融数据_2026-06-22.md`；区间涨跌为2026-06-03；SOXX压力窗口为2026-06-04。MRAAY本地金融资料缺失，目标公司价格/估值使用公司调研与MarketWatch 2026-06-23延时报价交叉校准，IV缺失。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 MRAAY vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。MRAAY 的强项是数据中心相关收入已经进入FY2026指引、server-related capacitor sales `+85%-90%`、Q4 B2B和backlog硬锚、净现金资产负债表以及近期价格已大幅确认AI MLCC重估。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是Forward P/E约`68x`、Forward P/S约`11x`，估值已透支一部分AI MLCC右尾；本地日度IV和区间涨跌缺失，6/23盘中又出现大回撤。",
        "- A 最适合的投资者画像：想用相对成熟、现金流强、资产负债表强的日系元件龙头配置AI服务器电源完整性、高端MLCC和数据中心功率链，但不想承担纯小盘光互联或NeoCloud极端波动的资金。",
        "- A 最不适合的投资者画像：只追求最高增速、小基数、强订单披露、高IV和事件驱动短线爆发的资金；这类资金通常会更偏NVDA/AVGO/MU/ALAB/CRDO/AAOI/MPWR/VRT/POWL/BE/OKLO/SMR等。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常在AI主链收入、直接订单/RPO、估值消化、价格确认或更高短线beta上压过MRAAY。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：MRAAY 是项目内AI物理层供应链里的强势但已重估标的，最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它胜过多数传统慢增长、资料不足或远期叙事标的，但面对顶级AI芯片、HBM、云算力、强订单电气设备和高beta光互联时需要按思路拆分。",
        "- 后续最重要跟踪数据：季度order/B2B/backlog；data-center-related revenue是否跑在3250亿日元年度指引之上；server-related capacitor sales是否维持`+85%-90%`或继续上修；Capacitor ASP是否高于`+5%-10%`；数据中心电容capex与良率；power module新项目`+250亿日元`兑现；SiCap/iPaS/VPD客户认证；High-Frequency Device and Communications止跌；库存、FCF与汇率敏感性。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "MRAAY"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "配电_电源_功率器件")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", "1,940-1,980 十亿日元，中心值为FY2026官方指引1,960.0十亿日元"]),
        base.row(["乐观/极度乐观收入", "乐观：2,050-2,120 十亿日元；极度乐观：2,200-2,300 十亿日元"]),
        base.row(["利润和现金流结论", "基准经营利润370-390十亿日元，中心值为官方380.0十亿日元；净利润约285-305十亿日元；经营现金流仍为正，但FY2026约250.0十亿日元capex和数据中心库存建设会压低FCF弹性。"]),
        base.row(["最大传导瓶颈", "高端AI MLCC并非普通MLCC产线简单切换，受薄层陶瓷、内电极、烧结、测试分选、客户AVL/可靠性认证和12-24+个月扩产节奏约束。"]),
        base.row(["最大反证", "数据中心相关FY2026收入虽升至约16.6%占比，但通信/RF/手机模块、家电、PC和普通周期业务仍会抵消；SiCap/VPD/800V等远期期权缺少NTM可确认收入。"]),
        base.row(["近端催化剂", "FY2026季度订单、B2B、backlog、data-center revenue、server capacitor sales、Capacitor ASP、power module新项目、数据中心capex/良率和传统通信止跌。"]),
        base.row(["日度市场数据", market_snapshot_text(a)]),
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
        base.row(["直接同业", "同属高端被动元件、功率管理、模拟/功率半导体、保护器件或AI服务器板级电源完整性元件供应商；优先比较订单/收入表、产品代际、客户认证、利润率和估值。", "TTDKY、VSH、LFUS、IFNNY、MPWR、MCHP、ON、STM、TXN", "判断力度最高；若直接同业在AI供电、功率器件、估值或动量上明显更强，可在对应列压过MRAAY。"]),
        base.row(["相邻替代", "同属AI物理层、光互联、连接器、电气设备、冷却、电源模块或数据中心基础设施资金篮子，但产品不完全重叠。", "GLW、APH、COHR、LITE、CRDO、ETN、HUBB、MIELY、VRT、POWL", "中等力度；赛道热度不能自动胜出，必须落实到订单、利润捕获、估值消化和价格确认。"]),
        base.row(["上下游", "AI芯片、HBM、服务器、云厂、IDC、公用事业和电力资产是MRAAY高端MLCC、电源模块和PDN需求链上下游；比较时区分客户收入规模与MRAAY可捕获利润。", "NVDA、AVGO、MU、AMD、TSM、SMCI、DELL、MSFT、AMZN、GOOGL、CEG、VST", "不把下游capex直接等同MRAAY收入；若对方拥有更直接AI收入、RPO、订单或价格确认，可在右尾、催化和动量列胜出。"]),
        base.row(["跨赛道", "半导体设备、材料、软件、工业、医疗和其他业务差异较大的公司，作为组合资金替代比较增长质量、风险调整收益、估值消化和下行保护。", "ASML、AMAT、LRCX、LIN、TMO、DHR、ADBE、RKLB", "默认降低结论力度；除非增长质量、估值或风险明显拉开，否则使用中性或微倾向。"]),
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
        catchup = "MRAAY需要披露更清晰的数据中心客户、订单/backlog、交付窗口、ASP和高端MLCC产能/良率，并证明高估值能被利润与FCF持续消化。"
        if row_obj["relationship"] == "上下游":
            catchup = "MRAAY需要证明AI芯片/云厂/服务器capex能持续落到其高端MLCC、电源模块和PDN收入，而不是只停留在行业TAM。"
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
        catchup = "B需要拿出更硬的NTM收入/利润兑现、订单或客户合同，并证明估值、现金流和压力窗口能承受波动。"
        if "右尾弹性优先" in wins and row_obj["final_choice"] == "A":
            catchup = "B需要把右尾叙事转成可确认收入、利润和现金流，并降低估值或融资反证。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/配电_电源_功率器件/MRAAY_Murata_Manufacturing_公司调研_2026-06-23.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖本次公司评估全集中除MRAAY外 {len(companies) - len(missing_fin) - 1}/{len(companies) - 1} 家，缺失可用价格/估值的非MRAAY公司为：{('、'.join(missing_fin) if missing_fin else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；SOXX压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。上述本地文件均无MRAAY行，因此目标公司动量/估值采用公司调研和外部延时报价交叉校准。",
        "- MRAAY 外部行情交叉检查：MarketWatch `https://www.marketwatch.com/investing/stock/mraay` 与 `https://www.marketwatch.com/investing/stock/mraay/analystestimates`，用于确认2026-06-23延时报价、前收、市值、P/E和分析师EPS估计趋势；本报告仍以项目内正式公司评估作为经营建档主依据。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/AI服务器_存储_芯片/行业调研_MLCC与高端陶瓷电容_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-06-10.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- MRAAY 日度/外部快照：{market_snapshot_text(a)}",
        "- 自动化脚本：`scripts/generate_mraay_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用正式评估最低分校准，对MRAAY的FY2026指引、data-center-related收入、Q4订单/backlog、净现金、外部行情和高估值限制做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
        raise SystemExit("缺少 MRAAY 正式评估文件")
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
                "mraay_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "mraay_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "mraay_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
