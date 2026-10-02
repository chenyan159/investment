from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "FLNC"
TARGET_NAME = "Fluence Energy"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "FLNC_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_STORAGE_PEERS = {
    "ENPH",  # residential solar + battery energy systems
    "GNRC",  # backup power / storage / home energy systems
    "TSLA",  # Megapack / storage inside a larger company
}

UPSTREAM_DOWNSTREAM = {
    "AEP",
    "APD",
    "CEG",
    "DTE",
    "ET",
    "ETR",
    "LIN",
    "VST",
    "AMZN",
    "MSFT",
    "GOOGL",
    "META",
    "ORCL",
    "BABA",
    "IBM",
    "EQIX",
    "DLR",
    "CRWV",
    "APLD",
    "IREN",
    "NBIS",
    "NTNX",
    "DELL",
    "SMCI",
    "HPE",
    "JBL",
    "FLEX",
    "PENG",
    "SANM",
    "FN",
    "AMPX",  # battery cell supplier exposure
    "ENS",  # batteries / backup power adjacent upstream
}

POWER_ADJACENT = {
    "ABBNY",
    "AEIS",
    "AAON",
    "ATKR",
    "BE",
    "BWXT",
    "CARR",
    "CAT",
    "CMI",
    "DKILY",
    "DOV",
    "EME",
    "FCEL",
    "FIX",
    "GEV",
    "HTHIY",
    "HUBB",
    "IESC",
    "JCI",
    "MIELY",
    "MOD",
    "MRAAY",
    "MYRG",
    "NVT",
    "OKLO",
    "PH",
    "PNR",
    "POWI",
    "POWL",
    "PSIX",
    "PWR",
    "RYCEY",
    "SMR",
    "TT",
    "TTDKY",
    "VICR",
    "VRT",
}

POWER_ELECTRONICS_ADJACENT = {
    "AOSL",
    "DIOD",
    "ETN",
    "IFNNY",
    "LFUS",
    "MCHP",
    "MPWR",
    "NVTS",
    "ON",
    "ST",
    "STM",
    "TXN",
    "VSH",
    "WOLF",
}

