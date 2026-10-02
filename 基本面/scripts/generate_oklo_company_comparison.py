from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as project_calibration


TARGET = "OKLO"
TARGET_NAME = "Oklo Inc"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "OKLO_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_NUCLEAR_PEERS = {"SMR"}

ADJACENT_POWER_AND_NUCLEAR = {
    "AEP",
    "BE",
    "BWXT",
    "CEG",
    "CMI",
    "DTE",
    "ENS",
    "ENPH",
    "ETR",
    "FCEL",
    "FLNC",
    "GEV",
    "GNRC",
    "HTHIY",
    "PSIX",
    "PWR",
    "RYCEY",
    "VST",
    "AMPX",
    "ET",
    "ETN",
    "VRT",
    "POWL",
    "HUBB",
    "NVT",
    "ABBNY",
    "AEIS",
    "POWI",
    "VICR",
    "MOD",
    "AAON",
    "TT",
    "CARR",
    "JCI",
    "FIX",
    "EME",
    "MYRG",
    "IESC",
    "CAT",
    "CMI",
    "APD",
    "LIN",
}

AI_POWER_CUSTOMERS_AND_LOAD = {
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
    "DELL",
    "SMCI",
    "HPE",
    "JBL",
    "PENG",
    "FLEX",
    "FN",
    "SANM",
}

OKLO_SCORES = {
    "NTM兑现优先": 28.0,
    "右尾弹性优先": 91.5,
    "风险调整收益": 37.0,
    "下行保护优先": 25.0,
    "估值消化优先": 18.0,
    "近端催化优先": 72.0,
    "价格确认/动量": 58.0,
    "激进短线": 94.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def apply_score_floors(companies: dict[str, dict], floors: dict[str, dict[str, float]]) -> None:
    for ticker, strategy_floors in floors.items():
        company = companies.get(ticker)
        if not company:
            continue
        for strategy, floor in strategy_floors.items():
            current = company.setdefault("scores", {}).get(strategy, 0)
            company["scores"][strategy] = max(float(current), float(floor))


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
            "S": scored[max(0, int(total * 0.08) - 1)],
            "A": scored[max(0, int(total * 0.25) - 1)],
            "B": scored[max(0, int(total * 0.55) - 1)],
            "C": scored[max(0, int(total * 0.80) - 1)],
        }
        for company in companies.values():
            score = company.get("scores", {}).get(strategy)
            if score is None:
                tier = "资料不足"
                rank = None
            elif score >= cuts["S"]:
                tier = "S"
                rank = sum(1 for item in scored if item > score) + 1
            elif score >= cuts["A"]:
                tier = "A"
                rank = sum(1 for item in scored if item > score) + 1
            elif score >= cuts["B"]:
                tier = "B"
                rank = sum(1 for item in scored if item > score) + 1
            elif score >= cuts["C"]:
                tier = "C"
                rank = sum(1 for item in scored if item > score) + 1
            else:
                tier = "D"
                rank = sum(1 for item in scored if item > score) + 1
            company.setdefault("tiers", {})[strategy] = tier
            company.setdefault("ranks", {})[strategy] = rank
            company.setdefault("rank_total", {})[strategy] = total

    for company in companies.values():
        if not company.get("fin", {}).get("price"):
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company.setdefault("tiers", {})[strategy] = "资料不足"
                company.setdefault("ranks", {})[strategy] = None


