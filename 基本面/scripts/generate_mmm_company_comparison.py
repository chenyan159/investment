from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base


TARGET = "MMM"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MMM_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_MATERIAL_PEERS = {
    "ASGLY",
    "CC",
    "DD",
    "ECL",
    "ENTG",
    "MTRN",
    "Q",
    "ROG",
    "SHECY",
}

ADJACENT_MATERIAL_AND_INDUSTRIAL = {
    "AJNMY",
    "APD",
    "AXTI",
    "CARR",
    "DCI",
    "DHR",
    "DKILY",
    "DOV",
    "FTV",
    "HOCPY",
    "JCI",
    "LIN",
    "MOD",
    "MRAAY",
    "NDSN",
    "PH",
    "PNR",
    "SMTOY",
    "SOMMY",
    "TMO",
    "TT",
}

SEMI_AND_AI_DOWNSTREAM_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "云算力_IDC_AI软件平台",
    "封测_检测_计量_光罩",
    "晶圆制造_前道设备",
}


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for strategy in STRATS:
        ordered = sorted(
            companies.items(),
            key=lambda item: item[1].setdefault("scores", {}).get(strategy, 0),  # type: ignore[union-attr]
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

    for company in companies.values():
        if not company.get("fin") or not company["fin"].get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    base.score_companies(companies)

    # 3M is a cash-flow and legal-overhang repair story with small but real
    # AI/DC materials optionality. The raw parser over-promotes downside and
    # right-tail because it counts mature cash flow and EBO mentions too heavily.
    overrides = {
        "NTM兑现优先": 61.2,
        "右尾弹性优先": 41.5,
        "风险调整收益": 51.8,
        "下行保护优先": 84.0,
        "估值消化优先": 58.2,
        "近端催化优先": 59.0,
        "价格确认/动量": 44.2,
        "激进短线": 63.0,
    }
    for strategy, score in overrides.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score  # type: ignore[index]
    recompute_tiers(companies)


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_MATERIAL_PEERS:
        return "直接同业"
    if ticker in ADJACENT_MATERIAL_AND_INDUSTRIAL or category == "半导体材料_化学品_基板":
        return "相邻替代"
    if category in SEMI_AND_AI_DOWNSTREAM_CATS:
        return "上下游"
    if category in INFRA_CATS:
        return "上下游"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict[str, object], diff: float, rel: str) -> str:
    ticker = str(company["ticker"])
    cat = str(company.get("category", ""))
    if winner == "A":
        return {
            "NTM兑现优先": "A有FY2026指引、orders和backlog转收入锚",
            "右尾弹性优先": "A有EBO和DC电气材料小右尾",
            "风险调整收益": "A现金流、17x FwdPE和业务分散更均衡",
            "下行保护优先": "A现金流和多元工业底盘更稳",
            "估值消化优先": "A EPS/OCF路径较易消化估值",
            "近端催化优先": "A有Q2-Q3 backlog、EBO和DC power验证",
            "价格确认/动量": "A估值修复和一月价格确认略好",
            "激进短线": "A修复交易叠加EBO新闻流略优",
        }[strat]
    if winner == "B":
        if ticker in DIRECT_MATERIAL_PEERS:
            return {
                "NTM兑现优先": "B同业产品级收入或订单更清楚",
                "右尾弹性优先": "B同业电子材料/水处理右尾更集中",
                "风险调整收益": "B同业风险收益组合更优",
                "下行保护优先": "B同业压力期或现金流缓冲更好",
                "估值消化优先": "B同业增长更能覆盖估值",
                "近端催化优先": "B同业订单/分拆/产品催化更近",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业弹性和资金关注更强",
            }[strat]
        if cat in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链收入兑现更短链",
                "右尾弹性优先": "B直接AI右尾和小基数更大",
                "风险调整收益": "B上行空间更能覆盖风险",
                "下行保护优先": "B需求能见度或现金流韧性更好",
                "估值消化优先": "B高速增长更能消化估值",
                "近端催化优先": "B产品/RPO/订单催化更密集",
                "价格确认/动量": "B价格确认和资金偏好更强",
                "激进短线": "B高beta和AI叙事更适合进攻",
            }[strat]
        if cat in INFRA_CATS:
            return {
                "NTM兑现优先": "B AI电力/机电订单兑现更直接",
                "右尾弹性优先": "B AI电力/机电右尾更大",
                "风险调整收益": "B增长和估值组合更优",
                "下行保护优先": "B订单粘性或公用属性更强",
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
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strat in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "质量、估值和兑现接近"
    return "档位接近需再验证"


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
        strong_cut, suggest_cut, micro_cut = 24, 11, 4
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
    return f"{label}：{reason_for(strat, winner, b, diff, rel)}"


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
    if score > 0.15:
        return "A"
    if score < -0.15:
        return "B"

    a = row_obj["_a"]  # type: ignore[index]
    b = row_obj["b"]  # type: ignore[index]
    quality_tie_break = (
        a["scores"]["风险调整收益"]
        + a["scores"]["估值消化优先"]
        + a["scores"]["NTM兑现优先"] * 0.7
        + a["scores"]["下行保护优先"] * 0.7
        - b["scores"]["风险调整收益"]
        - b["scores"]["估值消化优先"]
        - b["scores"]["NTM兑现优先"] * 0.7
        - b["scores"]["下行保护优先"] * 0.7
    )
    return "A" if quality_tie_break >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], choice: str) -> str:
    diffs = {strat: a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0) for strat in STRATS}  # type: ignore[union-attr]
    if choice == "A":
        if diffs["下行保护优先"] > 12:
            return "MMM现金流、多元工业材料底盘和17x Forward PE比B更适合防守配置。"
        if diffs["NTM兑现优先"] > 10:
            return "MMM有FY2026指引、orders/backlog和现金流支撑，B的NTM兑现更弱。"
        if diffs["估值消化优先"] > 10:
            return "MMM用EPS和OCF消化估值的路径比B更清楚。"
        return "MMM在质量、现金流和估值消化上略胜，B的成长证据不足以覆盖反证。"
    if diffs["右尾弹性优先"] < -18:
        return f"{b['ticker']}的直接AI收入、小基数或平台型右尾明显强于MMM。"
    if diffs["NTM兑现优先"] < -14:
        return f"{b['ticker']}的订单/RPO/backlog或收入确认证据比MMM更硬。"
    if diffs["估值消化优先"] < -12:
        return f"{b['ticker']}的增长和估值匹配度优于MMM。"
    if diffs["价格确认/动量"] < -14:
        return f"{b['ticker']}的价格确认和资金偏好明显强于MMM。"
    return f"{b['ticker']}在多数投资思路下比MMM更符合项目内资金配置目标。"


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
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        row_obj: dict[str, object] = {
            "_a": a,
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
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]

    product_names: list[str] = []
    for product in a["products"]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])
        if len(product_names) >= 7:
            break

    daily_snapshot = (
        f"2026-06-22 收盘价 `{fmt_num(fin.get('price'), 2)}`，市值 `{fmt_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `{fmt_num(fin.get('ttm_pe'))}`，Forward PE `{fmt_num(fin.get('forward_pe'))}`，"
        f"P/S `{fmt_num(fin.get('ps'))}`，EV/EBITDA `{fmt_num(fin.get('ev_ebitda'))}`；"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`、Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03 两周/一月涨跌 `{fmt_pct(mom2.get('mom2w'))}`/`{fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04 SOXX三段压力窗口累计 `{fmt_pct(soxx.get('soxx_cum'))}`。"
    )

    support = {
        "NTM兑现优先": (
            "FY2026 adjusted sales约+4%、organic约+3%、EPS `8.50-8.70`，Q1 orders low-double-digits且backlog YoY `+20%`",
            "公司级基准收入仅`+1.5%-+4.0%`，AI/DC小业务不足以显著抬升整体收入斜率",
        ),
        "右尾弹性优先": (
            "EBO已full-rate production、inside DC约`$0.1B`年化、EBO产能more than double，DC power约`$0.5B`年化",
            "严格DC收入约2%-3%，EBO客户/订单/ASP未披露；极度乐观需多环节同时突破",
        ),
        "风险调整收益": (
            "Forward PE约`17.23x`、OCF指引`$5.6-$5.8B`、S&I margin 25%+，叠加法律折价修复空间",
            "PFAS/法律现金流、总负债和低增长限制赔率，SOXX压力期表现并不强",
        ),
        "下行保护优先": (
            "多元工业材料、消费品、S&I现金流和回购能力提供底盘，估值不按AI高倍数定价",
            "三段SOXX压力窗口累计`-28.62%`、IV约40%、权益薄和法律负债使其不能进顶级防守档",
        ),
        "估值消化优先": (
            "Forward PE约`17.23x`，若EPS和OCF兑现，估值可由低个位数收入+margin扩张消化",
            "P/S `3.40x`、EV/EBITDA `14.60x`对低增长工业材料不算便宜，需backlog和margin兑现",
        ),
        "近端催化优先": (
            "Q2-Q3可验证orders/backlog转收入、T&E semiconductor/data center、EBO扩产/验证和DC power披露",
            "缺少AI硬件链式大额订单/RPO，EBO扩产主要到2027-01，近端重估力度有限",
        ),
        "价格确认/动量": (
            "2026-06-03一月涨跌`+6.42%`，2026-06-22价格较早期快照继续上移，修复交易有确认",
            "两周涨跌仅`+1.25%`，SOXX压力期回撤大，动量弱于AI主链高beta公司",
        ),
        "激进短线": (
            "EBO、DC power、PFAS折价修复和回购可带来事件交易",
            "大盘工业材料公司，AI/DC收入占比小，短线beta和资金关注弱于AI芯片、光互联、NeoCloud",
        ),
    }

    out: list[str] = [
        "# MMM 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：MMM / 3M",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 `金融资料/每日金融数据/每日金融数据_2026-06-22.md`；区间涨跌为 2026-06-03；SOXX 压力窗口为 2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 MMM vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。MMM 的 AI/DC 暴露按“小比例但真实”的材料和连接件期权处理，不把客户总 capex 直接映射为3M收入。",
    ]
    if missing_fin:
        out.append(
            f"> 金融资料覆盖差异：正式评估公司 {n} 家，2026-06-22 金融快照覆盖 {n - len(missing_fin)} 家；缺少日度金融明细的公司为 {', '.join(missing_fin)}，价格/估值/IV/动量相关档位按资料不足或低置信处理。"
        )
    out += [
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。MMM 的相对优势集中在下行保护、估值消化、风险调整收益和部分 NTM 兑现；核心来自 2026 指引、Q1 orders/backlog、S&I 高利润率、OCF 和法律/PFAS 折价修复。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 AI/DC 收入占比小、EBO仍缺客户/订单/ASP披露、公司级收入增速低、短线 beta 和价格确认弱于AI主链。",
        "- A 最适合的投资者画像：希望买多元工业材料修复、现金流、回购、法律不确定性下降，同时保留小比例 EBO/DC power/半导体材料期权的稳健配置者。",
        "- A 最不适合的投资者画像：只追求AI芯片、光互联、NeoCloud、电力设备那种高增长大右尾、强订单催化和高beta短线爆发的进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]])}。这些公司通常拥有更直接的AI收入化、更硬订单/RPO/backlog、更强价格确认或更大右尾。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：MMM 对 {sum(1 for x in comparisons if x['final_choice'] == 'A')}/{len(comparisons)} 家公司最终占优，对 {sum(1 for x in comparisons if x['final_choice'] == 'B')}/{len(comparisons)} 家公司落后；它是中上质量的工业材料修复股，不是项目内高增长核心。",
        "- 后续最重要跟踪数据：Q2-Q3 orders/backlog转收入、T&E semiconductor/data center增速、EBO客户validation/订单/ASP、data center power revenue是否继续披露、S&I margin、Consumer organic、PFAS/法律现金支付、inventory、adjusted FCF conversion和回购节奏。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "MMM"]),
        base.row(["公司名称", "3M"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`254-260亿美元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "3M不是GPU、光模块、变压器或EPC主承包商；AI/DC需求需经过客户规格、认证、渠道和施工窗口，再通过orders/backlog转收入。"]),
        base.row(["最大反证", "Consumer/auto/consumer electronics弱、PFAS/法律现金支付、tariff/input cost、EBO客户/订单未披露、SOXX压力期表现弱。"]),
        base.row(["近端催化剂", "Q2-Q3 orders/backlog、T&E semiconductor/data center、EBO validation/产能进度、data center power收入、S&I margin和FCF conversion。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        "建档口径：对同一批 189 家正式评估公司，抽取基准/乐观/极度乐观 NTM 收入增速、经营利润率、FCF/可信度/瓶颈、估值、IV、区间涨跌和 SOXX 压力窗口表现。每个投资思路独立排序，`S` 约为前 7%，`A` 约为 7%-25%，`B` 约为 25%-55%，`C` 约为 55%-85%，`D` 为后 15%；关键日度数据缺失时降权，不因对方资料不足给强烈建议。",
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
        base.row(["直接同业", "与MMM在特种材料、电子材料、电气材料、工业化学品、水/表面处理或高可靠工程材料上有较高重叠，优先比较产品级收入、订单、margin、法律尾部和估值。", "DD、Q、ECL、ENTG、ROG、SHECY", "同业证据权重最高；若B有更直接电子材料或水处理收入，MMM的AI/DC右尾需降权。"]),
        base.row(["相邻替代", "同属半导体材料、工业气体、过滤、水处理、生命科学/工业材料或数据中心物理材料资金篮子，但产品不完全竞争。", "APD、LIN、DHR、TMO、PNR、TT、DOV", "重点比较增长质量、估值消化、下行保护和可见催化；不因MMM现金流好就忽略增长差距。"]),
        base.row(["上下游", "B是MMM服务或受同一AI capex驱动的半导体制造、先进封装、AI芯片、光互联、服务器、云/IDC、电力/机电链条。", "NVDA、TSM、AVGO、AMAT、VRT、ETN、MSFT、AMZN", "不把下游AI capex直接映射为MMM收入；也不把材料上游自动等同更好，核心看利润捕获和订单。"]),
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
        need = "需要MMM把EBO/DC power/半导体材料转成可披露订单、收入和margin上修，并降低PFAS/法律现金流和压力期回撤反证。"
        if comparison["relationship"] == "直接同业":
            need = "需要MMM在材料同业中拿出更高收入增速、产品级订单、margin和现金流证据，并证明EBO/DC材料不是小额期权。"
        elif comparison["relationship"] == "上下游":
            need = "需要MMM证明其电气材料、EBO、TIM和电子材料能捕获下游AI利润池，而非仅小额间接受益。"
        elif comparison["relationship"] == "跨赛道":
            need = "需要MMM用更硬的利润/现金流兑现或订单催化抵消跨赛道公司的高增长和强动量。"
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
        "- 公司 A 公司调研文件：`公司调研/半导体材料_化学品_基板/MMM_3M_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_高速连接器、背板与结构化布线_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_AEC、DAC与高速铜缆_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_先进封装材料与热界面材料_2026-06-10.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装湿化学与表面处理材料_2026-06-11.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_mmm_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对 MMM 的多元工业材料底盘、EBO/DC power 小比例右尾、PFAS/法律现金流、SOXX压力窗口和近端Q2-Q3验证做人工校准后建档；未读取下游量化目录或现成排序结论。",
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
        "mmm_tiers": companies[TARGET]["tiers"],
        "mmm_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
        "mmm_ranks": companies[TARGET]["ranks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
