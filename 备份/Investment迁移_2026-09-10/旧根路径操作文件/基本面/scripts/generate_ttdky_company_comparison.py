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
import generate_mraay_company_comparison as mraay_calibration


TARGET = "TTDKY"
TARGET_NAME = "TDK Corporation"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "TTDKY_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH
base.FIN_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-23.md"
base.MOM2W_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去两周_2026-06-23.md"
base.MOM1M_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去1个月_2026-06-23.md"
base.SOXX_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_COMPONENT_PEERS = {
    "AOSL",
    "BELFB",
    "DIOD",
    "IFNNY",
    "LFUS",
    "MCHP",
    "MPWR",
    "MRAAY",
    "NVTS",
    "ON",
    "POWI",
    "ST",
    "STM",
    "TXN",
    "VICR",
    "VSH",
    "WOLF",
}

AI_POWER_AND_BOARD_ALTS = {
    "ABBNY",
    "AEIS",
    "ALAB",
    "APH",
    "BDC",
    "ETN",
    "GEV",
    "HUBB",
    "HTHIY",
    "MIELY",
    "NVT",
    "POWL",
    "SMTOY",
    "TEL",
}

OPTICAL_AND_NETWORK_ALTS = {
    "AAOI",
    "ANET",
    "AVGO",
    "CIEN",
    "COHR",
    "CRDO",
    "CSCO",
    "GLW",
    "LITE",
    "LWLG",
    "MTSI",
    "NOK",
    "POET",
    "QCOM",
    "RMBS",
    "SITM",
    "SMTC",
    "VIAV",
    "VISN",
}

STORAGE_AND_SERVER_CHAIN = {
    "AMKR",
    "AMZN",
    "ARM",
    "ASX",
    "BABA",
    "CLS",
    "DELL",
    "DLR",
    "EQIX",
    "FLEX",
    "FN",
    "GOOGL",
    "HPE",
    "IBM",
    "IMOS",
    "INTC",
    "JBL",
    "META",
    "MRVL",
    "MSFT",
    "MU",
    "NTAP",
    "NTNX",
    "NVDA",
    "ORCL",
    "PENG",
    "PSTG",
    "SANM",
    "SIMO",
    "SMCI",
    "SNDK",
    "STX",
    "TSM",
    "UMC",
    "WDC",
}

DATA_CENTER_INFRA_ALTS = {
    "AAON",
    "APD",
    "APLD",
    "BE",
    "CARR",
    "CAT",
    "CEG",
    "CMI",
    "CRWV",
    "DKILY",
    "DOV",
    "EME",
    "ENS",
    "FIX",
    "FLNC",
    "GNRC",
    "IESC",
    "IREN",
    "JCI",
    "MOD",
    "MYRG",
    "NBIS",
    "PH",
    "PNR",
    "PWR",
    "RYCEY",
    "TT",
    "VRT",
    "VST",
}

SEMICONDUCTOR_EQUIPMENT_MATERIALS = {
    "ACLS",
    "ACMR",
    "AJNMY",
    "AMAT",
    "ASGLY",
    "ASMIY",
    "ASML",
    "ASMVY",
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
    "UCTT",
    "VECO",
}


TTDKY_SCORES = {
    "NTM兑现优先": 62.5,
    "右尾弹性优先": 56.0,
    "风险调整收益": 46.5,
    "下行保护优先": 64.0,
    "估值消化优先": 49.0,
    "近端催化优先": 61.5,
    "价格确认/动量": 72.5,
    "激进短线": 76.0,
}