def score_companies(companies: dict[str, dict]) -> None:
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    base.score_companies(companies)
    base.TARGET = old_target

    apply_score_floors(companies, getattr(project_calibration, "SCORE_FLOORS", {}))

    # OKLO must be treated as a long-duration advanced nuclear option, not as a
    # normal revenue comp. Formal evaluation supports very high right-tail and
    # aggressive-trading optionality, while NTM revenue, valuation digestion and
    # downside protection remain weak.
    target = companies[TARGET]
    for strategy, score in OKLO_SCORES.items():
        target.setdefault("scores", {})[strategy] = score

    recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_NUCLEAR_PEERS:
        return "直接同业"
    if ticker in AI_POWER_CUSTOMERS_AND_LOAD or category in {"云算力_IDC_AI软件平台", "AI服务器_存储_EMS"}:
        return "上下游"
    if ticker in ADJACENT_POWER_AND_NUCLEAR or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def label_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    at = a.get("tiers", {}).get(strategy, "资料不足")
    bt = b.get("tiers", {}).get(strategy, "资料不足")
    if at == "资料不足" or bt == "资料不足":
        if at == bt:
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    score_diff = float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0))
    tier_gap = tier_value(at) - tier_value(bt)
    abs_diff = abs(score_diff)
    if abs_diff < 4:
        return "中性"

    if rel == "直接同业":
        strong_cut, suggest_cut, micro_cut = 18, 8, 4
    elif rel in {"相邻替代", "上下游"}:
        strong_cut, suggest_cut, micro_cut = 22, 10, 4
    else:
        strong_cut, suggest_cut, micro_cut = 26, 12, 4

    if score_diff > 0:
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


def reason_for(strategy: str, winner: str, b: dict, rel: str) -> str:
    ticker = str(b["ticker"])
    category = str(b.get("category", ""))
    if winner == "A":
        return {
            "NTM兑现优先": "B兑现更弱，A现金厚但仍是小额收入",
            "右尾弹性优先": "A拥有Meta/Switch GW级先进核电期权",
            "风险调整收益": "A净现金厚可支撑远期执行",
            "下行保护优先": "B反证更重且A现金缓冲更厚",
            "估值消化优先": "B估值更难被业绩支撑",
            "近端催化优先": "A有DOE/NRC、Meta和ARMEC节点",
            "价格确认/动量": "A高关注度和核电主题仍被交易",
            "激进短线": "A高IV叠加先进核电叙事更适合进攻",
        }[strategy]

    if winner == "B":
        if rel == "直接同业":
            return {
                "NTM兑现优先": "B已有更可见收入路径",
                "右尾弹性优先": "B同业核电右尾不弱于A",
                "风险调整收益": "B同业赔率更均衡",
                "下行保护优先": "B同业估值或压力期反证更轻",
                "估值消化优先": "B同业收入基数更能支撑估值",
                "近端催化优先": "B同业监管/客户节点更可验证",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业短线弹性不弱且基数更低",
            }[strategy]
        if category in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链订单/收入兑现更短链",
                "右尾弹性优先": "B AI主链右尾可收入化更直接",
                "风险调整收益": "B上行下行组合优于A长周期执行",
                "下行保护优先": "B现金流或需求能见度更好",
                "估值消化优先": "B高增长更能消化估值",
                "近端催化优先": "B产品/订单/财报催化更近",
                "价格确认/动量": "B价格确认和资金偏好更强",
                "激进短线": "B AI高beta交易更顺",
            }[strategy]
        if category in INFRA_CATS:
            return {
                "NTM兑现优先": "B订单、backlog或交付更快收入化",
                "右尾弹性优先": "B电力设备放量右尾更近",
                "风险调整收益": "B增长、现金流和估值组合更优",
                "下行保护优先": "B现金流/估值/压力期更稳",
                "估值消化优先": "B用NTM业绩消化估值更容易",
                "近端催化优先": "B订单/产能/财报节点更近",
                "价格确认/动量": "B趋势确认强于A",
                "激进短线": "B短线弹性更易被业绩验证",
            }[strategy]
        return {
            "NTM兑现优先": "B未来12个月兑现证据更直接",
            "右尾弹性优先": f"{ticker}右尾更可验证或更大",
            "风险调整收益": "B上行和下行组合更好",
            "下行保护优先": "B资产质量、现金流或估值缓冲更好",
            "估值消化优先": "B当前估值更容易被业绩消化",
            "近端催化优先": "B未来两个季度催化更明确",
            "价格确认/动量": "B价格行为更强",
            "激进短线": "B短线关注度或爆发力更强",
        }[strategy]

    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    return {
        "NTM兑现优先": "NTM证据差距不够强",
        "右尾弹性优先": "右尾证据互有强弱",
        "风险调整收益": "赔率和风险接近",
        "下行保护优先": "防守证据接近",
        "估值消化优先": "估值消化均有压力",
        "近端催化优先": "近端催化强度接近",
        "价格确认/动量": "价格确认差距有限",
        "激进短线": "短线弹性差距有限",
    }[strategy]


