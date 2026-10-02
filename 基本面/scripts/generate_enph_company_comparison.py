from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "ENPH"
TARGET_NAME = "Enphase Energy"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ENPH_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {
    "GNRC",  # residential backup / home energy systems
    "FLNC",  # battery storage, more utility-scale but same storage allocation bucket
    "TSLA",  # Powerwall / solar / energy storage competitor inside a much larger company
}

ENERGY_ADJACENT = {
    "AEP",
    "BE",
    "BWXT",
    "CEG",
    "CMI",
    "DTE",
    "ENS",
    "ET",
    "ETR",
    "FCEL",
    "GEV",
    "HTHIY",
    "OKLO",
    "PWR",
    "PSIX",
    "RYCEY",
    "SMR",
    "VST",
    "AMPX",
}

POWER_ELECTRONICS_ADJACENT = {
    "ABBNY",
    "AEIS",
    "AOSL",
    "DIOD",
    "ETN",
    "HUBB",
    "IFNNY",
    "LFUS",
    "MCHP",
    "MIELY",
    "MPWR",
    "MRAAY",
    "NVTS",
    "ON",
    "POWI",
    "POWL",
    "ST",
    "STM",
    "TTDKY",
    "TXN",
    "VICR",
    "VSH",
    "WOLF",
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

    # ENPH calibration:
    # - NTM has real Q2 guide / safe harbor / battery shipment anchors, but base
    #   revenue is still roughly flat to down versus Q1 2026 TTM.
    # - IQ SST is a real high-beta AI power option, but it has no customer,
    #   backlog or revenue confirmation inside the NTM window.
    # - 2026-06-22 price is back to $52.41 after the 2026-06-03 surge to $69.02,
    #   so stale one-month momentum is discounted.
    overrides = {
        "NTM兑现优先": 60.0,
        "右尾弹性优先": 76.0,
        "风险调整收益": 42.0,
        "下行保护优先": 38.0,
        "估值消化优先": 51.0,
        "近端催化优先": 64.0,
        "价格确认/动量": 52.0,
        "激进短线": 84.0,
    }
    for strategy, score in overrides.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score
    calibrated.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in ENERGY_ADJACENT or ticker in POWER_ELECTRONICS_ADJACENT:
        return "相邻替代"
    if category in {"电力_发电_能源_储能", "配电_电源_功率器件"}:
        return "相邻替代"
    if category in INFRA_CATS:
        return "相邻替代"
    if category in DATA_CENTER_DEMAND_CATS:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, winner: str, company: dict, rel: str, diff: float) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))

    if winner == "A":
        return {
            "NTM兑现优先": "A有Q2指引、safe harbor和电池出货锚",
            "右尾弹性优先": "A有IQ SST和小市值重定价期权",
            "风险调整收益": "A净现金和高毛利底盘更均衡",
            "下行保护优先": "A净现金和低收入季FCF仍为正",
            "估值消化优先": "A估值较高弹性小票更能用修复消化",
            "近端催化优先": "A有Q2出货、IQ9/10C和SST demo节点",
            "价格确认/动量": "A曾有强反弹且B价格更弱",
            "激进短线": "A高IV、IQ SST和政策交易弹性更高",
        }[strategy]

    if winner == "B":
        if ticker in DIRECT_PEERS:
            return {
                "NTM兑现优先": "B同业收入/订单兑现更直接",
                "右尾弹性优先": "B同业能源或储能右尾更可收入化",
                "风险调整收益": "B同业风险收益组合更稳",
                "下行保护优先": "B同业现金流或需求底盘更安全",
                "估值消化优先": "B同业增长与估值更匹配",
                "近端催化优先": "B同业订单或产品催化更近",
                "价格确认/动量": "B同业价格趋势更强",
                "激进短线": "B同业短线beta和关注度更强",
            }[strategy]
        if category in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B AI主链订单/RPO兑现更短链",
                "右尾弹性优先": "B直接AI右尾和收入基数弹性更大",
                "风险调整收益": "B上行空间更能覆盖执行风险",
                "下行保护优先": "B需求能见度或现金流韧性更强",
                "估值消化优先": "B高速增长更能消化估值",
                "近端催化优先": "B产品/订单催化更密集",
                "价格确认/动量": "B价格确认和资金偏好更强",
                "激进短线": "B高beta和AI主线资金更适合进攻",
            }[strategy]
        if category in {"电力_发电_能源_储能", "配电_电源_功率器件"} or category in INFRA_CATS:
            return {
                "NTM兑现优先": "B订单、backlog或交付路径更硬",
                "右尾弹性优先": "B AI电力/功率链收入化更直接",
                "风险调整收益": "B增长、现金流和估值组合更优",
                "下行保护优先": "B订单粘性或受监管资产更稳",
                "估值消化优先": "B用订单兑现消化估值更容易",
                "近端催化优先": "B项目、订单或产能催化更明确",
                "价格确认/动量": "B趋势确认强于A回落后的走势",
                "激进短线": "B电力或功率主题短线弹性更强",
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
    if strategy == "价格确认/动量":
        return "A反弹已回吐而B确认度也有限"
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


def cell_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    label = label_for(strategy, a, b, rel)
    diff = float(a.get("scores", {}).get(strategy, 0)) - float(b.get("scores", {}).get(strategy, 0))
    winner = "A" if "投A" in label else "B" if "投B" in label else "中性"
    return f"{label}：{reason_for(strategy, winner, b, rel, diff)}"


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in str(row_obj[strategy]))
    b_count = sum(1 for strategy in STRATS if "投B" in str(row_obj[strategy]))
    neutral = len(STRATS) - a_count - b_count
    return a_count, b_count, neutral


