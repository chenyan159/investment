from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "FCEL"
TARGET_NAME = "FuelCell Energy"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "FCEL_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {
    "BE",  # fuel-cell / onsite data-center power
    "GNRC",  # backup and onsite generation
    "PSIX",  # onsite power engines and generators
}

POWER_ADJACENT = {
    "AEP",
    "ABBNY",
    "AEIS",
    "AMPX",
    "APD",
    "BWXT",
    "CARR",
    "CAT",
    "CEG",
    "CMI",
    "DKILY",
    "DOV",
    "DTE",
    "EME",
    "ENPH",
    "ENS",
    "ET",
    "ETN",
    "ETR",
    "FIX",
    "FLNC",
    "GEV",
    "HTHIY",
    "HUBB",
    "IESC",
    "JCI",
    "LIN",
    "MOD",
    "MRAAY",
    "MYRG",
    "NVT",
    "OKLO",
    "PH",
    "POWI",
    "POWL",
    "PWR",
    "RYCEY",
    "SMR",
    "TT",
    "TTDKY",
    "VICR",
    "VRT",
    "VST",
}

DATA_CENTER_DEMAND_CATS = {
    "AI服务器_存储_EMS",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "云算力_IDC_AI软件平台",
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def score_companies(companies: dict[str, dict]) -> None:
    calibrated.score_companies(companies)

    # FCEL calibration:
    # - NTM is weak because base revenue is only $130-180M, no FY2026 guide
    #   exists, product backlog is small, and data-center pipeline is not signed.
    # - Right-tail and aggressive short-term scores are high because the company
    #   has tiny revenue base, 4GW proposal pipeline, standardized 12.5MW block,
    #   very high IV, and strong recent price confirmation.
    # - Downside protection and valuation digestion are penalized for negative
    #   gross margin, operating losses, dilution risk, high P/S, and a very poor
    #   SOXX pressure-window history.
    overrides = {
        "NTM兑现优先": 57.0,
        "右尾弹性优先": 88.0,
        "风险调整收益": 39.0,
        "下行保护优先": 34.0,
        "估值消化优先": 48.0,
        "近端催化优先": 62.0,
        "价格确认/动量": 74.0,
        "激进短线": 100.0,
    }
    for strategy, score in overrides.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score
    calibrated.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in POWER_ADJACENT or category == "电力_发电_能源_储能" or category in INFRA_CATS:
        return "相邻替代"
    if category in DATA_CENTER_DEMAND_CATS:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, winner: str, company: dict, rel: str, _diff: float) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))

    if winner == "A":
        return {
            "NTM兑现优先": "A低位收入和现有backlog仍略有锚",
            "右尾弹性优先": "A有4GW pipeline和小基数右尾",
            "风险调整收益": "A净现金和右尾赔率略可抵消风险",
            "下行保护优先": "B现金流或资产反证更重",
            "估值消化优先": "A若签约大单可快速压低PS",
            "近端催化优先": "A数据中心签约和产能节点更近",
            "价格确认/动量": "A价格与高IV确认资金关注",
            "激进短线": "A高IV叠加AI电力二线弹性更强",
        }[strategy]

    if winner == "B":
        if ticker in DIRECT_PEERS:
            return {
                "NTM兑现优先": "B同业订单/backlog兑现更硬",
                "右尾弹性优先": "B同业客户项目证据更硬",
                "风险调整收益": "B同业风险收益组合更均衡",
                "下行保护优先": "B同业毛利和现金流更安全",
                "估值消化优先": "B同业估值消化更可验证",
                "近端催化优先": "B同业交付或订单催化更确定",
                "价格确认/动量": "B同业趋势更强或不过热",
                "激进短线": "B同业短线弹性更可交易",
            }[strategy]
        if category in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链收入/RPO兑现更短链",
                "右尾弹性优先": "B直接AI收入弹性更大",
                "风险调整收益": "B上行更能覆盖执行风险",
                "下行保护优先": "B需求能见度或现金流更强",
                "估值消化优先": "B高速增长更能消化估值",
                "近端催化优先": "B订单/产品催化更密集",
                "价格确认/动量": "B价格确认和资金偏好更强",
                "激进短线": "B AI主线beta更适合进攻",
            }[strategy]
        if rel in {"相邻替代", "上下游"}:
            return {
                "NTM兑现优先": "B订单或资产底盘兑现更稳",
                "右尾弹性优先": "B右尾更直接或更有证据",
                "风险调整收益": "B增长现金流估值组合更优",
                "下行保护优先": "B现金流和估值缓冲更强",
                "估值消化优先": "B更容易用业绩消化估值",
                "近端催化优先": "B项目或客户节点更明确",
                "价格确认/动量": "B趋势确认强于A的高波动",
                "激进短线": "B短线爆发力或主线资金更强",
            }[strategy]
        return {
            "NTM兑现优先": "B未来12个月兑现证据更直接",
            "右尾弹性优先": "B极端情景收入弹性更大",
            "风险调整收益": "B上行和下行组合更好",
            "下行保护优先": "B资产质量或估值缓冲更强",
            "估值消化优先": "B当前估值更容易被业绩消化",
            "近端催化优先": "B未来两个季度催化更明确",
            "价格确认/动量": "B价格行为更强",
            "激进短线": "B短线波动和关注度更适合进攻",
        }[strategy]

    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "风险和估值证据接近"
    return "档位接近需再验证"


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
        strong_cut, suggest_cut, micro_cut = 30, 15, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 25, 12, 4
    elif rel == "直接同业":
        strong_cut, suggest_cut, micro_cut = 18, 8, 4
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
    diff = float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0))
    winner = "A" if "投A" in label else "B" if "投B" in label else "中性"
    return f"{label}：{reason_for(strategy, winner, b, rel, diff)}"


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in str(row_obj[strategy]))
    b_count = sum(1 for strategy in STRATS if "投B" in str(row_obj[strategy]))
    return a_count, b_count, len(STRATS) - a_count - b_count