FLNC_SCORES = {
    # Strong backlog / FY2026 guide / +43%-59% NTM baseline, but H2 delivery
    # intensity, low gross margin and negative FCF keep it below the best
    # quality compounders.
    "NTM兑现优先": 70.0,
    # AI data-center BESS, Smartstack, 41.3GW/147GWh pipeline and hyperscaler
    # MSAs provide real upside, but PO / GWh / margin evidence is not yet hard.
    "右尾弹性优先": 84.0,
    # High upside is offset by negative TTM EPS, high IV, working capital drag
    # and very weak pressure-window behavior.
    "风险调整收益": 44.0,
    "下行保护优先": 32.0,
    # P/S is optically low, but forward PE is high and EBITDA/cash conversion is
    # not yet proven, so valuation digestion is only mid-pack.
    "估值消化优先": 52.0,
    "近端催化优先": 74.0,
    "价格确认/动量": 95.0,
    "激进短线": 88.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict]) -> None:
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    calibrated.score_companies(companies)
    base.TARGET = old_target

    for strat, score in FLNC_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strat] = score
    calibrated.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    if ticker in DIRECT_STORAGE_PEERS:
        return "直接同业"
    if ticker in UPSTREAM_DOWNSTREAM:
        return "上下游"
    if ticker in POWER_ADJACENT or ticker in POWER_ELECTRONICS_ADJACENT:
        return "相邻替代"
    if category in {"电力_发电_能源_储能", "配电_电源_功率器件"}:
        return "相邻替代"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict, rel: str, diff: float) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    if winner == "A":
        return {
            "NTM兑现优先": "A有FY2026指引和56亿美元backlog锚",
            "右尾弹性优先": "A有AI数据中心BESS与Smartstack期权",
            "风险调整收益": "A增长上行可部分覆盖执行风险",
            "下行保护优先": "A若对手更弱才凭backlog胜出",
            "估值消化优先": "A低P/S叠加收入高增可部分消化",
            "近端催化优先": "A有Q3首单、H2交付和毛利验证",
            "价格确认/动量": "A一月翻倍且价格守住涨幅",
            "激进短线": "A高IV和AI电力储能题材更适合进攻",
        }[strat]

    if winner == "B":
        if ticker in DIRECT_STORAGE_PEERS:
            return {
                "NTM兑现优先": "B同业收入/利润兑现链更稳",
                "右尾弹性优先": "B同业储能或能源右尾更可收入化",
                "风险调整收益": "B同业现金流和估值组合更好",
                "下行保护优先": "B同业资产质量或现金流更安全",
                "估值消化优先": "B同业估值消化压力低于A",
                "近端催化优先": "B同业订单或产品节点更确定",
                "价格确认/动量": "B同业价格趋势更强或更稳",
                "激进短线": "B同业短线beta或关注度更强",
            }[strat]
        if ticker in UPSTREAM_DOWNSTREAM or category in {"云算力_IDC_AI软件平台", "AI服务器_存储_EMS"}:
            return {
                "NTM兑现优先": "B需求端/RPO/收入兑现更短链",
                "右尾弹性优先": "B直接AI负载或算力右尾更大",
                "风险调整收益": "B增长与现金流组合更均衡",
                "下行保护优先": "B资产质量或合同现金流更强",
                "估值消化优先": "B业绩兑现更容易消化估值",
                "近端催化优先": "B云/算力/订单催化更密集",
                "价格确认/动量": "B价格确认和资金偏好更强",
                "激进短线": "B高beta和AI主线资金更强",
            }[strat]
        if category in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链收入兑现更直接",
                "右尾弹性优先": "B半导体/网络右尾更大",
                "风险调整收益": "B上行空间更能覆盖风险",
                "下行保护优先": "B需求能见度或盈利质量更好",
                "估值消化优先": "B高增速更能消化估值",
                "近端催化优先": "B产品/订单催化更近",
                "价格确认/动量": "B趋势确认强于A",
                "激进短线": "B短线爆发力更强",
            }[strat]
        if category in INFRA_CATS or ticker in POWER_ADJACENT or ticker in POWER_ELECTRONICS_ADJACENT:
            return {
                "NTM兑现优先": "B订单、backlog或盈利兑现更稳",
                "右尾弹性优先": "B AI电力链右尾更硬",
                "风险调整收益": "B增长、现金流和估值组合更优",
                "下行保护优先": "B订单粘性和利润稳定性更强",
                "估值消化优先": "B用订单利润消化估值更容易",
                "近端催化优先": "B订单/产能/财报催化更明确",
                "价格确认/动量": "B趋势确认或不过热程度更好",
                "激进短线": "B电气化交易弹性更强",
            }[strat]
        return {
            "NTM兑现优先": "B未来12个月兑现证据更直接",
            "右尾弹性优先": "B极端情景收入弹性更大",
            "风险调整收益": "B上行和下行组合更好",
            "下行保护优先": "B资产质量或估值缓冲更强",
            "估值消化优先": "B当前估值更容易被业绩消化",
            "近端催化优先": "B未来两个季度催化更明确",
            "价格确认/动量": "B价格行为更强",
            "激进短线": "B短线波动和关注度更适合进攻",
        }[strat]

    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strat == "下行保护优先":
        return "两者防守证据均不充分"
    if strat == "估值消化优先":
        return "估值消化证据接近"
    return "档位接近需再验证"


def label_for(strat: str, a: dict, b: dict, rel: str) -> str:
    at = a.get("tiers", {}).get(strat, "资料不足")
    bt = b.get("tiers", {}).get(strat, "资料不足")
    if "资料不足" in (at, bt):
        if at == bt:
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    diff = float(a.get("scores", {}).get(strat, 0)) - float(b.get("scores", {}).get(strat, 0))
    tier_gap = tier_value(at) - tier_value(bt)
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