def fmt_num(value: object, decimals: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{decimals}f}"
    except Exception:
        return "缺失"


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"${float(value):.2f}B"
    except Exception:
        return "缺失"


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):+.2f}%"
    except Exception:
        return "缺失"


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def inject_ttdky_market_data(companies: dict[str, dict[str, object]]) -> None:
    company = companies.get(TARGET)
    if not company:
        return
    fin = company.setdefault("fin", {})
    if isinstance(fin, dict):
        # The daily row marks P/S as bad because ADR is in USD and financials are
        # in JPY. Use the company research / external quote cross-check value
        # instead of allowing the parser to treat 0.02x as real valuation support.
        fin["ps"] = 3.08
        fin["ps_source_override"] = "公司调研和外部行情交叉检查：2026-06-22/23 P/S 约 3.08x；原日度行 P/S=0.02x 标记为 currency_mismatch bad"


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for strategy in STRATS:
        ordered = sorted(
            companies.items(),
            key=lambda item: item[1].get("scores", {}).get(strategy, -999),  # type: ignore[union-attr]
            reverse=True,
        )
        total = len(ordered)
        for rank, (_ticker, company) in enumerate(ordered, start=1):
            pct = rank / total
            if pct <= 0.07:
                tier = "S"
            elif pct <= 0.25:
                tier = "A"
            elif pct <= 0.55:
                tier = "B"
            elif pct <= 0.85:
                tier = "C"
            else:
                tier = "D"
            company.setdefault("tiers", {})[strategy] = tier  # type: ignore[index]
            company.setdefault("ranks", {})[strategy] = rank  # type: ignore[index]
            company.setdefault("rank_total", {})[strategy] = total  # type: ignore[index]

    for company in companies.values():
        if not company.get("fin", {}).get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"  # type: ignore[index]
                company.setdefault("ranks", {})[strategy] = None  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    inject_ttdky_market_data(companies)
    base.TARGET = TARGET
    base.score_companies(companies)
    inject_ttdky_market_data(companies)

    floors: dict[str, dict[str, float]] = {}
    floors.update(getattr(project_calibration, "SCORE_FLOORS", {}))
    floors.update(getattr(etn_calibration, "LOCAL_SCORE_FLOORS", {}))
    floors["ETN"] = getattr(etn_calibration, "ETN_SCORES", {})
    floors["HUBB"] = getattr(hubb_calibration, "HUBB_SCORES", {})
    floors["MRAAY"] = getattr(mraay_calibration, "MRAAY_SCORES", {})

    for ticker, strategy_floors in floors.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in strategy_floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)  # type: ignore[union-attr]
            company["scores"][strategy] = max(float(current), float(floor))  # type: ignore[index]

    company_a = companies[TARGET]
    for strategy, score in TTDKY_SCORES.items():
        company_a.setdefault("scores", {})[strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_COMPONENT_PEERS:
        return "直接同业"
    if ticker in AI_POWER_AND_BOARD_ALTS or ticker in OPTICAL_AND_NETWORK_ALTS or ticker in DATA_CENTER_INFRA_ALTS:
        return "相邻替代"
    if ticker in STORAGE_AND_SERVER_CHAIN:
        return "上下游"
    if ticker in SEMICONDUCTOR_EQUIPMENT_MATERIALS:
        return "跨赛道"
    if category in {"配电_电源_功率器件", "AI网络_光互联_连接器", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, label: str, b: dict[str, object], rel: str) -> str:
    ticker = str(b["ticker"])
    if label == "中性":
        if rel == "跨赛道":
            return "业务差异大且证据互抵"
        return "档位接近且证据互有强弱"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "A有FY3/27指引和Magnetic硬锚",
            "右尾弹性优先": "A有AI被动元件、HDD和热管理期权",
            "风险调整收益": "A分散底盘和AI增量组合更均衡",
            "下行保护优先": "A净现金和元件平台底盘更稳",
            "估值消化优先": "A估值相对可被利润改善消化",
            "近端催化优先": "A分部兑现和Fabric8Labs验证更近",
            "价格确认/动量": "A近月动量确认更强",
            "激进短线": "A AI元件重估和动量更适合进攻",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker} 同业收入/订单兑现更硬",
            "右尾弹性优先": f"{ticker} AI供电或元件右尾更大",
            "风险调整收益": f"{ticker} 同业增长估值组合更优",
            "下行保护优先": f"{ticker} 同业现金流或估值缓冲更好",
            "估值消化优先": f"{ticker} 同业估值更易消化",
            "近端催化优先": f"{ticker} 同业订单/产品催化更近",
            "价格确认/动量": f"{ticker} 同业价格确认更强",
            "激进短线": f"{ticker} 同业beta和关注度更高",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker} 收入/RPO或客户兑现更短链",
            "右尾弹性优先": f"{ticker} AI主链或存储需求右尾更大",
            "风险调整收益": f"{ticker} 上行和下行组合更优",
            "下行保护优先": f"{ticker} 现金流或资产质量更防守",
            "估值消化优先": f"{ticker} 业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker} 订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker} 价格确认和资金偏好更强",
            "激进短线": f"{ticker} 高beta和AI关注度更适合短线",
        }[strategy]

    if rel == "相邻替代" or str(b.get("category", "")) in INFRA_CATS | HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker} 订单/backlog或交付更清楚",
            "右尾弹性优先": f"{ticker} 右尾或利润池弹性更直接",
            "风险调整收益": f"{ticker} 增长与估值组合更优",
            "下行保护优先": f"{ticker} 现金流或压力期表现更安全",
            "估值消化优先": f"{ticker} 订单兑现更能消化估值",
            "近端催化优先": f"{ticker} 近端订单或产能催化更强",
            "价格确认/动量": f"{ticker} 趋势和资金偏好更强",
            "激进短线": f"{ticker} 主题beta和波动更适合进攻",
        }[strategy]

    return {
        "NTM兑现优先": f"{ticker} 未来12个月兑现证据更直接",
        "右尾弹性优先": f"{ticker} 极端情景上行更大",
        "风险调整收益": f"{ticker} 风险调整赔率更好",
        "下行保护优先": f"{ticker} 估值或资产质量更安全",
        "估值消化优先": f"{ticker} 当前估值更易消化",
        "近端催化优先": f"{ticker} 未来两个季度催化更明确",
        "价格确认/动量": f"{ticker} 价格行为更强",
        "激进短线": f"{ticker} 短线关注度和波动更强",
    }[strategy]


