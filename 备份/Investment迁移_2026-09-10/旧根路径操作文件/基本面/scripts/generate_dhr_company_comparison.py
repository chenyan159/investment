from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "DHR"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "DHR_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {"TMO"}
LIFE_SCIENCE_ADJACENT = {"FTV", "TDY", "KEYS", "MSI"}
FILTRATION_WATER_ADJACENT = {"DD", "ECL", "PNR", "DCI", "NDSN", "MMM", "DOV", "PH", "CARR", "JCI", "TT", "DKILY"}
MATERIAL_ADJACENT = {
    "AJNMY",
    "APD",
    "ASGLY",
    "AXTI",
    "CC",
    "DKILY",
    "ENTG",
    "HOCPY",
    "LIN",
    "MRAAY",
    "MTRN",
    "NDSN",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
}
SEMI_DOWNSTREAM_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "封测_检测_计量_光罩",
    "晶圆制造_前道设备",
}
DC_DOWNSTREAM_CATS = {
    "云算力_IDC_AI软件平台",
    "机电_冷却_工程_水处理_边缘工业AI",
    "电力_发电_能源_储能",
    "配电_电源_功率器件",
}


def supplement_dhr_finance(companies: dict[str, dict[str, object]]) -> None:
    """DHR was added after the formal 2026-06-22 daily snapshot files."""
    dhr = companies[TARGET]
    dhr["fin"] = {
        "category": "半导体材料_化学品_基板",
        "name": "Danaher Corporation",
        "price_date": "2026-06-23",
        "price": 178.19,
        "market_cap_b": 126.73,
        "ttm_pe": 34.40,
        "forward_pe": 21.10,
        "ps": 5.10,
        "pb": None,
        "ev_ebitda": None,
        "eps": 5.18,
        "call_iv": None,
        "put_iv": None,
        "currency": "USD",
        "financial_currency": "USD",
        "shares_outstanding": "约710.75M",
        "ttm_revenue": "$24.84B",
        "ttm_revenue_b": 24.84,
        "ttm_eps": 5.18,
        "forward_eps": 8.45,
        "listing_type": "common/equity",
        "source_timestamp": "2026-06-23 11:00:09 UTC",
        "valuation_check": "supplemental; daily finance 2026-06-22 missing DHR",
        "notes": "DHR不在金融资料/每日金融数据_2026-06-22.md；补充价格/市值来自DHR公司调研中的2026-06-23补充行情记录；IV缺失。",
    }
    dhr["mom2"] = {}
    dhr["mom1"] = {}
    dhr["soxx"] = {}