def final_choice(row_obj: dict) -> str:
    weights = {
        "NTM兑现优先": 1.20,
        "风险调整收益": 1.20,
        "下行保护优先": 1.00,
        "估值消化优先": 1.00,
        "右尾弹性优先": 0.95,
        "近端催化优先": 0.85,
        "价格确认/动量": 0.60,
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
        tag = base.tag_in_cell(str(row_obj[strategy]))
        score += weights[strategy] * label_score.get(tag, 0.0)
    return "A" if score > 0.15 else "B" if score < -0.15 else "中性"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    ticker = str(b.get("ticker", ""))
    category = str(b.get("category", ""))
    diffs = {
        strategy: float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0))
        for strategy in STRATS
    }
    if choice == "中性":
        return "FCEL的AI电力右尾与B的主业证据风格差异大，当前不足以强判。"
    if choice == "A":
        if diffs["右尾弹性优先"] > 12:
            return "FCEL的4GW pipeline、12.5MW block和小基数使右尾更大，但仍需签约验证。"
        if diffs["激进短线"] > 12 or diffs["价格确认/动量"] > 12:
            return "FCEL的高IV、强价格关注和AI电力二线叙事更适合短线进攻。"
        if diffs["估值消化优先"] > 10:
            return "FCEL若把pipeline转成订单，收入基数太小会带来更快估值压缩。"
        return "FCEL以高弹性和事件期权略胜，但不是低风险或确定性更强。"

    if category in HIGH_GROWTH_CATS:
        return f"{ticker}的AI主链收入、订单或平台地位比FCEL的pipeline期权更直接。"
    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的未来12个月订单、backlog或收入兑现链条比FCEL更短。"
    if diffs["下行保护优先"] < -14:
        return f"{ticker}的现金流、估值或资产底盘比FCEL高IV/亏损结构更安全。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}当前增长和估值匹配度优于FCEL。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的风险调整收益比FCEL更均衡。"
    return f"{ticker}在多数投资思路下的增长质量、催化或估值组合优于FCEL。"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong: list[str] = []
    b_strong: list[str] = []
    close: list[str] = []
    for strategy in STRATS:
        av = tier_value(a.get("tiers", {}).get(strategy))
        bv = tier_value(b.get("tiers", {}).get(strategy))
        short = strategy.replace("优先", "").replace("/动量", "动量")
        if av > bv:
            a_strong.append(short)
        elif av < bv:
            b_strong.append(short)
        else:
            close.append(short)

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
            "name": b.get("name", ""),
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
    return sorted(rows, key=lambda item: (rel_order.get(str(item["relationship"]), 9), str(item["ticker"])))


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
    selected = [row_obj for row_obj in rows if row_obj["final_choice"] == final]
    if final == "B":
        selected.sort(key=lambda item: (item["bc"] - item["ac"], item["bc"], -item["nc"]), reverse=True)
    else:
        selected.sort(key=lambda item: (item["ac"] - item["bc"], item["ac"], -item["nc"]), reverse=True)
    return selected[:limit]