def label_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    at = a.get("tiers", {}).get(strategy, "资料不足")  # type: ignore[union-attr]
    bt = b.get("tiers", {}).get(strategy, "资料不足")  # type: ignore[union-attr]
    if "资料不足" in (at, bt):
        if at == bt:
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    diff = float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0))  # type: ignore[union-attr]
    tier_gap = tier_value(str(at)) - tier_value(str(bt))
    abs_diff = abs(diff)
    if abs_diff < 4 and abs(tier_gap) == 0:
        return "中性"

    if rel == "直接同业":
        strong_cut, suggest_cut, micro_cut = 22, 10, 4
    elif rel in {"相邻替代", "上下游"}:
        strong_cut, suggest_cut, micro_cut = 25, 12, 4
    else:
        strong_cut, suggest_cut, micro_cut = 30, 15, 5

    if diff > 0:
        if tier_gap >= 3 or abs_diff >= strong_cut:
            return "强烈建议投A"
        if tier_gap >= 2 or abs_diff >= suggest_cut:
            return "建议投A"
        if tier_gap >= 1 or abs_diff >= micro_cut:
            return "微倾向投A"
    else:
        if tier_gap <= -3 or abs_diff >= strong_cut:
            return "强烈建议投B"
        if tier_gap <= -2 or abs_diff >= suggest_cut:
            return "建议投B"
        if tier_gap <= -1 or abs_diff >= micro_cut:
            return "微倾向投B"
    return "中性"


def cell_for(strategy: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    label = label_for(strategy, a, b, rel)
    return f"{label}：{reason_for(strategy, label, b, rel)}"


def direction_counts(row_obj: dict[str, object]) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in str(row_obj[strategy]))
    b_count = sum(1 for strategy in STRATS if "投B" in str(row_obj[strategy]))
    return a_count, b_count, 8 - a_count - b_count


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