def apply_global_floors(companies: dict[str, dict[str, object]]) -> None:
    for ticker, floors in calibrated.SCORE_FLOORS.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strat, floor in floors.items():
            current = company.setdefault("scores", {}).get(strat, 0)  # type: ignore[assignment]
            company["scores"][strat] = max(current, floor)  # type: ignore[index]


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
    supplement_dhr_finance(companies)
    base.score_companies(companies)
    apply_global_floors(companies)

    # DHR is a quality life-science/diagnostics compounder with a visible
    # bioprocessing recovery and Masimo consolidation, but weak direct AI beta.
    overrides = {
        "NTM兑现优先": 68.0,
        "右尾弹性优先": 50.0,
        "风险调整收益": 61.0,
        "下行保护优先": 74.0,
        "估值消化优先": 58.0,
        "近端催化优先": 59.0,
        "价格确认/动量": 43.0,
        "激进短线": 39.0,
    }
    for strat, score in overrides.items():
        companies[TARGET].setdefault("scores", {})[strat] = score  # type: ignore[index]
    recompute_tiers(companies)


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in LIFE_SCIENCE_ADJACENT or ticker in FILTRATION_WATER_ADJACENT or ticker in MATERIAL_ADJACENT:
        return "相邻替代"
    if category == "半导体材料_化学品_基板":
        return "相邻替代"
    if category in SEMI_DOWNSTREAM_CATS or category in DC_DOWNSTREAM_CATS:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict[str, object], diff: float) -> str:
    ticker = str(company["ticker"])
    cat = str(company.get("category", ""))
    if winner == "A":
        return {
            "NTM兑现优先": "A有Bioprocessing、RPO和Masimo并表锚",
            "右尾弹性优先": "A有生物工艺和Pall过滤小右尾",
            "风险调整收益": "A复购耗材和FCF质量更均衡",
            "下行保护优先": "A recurring收入和现金流底盘更稳",
            "估值消化优先": "A约21x FwdPE可由EPS兑现消化",
            "近端催化优先": "A有Masimo指引和bioprocess订单验证",
            "价格确认/动量": "A估值修复线索略优",
            "激进短线": "A低预期修复赔率略好",
        }[strat]
    if winner == "B":
        if ticker in DIRECT_PEERS:
            return {
                "NTM兑现优先": "B同业收入/RPO规模更硬",
                "右尾弹性优先": "B同业AI/Clario/工具右尾更大",
                "风险调整收益": "B同业上行和估值组合更优",
                "下行保护优先": "B同业规模和RPO缓冲更强",
                "估值消化优先": "B同业业绩消化更清楚",
                "近端催化优先": "B同业并购/RPO催化更直接",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业短线关注度更强",
            }[strat]
        if cat in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链收入兑现更短链",
                "右尾弹性优先": "B直接AI右尾和小基数更大",
                "风险调整收益": "B上行空间更能覆盖风险",
                "下行保护优先": "B需求能见度或现金流韧性更好",
                "估值消化优先": "B高速增长更能消化估值",
                "近端催化优先": "B产品/订单催化更密集",
                "价格确认/动量": "B价格确认和资金偏好更强",
                "激进短线": "B高beta和AI叙事更适合进攻",
            }[strat]
        if cat in INFRA_CATS:
            return {
                "NTM兑现优先": "B订单/backlog交付更直接",
                "右尾弹性优先": "B AI电力/机电右尾更大",
                "风险调整收益": "B增长和估值组合更优",
                "下行保护优先": "B订单粘性或防守属性更强",
                "估值消化优先": "B用订单兑现消化估值更快",
                "近端催化优先": "B订单/产能/财报催化更近",
                "价格确认/动量": "B价格趋势更强",
                "激进短线": "B电气化交易弹性更强",
            }[strat]
        return {
            "NTM兑现优先": "B未来12个月兑现证据更直接",
            "右尾弹性优先": "B极端情景上行更大",
            "风险调整收益": "B上行和下行组合更好",
            "下行保护优先": "B现金流或估值缓冲更好",
            "估值消化优先": "B当前估值更容易被业绩消化",
            "近端催化优先": "B未来两个季度催化更明确",
            "价格确认/动量": "B价格行为更强",
            "激进短线": "B短线波动和关注度更适合进攻",
        }[strat]
    return {
        "NTM兑现优先": "NTM证据接近",
        "右尾弹性优先": "右尾证据互有强弱",
        "风险调整收益": "赔率和风险接近",
        "下行保护优先": "防守证据接近",
        "估值消化优先": "估值消化差距不大",
        "近端催化优先": "近端催化强度接近",
        "价格确认/动量": "DHR缺正式动量数据",
        "激进短线": "短线弹性差距有限",
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
        strong_cut, suggest_cut, micro_cut = 26, 13, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 23, 11, 4
    else:
        strong_cut, suggest_cut, micro_cut = 20, 9, 4

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


def final_choice(row_obj: dict[str, object]) -> str:
    weights = {
        "NTM兑现优先": 1.20,
        "风险调整收益": 1.15,
        "估值消化优先": 1.05,
        "下行保护优先": 1.00,
        "右尾弹性优先": 0.85,
        "近端催化优先": 0.80,
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
    for strat in STRATS:
        label = base.tag_in_cell(str(row_obj[strat]))
        score += weights[strat] * label_score.get(label, 0.0)
    return "A" if score > 0.15 else "B" if score < -0.15 else "中性"


def key_reason(a: dict[str, object], b: dict[str, object], choice: str) -> str:
    if choice == "中性":
        return "DHR的质量/防守与对手的增长/估值证据未拉开可强判差距。"
    diffs = {strat: a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0) for strat in STRATS}  # type: ignore[union-attr]
    if choice == "A":
        if diffs["下行保护优先"] > 12:
            return "DHR recurring revenue、FCF和诊断/生物工艺底盘更适合防守配置。"
        if diffs["NTM兑现优先"] > 10:
            return "DHR有Bioprocessing、RPO、FY2026指引和Masimo并表支撑NTM兑现。"
        if diffs["估值消化优先"] > 10:
            return "DHR估值虽不便宜，但EPS/FCF兑现路径比B更容易消化。"
        return "DHR在经营质量、现金流和下行保护上略胜，B的增长证据不足以覆盖反证。"
    if diffs["右尾弹性优先"] < -18:
        return f"{b['ticker']}的直接AI收入、小基数或平台型右尾明显强于DHR。"
    if diffs["NTM兑现优先"] < -14:
        return f"{b['ticker']}的订单/RPO/backlog或收入确认证据比DHR更硬。"
    if diffs["估值消化优先"] < -12:
        return f"{b['ticker']}的增长和估值匹配度优于DHR。"
    if diffs["价格确认/动量"] < -14:
        return f"{b['ticker']}的价格确认和资金偏好明显强于DHR。"
    return f"{b['ticker']}在多数投资思路下比DHR更符合项目内资金配置目标。"


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
        choice = final_choice(row_obj)
        row_obj["final_choice"] = choice
        row_obj["key_reason"] = key_reason(a, b, choice)
        rows.append(row_obj)

    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return sorted(rows, key=lambda x: (rel_order.get(str(x["relationship"]), 9), str(x["ticker"])))


def fmt_num(value: object, decimals: int = 1) -> str:
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
    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy in STRATS:
            stats[strategy][base.tag_in_cell(str(comparison[strategy]))] += 1
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
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker].get("fin") or not companies[ticker]["fin"].get("price")  # type: ignore[union-attr]
    ]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    fin = a["fin"]  # type: ignore[assignment]

    product_names: list[str] = []
    for product in a["products"]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])
        if len(product_names) >= 7:
            break

    daily_snapshot = (
        f"DHR未纳入2026-06-22正式每日金融数据；补充快照为2026-06-23价格 `{fmt_num(fin.get('price'), 2)}`，"
        f"市值 `{fmt_b(fin.get('market_cap_b'))}`，TTM PE `{fmt_num(fin.get('ttm_pe'), 1)}`，"
        f"Forward PE `{fmt_num(fin.get('forward_pe'), 1)}`，P/S `{fmt_num(fin.get('ps'), 1)}`；"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`、Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        "DHR在2026-06-03两周/一月区间涨跌和2026-06-04 SOXX压力窗口文件中缺失，价格确认、动量和激进短线均按保守口径。"
    )

    support = {
        "NTM兑现优先": (
            "FY2026 legacy core `+3%-+6%`、2026Q1 RPO `$5.3B`且48%一年内确认、Masimo已于2026-06-10并表",
            "Q1 total core仅`+0.5%`，Cepheid respiratory弱，Life Sciences equipment仍弱",
        ),
        "右尾弹性优先": (
            "Bioprocessing equipment orders `+30%+`、Masimo急诊监护、Pall半导体过滤和液冷过滤有小右尾",
            "AI数据中心液冷过滤缺DHR-specific订单，极度乐观需多个非线性环节同时成立",
        ),
        "风险调整收益": (
            "2025 FCF约`$5.3B`、recurring revenue约85%、生命科学/诊断复购质量高",
            "Forward PE约`21.1x`并不低，Masimo杠杆/整合和中国诊断价格压力降低赔率",
        ),
        "下行保护优先": (
            "诊断试剂、bioprocessing耗材、服务和强FCF提供防守底盘",
            "并购后净杠杆上升，生命科学工具和诊断仍受预算/报销周期影响",
        ),
        "估值消化优先": (
            "基准NTM收入`$26.6-$27.5B`、adjusted EBITDA `$8.4-$9.1B`，EPS/FCF可支撑中速消化",
            "估值要求已隐含bioprocessing修复和Masimo增厚，低个位数core会压制倍数",
        ),
        "近端催化优先": (
            "2026Q2财报将更新Masimo全年并表指引，bioprocessing订单转收入和consumables增长可验证",
            "缺少AI硬件链那种大额订单、客户认证或产能放量催化",
        ),
        "价格确认/动量": (
            "补充价格较2024-2025高估值阶段已有压缩，若Q2指引增厚可能形成修复",
            "正式区间涨跌和SOXX压力窗口未覆盖DHR，无法给强价格确认",
        ),
        "激进短线": (
            "Masimo指引、bioprocess订单转收入和Pall过滤订单披露可带来事件驱动",
            "低beta复利资产，不是高IV、高关注、直接AI订单型短线标的",
        ),
    }

    out: list[str] = [
        "# DHR 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：DHR / Danaher Corporation",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV主体为 `金融资料/每日金融数据/每日金融数据_2026-06-22.md`；DHR因未纳入该日度文件，价格/估值用2026-06-23补充快照；区间涨跌为2026-06-03；SOXX压力窗口为2026-06-04；DHR自身区间涨跌、IV和SOXX窗口缺失。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 DHR vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。DHR 的优势集中在下行保护、NTM经营兑现和质量型风险收益，而不是高右尾或激进短线。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是直接AI收入占比很小、Pall液冷/半导体过滤缺订单披露、正式动量/IV数据缺失。",
        "- A 最适合的投资者画像：偏稳健、重视复购耗材、诊断试剂、FCF、并购整合和bioprocessing周期修复的质量型配置者。",
        "- A 最不适合的投资者画像：只追求AI主链订单、非线性收入上修、高beta动量和短线资金爆发的进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:10]])}。这些公司通常具备更直接AI收入化、更硬订单/RPO/backlog、更高右尾或更强价格确认。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：DHR 是高质量中速复利资产，在防守与经营质量上靠前，但在全项目高增长/AI主链/动量资金口径下不是核心胜方。",
        "- 后续最重要跟踪数据：2026Q2 Masimo并表指引、Biotechnology core growth、bioprocess equipment orders转收入、consumables growth、Cepheid respiratory/non-respiratory test mix、Diagnostics China price impact、Life Sciences filtration/microelectronics demand、RPO、adjusted operating margin、FCF conversion和净杠杆。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "DHR"]),
        base.row(["公司名称", "Danaher Corporation"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`$26.6-$27.5B`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "Bioprocessing equipment orders能否转成2026H2-2027Q1收入并拉动后续高毛利耗材；Masimo能否并表后不稀释Diagnostics利润质量。"]),
        base.row(["最大反证", "Q1 core仅+0.5%、Cepheid respiratory弱、China diagnostics price压力、Life Sciences equipment低迷、Pall AI/DC过滤缺DHR-specific订单。"]),
        base.row(["近端催化剂", "Q2财报更新Masimo全年并表指引、bioprocess订单转收入、consumables强度、non-respiratory Cepheid、Pall microelectronics过滤需求。"]),
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
        base.row(["直接同业", "与DHR在生命科学工具、临床诊断、生物工艺耗材/服务和医疗工具平台高度重叠，优先看RPO、耗材复购、并购整合、margin和FCF。", "TMO", "同业证据权重最高；若TMO的RPO/规模更硬，DHR只能在估值或业务mix上反超。"]),
        base.row(["相邻替代", "同属材料、过滤、水处理、电子化学品、生命科学/工业工具或数据中心物理基础设施资金篮子，但产品不完全竞争。", "DD、ECL、PNR、DCI、ENTG、LIN、FTV、TDY", "重点比较增长质量、估值消化、下行保护和可见催化；DHR质量高不自动压过更高增长标的。"]),
        base.row(["上下游", "B处在DHR可服务或受同一AI capex驱动的半导体制造、先进封装、AI芯片、光互联、服务器、云/IDC或电力/机电链条。", "TSM、ASML、NVDA、AVGO、VRT、MSFT、AMZN", "不把下游AI capex直接映射为DHR收入；Pall过滤只按公司披露和订单证据加权。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "RKLB、TSLA、CRWD、CAT、MSI", "默认降低结论力度；除非档位差明显，否则优先微倾向或中性。"]),
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
                    comparison["classification"],
                    comparison["relationship"],
                    comparison["grade_diff"],
                    *[comparison[strat] for strat in STRATS],
                    comparison["majority"],
                    comparison["final_choice"],
                    comparison["key_reason"],
                ]
            )
        )

    out += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        out.append(base.row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy in STRATS if (base.tag_in_cell(str(comparison[strategy])) or "").endswith("投B")]
        need = "需要DHR披露Pall半导体/液冷过滤订单、Masimo EPS/EBITDA增厚、bioprocess订单持续转收入，并把core growth抬到高个位数。"
        if comparison["relationship"] == "直接同业":
            need = "需要DHR在bioprocess、diagnostics和Masimo整合上拿出比TMO更高的收入兑现、margin和FCF证据。"
        elif comparison["relationship"] == "上下游":
            need = "需要DHR证明其Pall过滤/诊断/生命科学工具能捕获下游AI或半导体利润池，而非仅小额间接受益。"
        elif comparison["relationship"] == "跨赛道":
            need = "需要DHR用更硬的利润/现金流兑现或订单催化抵消跨赛道公司的高增长和强动量。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["key_reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy in STRATS if (base.tag_in_cell(str(comparison[strategy])) or "").endswith("投A")]
        need = "需要B提高收入确认、利润/现金流质量或估值消化能力，或出现明确订单/指引上修。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要B把右尾叙事转成可确认收入和利润，并降低估值、波动或资产负债表反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["key_reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/半导体材料_化学品_基板/DHR_Danaher_Corporation_公司调研_2026-06-23.md`。",
        "- 关键行业资料：`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体高纯水、气体与化学流体系统_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_硅片、光刻胶与前道材料_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_高纯氟聚合物流体系统_2026-06-23.md`；`行业调研/AI园区电力_机电_冷却/行业调研_冷却液、水处理、过滤与制冷剂_2026-06-11.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md`；`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；DHR不在该日度文件内，已用2026-06-23补充价格/估值快照；DHR正式IV、区间涨跌和SOXX压力窗口仍按缺失/保守口径处理。缺少当日价格/估值/IV 的其他公司为 {('、'.join([x for x in missing_fin if x != TARGET]) if [x for x in missing_fin if x != TARGET] else '无')}。",
        f"- 公司 A 日度/补充数据摘录：{daily_snapshot}",
        "- 公司 A 补充行情来源：DHR公司调研文件中的2026-06-23补充行情记录，价格 `$178.19`、市值约 `$126.73B`、PE约`34.40`、EPS约`5.18`；该文件同时记录了2026-06-22最近收盘价`$178.19`。",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_dhr_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对DHR的Masimo并表、bioprocessing修复、Pall半导体/液冷过滤小期权、缺失正式日度行情字段做人工校准后建档。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "dhr_tiers": companies[TARGET]["tiers"],
        "dhr_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
        "dhr_ranks": companies[TARGET]["ranks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
