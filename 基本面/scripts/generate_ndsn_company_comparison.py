from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "NDSN"
TARGET_NAME = "Nordson"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "NDSN_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_PEERS = {
    "DOV",
    "FTV",
    "KEYS",
    "TDY",
    "MKSI",
    "ONTO",
    "CAMT",
    "COHU",
    "FORM",
    "KLIC",
    "TER",
    "ATEYY",
    "ASMVY",
}

INDUSTRIAL_ADJACENT = {
    "AAON",
    "ALLE",
    "CARR",
    "CAT",
    "DCI",
    "DD",
    "DHR",
    "DKILY",
    "ECL",
    "EME",
    "FIX",
    "IESC",
    "JCI",
    "MOD",
    "MMM",
    "MSI",
    "MYRG",
    "PH",
    "PNR",
    "TMO",
    "TT",
}

MATERIAL_AND_FLUID_ADJACENT = {
    "AJNMY",
    "APD",
    "ASGLY",
    "AXTI",
    "CC",
    "ENTG",
    "HOCPY",
    "LIN",
    "MRAAY",
    "MTRN",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
}

SEMI_EQUIPMENT_ALTS = {
    "ACLS",
    "ACMR",
    "AMAT",
    "ASMIY",
    "ASML",
    "BESIY",
    "DSCSY",
    "ICHR",
    "KLAC",
    "LRCX",
    "MICLF",
    "NVMI",
    "PLAB",
    "TOELY",
    "UCTT",
    "VECO",
}

SEMI_CUSTOMERS_AND_DEMAND_CHAIN = {
    "AMKR",
    "ASX",
    "GFS",
    "IMOS",
    "INTC",
    "TSM",
    "TSEM",
    "UMC",
    "NVDA",
    "AMD",
    "AVGO",
    "MRVL",
    "QCOM",
    "ALAB",
    "ARM",
    "MU",
    "SMCI",
    "DELL",
    "HPE",
    "JBL",
    "FLEX",
    "CLS",
    "PENG",
    "FN",
}