def cell_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    label = label_for(strategy, a, b, rel)
    winner = "A" if "投A" in label else "B" if "投B" in label else "中性"
    return f"{label}：{reason_for(strategy, winner, b, rel)}"


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in row_obj[strategy])
    b_count = sum(1 for strategy in STRATS if "投B" in row_obj[strategy])
    return a_count, b_count, 8 - a_count - b_count


def final_choice(row_obj: dict) -> str:
    weights = {
        "NTM兑现优先": 1.15,
        "风险调整收益": 1.15,
        "估值消化优先": 1.05,
        "下行保护优先": 0.95,
        "右尾弹性优先": 0.90,
        "近端催化优先": 0.80,
        "价格确认/动量": 0.45,
        "激进短线": 0.55,
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
        label = base.tag_in_cell(row_obj[strategy])
        score += weights[strategy] * label_score.get(label, 0.0)
    return "A" if score > 0.15 else "B" if score < -0.15 else "中性"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong = [s for s in STRATS if tier_value(a.get("tiers", {}).get(s)) > tier_value(b.get("tiers", {}).get(s))]
    b_strong = [s for s in STRATS if tier_value(a.get("tiers", {}).get(s)) < tier_value(b.get("tiers", {}).get(s))]
    close = [s for s in STRATS if tier_value(a.get("tiers", {}).get(s)) == tier_value(b.get("tiers", {}).get(s))]

    def short(items: list[str]) -> str:
        return "、".join([item.replace("优先", "").replace("/动量", "动量") for item in items[:3]]) if items else "无"

    return f"A强:{short(a_strong)}；B强:{short(b_strong)}；接近:{short(close)}"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    if choice == "中性":
        return "两家公司风格差异较大，A的远期核电期权与B的经营证据没有拉开强判差距。"
    diffs = {strategy: float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0)) for strategy in STRATS}
    if choice == "A":
        if diffs["右尾弹性优先"] > 18:
            return "OKLO 的Meta/Switch等GW级先进核电期权和小收入基数带来更大非线性右尾。"
        if diffs["激进短线"] > 16:
            return "OKLO 的高IV、先进核电叙事和监管/客户节点更适合激进短线进攻。"
        if diffs["近端催化优先"] > 12:
            return "OKLO 的DOE/NRC、Meta预付款/开发节点、ARMEC/同位素进展更可能触发重定价。"
        return "OKLO 在该对比中主要靠远期期权和主题弹性胜出，而不是靠NTM财务质量。"

    if diffs["NTM兑现优先"] < -14:
        return f"{b['ticker']} 的NTM收入、利润、订单或交付证据比OKLO更短链、更可兑现。"
    if diffs["估值消化优先"] < -12:
        return f"{b['ticker']} 有收入/利润基础支撑估值，OKLO无商业售电且PS缺失。"
    if diffs["下行保护优先"] < -12:
        return f"{b['ticker']} 的现金流、估值缓冲或压力窗口表现明显优于OKLO。"
    if diffs["风险调整收益"] < -12:
        return f"{b['ticker']} 的上行和下行组合更均衡，OKLO执行链和估值反证更重。"
    if diffs["价格确认/动量"] < -14:
        return f"{b['ticker']} 的价格确认和资金偏好更强，OKLO压力期跌幅反证较大。"
    return f"{b['ticker']} 在多数投资思路下的增长质量、兑现确定性或估值组合更适合当前配置。"


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
        choice = final_choice(row_obj)
        row_obj["final_choice"] = choice
        row_obj["key_reason"] = key_reason(a, b, row_obj, choice)
        rows.append(row_obj)

    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return sorted(rows, key=lambda item: (rel_order.get(item["relationship"], 9), item["ticker"]))


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