def render_report(companies: dict[str, dict], comparisons: list[dict]) -> str:
    a = companies[TARGET]
    latest_dates = sorted({str(company["date"]) for company in companies.values() if company.get("date")})
    date_range = f"{latest_dates[0]} 至 {latest_dates[-1]}" if latest_dates else "缺失"
    missing_fin = sorted([ticker for ticker, company in companies.items() if not company.get("fin")])
    fin = a.get("fin", {})
    mom2 = a.get("mom2", {})
    mom1 = a.get("mom1", {})
    soxx = a.get("soxx", {})

    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {fmt_num(fin.get('call_iv'), 1)}%，"
        f"Put IV {fmt_num(fin.get('put_iv'), 1)}%；2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}，"
        f"过去一月 {fmt_pct(mom1.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    stats: dict[str, Counter] = {strategy: Counter() for strategy in STRATS}
    for row_obj in comparisons:
        for strategy in STRATS:
            stats[strategy][base.tag_in_cell(str(row_obj[strategy]))] += 1
    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy])[:3]
    strong_b = majority_rows(comparisons, "B", 45)
    strong_a = majority_rows(comparisons, "A", 45)
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "B")
    final_neutral = len(comparisons) - final_a - final_b

    products = []
    for product in a.get("products", [])[:8]:
        products.append(str(product[0]).split("：")[0])
    product_text = "；".join(products) if products else "12.5MW/2.5MW FuelCell Energy Block；Service/LTSA；Generation PPA；Advanced Technologies"
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])

    support = {
        "NTM兑现优先": ("FY2026 Q2收入$35.6M、6M收入$66.1M、product backlog $36.1M、service backlog $155.4M，基准收入$130-180M有低位锚", "无FY2026收入指引，data-center pipeline未签约，基准收入相对TTM为-23%至+7%且利润仍亏"),
        "右尾弹性优先": ("4GW proposal pipeline、12.5MW标准化block、SDCL 450MW和DPP/TESIAC 360MW合作、极度乐观收入$650M-1.0B提供非线性上限", "pipeline不是backlog，缺客户名/MW/金额/deposit/交付窗口，Bloom等同业领先"),
        "风险调整收益": ("现金含受限现金$440.9M、净现金结构、小市值和大右尾给出赔率", "毛利率仍为负、经营亏损、ATM摊薄和高IV使风险收益不均衡"),
        "下行保护优先": ("账面现金和current ratio给12个月续航缓冲", "SOXX压力窗口累计-98.87%、Call IV 154.8%、负毛利、Groton/Generation亏损和融资摊薄削弱防守"),
        "估值消化优先": ("若乐观收入$300-500M或极度乐观收入兑现，P/S可快速压缩；净现金降低企业价值压力", "2026-06-22 P/S 9.82且PE不可用，基准收入和利润无法消化当前市值"),
        "近端催化优先": ("Q3/Q4韩国模块、data-center客户签约、Torrington 500MW扩产、Rotterdam碳捕集模块和Q3/Q4 backlog变化都可验证", "最关键催化仍是未签约pipeline，时间表和客户付款未披露"),
        "价格确认/动量": ("2026-06-03过去一月+63.86%，2026-06-22价格高于6月初锚点，高IV显示资金关注", "过去两周仅+7.86%，压力窗口回撤极深，高波动可能已部分透支"),
        "激进短线": ("Call IV 154.8%、Put IV 156.3%、小市值、AI数据中心电力短缺和4GW pipeline适合高beta事件交易", "任何未签约、毛利、现金流或增发反证都会放大短线回撤"),
    }

    lines: list[str] = []
    lines.append("# FCEL 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：FCEL / {TARGET_NAME}")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(comparisons)}")
    lines.append(f"公司评估文件日期范围：{date_range}")
    lines.append("日度数据日期：2026-06-22 金融数据；2026-06-03 区间涨跌；2026-06-04 SOXX 压力窗口")
    lines.append("")
    lines.append("> 口径说明：本报告只使用 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/`、`行业调研/` 和 `金融资料/` 上游资料；未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。每一行是 FCEL 与一家项目内公司 B 的二选一判断。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.append(f"- A 最占优的投资思路：{'、'.join(a_best)}。FCEL 的优势主要是小基数、高IV、4GW数据中心pipeline和AI电力二线右尾，不是已经进入收入表的高质量增长。")
    lines.append(f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。最大短板是NTM收入和利润兑现弱、基准情景仍亏损、SOXX压力窗口回撤深、当前估值需要乐观情景才能解释。")
    lines.append("- A 最适合的投资者画像：愿意用小仓位押注AI数据中心现场电力签约、12.5MW block商业化、Torrington扩产和高波动事件交易的激进型资金。")
    lines.append("- A 最不适合的投资者画像：重视确定订单/backlog、正毛利、FCF、低IV、低回撤和可用基准业绩消化估值的稳健配置者。")
    lines.append("- 多数思路下最强反方公司：" + "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]]) + "。这些公司通常有更硬的AI主链收入、订单/RPO/backlog、现金流质量、下行保护或估值消化。")
    lines.append(f"- 如果只追求更高增长、更好公司，A 的总体位置：FCEL 是项目内高右尾/高波动/低确定性的事件型标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家。它可以作为AI电力供给二线期权，但不能替代BE、GEV、ETN、VRT、NVDA、AVGO、MU等已经有更硬收入或订单证据的主线公司。")
    lines.append("- 后续最重要跟踪数据：data-center signed MW、客户名、合同金额、deposit/deferred revenue、product backlog、Torrington实际MW/year、product gross margin、service attach、Groton upgrade、generation GM、OCF/FCF、ATM融资节奏和Rotterdam碳捕集demo。")
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | FCEL |")
    lines.append(f"| 公司名称 | {TARGET_NAME} |")
    lines.append(f"| 产业链分类 | {a.get('category', '电力_发电_能源_储能')} |")
    lines.append(f"| 重要产品/业务线 | {product_text} |")
    lines.append(f"| NTM 基准收入 | {a.get('base_rev') or '$130-180M'} |")
    lines.append(f"| 乐观/极度乐观收入 | 乐观：{a.get('bull_rev')}；极度乐观：{a.get('extreme_rev')} |")
    lines.append(f"| 利润和现金流结论 | 基准经营利润率：{a.get('base_margin')}；利润/现金流：{a.get('base_profit')}；{a.get('base_cash')} |")
    lines.append("| 最大传导瓶颈 | `4GW proposal pipeline -> executed agreement -> product/service backlog -> manufacturing slot -> commissioning/revenue recognition -> positive gross margin`，目前主要卡在pipeline到signed backlog之间。 |")
    lines.append("| 最大反证 | product backlog只有$36.1M，data-center signed backlog为0；FY2026 Q2 gross margin -36.3%，Generation GM -154.1%，经营亏损和ATM融资摊薄仍重。 |")
    lines.append("| 近端催化剂 | 首个数据中心客户/MW/金额/deposit披露、Q3/Q4韩国模块交付、Torrington扩产进度、Groton升级、Rotterdam碳捕集demo、product backlog和product GM改善。 |")
    lines.append("| 日度数据 | " + daily_snapshot + " |")
    lines.append("")
    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append("| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for strategy in STRATS:
        position = f"评分排名 {a.get('ranks', {}).get(strategy)}/{a.get('rank_total', {}).get(strategy, len(companies))}"
        lines.append(f"| {strategy} | {a.get('tiers', {}).get(strategy, '资料不足')} | {position} | {support[strategy][0]} | {support[strategy][1]} |")
    lines.append("")
    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | 与FCEL在燃料电池、数据中心自备电源、现场连续电力或燃气/柴油替代供电方案上争夺同一需求池，优先比较签约MW、product backlog、毛利、可靠性和现金流。 | BE、GNRC、PSIX | 同业证据权重最高；BE等若有更硬客户项目和毛利证据，可直接压过FCEL的pipeline期权。 |")
    lines.append("| 相邻替代 | 同属AI数据中心电力、核电/燃气/储能、配电、冷却、工程或能源基础设施资金篮子，但产品不完全相同。 | GEV、CEG、VST、ETN、VRT、SMR、OKLO、PWR、POWL、FLNC | 重点回答资金只能买一个时，谁更能把电力瓶颈转成订单、利润和可消化估值。 |")
    lines.append("| 上下游 | B位于云/IDC/服务器/芯片/网络等AI数据中心需求端或资本开支端，决定电力需求背景，但不自动等同FCEL收入。 | NVDA、AVGO、ANET、SMCI、MSFT、AMZN、EQIX、DLR | 不把下游AI capex直接映射给FCEL；只有FCEL拿到客户、订单或项目融资后才提高结论力度。 |")
    lines.append("| 跨赛道 | 半导体材料、设备、工业、软件安全等业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化和催化。 | ASML、TSM、CDNS、LIN、DHR、TMO | 默认降低结论力度；除非档位差明显，否则使用微倾向或中性。 |")
    lines.append("")
    lines.append("## 5. 全项目逐行投资思路决策表")
    lines.append("")
    lines.append("| 序号 | 公司B | 公司B分类 | 可比关系 | 档位差摘要 | NTM兑现优先 | 右尾弹性优先 | 风险调整收益 | 下行保护优先 | 估值消化优先 | 近端催化优先 | 价格确认/动量 | 激进短线 | 多数思路方向 | 最终更值得投 | 最关键理由 |")
    lines.append("| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for index, row_obj in enumerate(comparisons, 1):
        cells = [
            str(index),
            f"{row_obj['ticker']} / {row_obj['name']}",
            row_obj["classification"],
            row_obj["relationship"],
            row_obj["grade_diff"],
        ] + [row_obj[strategy] for strategy in STRATS] + [
            row_obj["majority"],
            row_obj["final_choice"],
            row_obj["key_reason"],
        ]
        lines.append("| " + " | ".join(str(cell).replace("|", "/").replace("\n", " ") for cell in cells) + " |")
    lines.append("")
    lines.append("## 6. 投资思路统计")
    lines.append("")
    lines.append("| 投资思路 | 强烈建议投A | 建议投A | 微倾向投A | 中性 | 微倾向投B | 建议投B | 强烈建议投B | A侧合计 | B侧合计 |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for strategy in STRATS:
        counter = stats[strategy]
        a_total = counter["强烈建议投A"] + counter["建议投A"] + counter["微倾向投A"]
        b_total = counter["微倾向投B"] + counter["建议投B"] + counter["强烈建议投B"]
        lines.append(
            f"| {strategy} | {counter['强烈建议投A']} | {counter['建议投A']} | {counter['微倾向投A']} | "
            f"{counter['中性']} | {counter['微倾向投B']} | {counter['建议投B']} | {counter['强烈建议投B']} | {a_total} | {b_total} |"
        )
    lines.append("")
    lines.append("## 7. 多数思路下 B 明显强于 A 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | B 胜出的主要投资思路 | 为什么 B 更值得投 | A 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for index, row_obj in enumerate(strong_b, 1):
        wins = [strategy for strategy in STRATS if "投B" in str(row_obj[strategy])]
        need = "FCEL需要把4GW pipeline转成客户名、signed MW、deposit、product backlog和正毛利，并降低ATM融资与现金流反证。"
        if row_obj["relationship"] == "直接同业":
            need = "FCEL需要在同业里证明比B更硬的MW签约、交付、SLA、product GM和现金回收。"
        elif row_obj["relationship"] == "上下游":
            need = "FCEL需要证明能实际捕获AI数据中心电力利润池，而不只是被AI capex叙事间接带动。"
        lines.append(f"| {index} | {row_obj['ticker']} / {row_obj['name']} | {'、'.join(wins[:6])} | {row_obj['key_reason']} | {need} |")
    lines.append("")
    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for index, row_obj in enumerate(strong_a, 1):
        wins = [strategy for strategy in STRATS if "投A" in str(row_obj[strategy])]
        need = "B需要拿出更清晰的高增长订单、近端催化、价格确认或同等高beta叙事，且不能只靠防守性胜出。"
        lines.append(f"| {index} | {row_obj['ticker']} / {row_obj['name']} | {'、'.join(wins[:6])} | {row_obj['key_reason']} | {need} |")
    lines.append("")
    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。")
    lines.append("- 公司 A 公司调研文件：`公司调研/电力_发电_能源_储能/FCEL_FuelCell_Energy_公司调研_2026-06-20.md`。")
    lines.append("- FCEL官方披露交叉核验：FuelCell Energy FY2026 Q2 results, 2026-06-08, https://investor.fce.com/press-releases/press-release-details/2026/FuelCell-Energy-Reports-Second-Fiscal-Quarter-2026-Results-Advances-Data-Center-Power-Strategy/default.aspx")
    lines.append("- 关键行业资料：`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`；`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`。")
    lines.append(f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 如有多份则取文件名日期最新；本次共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。")
    lines.append(f"- 公司全集最新正式评估文件清单：{file_list}")
    lines.append("- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。")
    lines.append(f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家；缺少当日价格/估值/IV 的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。")
    lines.append(f"- 公司 A 日度数据快照：{daily_snapshot}")
    lines.append("- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。")
    lines.append("- 自动化脚本：`scripts/generate_fcel_company_comparison.py`。脚本复用项目内正式评估和金融资料解析函数，使用同一批公司建立全项目相对档位，并对FCEL的4GW pipeline、未签约data-center backlog、负毛利、高IV、价格动量、现金缓冲、SOXX压力窗口和ATM摊薄风险做人工校准。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 FCEL 正式评估文件")
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
                "fcel_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "fcel_scores": {strategy: round(float(a.get("scores", {}).get(strategy, 0)), 2) for strategy in STRATS},
                "fcel_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