DATA_CENTER_AND_NETWORK_CHAIN = {
    "AAOI",
    "ANET",
    "APH",
    "BDC",
    "BELFB",
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
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
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


def apply_global_floors(companies: dict[str, dict[str, object]]) -> None:
    for ticker, floors in calibrated.SCORE_FLOORS.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strat, floor in floors.items():
            current = company.setdefault("scores", {}).get(strat, 0)  # type: ignore[assignment]
            company["scores"][strat] = max(current, floor)  # type: ignore[index]


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for strat in STRATS:
        ordered = sorted(
            companies.items(),
            key=lambda item: item[1].setdefault("scores", {}).get(strat, 0),  # type: ignore[union-attr]
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
            company.setdefault("tiers", {})[strat] = tier  # type: ignore[index]
            company.setdefault("ranks", {})[strat] = rank  # type: ignore[index]

    for company in companies.values():
        if not company.get("fin", {}).get("price"):  # type: ignore[union-attr]
            for strat in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strat] = "资料不足"  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target
    apply_global_floors(companies)

    # Nordson calibration from its formal 2026-06-12 assessment and 2026-06-22 daily data.
    # NDSN has credible NTM execution, high margins and cash flow, plus ATS advanced-packaging
    # optionality. The limiting facts are product-level opacity, only indirect AI exposure,
    # and a valuation that already prices a quality industrial compounder.
    overrides = {
        "NTM兑现优先": 66.0,
        "右尾弹性优先": 60.0,
        "风险调整收益": 63.0,
        "下行保护优先": 75.0,
        "估值消化优先": 58.0,
        "近端催化优先": 61.0,
        "价格确认/动量": 52.0,
        "激进短线": 45.0,
    }
    for strat, score in overrides.items():
        companies[TARGET].setdefault("scores", {})[strat] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in INDUSTRIAL_ADJACENT or ticker in MATERIAL_AND_FLUID_ADJACENT or ticker in SEMI_EQUIPMENT_ALTS:
        return "相邻替代"
    if ticker in SEMI_CUSTOMERS_AND_DEMAND_CHAIN or ticker in DATA_CENTER_AND_NETWORK_CHAIN:
        return "上下游"
    if category == "半导体材料_化学品_基板":
        return "相邻替代"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩"}:
        return "相邻替代"
    if category in HIGH_GROWTH_CATS:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict[str, object], diff: float) -> str:
    ticker = str(company["ticker"])
    cat = str(company.get("category", ""))
    rel = relationship(company)

    if winner == "中性":
        if rel == "跨赛道":
            return "业务差异较大且档位接近"
        return "档位接近需继续验证"

    if winner == "A":
        return {
            "NTM兑现优先": "A有FY2026指引和backlog支撑",
            "右尾弹性优先": "A先进封装点胶/检测仍有右尾",
            "风险调整收益": "A高毛利、FCF和低IV更均衡",
            "下行保护优先": "A MFS/IPS底盘和现金流更稳",
            "估值消化优先": "A估值可由利润和FCF消化",
            "近端催化优先": "A有Q3指引和ATS订单验证点",
            "价格确认/动量": "A温和修复且未明显过热",
            "激进短线": "A的ATS先进封装主题有事件弹性",
        }[strat]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker} 同业订单或收入兑现更硬",
            "右尾弹性优先": f"{ticker} 同业右尾或产品代际更大",
            "风险调整收益": f"{ticker} 同业赔率组合更优",
            "下行保护优先": f"{ticker} 同业防守或现金流更强",
            "估值消化优先": f"{ticker} 同业增长更能消化估值",
            "近端催化优先": f"{ticker} 同业订单/产品催化更直接",
            "价格确认/动量": f"{ticker} 同业价格确认更强",
            "激进短线": f"{ticker} 同业关注度和beta更高",
        }[strat]

    if cat in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker} 的AI主链收入兑现更短链",
            "右尾弹性优先": f"{ticker} 的直接AI右尾和小基数更大",
            "风险调整收益": f"{ticker} 的上行空间更能覆盖风险",
            "下行保护优先": f"{ticker} 的需求能见度或现金流更好",
            "估值消化优先": f"{ticker} 的高增长更能覆盖估值",
            "近端催化优先": f"{ticker} 的产品/订单催化更密集",
            "价格确认/动量": f"{ticker} 的价格确认和资金偏好更强",
            "激进短线": f"{ticker} 的高beta更适合短线进攻",
        }[strat]

    if cat in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker} 的电力/机电订单兑现更清楚",
            "右尾弹性优先": f"{ticker} 的AI基础设施右尾更大",
            "风险调整收益": f"{ticker} 的订单和估值组合更优",
            "下行保护优先": f"{ticker} 的防守属性或现金流更稳",
            "估值消化优先": f"{ticker} 的业绩增速更能消化估值",
            "近端催化优先": f"{ticker} 的近端订单或项目催化更强",
            "价格确认/动量": f"{ticker} 的价格确认更强",
            "激进短线": f"{ticker} 的AI电力/冷却beta更强",
        }[strat]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker} 的下游需求或收入表证据更硬",
            "右尾弹性优先": f"{ticker} 的需求池右尾更直接",
            "风险调整收益": f"{ticker} 的利润捕获或上行更优",
            "下行保护优先": f"{ticker} 的需求/现金流韧性更好",
            "估值消化优先": f"{ticker} 的增长与估值匹配更好",
            "近端催化优先": f"{ticker} 的客户/产能催化更清楚",
            "价格确认/动量": f"{ticker} 的资金确认更强",
            "激进短线": f"{ticker} 的短线叙事弹性更强",
        }[strat]

    return {
        "NTM兑现优先": f"{ticker} 的经营兑现更清楚",
        "右尾弹性优先": f"{ticker} 的右尾弹性更大",
        "风险调整收益": f"{ticker} 的风险调整后赔率更优",
        "下行保护优先": f"{ticker} 的压力期更安全",
        "估值消化优先": f"{ticker} 的估值消化更容易",
        "近端催化优先": f"{ticker} 的近端催化更明确",
        "价格确认/动量": f"{ticker} 的价格确认更强",
        "激进短线": f"{ticker} 的短线进攻属性更强",
    }[strat]