def final_choice(row_obj: dict[str, object]) -> str:
    weights = {
        "NTM兑现优先": 1.15,
        "风险调整收益": 1.25,
        "估值消化优先": 1.10,
        "下行保护优先": 1.00,
        "右尾弹性优先": 0.95,
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
        score += weights[strategy] * label_score.get(tag_in_cell(str(row_obj[strategy])) or "中性", 0.0)
    return "A" if score >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], choice: str) -> str:
    ticker = str(b["ticker"])
    diffs = {
        strategy: float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0))  # type: ignore[union-attr]
        for strategy in STRATS
    }
    if choice == "A":
        if diffs["NTM兑现优先"] > 10:
            return "TDK有FY3/27官方指引、Magnetic高增和Passive AI应用增长，NTM兑现更可锚定。"
        if diffs["价格确认/动量"] > 10:
            return "TDK近两周和近一月价格确认更强，AI元件/HDD重估已有资金验证。"
        if diffs["下行保护优先"] > 8:
            return "TDK净现金、分散元件平台和成熟收入底盘比对手更能缓冲下行。"
        if diffs["近端催化优先"] > 8:
            return "TDK接下来靠Magnetic/Passive分部兑现、Fabric8Labs关闭和AI电源链订单验证取得优势。"
        return "TDK的成熟收入底盘加AI元件/HDD可收入化增量，在综合赔率上略优。"

    if diffs["右尾弹性优先"] < -12:
        return f"{ticker} 的AI主链、小基数或高beta右尾明显大于TDK。"
    if diffs["NTM兑现优先"] < -12:
        return f"{ticker} 的订单/RPO/backlog或收入确认证据比TDK更硬。"
    if diffs["估值消化优先"] < -10:
        return f"{ticker} 的估值更容易被NTM业绩消化，TDK已包含AI元件重估。"
    if diffs["下行保护优先"] < -10:
        return f"{ticker} 的现金流、估值或压力期韧性强于TDK。"
    if diffs["价格确认/动量"] < -12:
        return f"{ticker} 价格确认和资金偏好强于TDK。"
    return f"{ticker} 在多数投资思路下比TDK更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong = []
    b_strong = []
    close = []
    for strategy in STRATS:
        av = tier_value(a.get("tiers", {}).get(strategy))  # type: ignore[union-attr]
        bv = tier_value(b.get("tiers", {}).get(strategy))  # type: ignore[union-attr]
        label = strategy.replace("优先", "").replace("/动量", "动量")
        if av > bv:
            a_strong.append(label)
        elif av < bv:
            b_strong.append(label)
        else:
            close.append(label)

    parts = []
    if a_strong:
        parts.append("A强:" + "、".join(a_strong[:3]))
    if b_strong:
        parts.append("B强:" + "、".join(b_strong[:3]))
    if close:
        parts.append("接近:" + "、".join(close[:2]))
    return "；".join(parts) if parts else "档位接近"