def top_majority(rows: list[dict], final: str, limit: int = 40) -> list[dict]:
    selected = [row for row in rows if row["final_choice"] == final]
    if final == "B":
        selected.sort(key=lambda row: (row["bc"] - row["ac"], row["bc"], -row["nc"]), reverse=True)
    else:
        selected.sort(key=lambda row: (row["ac"] - row["bc"], row["ac"], -row["nc"]), reverse=True)
    return [row for row in selected if abs(row["ac"] - row["bc"]) >= 3][:limit]


def winning_strats(row_obj: dict, side: str) -> str:
    token = f"投{side}"
    wins = [strategy for strategy in STRATS if token in row_obj[strategy]]
    return "、".join(wins) if wins else "无"


def render_report(companies: dict[str, dict], rows: list[dict]) -> str:
    a = companies[TARGET]
    total = len(companies)
    dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(dates)} 至 {max(dates)}"
    stats = {strategy: Counter() for strategy in STRATS}
    for row_obj in rows:
        for strategy in STRATS:
            stats[strategy][base.tag_in_cell(row_obj[strategy])] += 1

    a_side = {strategy: sum(stats[strategy][label] for label in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][label] for label in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy], reverse=True)[:2]
    a_worst = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy])[:3]
    strong_b = top_majority(rows, "B")
    strong_a = top_majority(rows, "A")
    final_a = sum(1 for row_obj in rows if row_obj["final_choice"] == "A")
    final_b = sum(1 for row_obj in rows if row_obj["final_choice"] == "B")
    final_n = sum(1 for row_obj in rows if row_obj["final_choice"] == "中性")
    missing_fin = [ticker for ticker in sorted(companies) if not companies[ticker].get("fin", {}).get("price")]
    product_names = [str(item[0]).split("：")[0] for item in a.get("products", [])[:6]]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])

    rank_text = {}
    for strategy in STRATS:
        rank = a.get("ranks", {}).get(strategy)
        tier = a.get("tiers", {}).get(strategy)
        rank_text[strategy] = f"第 {rank}/{total}，{tier} 档" if rank else f"{tier} 档"

    support = {
        "NTM兑现优先": ("现金/证券 $2.537B，可支撑开发，ARMEC/同位素可能小额收入", "2026Q1商业电力收入0，基准NTM仅$5-25M且亏损"),
        "右尾弹性优先": ("Meta 1.2GW、Switch 12GW、Equinix等pipeline使远期PPA右尾极大", "多数项目未转binding PPA/COD，收入时间主要在2030+"),
        "风险调整收益": ("净现金厚、监管节点推进、客户质量改善远期赔率", "估值约$10B、无售电、FOAK/燃料/融资执行链长"),
        "下行保护优先": ("资产负债表现金缓冲强，债务压力低", "Call IV 90.5%，三段SOXX压力累计-122.49%，亏损且无收入"),
        "估值消化优先": ("若开发款/同位素/ARMEC同步落地可边际缓解估值压力", "PS缺失、Forward EPS为负，当前估值需乐观远期兑现"),
        "近端催化优先": ("DOE PDSA、NRC PDC、Meta开发资金、ARMEC/Atomic Alchemy均可跟踪", "催化多提升可信度，未必进入NTM revenue或利润"),
        "价格确认/动量": ("2026-06-22仍维持高关注度和高IV，短窗两周+4.20%", "2026-06-03一月-7.37%，压力期表现极弱"),
        "激进短线": ("高IV、Sam Altman关联、先进核电/AI电力叙事适合高beta交易", "交易弹性来自叙事和事件，不来自NTM盈利兑现"),
    }

    fin = a.get("fin", {})
    mom2 = a.get("mom2", {})
    mom1 = a.get("mom1", {})
    soxx = a.get("soxx", {})
    a_fin_text = (
        f"2026-06-22 收盘价 `{fmt_num(fin.get('price'), 2)}`，市值 `{fmt_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `{fin.get('ttm_pe') or '不适用'}`，Forward PE `{fin.get('forward_pe') or '不适用'}`，"
        f"P/S `{fin.get('ps') or '缺失'}`，Call IV `{fmt_pct(fin.get('call_iv'))}`，Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03 过去两周 `{fmt_pct(mom2.get('mom2w'))}`、过去一月 `{fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04 三段 SOXX 压力窗口累计 `{fmt_pct(soxx.get('soxx_cum'))}`。"
    )

    out: list[str] = []
    out += [
        "# OKLO 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：OKLO / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{total}",
        f"被比较公司 B 数量：{total - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 OKLO vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、项目根 `tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。OKLO 的优势集中在先进核电、AI 数据中心 24/7 clean power、Meta/Switch/Equinix pipeline 和高波动交易弹性。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。核心短板是 NTM 商业电力收入为 0、基准收入只有小额 ARMEC/同位素/开发收入可能、经营亏损和估值消化压力大。",
        "- A 最适合的投资者画像：愿意用高波动和远期执行风险换取先进核电/AI电力非线性期权的进攻型资金，特别重视监管、客户预付款和首堆节点。",
        "- A 最不适合的投资者画像：要求未来 12 个月收入利润兑现、低估值安全边际、稳健现金流、低 IV 或压力期防守的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([row['ticker'] for row in strong_b[:12]])}。这些公司通常在 NTM 兑现、估值消化、现金流、压力期表现或 AI 主链收入化上明显强于 OKLO。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：OKLO 对 {final_a}/{len(rows)} 家公司多数思路占优，对 {final_b}/{len(rows)} 家公司多数思路落后，中性 {final_n} 家；它是全项目右尾/短线顶档之一，但不是综合质量或风险调整收益顶档。",
        "- 后续最重要跟踪数据：10-Q revenue、contract liabilities、restricted cash/customer deposits、OCF/CapEx；Meta Ohio 预付款金额和会计处理；Aurora-INL DSA/readiness/startup；A3F/燃料授权；Atomic Alchemy off-take；ARMEC 外部收入和毛利。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "OKLO"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "电力_发电_能源_储能")]),
        base.row(["重要产品/业务线", "；".join(product_names) if product_names else "Aurora powerhouses/PPA售电；Aurora-INL首堆；Meta/Switch/Equinix pipeline；燃料制造与回收；Atomic Alchemy同位素；ARMEC核制造"]),
        base.row(["NTM 基准收入", a.get("base_rev") or "$5M-$25M"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev') or '$25M-$75M'}；极度乐观：{a.get('extreme_rev') or '$75M-$200M'}"]),
        base.row(["利润和现金流结论", f"基准经营利润率/利润：{a.get('base_margin') or '经营亏损约-$190M至-$280M'}；{a.get('base_profit') or '净亏损约-$110M至-$210M'}；{a.get('base_cash') or 'FCF大概率为负，客户预付款/政府资金可缓冲'}"]),
        base.row(["最大传导瓶颈", "从GW级客户需求到NTM收入之间缺少binding PPA、可确认交付、燃料授权、项目融资、NTP、startup/COD和收入确认节点。"]),
        base.row(["最大反证", "2026Q1商业电力收入为0、Forward EPS为负、PS缺失，且SOXX压力窗口累计跌幅-122.49%。"]),
        base.row(["近端催化剂", "Aurora-INL DOE/NRC后续文件、Meta Ohio预付款/开发资金、客户转binding、燃料路径、Atomic Alchemy销售、ARMEC并表收入。"]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        out.append(base.row([strategy, a["tiers"][strategy], rank_text[strategy], support[strategy][0], support[strategy][1]]))

    out += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "先进核电/SMR开发公司或核能新建项目商业模式高度接近，优先比较许可、首堆、客户、融资、燃料和收入确认。", "SMR", "同业证据可放大判断力度；但若双方均pre-revenue，估值和现金流反证必须保守处理。"]),
        base.row(["相邻替代", "同属AI电力、核能、燃气/燃料电池、电气设备、工程和电网建设资金篮子。", "CEG、VST、BE、GEV、BWXT、ETN、VRT、POWL、PWR", "重点回答资金只能买一个时，谁的增长质量、收入化速度、估值消化和催化更好。"]),
        base.row(["上下游", "云厂、NeoCloud、IDC、服务器和AI负荷需求端，或燃料/utility供给端。", "META、MSFT、AMZN、GOOGL、ORCL、EQIX、DLR、CRWV、APLD、IREN", "不把下游收入规模直接等同于更好；关键是OKLO能否把负荷需求转为PPA、预付款和COD。"]),
        base.row(["跨赛道", "半导体、设备、材料、软件和工业品等与OKLO业务差异大，但作为组合资金替代仍可比较。", "NVDA、AVGO、TSM、ASML、MU、CDNS、LIN、TMO", "默认降低结论力度；除非增长质量、估值消化或风险收益明显拉开。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]

    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要", *STRATS, "多数思路方向", "最终更值得投", "最关键理由"]
    out.append(base.row(headers))
    out.append(base.row(["---:", "---", "---", "---", "---", *["---"] * 8, "---", "---", "---"]))
    for index, row_obj in enumerate(rows, start=1):
        out.append(
            base.row(
                [
                    index,
                    f"{row_obj['ticker']} / {row_obj['name']}",
                    row_obj["classification"],
                    row_obj["relationship"],
                    row_obj["grade_diff"],
                    *[row_obj[strategy] for strategy in STRATS],
                    row_obj["majority"],
                    row_obj["final_choice"],
                    row_obj["key_reason"],
                ]
            )
        )

    out += [
        "",
        "## 6. 投资思路统计",
        "",
        base.row(["投资思路", *TAG_ORDER, "A侧合计", "B侧合计"]),
        base.row(["---", *["---:"] * 9]),
    ]
    for strategy in STRATS:
        out.append(base.row([strategy, *[stats[strategy][label] for label in TAG_ORDER], a_side[strategy], b_side[strategy]]))

    out += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(strong_b, start=1):
        need = "OKLO需要把客户pipeline转为binding PPA/预付款/NTP，并在10-Q里看到收入、合同负债、OCF或CapEx节奏改善。"
        if row_obj["relationship"] == "跨赛道":
            need = "OKLO需要用更硬的监管、客户、燃料和收入确认证据证明右尾足以补偿跨赛道经营质量差距。"
        out.append(base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", winning_strats(row_obj, "B"), row_obj["key_reason"], need]))

    out += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(strong_a, start=1):
        need = "B需要拿出更大右尾、明确客户/订单/收入上修，或用更强动量和催化压过OKLO的先进核电期权。"
        if row_obj["relationship"] == "直接同业":
            need = "B需要证明其许可、首堆、燃料、客户和融资链条比OKLO更快闭环。"
        out.append(base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", winning_strats(row_obj, "A"), row_obj["key_reason"], need]))

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",
        f"- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；本次共 {total} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`分析报告/公司排序/`、`分析报告/简单排序/`、项目根 `tmp/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {total - len(missing_fin)}/{total} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{a_fin_text}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/电力_发电_能源_储能/OKLO_Oklo Inc_公司调研_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_oklo_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对 OKLO 的 pre-revenue、净现金、先进核电客户 pipeline、监管节点、高IV、高压力期回撤和估值消化压力做人工校准后建档；未读取下游量化目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    base.TARGET = TARGET
    base.OUT_PATH = OUT_PATH
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("OKLO not found in formal company evaluation universe")
    score_companies(companies)
    rows = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = render_report(companies, rows)
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "target": TARGET,
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(rows),
                "size": OUT_PATH.stat().st_size,
                "tiers": companies[TARGET]["tiers"],
                "scores": {strategy: round(companies[TARGET]["scores"][strategy], 2) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