def label_for(strat: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    at = a.get("tiers", {}).get(strat, "资料不足")  # type: ignore[union-attr]
    bt = b.get("tiers", {}).get(strat, "资料不足")  # type: ignore[union-attr]
    if "资料不足" in (at, bt):
        if at == bt:
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    diff = a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0)  # type: ignore[union-attr,operator]
    tier_gap = tier_value(str(at)) - tier_value(str(bt))
    abs_diff = abs(diff)
    if abs_diff < 4:
        return "中性"

    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 28, 14, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 24, 12, 4
    elif rel == "直接同业":
        strong_cut, suggest_cut, micro_cut = 20, 9, 4
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


def cell_for(strat: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    label = label_for(strat, a, b, rel)
    diff = a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0)  # type: ignore[union-attr,operator]
    winner = "A" if "投A" in label else "B" if "投B" in label else "中性"
    return f"{label}：{reason_for(strat, winner, b, diff)}"


def direction_counts(row_obj: dict[str, object]) -> tuple[int, int, int]:
    a_count = sum(1 for strat in STRATS if "投A" in str(row_obj[strat]))
    b_count = sum(1 for strat in STRATS if "投B" in str(row_obj[strat]))
    return a_count, b_count, 8 - a_count - b_count


def final_choice(row_obj: dict[str, object], a: dict[str, object], b: dict[str, object]) -> str:
    weights = {
        "NTM兑现优先": 1.20,
        "风险调整收益": 1.15,
        "估值消化优先": 1.05,
        "下行保护优先": 1.00,
        "右尾弹性优先": 0.90,
        "近端催化优先": 0.80,
        "价格确认/动量": 0.50,
        "激进短线": 0.50,
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
    for strat in STRATS:
        label = base.tag_in_cell(str(row_obj[strat]))
        score += weights[strat] * label_score.get(label, 0.0)
    if score > 0.15:
        return "A"
    if score < -0.15:
        return "B"
    risk_diff = a.get("scores", {}).get("风险调整收益", 0) - b.get("scores", {}).get("风险调整收益", 0)  # type: ignore[union-attr,operator]
    return "A" if risk_diff >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], choice: str) -> str:
    diffs = {strat: a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0) for strat in STRATS}  # type: ignore[union-attr]
    if choice == "A":
        if diffs["下行保护优先"] > 12:
            return "NDSN的MFS/IPS底盘、低IV和现金流质量提供更好下行保护。"
        if diffs["NTM兑现优先"] > 10:
            return "NDSN有FY2026指引、backlog同比+18%和三分部收入兑现支撑。"
        if diffs["估值消化优先"] > 10:
            return "NDSN估值不低但高毛利、EPS和FCF兑现路径比B更清楚。"
        if diffs["右尾弹性优先"] > 10:
            return "NDSN先进封装点胶/检测小基数右尾比B更可收入化。"
        return "NDSN在经营质量、现金流和先进封装小期权之间更均衡。"
    if diffs["右尾弹性优先"] < -18:
        return f"{b['ticker']} 的直接AI收入、小基数或平台型右尾明显强于NDSN。"
    if diffs["NTM兑现优先"] < -14:
        return f"{b['ticker']} 的订单/RPO/backlog或收入确认证据比NDSN更硬。"
    if diffs["估值消化优先"] < -12:
        return f"{b['ticker']} 的增长和估值匹配度优于NDSN。"
    if diffs["价格确认/动量"] < -14:
        return f"{b['ticker']} 的价格确认和短线资金偏好明显强于NDSN。"
    if diffs["下行保护优先"] < -14:
        return f"{b['ticker']} 的现金流、防御性或压力期表现明显优于NDSN。"
    return f"{b['ticker']} 在多数投资思路下比NDSN更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong: list[str] = []
    b_strong: list[str] = []
    close: list[str] = []
    for strat in STRATS:
        diff = a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0)  # type: ignore[union-attr,operator]
        label = strat.replace("优先", "").replace("/动量", "动量")
        if diff >= 8:
            a_strong.append(label)
        elif diff <= -8:
            b_strong.append(label)
        else:
            close.append(label)

    def joined(items: list[str]) -> str:
        if not items:
            return "无"
        return "、".join(items[:3]) + ("等" if len(items) > 3 else "")

    return f"A强：{joined(a_strong)}；B强：{joined(b_strong)}；接近：{joined(close)}"


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
            "b": b,
        }
        for strat in STRATS:
            row_obj[strat] = cell_for(strat, a, b, rel)
        ac, bc, nc = direction_counts(row_obj)
        row_obj["majority"] = f"A {ac} / B {bc} / 中性 {nc}"
        row_obj["ac"] = ac
        row_obj["bc"] = bc
        row_obj["nc"] = nc
        choice = final_choice(row_obj, a, b)
        row_obj["final_choice"] = choice
        row_obj["key_reason"] = key_reason(a, b, choice)
        rows.append(row_obj)

    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return sorted(rows, key=lambda x: (rel_order.get(str(x["relationship"]), 9), str(x["ticker"])))


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
    return f"${float(value):.2f}B"


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    return f"{float(value):.2f}%"


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(company_dates)} 至 {max(company_dates)}"
    stats = {strat: Counter() for strat in STRATS}
    for comparison in comparisons:
        for strat in STRATS:
            stats[strat][base.tag_in_cell(str(comparison[strat]))] += 1
    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b = sorted(
        comparisons,
        key=lambda x: (int(x["bc"]) - int(x["ac"]), x["b"]["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (int(x["ac"]) - int(x["bc"]), a["scores"]["下行保护优先"] - x["b"]["scores"]["下行保护优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if int(x["bc"]) >= 5 and int(x["bc"]) - int(x["ac"]) >= 3][:45]
    strong_a_rows = [x for x in strong_a if int(x["ac"]) >= 5 and int(x["ac"]) - int(x["bc"]) >= 3][:45]
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "B")
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker].get("fin") or not companies[ticker]["fin"].get("price")  # type: ignore[union-attr]
    ]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    fin = a.get("fin", {})
    mom2 = a.get("mom2", {})
    mom1 = a.get("mom1", {})
    soxx = a.get("soxx", {})

    product_names = [
        "ATS先进封装点胶/underfill/encapsulation/plasma",
        "ATS Test & Inspection/MRS/WaferSense",
        "ATS inspection software/Nordson Intelligence AI",
        "MFS医疗与高端流体部件",
        "IPS精密农业ARAG/CapstanAG",
        "IPS核心工业点胶/涂布/聚合物/包装",
    ]

    support = {
        "NTM兑现优先": (
            "FY2026H1收入+8.6%、Q2收入+8.5%、FY2026收入指引29.30-30.10亿美元，backlog同比+18%",
            "ATS产品级订单、AI/HPC客户、ATS backlog金额未披露，收入确认仍需折扣",
        ),
        "右尾弹性优先": (
            "ATS先进封装点胶/underfill/plasma、X-ray/光学/声学检测和WaferSense受HBM/CoWoS良率链拉动",
            "AI/HPC子集估算只占公司收入中个位数到低双位数，极度乐观需公司捕获和交付同时成立",
        ),
        "风险调整收益": (
            "2026-06-22 Forward PE 23.74、Call IV 33.3%，FY2026H1 FCF约2.934亿美元，净债务/TTM EBITDA约1.9x",
            "估值已体现高质量工业溢价，若ATS订单透明度不足或工业周期弱化，上行会被压缩",
        ),
        "下行保护优先": (
            "MFS EBITDA margin约37%、IPS约35%，医疗/工业流体和高毛利服务提供防守底盘；SOXX压力窗口累计-37.43%",
            "并购后杠杆、商誉/无形资产和工业周期仍是下行变量，防守性弱于公用事业/低估值现金流标的",
        ),
        "估值消化优先": (
            "基准NTM收入30.5-31.5亿美元、EBITDA 9.6-10.2亿美元，EPS/FCF可逐步消化估值",
            "23.74x远期PE与5.66x P/S不低，只有中高个位数收入增速时估值消化速度有限",
        ),
        "近端催化优先": (
            "Q3收入指引7.60-7.90亿美元、ATS/x-ray recovery、Q2 backlog+18%、MFS/IPS订单恢复可在1-2季验证",
            "缺少客户名单、产品级订单金额和明确AI项目排期，催化强度低于RPO/大订单硬锚公司",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+4.80%、过去一月+2.21%，2026-06-22价格295.06高于6月初289.45",
            "价格确认温和，远弱于光互联、HBM、NeoCloud和AI电力高beta标的",
        ),
        "激进短线": (
            "ATS先进封装/检测若被财报进一步点名，可能触发事件重估",
            "Call IV 33.3%且工业复合体属性强，短线爆发力明显弱于AI主链和高波动小盘",
        ),
    }

    daily_snapshot = (
        f"2026-06-22 收盘价 `{fmt_num(fin.get('price'))}` 美元，市值 `{fmt_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `{fmt_num(fin.get('ttm_pe'))}`，Forward PE `{fmt_num(fin.get('forward_pe'))}`，"
        f"P/S `{fmt_num(fin.get('ps'))}`，P/B `{fmt_num(fin.get('pb'))}`，EV/EBITDA `{fmt_num(fin.get('ev_ebitda'))}`，"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`、Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03 过去两周 `{fmt_pct(mom2.get('mom2w'))}`、过去一月 `{fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04 三段 SOXX 压力窗口累计 `{fmt_pct(soxx.get('soxx_cum'))}`。"
    )

    out: list[str] = [
        "# NDSN 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：NDSN / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04；日度新闻最新文件日期为 2026-06-23。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 NDSN vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。NDSN 的优势集中在下行保护、NTM兑现和风险调整收益：FY2026指引、backlog同比+18%、高毛利三分部、MFS/IPS现金流底盘和ATS先进封装小期权同时存在。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。短板是AI/HPC收入、ATS产品级订单和客户名不披露，右尾不如直接AI主链，短线beta和价格确认也不强。",
        "- A 最适合的投资者画像：希望买高质量工业精密技术平台，同时获得先进封装点胶、检测量测、WaferSense和电子组装良率链间接受益，但不愿承担纯AI硬件高波动的配置者。",
        "- A 最不适合的投资者画像：只追求最高收入增速、最大非线性右尾、明确大额订单/RPO、或短期高beta爆发的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]])}。这些公司通常拥有更直接AI主链收入、订单/RPO/backlog、数据中心电力/网络/芯片核心利润池或更强价格确认。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：NDSN 是项目内中上档质量型工业/半导体良率链标的，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家；它强于不少低兑现、高波动或现金流弱标的，但面对NVDA/AVGO/MU/ALAB/CRDO/CEG/ETN/VRT等核心AI主链或电力稀缺公司通常不占优。",
        "- 后续最重要跟踪数据：季度backlog同比和绝对金额、ATS order commentary、advanced packaging/x-ray/MRS/AMI/WaferSense订单或客户案例、MFS organic growth和margin、IPS precision agriculture整合、gross margin、EBITDA margin、库存、应收、FCF conversion、是否首次披露AI/HPC/HBM/CoWoS/FOPLP或软件订阅相关收入。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "NDSN"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "30.5-31.5亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "ATS先进封装/检测需求能否从行业需求池进入Nordson产品级订单、交付和收入；公司不披露AI客户、产品级订单、ATS backlog金额或交付排期。"]),
        base.row(["最大反证", "AI/HPC收入仅为模型估算且占比不高；若Q3/Q4 ATS订单放缓、x-ray/advanced packaging验收延迟、MFS/IPS周期转弱，估值消化和右尾都会降档。"]),
        base.row(["近端催化剂", "FY2026Q3收入指引兑现、Q2 backlog+18%能否继续、ATS/x-ray recovery、先进封装客户案例、MFS organic growth、IPS precision agriculture并购协同和FCF conversion。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strat in STRATS:
        out.append(base.row([strat, a["tiers"][strat], rank_text[strat], support[strat][0], support[strat][1]]))  # type: ignore[index]

    out += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与NDSN在精密点胶、工业流体、检测计量、半导体封装/电子制造设备或工业技术平台需求池高度重叠，优先比较订单、产品代际、margin、客户质量和估值。", "DOV、FTV、KEYS、TDY、MKSI、ONTO、CAMT、COHU、FORM、TER", "同业证据权重最高；若对手在检测量测、设备订单或产品代际上明显更强，可给建议或强烈建议。"]),
        base.row(["相邻替代", "同属半导体设备/材料、工业精密技术、液冷/流体控制、生命科学工具或数据中心物理基础设施资金篮子，但产品不直接竞争。", "DHR、TMO、DD、ENTG、AMAT、ASML、LRCX、KLAC、VRT、ETN、NVT", "重点回答资金只能买一个时，谁的增长质量、估值消化、现金流和近端催化更好。"]),
        base.row(["上下游", "B位于NDSN先进封装、检测计量、电子组装或AI数据中心间接需求链的上游/下游，如AI芯片、HBM、服务器、云厂、封测、代工和网络链。", "NVDA、AVGO、AMD、MU、TSM、ASX、AMKR、MSFT、AMZN、DELL", "不把下游AI CapEx直接等同NDSN收入，核心看利润捕获、订单硬度、收入确认和议价权。"]),
        base.row(["跨赛道", "业务差异较大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "软件、航天、部分能源和消费/工业平台公司", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    out.append(base.row(headers))
    out.append(base.row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for index, row_obj in enumerate(comparisons, start=1):
        b = row_obj["b"]
        out.append(
            base.row(
                [
                    index,
                    base.short_name(b),  # type: ignore[arg-type]
                    row_obj["classification"],
                    row_obj["relationship"],
                    row_obj["grade_diff"],
                    *[row_obj[strat] for strat in STRATS],
                    row_obj["majority"],
                    row_obj["final_choice"],
                    row_obj["key_reason"],
                ]
            )
        )

    out += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strat in STRATS:
        out.append(base.row([strat] + [stats[strat][tag] for tag in TAG_ORDER] + [a_side[strat], b_side[strat]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, row_obj in enumerate(strong_b_rows, start=1):
        b = row_obj["b"]
        wins = [strat for strat in STRATS if (base.tag_in_cell(str(row_obj[strat])) or "").endswith("投B")]
        need = "需要NDSN披露ATS产品级订单、客户、backlog金额、交付排期，并证明先进封装/检测收入占比和margin持续上行。"
        if row_obj["relationship"] == "直接同业":
            need = "需要NDSN在精密点胶/检测同业中证明ATS订单、margin、客户指定和收入兑现强于B。"
        elif row_obj["relationship"] == "上下游":
            need = "需要NDSN证明自己能从下游AI芯片、封测、服务器或云厂CapEx中捕获可观利润，而不只是小额间接受益。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), row_obj["key_reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, row_obj in enumerate(strong_a_rows, start=1):
        b = row_obj["b"]
        wins = [strat for strat in STRATS if (base.tag_in_cell(str(row_obj[strat])) or "").endswith("投A")]
        need = "需要B提高收入确认可信度、现金流质量和估值消化能力，或出现明确订单/指引上修。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要B把右尾叙事转成可确认收入和利润，并降低估值、波动或资产负债表反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), row_obj["key_reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/半导体材料_化学品_基板/NDSN_Nordson_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体检测量测设备_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装湿化学与表面处理材料_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体设备子系统与真空_RF_流体模块_2026-06-11.md`；`行业调研/AI园区电力_机电_冷却/行业调研_液冷小组件与流体控制_2026-06-10.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_ndsn_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用既有正式脚本的最低分校准，对NDSN的FY2026指引、backlog+18%、ATS先进封装/检测小期权、MFS/IPS现金流底盘、估值、IV和价格动量做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
        "",
        "### 公司全集最新正式评估文件清单",
        "",
        base.row(["股票代号", "公司名称", "评估日期", "正式评估文件"]),
        base.row(["---", "---", "---", "---"]),
    ]
    for ticker in sorted(companies):
        company = companies[ticker]
        out.append(base.row([ticker, company["name"], company["date"], f"`分析报告/公司评估/结果/{company['path'].name}`"]))  # type: ignore[index,union-attr]

    out.append("")
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 NDSN 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "ndsn_tiers": companies[TARGET]["tiers"],
        "ndsn_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
        "ndsn_ranks": companies[TARGET]["ranks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