def comparison_sort_key(row_obj: dict[str, object]) -> tuple[int, str, str]:
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return (rel_order.get(str(row_obj["relationship"]), 9), str(row_obj["classification"]), str(row_obj["ticker"]))


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    rows: list[dict[str, object]] = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        row_obj: dict[str, object] = {
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
        row_obj["key_reason"] = key_reason(a, b, str(row_obj["final_choice"]))
        rows.append(row_obj)
    return sorted(rows, key=comparison_sort_key)


def majority_rows(rows: list[dict[str, object]], side: str, limit: int = 45) -> list[dict[str, object]]:
    if side == "B":
        selected = [row for row in rows if int(row["bc"]) >= 5 and int(row["bc"]) - int(row["ac"]) >= 3]
        selected.sort(key=lambda row: (int(row["bc"]) - int(row["ac"]), int(row["bc"]), -int(row["nc"])), reverse=True)
    else:
        selected = [row for row in rows if int(row["ac"]) >= 5 and int(row["ac"]) - int(row["bc"]) >= 3]
        selected.sort(key=lambda row: (int(row["ac"]) - int(row["bc"]), int(row["ac"]), -int(row["nc"])), reverse=True)
    return selected[:limit]


def market_snapshot_text(a: dict[str, object]) -> str:
    fin = a.get("fin", {})
    mom2 = a.get("mom2", {})
    mom1 = a.get("mom1", {})
    soxx = a.get("soxx", {})
    return (
        f"2026-06-23 每日金融数据：TTDKY 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM P/E {fmt_num(fin.get('ttm_pe'))}，Forward P/E {fmt_num(fin.get('forward_pe'))}；"
        "P/S 原始行因 USD/JPY 币种错配标为 bad，本报告采用公司调研/外部行情交叉检查约 3.08x；"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}。"
        f"区间涨跌：截至 {mom2.get('latest_trade_date', '缺失')} 的过去两周 {fmt_pct(mom2.get('mom2w'))}，"
        f"截至 {mom1.get('latest_trade_date', '缺失')} 的过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-23 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    latest_dates = sorted({str(company["date"]) for company in companies.values() if company.get("date")})
    date_range = f"{latest_dates[0]} 至 {latest_dates[-1]}" if latest_dates else "缺失"
    missing_fin = sorted([ticker for ticker, company in companies.items() if not company.get("fin", {}).get("price")])

    stats: dict[str, Counter] = {strategy: Counter() for strategy in STRATS}
    for row_obj in comparisons:
        for strategy in STRATS:
            stats[strategy][tag_in_cell(str(row_obj[strategy]))] += 1

    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b = majority_rows(comparisons, "B", 45)
    strong_a = majority_rows(comparisons, "A", 45)
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = len(comparisons) - final_a

    support = {
        "NTM兑现优先": (
            "B",
            "FY3/27官方指引营收2,580十亿日元、OP 295十亿日元；Magnetic指引+21%~+24%，Passive指引+5%~+8%",
            "公司总收入指引仅+3%，Energy小型电池-3%~0%且手机假设-10%，未披露统一backlog",
        ),
        "右尾弹性优先": (
            "B",
            "AI server MLCC/电容、功率电感/µPOL、HDD heads/suspension、800VDC和Fabric8Labs热管理提供多条右尾",
            "AI/DC当前直接或近直接收入仍小，部分产品份额、客户和订单未披露，Fabric8Labs未并表",
        ),
        "风险调整收益": (
            "B",
            "净现金、OCF、成熟电子元件平台和HDD/Passive可收入化增量让上行不是纯叙事",
            "Forward P/E约31x且P/S约3.08x，FY3/27 FCF指引仅60十亿日元，CAPEX 370十亿日元压现金流",
        ),
        "下行保护优先": (
            "C",
            "现金和电子元件底盘较强，收入分散在Energy、Passive、Magnetic、Sensor四条线",
            "SOXX三段压力窗口累计-52.55%，且OTC ADR无干净IV覆盖，不能按低波动防守资产处理",
        ),
        "估值消化优先": (
            "C",
            "FY3/27 OP +8.3%、净利+15.0%，Magnetic/Passive mix改善可部分消化估值",
            "FY3/27收入只+3.0%，Forward P/E约31x，必须看到AI socket和HDD连续超指引才好消化",
        ),
        "近端催化优先": (
            "B",
            "FY3/27 Q1/Q2分部兑现、Magnetic高增、Passive AI应用产品、µPOL/FS1525/FS3303和Fabric8Labs关闭都是1-2季验证点",
            "催化更多是经营验证而非已披露大额订单；Fabric8Labs监管、客户和收入表仍未确认",
        ),
        "价格确认/动量": (
            "B",
            "2026-06-23区间文件显示过去两周+8.45%、过去一月+19.69%，AI元件/HDD重估已有价格确认",
            "动量强度低于项目内最热AI主链和高beta小盘，且无期权IV数据辅助判断",
        ),
        "激进短线": (
            "C",
            "AI被动元件、HDD数据湖、Fabric8Labs和近月动量给短线进攻资金叙事入口",
            "OTC ADR、IV缺失、公司体量大、总收入增速低，爆发力弱于光互联、NeoCloud、核能和小盘电力设备",
        ),
    }

    product_names = [
        "ICT小型锂电池/Energy core",
        "AI server MLCC与高端电容",
        "功率电感/µPOL/TDK-Lambda电源",
        "HDD heads/suspension assemblies",
        "BBU/UPS/储能元件",
        "服务器热传感/Edge AI sensors",
        "Fabric8Labs热管理",
    ]
    strong_b_names = "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]]) or "无"

    lines: list[str] = [
        "# TTDKY 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：TTDKY / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-23；过去两周、过去1个月区间涨跌为 2026-06-23；SOXX 三段压力窗口为 2026-06-23。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 TTDKY vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或既有公司对比成品的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。TDK 的优势不是总收入高速增长，而是 FY3/27 分部指引、Magnetic/HDD 已进入收入表、Passive AI 应用产品增长、近月价格确认和多条AI电源/存储/热管理期权共同支撑。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。短板是 FY3/27 总收入指引仅 `+3.0%`，Forward P/E 约 `31x`，FCF 指引只有 `60` 十亿日元，SOXX压力窗口累计 `-52.55%`，且期权IV缺失。",
        "- A 最适合的投资者画像：想用成熟日系电子元件平台配置AI服务器电源链、nearline HDD/AI数据湖、热管理并购期权，同时能接受低总收入增速和高估值验证压力的中等进攻型资金。",
        "- A 最不适合的投资者画像：只追求最高小基数右尾、直接AI芯片/光互联订单、低估值高FCF防守，或需要期权链表达短线进攻的资金。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常在直接AI收入、订单/RPO、右尾beta、估值消化、防守属性或短线关注度上压过 TDK。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：TDK 是项目内AI物理层元件和存储供应链里的中上档重估标的，最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家；它胜过大量传统慢增长或资料不足公司，但面对顶级AI芯片、云算力、光互联、强订单电力设备和Murata等直接元件强对手时，需要按投资思路拆分。",
        "- 后续最重要跟踪数据：FY3/27 Q1/Q2分部收入和OPM；Passive中AI server电容/电感订单、价格和lead time；Magnetic季度收入、HDD heads/suspension评论和nearline HDD订单；Energy小型电池库存与大客户需求；FS1525/FS3303/TDK-Lambda客户design win；Fabric8Labs交易关闭、Tier 1客户、收入、产能和毛利；CAPEX、库存、应收和FCF。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "TTDKY"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "配电_电源_功率器件")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", "2,560-2,600 十亿日元，中心值接近FY3/27官方指引2,580十亿日元"]),
        base.row(["乐观/极度乐观收入", "乐观：2,660-2,780 十亿日元；极度乐观：2,850-3,050 十亿日元"]),
        base.row(["利润和现金流结论", "基准经营利润285-305十亿日元、归母净利润215-230十亿日元；FCF 50-80十亿日元，接近官方60十亿日元指引，CAPEX 370十亿日元压现金流。"]),
        base.row(["最大传导瓶颈", "AI需求能否变成TDK可确认收入，核心在高端MLCC/电源socket份额、µPOL/TDK-Lambda客户认证、HDD高容量盘订单稳定性、Fabric8Labs关闭和量产认证。"]),
        base.row(["最大反证", "TDK未披露统一backlog/bookings；AI server MLCC和µPOL客户/份额不足；Energy占收入过半且FY3/27指引-3%~0%；估值已交易AI期权。"]),
        base.row(["近端催化剂", "FY3/27 Q1/Q2分部兑现、Magnetic +21%~+24%指引验证、Passive AI应用增长、FS1525/FS3303客户导入、Fabric8Labs交易关闭和客户披露。"]),
        base.row(["日度市场数据", market_snapshot_text(a)]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        tier = a.get("tiers", {}).get(strategy, "资料不足")  # type: ignore[union-attr]
        rank = a.get("ranks", {}).get(strategy)  # type: ignore[union-attr]
        rank_total = a.get("rank_total", {}).get(strategy, len(companies))  # type: ignore[union-attr]
        position = f"{support[strategy][0]}档；评分排名 {rank}/{rank_total}"
        lines.append(base.row([strategy, tier, position, support[strategy][1], support[strategy][2]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "同属AI服务器板级电源完整性、被动元件、功率/模拟/保护器件或高可靠电子元件供应链；优先看客户认证、订单/收入表、产品代际、利润率和估值。", "MRAAY、MPWR、IFNNY、TXN、ON、STM、VSH、LFUS、BELFB", "判断力度最高；若直接同业在AI MLCC、功率模块、估值或价格确认上明显更强，可在对应列压过TDK。"]),
        base.row(["相邻替代", "同属AI物理层、光互联、电气设备、数据中心电力/冷却、连接器或板级电源资金篮子，但产品不完全重叠。", "APH、TEL、CRDO、COHR、GLW、ETN、HUBB、VRT、POWL、GEV", "中等力度；赛道热度不能自动胜出，必须落到订单、利润捕获、估值消化和价格确认。"]),
        base.row(["上下游", "AI芯片、云厂、服务器、存储、EMS和HDD/SSD客户链是TDK高端被动元件、HDD heads和电源产品的需求来源；比较时区分下游收入规模与TDK可捕获利润。", "NVDA、AVGO、MU、TSM、MSFT、AMZN、DELL、SMCI、STX、WDC", "不把下游capex直接等同TDK收入；若对方拥有更直接AI收入、RPO、订单或价格确认，可在右尾、催化和动量列胜出。"]),
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
        wins = [strategy for strategy in STRATS if "投B" in str(row_obj[strategy])]
        catchup = "TDK需要披露更清晰的AI server MLCC/电源客户、订单/backlog、ASP和产能/良率，并证明高估值能被利润与FCF持续消化。"
        if row_obj["relationship"] == "上下游":
            catchup = "TDK需要证明AI芯片/云厂/服务器/HDD capex能持续落到其高端MLCC、电源模块和HDD heads收入，而不是只停留在行业TAM。"
        elif row_obj["relationship"] == "直接同业":
            catchup = "TDK需要在直接同业中证明AI MLCC、µPOL、磁性存储或热管理订单更硬，并把Forward P/E压力降下来。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for idx, row_obj in enumerate(strong_a, 1):
        wins = [strategy for strategy in STRATS if "投A" in str(row_obj[strategy])]
        catchup = "B需要拿出更硬的NTM收入/利润兑现、订单或客户合同，并证明估值、现金流和压力窗口能承受波动。"
        if row_obj["final_choice"] == "A" and "右尾弹性优先" in wins:
            catchup = "B需要把右尾叙事转成可确认收入、利润和现金流，并降低估值或融资反证。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/配电_电源_功率器件/TTDKY_TDK_Corporation_公司调研_2026-06-23.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；覆盖本次公司评估全集中 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失可用价格/估值的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-23.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-23.md`；SOXX压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md`。",
        "- TTDKY 日度/外部快照：`每日金融数据_2026-06-23.md`显示价格24.06美元、市值45.67B美元、TTM P/E 37.59、Forward P/E 31.25、IV缺失；P/S原始0.02x因USD/JPY错配标为bad，本报告采用公司调研和外部行情交叉检查约3.08x。",
        "- 外部行情和官方披露交叉检查：TDK FY March 2026 Full Year Performance Briefing `https://www.tdk.com/en/ir/ir_events/conference/2026/4q_1.html`；TDK FY3/26 performance briefing PDF `https://www.tdk.com/system/files/20264q_0mqf56xw_en.pdf`；TDK Fabric8Labs收购新闻稿 `https://www.tdk.com/en/news_center/press/20260610_01.html`；Yahoo Finance TTDKY行情页 `https://finance.yahoo.com/quote/TTDKY/`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/AI服务器_存储_芯片/行业调研_MLCC与高端陶瓷电容_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_HDD、对象存储与冷温数据存储_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_动态UPS、飞轮与超级电容_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_ttdky_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用正式评估最低分校准，对TTDKY的FY3/27指引、AI被动元件/HDD/Fabric8Labs、日度估值修正、SOXX压力窗口和价格动量做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
        raise SystemExit("缺少 TTDKY 正式评估文件")
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
                "ttdky_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "ttdky_scores": {strategy: round(float(a.get("scores", {}).get(strategy, 0)), 2) for strategy in STRATS},
                "ttdky_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