def final_choice(row_obj: dict) -> str:
    weights = {
        "NTM兑现优先": 1.20,
        "风险调整收益": 1.15,
        "估值消化优先": 1.05,
        "下行保护优先": 0.95,
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
        return "ENPH的IQ SST期权与B的主业证据风格差异大，当前不足以强判。"
    if choice == "A":
        if diffs["右尾弹性优先"] > 12:
            return "ENPH的IQ SST、微逆/储能平台和小市值重定价期权强于B的右尾证据。"
        if diffs["近端催化优先"] > 10:
            return "ENPH的Q2 safe harbor出货、IQ9/10C和2026年底SST demo节点更近。"
        if diffs["估值消化优先"] > 10:
            return "ENPH虽有政策风险，但Forward PE和修复空间比B更容易解释。"
        if diffs["NTM兑现优先"] > 8:
            return "ENPH有Q2指引、safe harbor和电池MWh锚，B的NTM收入证据更弱。"
        return "ENPH在修复弹性、净现金和新产品期权上略胜，B的确定性不足以覆盖。"

    if category in HIGH_GROWTH_CATS:
        return f"{ticker}的AI主链收入、订单或平台地位比ENPH的SST期权更直接。"
    if diffs["下行保护优先"] < -14:
        return f"{ticker}的现金流、估值或资产底盘比ENPH高IV/政策风险更安全。"
    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的未来12个月订单、backlog或收入兑现链条比ENPH更短。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}当前增长和估值匹配度优于ENPH。"
    if diffs["价格确认/动量"] < -12:
        return f"{ticker}的价格确认强于ENPH从6月初反弹高点回落后的走势。"
    return f"{ticker}在多数投资思路下的增长质量、催化或估值组合优于ENPH。"


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
    product_text = "；".join(products) if products else "微型逆变器、IQ Battery、软件/网关、EV充电、IQ SST"
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])

    support = {
        "NTM兑现优先": ("B", "中游偏后", "Q2 2026收入指引2.80-3.10亿美元、safe harbor约0.85亿美元、IQ Battery 100-110MWh、PWT backlog 8.737亿美元提供锚", "基准NTM收入12.5-14.5亿美元，较Q1 TTM约-11%至+4%；住宅需求和电池出货仍弱"),
        "右尾弹性优先": ("A", "强势但非顶档", "IQ SST面向35kV/15kV到800VDC/+-400VDC，2026 demo、2027 pilot、2028 volume shipment，叠加小市值和高IV", "截至评估日无客户、订单、backlog、认证和收入；不能把SST TAM放入NTM基准"),
        "风险调整收益": ("C", "中性偏弱", "净现金约3.58亿美元、低收入季度FCF仍为正、non-GAAP毛利率仍在40%+，高毛利主业有修复期权", "Call IV 91.6%、TTM PE 51.89、P/S 4.93、政策和住宅光伏周期反证较重"),
        "下行保护优先": ("D", "全项目后段", "资产负债表健康、流动性强、可转债压力低", "SOXX压力窗口累计-67.78%，高IV、高估值和25D/FEOC/渠道风险使防守性很弱"),
        "估值消化优先": ("C", "中后段", "Forward PE 21.75低于高估值AI小票，若Q2/H2修复可部分消化", "基准收入不高增且当前价仍要求修复兑现；若电池MWh和微逆需求不恢复，估值消化慢"),
        "近端催化优先": ("B", "中上", "Q2 safe harbor出货、IQ9N/IQ9S、IQ Battery 10C、PWT backlog跟踪和2026年底SST demo可在1-2季验证", "SST商业收入窗口在2028以后；近期催化更多是验证而非大额收入"),
        "价格确认/动量": ("C", "中后段", "2026-06-03两周+29.86%、一月+103.90%说明资金可快速重定价", "2026-06-22收盘价52.41美元已低于6月3日69.02美元，价格确认明显回吐"),
        "激进短线": ("B", "中上", "91.6% Call IV、IQ SST新闻流、政策/税收/solar修复交易和小市值带来高beta", "高IV意味着期权成本高，且缺少SST订单会让短线交易快速回撤"),
    }

    lines: list[str] = []
    lines.append("# ENPH 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：ENPH / {TARGET_NAME}")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(comparisons)}")
    lines.append(f"公司评估文件日期范围：{date_range}")
    lines.append("日度数据日期：2026-06-22 金融数据；2026-06-03 区间涨跌；2026-06-04 SOXX 压力窗口")
    lines.append("")
    lines.append("> 口径说明：本报告只使用 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/`、`行业调研/` 和 `金融资料/` 上游资料；未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。每一行是 ENPH 与一家项目内公司 B 的二选一判断。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.append(f"- A 最占优的投资思路：{'、'.join(a_best)}。ENPH 的相对优势来自 IQ SST 远期期权、微逆/储能平台小市值重定价弹性、Q2 safe harbor 出货和高 IV 交易属性。")
    lines.append(f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。最大短板是下行保护差、6月初价格反弹回吐、住宅光伏政策/周期反证重，以及 IQ SST 目前没有客户、订单、backlog 或收入。")
    lines.append("- A 最适合的投资者画像：能承受高波动、愿意押注分布式电力电子低位修复和 IQ SST 进入 AI 数据中心电力架构的激进型资金；更像事件/右尾仓位，不像稳健核心仓位。")
    lines.append("- A 最不适合的投资者画像：重视下行保护、现金流稳定、低估值消化、确定性订单/backlog 或需要当下直接 AI 数据中心收入的资金。")
    lines.append("- 多数思路下最强反方公司：" + "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]]) + "。这些公司通常拥有更直接的 AI 主链收入、订单/RPO/backlog、电力设备交付或更强估值消化。")
    lines.append(f"- 如果只追求更高增长、更好公司，A 的总体位置：ENPH 是高弹性、低防守的中后段配置标的；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家。它可以作为 IQ SST/住宅太阳能修复期权，但不能替代 NVDA/AVGO/MU/ANET/VRT/ETN/GEV 等已经有更硬收入或订单证据的主线公司。")
    lines.append("- 后续最重要跟踪数据：Q2 2026 实际收入和 safe harbor shipments、IQ Battery MWh 是否回到150MWh+/季、PWT backlog新增与确认窗口、美国sell-through、欧洲收入、IQ9N/IQ9S商用项目、45X/FEOC/关税毛利影响、库存/应收、2026年底IQ SST demo、2027 customer pilot、客户名、认证和付费订单。")
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | ENPH |")
    lines.append(f"| 公司名称 | {TARGET_NAME} |")
    lines.append(f"| 产业链分类 | {a.get('category', '电力_发电_能源_储能')} |")
    lines.append(f"| 重要产品/业务线 | {product_text} |")
    lines.append(f"| NTM 基准收入 | {a.get('base_rev') or '12.5-14.5 亿美元'} |")
    lines.append(f"| 乐观/极度乐观收入 | 乐观：{a.get('bull_rev')}；极度乐观：{a.get('extreme_rev')} |")
    lines.append(f"| 利润和现金流结论 | 基准经营利润率：{a.get('base_margin')}；利润/现金流：{a.get('base_profit')}；{a.get('base_cash')} |")
    lines.append("| 最大传导瓶颈 | 美国住宅太阳能25D税收抵免到期后的需求断层，以及TPO/PWT safe harbor订单从订单池到2027-2030实际收入确认的节奏。 |")
    lines.append("| 最大反证 | IQ SST当前收入为0，缺少客户、订单、backlog、认证和收入确认路径；电池出货仍在100-110MWh/季附近，住宅需求和政策风险未消除。 |")
    lines.append("| 近端催化剂 | Q2 2026收入和safe harbor出货、IQ Battery MWh恢复、IQ9N/IQ9S商用项目、PWT backlog新增、45X/关税毛利修复、2026年底IQ SST demo。 |")
    lines.append("| 日度数据 | " + daily_snapshot + " |")
    lines.append("")
    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append("| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for strategy in STRATS:
        position = f"{support[strategy][1]}；评分排名 {a.get('ranks', {}).get(strategy)}/{a.get('rank_total', {}).get(strategy, len(companies))}"
        lines.append(f"| {strategy} | {a.get('tiers', {}).get(strategy, '资料不足')} | {position} | {support[strategy][2]} | {support[strategy][3]} |")
    lines.append("")
    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | 与ENPH在储能、住宅/分布式能源、逆变/备电和安装商/系统客户上存在直接或高度相邻需求池，优先比较订单、出货、毛利、客户和政策风险。 | GNRC、FLNC、TSLA | 同业证据权重最高；若B有更硬储能/备电收入和更低政策风险，可直接压过ENPH的SST期权。 |")
    lines.append("| 相邻替代 | 同属AI电力、储能、功率器件、数据中心电气或能源基础设施资金篮子，但产品或客户不完全重叠。 | BE、GEV、VST、CEG、ETN、VRT、POWI、NVTS、HUBB、POWL | 重点比较谁能把电力瓶颈更快转成订单和利润；不因ENPH有IQ SST概念就自动胜出。 |")
    lines.append("| 上下游 | B位于AI数据中心需求端、服务器/芯片/网络主链或云/IDC资本开支端，可能是ENPH IQ SST的需求背景或替代资金主线。 | NVDA、AVGO、ANET、SMCI、MSFT、AMZN、EQIX、DLR | 不把下游AI capex自动等同于ENPH收入；只有ENPH拿到客户/订单后才提高结论力度。 |")
    lines.append("| 跨赛道 | 业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。 | 半导体材料、检测、工业、软件安全等 | 默认降低结论力度；除非档位差明显，否则使用微倾向或中性。 |")
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
        need = "ENPH需要把IQ SST从demo推进到客户pilot/认证/订单/backlog，并证明Q2/H2微逆和电池收入恢复能转成利润和FCF。"
        if row_obj["relationship"] == "直接同业":
            need = "ENPH需要在储能/分布式能源同业中证明更高出货、毛利和订单质量，同时降低住宅政策与渠道风险。"
        elif row_obj["relationship"] == "上下游":
            need = "ENPH需要证明能实际捕获AI数据中心电力利润池，而不只是被AI capex叙事间接带动。"
        lines.append(f"| {index} | {row_obj['ticker']} / {row_obj['name']} | {'、'.join(wins[:6])} | {row_obj['key_reason']} | {need} |")
    lines.append("")
    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for index, row_obj in enumerate(strong_a, 1):
        wins = [strategy for strategy in STRATS if "投A" in str(row_obj[strategy])]
        need = "B需要拿出更清晰的NTM收入/利润兑现、订单或客户合同，并降低估值、现金流或资产负债表反证。"
        lines.append(f"| {index} | {row_obj['ticker']} / {row_obj['name']} | {'、'.join(wins[:6])} | {row_obj['key_reason']} | {need} |")
    lines.append("")
    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。")
    lines.append("- 公司 A 公司调研文件：`公司调研/电力_发电_能源_储能/ENPH_Enphase Energy_公司调研_2026-06-11.md`。")
    lines.append("- 关键行业资料：`行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心自备发电与微电网_2026-06-11.md`；`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`。")
    lines.append(f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 如有多份则取文件名日期最新；本次共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。")
    lines.append(f"- 公司全集最新正式评估文件清单：{file_list}")
    lines.append("- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。")
    lines.append(f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家；缺少当日价格/估值/IV 的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。")
    lines.append(f"- 公司 A 日度数据快照：{daily_snapshot}")
    lines.append("- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。")
    lines.append("- 自动化脚本：`scripts/generate_enph_company_comparison.py`。脚本复用项目内正式评估和金融资料解析函数，使用同一批公司建立全项目相对档位，并对ENPH的Safe Harbor、IQ SST、净现金、高IV、6月初反弹回吐和住宅光伏政策反证做人工校准。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 ENPH 正式评估文件")
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
                "enph_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "enph_scores": {strategy: round(float(a.get("scores", {}).get(strategy, 0)), 2) for strategy in STRATS},
                "enph_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