def cell_for(strat: str, a: dict, b: dict, rel: str) -> str:
    label = label_for(strat, a, b, rel)
    diff = float(a.get("scores", {}).get(strat, 0)) - float(b.get("scores", {}).get(strat, 0))
    winner = "A" if "投A" in label else "B" if "投B" in label else "中性"
    return f"{label}：{reason_for(strat, winner, b, rel, diff)}"


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strat in STRATS if "投A" in str(row_obj[strat]))
    b_count = sum(1 for strat in STRATS if "投B" in str(row_obj[strat]))
    return a_count, b_count, len(STRATS) - a_count - b_count


def final_choice(row_obj: dict) -> str:
    weights = {
        "NTM兑现优先": 1.18,
        "风险调整收益": 1.16,
        "估值消化优先": 1.08,
        "右尾弹性优先": 0.94,
        "近端催化优先": 0.82,
        "下行保护优先": 0.78,
        "价格确认/动量": 0.52,
        "激进短线": 0.42,
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
        label = base.tag_in_cell(row_obj[strat])
        score += weights[strat] * label_score.get(label, 0.0)
    return "A" if score > 0.15 else "B" if score < -0.15 else "中性"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    diffs = {strat: float(a.get("scores", {}).get(strat, 0)) - float(b.get("scores", {}).get(strat, 0)) for strat in STRATS}
    if choice == "中性":
        return "两家公司风格差异大，FLNC的储能右尾与对手的质量/估值证据未拉开可强判差距。"
    if choice == "A":
        if diffs["NTM兑现优先"] > 12:
            return "FLNC 的FY2026指引、56亿美元backlog和10.1GW合同backlog使收入兑现更强。"
        if diffs["右尾弹性优先"] > 14:
            return "FLNC 的AI数据中心BESS、Smartstack和hyperscaler MSA使右尾更大。"
        if diffs["近端催化优先"] > 12:
            return "FLNC 的Q3首单、H2交付、毛利和现金流验证节点更近。"
        if diffs["价格确认/动量"] > 16:
            return "FLNC 的价格确认和高IV显示短期资金关注度更强。"
        return "FLNC 用高增长、订单和近端催化压过对手，但要承受现金流和高波动。"

    if diffs["下行保护优先"] < -14:
        return f"{b['ticker']} 的现金流、估值缓冲或压力期韧性明显优于FLNC。"
    if diffs["风险调整收益"] < -12:
        return f"{b['ticker']} 的上行/下行组合更均衡，FLNC执行和现金流反证更重。"
    if diffs["估值消化优先"] < -12:
        return f"{b['ticker']} 更容易用利润兑现消化估值，FLNC仍需证明毛利和FCF。"
    if diffs["NTM兑现优先"] < -12:
        return f"{b['ticker']} 的NTM收入或利润兑现链条比FLNC更短。"
    if diffs["右尾弹性优先"] < -14:
        return f"{b['ticker']} 的极端情景收入弹性或AI主链右尾大于FLNC。"
    return f"{b['ticker']} 在多数投资思路下比FLNC更适合当前配置目标。"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong: list[str] = []
    b_strong: list[str] = []
    close: list[str] = []
    for strat in STRATS:
        gap = tier_value(a.get("tiers", {}).get(strat)) - tier_value(b.get("tiers", {}).get(strat))
        label = strat.replace("优先", "").replace("/动量", "动量")
        if gap > 0:
            a_strong.append(label)
        elif gap < 0:
            b_strong.append(label)
        else:
            close.append(label)

    def joined(items: list[str]) -> str:
        if not items:
            return "无"
        return "、".join(items[:3]) + ("等" if len(items) > 3 else "")

    return f"A强：{joined(a_strong)}；B强：{joined(b_strong)}；接近：{joined(close)}"


def build_comparisons(companies: dict[str, dict]) -> list[dict]:
    a = companies[TARGET]
    rows: list[dict] = []
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
        for strat in STRATS:
            row_obj[strat] = cell_for(strat, a, b, rel)
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


def strongest(rows: list[dict], final: str, limit: int = 45) -> list[dict]:
    selected = [row for row in rows if row["final_choice"] == final]
    if final == "B":
        selected.sort(key=lambda row: (row["bc"] - row["ac"], row["bc"], -row["nc"]), reverse=True)
    else:
        selected.sort(key=lambda row: (row["ac"] - row["bc"], row["ac"], -row["nc"]), reverse=True)
    return selected[:limit]


def render_report(companies: dict[str, dict], comparisons: list[dict]) -> str:
    a = companies[TARGET]
    latest_dates = sorted({company["date"] for company in companies.values() if company.get("date")})
    date_range = f"{latest_dates[0]} 至 {latest_dates[-1]}" if latest_dates else "缺失"
    missing_fin = sorted([ticker for ticker, company in companies.items() if not company.get("fin") or not company.get("fin", {}).get("price")])
    fin = a.get("fin", {})
    mom2 = a.get("mom2", {})
    mom1 = a.get("mom1", {})
    soxx = a.get("soxx", {})

    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}，P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_num(fin.get('call_iv'), 1)}%，Put IV {fmt_num(fin.get('put_iv'), 1)}%；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}，过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    stats: dict[str, Counter] = {strat: Counter() for strat in STRATS}
    for row_obj in comparisons:
        for strat in STRATS:
            stats[strat][base.tag_in_cell(row_obj[strat])] += 1

    a_side = {strat: sum(stats[strat][tag] for tag in TAG_ORDER[:3]) for strat in STRATS}
    b_side = {strat: sum(stats[strat][tag] for tag in TAG_ORDER[4:]) for strat in STRATS}
    a_best = sorted(STRATS, key=lambda strat: a_side[strat] - b_side[strat], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda strat: a_side[strat] - b_side[strat])[:3]
    strong_b = strongest(comparisons, "B")
    strong_a = strongest(comparisons, "A")
    final_a = sum(1 for row in comparisons if row["final_choice"] == "A")
    final_b = sum(1 for row in comparisons if row["final_choice"] == "B")
    final_neutral = len(comparisons) - final_a - final_b

    product_names = [str(product[0]).split("：")[0].split(" / ")[0] for product in a.get("products", [])[:6]]
    file_list = "；".join([f"{ticker}:{Path(companies[ticker]['path']).name}" for ticker in sorted(companies)])
    rank_text = {
        strat: f"第 {a.get('ranks', {}).get(strat)}/{a.get('rank_total', {}).get(strat, len(companies))}，{a.get('tiers', {}).get(strat)} 档"
        for strat in STRATS
    }
    support = {
        "NTM兑现优先": (
            "FY2026指引32-36亿美元、NTM基准37-41亿美元、backlog 56亿美元、products contracted backlog 10.1GW",
            "FY2026H2需确认22.6-26.6亿美元，H1调整后毛利8.3%、FCF为-2.854亿美元，执行和回款压力大",
        ),
        "右尾弹性优先": (
            "乐观44-50亿美元、极度乐观55-63亿美元；AI数据中心BESS、2个hyperscaler MSA、Smartstack和41.3GW/147GWh pipeline提供非线性上限",
            "MSA/reference architecture不等于PO、GWh、交付窗口或毛利条款，极度乐观可信度仅低到中",
        ),
        "风险调整收益": (
            "收入高增、低P/S和储能/AI电力题材给上行赔率",
            "TTM EPS为负、Forward PE 124.92、EV/EBITDA为负、Call IV 124.2%、SOXX压力窗口累计-90.92%",
        ),
        "下行保护优先": (
            "backlog和FY2026指引给收入底部锚，9亿美元liquidity提供短期缓冲",
            "H1 FCF为负、存货7.642亿美元、客户延期/验收/低毛利风险高，历史压力窗口回撤深",
        ),
        "估值消化优先": (
            "2026-06-22 P/S 1.80低于多数高弹性AI主题股，若FY2026H2交付兑现可显著摊薄销售倍数",
            "盈利尚未稳定，Forward PE 124.92且EV/EBITDA为负，基准EBITDA不足以轻松支撑重估",
        ),
        "近端催化优先": (
            "FY2026Q3 hyperscaler首单、H2收入ramp、adjusted GM、OCF/FCF、Smartstack交付和data-center pipeline转PO均在1-2季内可验证",
            "催化强但反证也近，若Q3首单缺席或H2交付/毛利不达标，重定价会反向发生",
        ),
        "价格确认/动量": (
            "截至2026-06-03过去两周+31.20%、过去一月+103.86%，2026-06-22收盘25.19仍守住6月初价格区间",
            "上涨已显著反映预期，且价格文件基准日为2026-06-03，后续需继续用新版金融资料确认",
        ),
        "激进短线": (
            "Call IV 124.2%、Put IV 125.8%、AI数据中心储能叙事、Q3订单窗口和一月翻倍动量适合高风险进攻",
            "高IV和高回撤说明容错率低，不适合作为低风险短线；若基本面反证出现会快速杀估值",
        ),
    }

    lines: list[str] = []
    lines += [
        "# FLNC 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：FLNC / Fluence Energy",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：2026-06-22 金融数据；2026-06-03 区间涨跌；2026-06-04 SOXX 三段压力窗口",
        "",
        "> 口径说明：本报告只使用 `分析报告/公司评估/结果/`、`公司调研/`、`行业调研/` 和 `金融资料/` 等上游资料；未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。每一行是 FLNC 与一家项目内公司 B 的二选一判断。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。FLNC 的强项集中在价格确认、储能/AI电力右尾、近端催化和订单/backlog支撑的高增长，不是防守型或低波动型资产。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。最大短板是下行保护、风险调整收益和估值消化：H1 FCF为负、毛利仍低、存货高、Forward PE高且历史压力窗口回撤深。",
        "- A 最适合的投资者画像：愿意为 utility-scale BESS、AI 数据中心 BESS、Smartstack 和 hyperscaler MSA 的非线性订单期权承担高波动、高执行风险的进攻型资金。",
        "- A 最不适合的投资者画像：要求稳定现金流、低IV、压力期韧性、明确盈利质量或估值已被NTM业绩充分消化的稳健配置者。",
        f"- 多数思路下最强反方公司：{'、'.join([row['ticker'] for row in strong_b[:12]])}。这些公司通常在现金流质量、估值消化、直接AI主链收入化、订单利润率或下行保护上强于FLNC。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：FLNC 是全项目偏进攻的储能/AI电力可选项；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家。它不是综合质量顶档，但在右尾、催化和价格确认口径下有明显存在感。",
        "- 后续最重要跟踪数据：FY2026Q3 revenue、adjusted gross margin、adjusted EBITDA、operating cash flow、free cash flow、inventory、backlog dollar/GW/GWh、hyperscaler first order金额/GWh/交付窗口、Smartstack项目数量、data-center pipeline从MSA到PO的转化率、Services AUM/Digital AUM/ARR、客户延期/取消/LD或warranty事件。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "FLNC"]),
        base.row(["公司名称", "Fluence Energy"]),
        base.row(["产业链分类", a.get("category", "电力_发电_能源_储能")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "37-41 亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev')}；极度乐观：{a.get('extreme_rev')}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a.get('base_margin')}；利润/现金流：{a.get('base_profit')}；{a.get('base_cash')}"]),
        base.row(["最大传导瓶颈", "FY2026H2大额交付、港口/物流、电芯/PCS/消防/并网验收、客户延期权、工作资本和库存周转。"]),
        base.row(["最大反证", "H1 adjusted GM仅8.3%、H1 FCF为-2.854亿美元、存货7.642亿美元；AI数据中心MSA尚未等同公开PO和收入计划。"]),
        base.row(["近端催化剂", "FY2026Q3 hyperscaler首单、H2 revenue ramp、adjusted GM、OCF/FCF、Smartstack交付、data-center pipeline转PO、Services/Digital AUM和ARR。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strat in STRATS:
        lines.append(base.row([strat, a.get("tiers", {}).get(strat, "资料不足"), rank_text[strat], support[strat][0], support[strat][1]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与FLNC争夺储能、备电、园区/住宅/utility BESS或同一能源系统配置资金，优先看订单/backlog、项目交付、毛利、客户质量和估值。", "TSLA、ENPH、GNRC", "同业证据权重最高；若B有更稳现金流或FLNC有更强AI BESS订单，允许提高判断力度。"]),
        base.row(["相邻替代", "同属AI电力、配电、电源、冷却、工程或电气化基础设施资金篮子，但不直接卖同类BESS系统。", "BE、GEV、ETN、VRT、POWL、PWR、SMR、OKLO、AAON、TT", "重点回答资金只能买一个时谁的增长质量、利润捕获、估值消化和近端催化更优。"]),
        base.row(["上下游", "B是储能电池/UPS/电力供应链、utility/IPP/数据中心客户或AI负载需求端，决定FLNC订单池但也可能自身捕获利润。", "AMPX、ENS、CEG、VST、AEP、MSFT、AMZN、ORCL、CRWV、EQIX", "区分收入规模、议价权和利润池，不能把下游需求大直接等同于FLNC更好。"]),
        base.row(["跨赛道", "半导体、设备、材料、软件和工业等业务差异较大，但仍作为项目内资金配置替代。", "NVDA、AVGO、TSM、ASML、MU、CDNS、BABA", "默认降低结论力度；只有增长质量、估值消化、下行保护或价格确认明显拉开时才给建议/强烈建议。"]),
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
        ] + [row_obj[strat] for strat in STRATS] + [
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
    for strat in STRATS:
        c = stats[strat]
        lines.append(base.row([strat] + [c[tag] for tag in TAG_ORDER] + [a_side[strat], b_side[strat]]))

    lines += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for idx, row_obj in enumerate(strong_b, 1):
        wins = [strat for strat in STRATS if "投B" in row_obj[strat]]
        catchup = "FLNC需要把hyperscaler MSA转为公开PO/GWh/交付窗口，并同步证明GM、OCF/FCF和存货周转改善。"
        if "下行保护优先" in wins or "风险调整收益" in wins:
            catchup = "FLNC需要用连续季度正FCF、双位数稳定毛利和较低回撤证明它不只是高beta储能题材。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for idx, row_obj in enumerate(strong_a, 1):
        wins = [strat for strat in STRATS if "投A" in row_obj[strat]]
        catchup = "B需要拿出同等强度的订单/backlog、客户项目、收入增速或近端重定价证据，并证明估值没有被透支。"
        if "下行保护优先" in wins:
            catchup = "B需要在保留防守性的同时补足增长右尾、订单催化和价格确认。"
        lines.append(base.row([idx, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；本次共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺少可用价格/估值的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/电力_发电_能源_储能/FLNC_Fluence Energy_公司调研_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_flnc_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对FLNC的backlog、FY2026指引、AI数据中心BESS期权、低毛利、负FCF、高IV和压力窗口回撤做人工校准后建档；未读取下游量化目录或现成排序结论。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
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
                "size": OUT_PATH.stat().st_size,
                "flnc_tiers": {strat: a.get("tiers", {}).get(strat) for strat in STRATS},
                "flnc_ranks": {strat: a.get("ranks", {}).get(strat) for strat in STRATS},
                "final_A": sum(1 for row in comparisons if row["final_choice"] == "A"),
                "final_B": sum(1 for row in comparisons if row["final_choice"] == "B"),
                "final_neutral": sum(1 for row in comparisons if row["final_choice"] == "中性"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
