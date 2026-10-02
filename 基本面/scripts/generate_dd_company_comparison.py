from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "DD"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "DD_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS

DIRECT_PEERS = {
    "CC",
    "Q",
    "ECL",
    "PNR",
    "MMM",
}
MATERIAL_ADJACENT = {
    "AJNMY",
    "APD",
    "ASGLY",
    "AXTI",
    "DHR",
    "DKILY",
    "ENTG",
    "HOCPY",
    "LIN",
    "MRAAY",
    "MTRN",
    "NDSN",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
    "TMO",
}
WATER_HEALTHCARE_ADJACENT = {"CARR", "DCI", "DOV", "FTV", "JCI", "MOD", "TT"}
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
}


def mid_growth(value: object) -> float | None:
    text = str(value).replace("−", "-").replace("～", "-").replace("—", "-").replace("–", "-")
    ranged = re.search(
        r"([+-]?)\s*(\d+(?:\.\d+)?)\s*%\s*(?:至|到|-)\s*([+-]?)\s*(\d+(?:\.\d+)?)\s*%",
        text,
    )
    if not ranged:
        ranged = re.search(r"([+-])\s*(\d+(?:\.\d+)?)\s*-\s*([+-]?)\s*(\d+(?:\.\d+)?)\s*%", text)
    if ranged:
        sign1, num1, sign2, num2 = ranged.groups()
        signed1 = -1 if sign1 == "-" else 1
        signed2 = -1 if sign2 == "-" else signed1 if sign2 == "" else 1
        return (signed1 * float(num1) + signed2 * float(num2)) / 2

    vals: list[float] = []
    for match in re.finditer(r"([+-]?)\s*(\d+(?:\.\d+)?)\s*%", text):
        vals.append((-1 if match.group(1) == "-" else 1) * float(match.group(2)))
    return sum(vals) / len(vals) if vals else None


def fix_growth_ranges(companies: dict[str, dict[str, object]]) -> None:
    for company in companies.values():
        for scenario, field in [
            ("bear", "bear_growth"),
            ("base", "base_growth"),
            ("bull", "bull_growth"),
            ("extreme", "extreme_growth"),
        ]:
            record = company.get("scenarios", {}).get(scenario, {})  # type: ignore[union-attr]
            for key, value in record.items():
                if "增速" in key or "绝对" in key:
                    parsed = mid_growth(value)
                    if parsed is not None:
                        company[field] = parsed
                    break


def supplement_dd_finance(companies: dict[str, dict[str, object]]) -> None:
    """DD was added after the latest daily financial snapshot; keep the gap explicit."""
    dd = companies[TARGET]
    if dd.get("fin") and dd["fin"].get("price"):  # type: ignore[index,union-attr]
        return
    dd["fin"] = {
        "category": "半导体材料_化学品_基板",
        "name": "DuPont de Nemours",
        "price_date": "2026-06-23",
        "price": 48.19,
        "market_cap_b": 19.89,
        "ttm_pe": None,
        "forward_pe": 20.0,
        "ps": 2.8,
        "pb": None,
        "ev_ebitda": 12.5,
        "eps": -0.07,
        "call_iv": None,
        "put_iv": None,
        "source_timestamp": "2026-06-23 11:22:17 UTC",
        "valuation_check": "supplemental; daily finance 2026-06-22 missing DD",
        "notes": "DD不在金融资料/每日金融数据_2026-06-22.md；价格和市值用2026-06-23 web finance/company调研补充，IV缺失。",
    }
    dd["mom2"] = {}
    dd["mom1"] = {}
    dd["soxx"] = {}


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    for strategy in STRATS:
        ordered = sorted(companies.items(), key=lambda item: item[1]["scores"][strategy], reverse=True)  # type: ignore[index]
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
        if not company["fin"].get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company["tiers"][strategy] = "资料不足"  # type: ignore[index]


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    fix_growth_ranges(companies)
    supplement_dd_finance(companies)
    base.score_companies(companies)

    # Post-Qnity DD is a quality water/healthcare/specialty-materials platform:
    # good NTM evidence and balance-sheet quality, but no direct AI-hardware right tail.
    dd = companies[TARGET]
    overrides = {
        "NTM兑现优先": 70.0,
        "右尾弹性优先": 48.0,
        "风险调整收益": 63.0,
        "下行保护优先": 70.0,
        "估值消化优先": 61.0,
        "近端催化优先": 56.0,
        "价格确认/动量": 42.0,
        "激进短线": 41.0,
    }
    for strategy, score in overrides.items():
        dd["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in MATERIAL_ADJACENT or category == "半导体材料_化学品_基板":
        return "相邻替代"
    if ticker in WATER_HEALTHCARE_ADJACENT:
        return "相邻替代"
    if category in SEMI_DOWNSTREAM_CATS or category in DC_DOWNSTREAM_CATS:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A有FY2026指引和HWT收入锚",
            "右尾弹性优先": "A有Water/Healthcare上修期权",
            "风险调整收益": "A低杠杆和现金流质量更稳",
            "下行保护优先": "A HWT高margin且净杠杆低",
            "估值消化优先": "A中速利润可覆盖约20x FwdPE",
            "近端催化优先": "A有Q2/Q3 Water和HWT验证",
            "价格确认/动量": "B价格反证更弱于A",
            "激进短线": "A低预期修复赔率略好",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B订单/RPO或收入兑现更硬",
            "右尾弹性优先": "B直接AI右尾或小基数更大",
            "风险调整收益": "B上行/下行组合更优",
            "下行保护优先": "B现金流或压力期更安全",
            "估值消化优先": "B增长更能消化估值",
            "近端催化优先": "B近端订单/产品催化更强",
            "价格确认/动量": "B价格趋势确认更强",
            "激进短线": "B高beta和资金关注更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "质量、估值和兑现接近"
    return "档位接近需再验证"


def label_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    at = a["tiers"][strategy]  # type: ignore[index]
    bt = b["tiers"][strategy]  # type: ignore[index]
    if at == "资料不足" or bt == "资料不足":
        if at == "资料不足" and bt == "资料不足":
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    tier_diff = TIER_VAL[at] - TIER_VAL[bt]  # type: ignore[index,operator]
    score_diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
    if score_diff >= 28 or tier_diff >= 3:
        tag = "强烈建议投A"
    elif score_diff >= 13 or tier_diff >= 2:
        tag = "建议投A"
    elif score_diff >= 5:
        tag = "微倾向投A"
    elif score_diff <= -28 or tier_diff <= -3:
        tag = "强烈建议投B"
    elif score_diff <= -13 or tier_diff <= -2:
        tag = "建议投B"
    elif score_diff <= -5:
        tag = "微倾向投B"
    else:
        tag = "中性"

    if rel == "跨赛道":
        if tag == "强烈建议投A" and not (abs(score_diff) >= 38 or abs(tier_diff) >= 4):
            tag = "建议投A"
        elif tag == "强烈建议投B" and not (abs(score_diff) >= 38 or abs(tier_diff) >= 4):
            tag = "建议投B"
        elif tag == "建议投A" and abs(score_diff) < 18 and abs(tier_diff) < 2:
            tag = "微倾向投A"
        elif tag == "建议投B" and abs(score_diff) < 18 and abs(tier_diff) < 2:
            tag = "微倾向投B"
    if rel == "直接同业" and abs(score_diff) >= 18 and tag.startswith("建议"):
        tag = "强烈" + tag
    return tag


def cell_for(a: dict[str, object], b: dict[str, object], strategy: str, rel: str) -> str:
    tag = label_for(a, b, strategy, rel)
    return f"{tag}：{reason_for(strategy, tag, rel)}"


def direction_counts(cells: list[str]) -> tuple[int, int, int]:
    a_count = b_count = neutral = 0
    for cell in cells:
        tag = base.tag_in_cell(cell) or ""
        if tag.endswith("投A"):
            a_count += 1
        elif tag.endswith("投B"):
            b_count += 1
        else:
            neutral += 1
    return a_count, b_count, neutral


def final_choice(a: dict[str, object], b: dict[str, object], cells: list[str]) -> str:
    a_count, b_count, _neutral = direction_counts(cells)
    if a_count > b_count:
        return "A"
    if b_count > a_count:
        return "B"
    quality_weight = (
        a["scores"]["风险调整收益"]
        + a["scores"]["下行保护优先"] * 0.8
        + a["scores"]["估值消化优先"]
        + a["scores"]["NTM兑现优先"] * 0.7
        - b["scores"]["风险调整收益"]
        - b["scores"]["下行保护优先"] * 0.8
        - b["scores"]["估值消化优先"]
        - b["scores"]["NTM兑现优先"] * 0.7
    )
    return "A" if quality_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 12:  # type: ignore[index,operator]
            return "DD的HWT利润率、低净杠杆和现金流底座比B更适合防守配置。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "DD有FY2026指引、HWT/Healthcare收入锚，B的NTM兑现证据更弱。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
            return "DD的约20x Forward PE和中速EBITDA路径比B更容易消化。"
        return "DD在质量、防守和估值消化上略胜，B的增长证据不足以覆盖反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']}的直接AI收入、小基数或平台型右尾明显强于DD。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']}的订单/RPO/backlog或收入确认证据比DD更硬。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']}的价格确认和资金偏好明显强于DD。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']}的增长和估值匹配度优于DD。"
    return f"{b['ticker']}在多数投资思路下比DD更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong, b_strong, close = [], [], []
    for strategy in STRATS:
        diff = a["scores"][strategy] - b["scores"][strategy]  # type: ignore[index,operator]
        label = strategy.replace("优先", "").replace("/动量", "动量")
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
    output: list[dict[str, object]] = []
    for ticker in sorted(companies):
        if ticker == TARGET:
            continue
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(a, b, strategy, rel) for strategy in STRATS]
        a_count, b_count, neutral = direction_counts(cells)
        final = final_choice(a, b, cells)
        output.append(
            {
                "ticker": ticker,
                "b": b,
                "rel": rel,
                "cells": cells,
                "ac": a_count,
                "bc": b_count,
                "nc": neutral,
                "final": final,
                "summary": grade_diff_summary(a, b),
                "reason": key_reason(a, b, final),
            }
        )
    return output


def fmt_num(value: object, suffix: str = "", precision: int = 2) -> str:
    if value is None:
        return "缺失"
    if isinstance(value, float):
        return f"{value:.{precision}f}{suffix}"
    return f"{value}{suffix}"


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    return f"${float(value):.2f}B"


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    return f"{float(value):.2f}%"


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(company_dates)} 至 {max(company_dates)}"
    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][base.tag_in_cell(cell)] += 1
    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b = sorted(
        comparisons,
        key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["下行保护优先"] - x["b"]["scores"]["下行保护优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3][:45]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3][:45]  # type: ignore[operator]
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker]["fin"] or not companies[ticker]["fin"].get("price")  # type: ignore[union-attr]
    ]

    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    daily_snapshot = (
        f"DD未纳入2026-06-22正式每日金融数据；补充快照为2026-06-23价格 `{fmt_num(fin.get('price'))}`，"
        f"市值 `{fmt_b(fin.get('market_cap_b'))}`，Forward PE 约 `{fmt_num(fin.get('forward_pe'))}`，"
        f"P/S 约 `{fmt_num(fin.get('ps'))}`，EV/EBITDA 约 `{fmt_num(fin.get('ev_ebitda'))}`；"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`、Put IV `{fmt_pct(fin.get('put_iv'))}`缺失；"
        f"2026-06-03正式两周/一月区间涨跌为 `{fmt_pct(mom2.get('mom2w'))}`/`{fmt_pct(mom1.get('mom1m'))}`，"
        f"2026-06-04 SOXX压力窗口为 `{fmt_pct(soxx.get('soxx_cum'))}`。"
    )

    product_names = []
    for product in a["products"]:  # type: ignore[index]
        product_name = str(product[0]).split("：")[0]
        if "原 Electronics" in product_name or "Aramids" in product_name:
            continue
        product_names.append(product_name)
        if len(product_names) >= 6:
            break

    support = {
        "NTM兑现优先": (
            "FY2026收入指引`$7.155-7.215B`、Operating EBITDA `$1.730-1.760B`，HWT和Healthcare有A/B级收入锚",
            "公司级增速主要是中个位数，Water backlog、AI/DC收入和客户项目未披露",
        ),
        "右尾弹性优先": (
            "Water RO/UF/IX/EDI、微电子高纯水、数据中心回用水和Healthcare项目可形成中长期上修",
            "Qnity已分拆，旧DuPont电子/先进封装材料不进入DD，右尾明显小于AI主链",
        ),
        "风险调整收益": (
            "净债务约`1.4x 2026E EBITDA`、HWT 30%+ margin、FCF为正，估值约20x Forward PE",
            "PFAS/环境尾部、GAAP利润特殊项、Building/DI周期和AI收入不透明限制赔率",
        ),
        "下行保护优先": (
            "Healthcare/Water替换需求、低杠杆、现金流和高margin分部提供防守底座",
            "化工法律尾部和建筑/工业周期仍会压制；本次正式IV与压力窗口数据缺失",
        ),
        "估值消化优先": (
            "中速收入+Operating EBITDA路径清楚，Forward PE约20x、PS约2.8x未按AI高倍数定价",
            "增长率不高，若Water没有订单证据或DI继续拖累，估值难上移",
        ),
        "近端催化优先": (
            "Q2/Q3收入、HWT margin、Water organic恢复、Healthcare高个位数、回购和分拆后现金流可验证",
            "缺少明确AI fab/DC水处理订单、backlog或大客户认证，催化强度弱于AI硬件链",
        ),
        "价格确认/动量": (
            "2026-06-23补充价格约`$48.19`，估值未显著泡沫化",
            "DD缺少正式区间涨跌和SOXX压力窗口数据；市场尚未用价格确认AI水处理叙事",
        ),
        "激进短线": (
            "低预期、组合简化和Water/Healthcare新闻流可能带来修复交易",
            "无高IV/强动量/直接AI订单，短线进攻性显著弱于小基数AI主链",
        ),
    }

    out: list[str] = []
    out += [
        "# DD 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：DD / DuPont de Nemours",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV主体为 `金融资料/每日金融数据/每日金融数据_2026-06-22.md`；DD因未纳入该日度文件，价格/市值用2026-06-23补充快照；区间涨跌为2026-06-03；SOXX压力窗口为2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 DD vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；Qnity已分拆，旧DuPont电子材料不计入当前DD。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。DD 的优势集中在 HWT/Healthcare 经营质量、现金流、低杠杆和估值消化，适合作为中低速高质量材料/水处理资产。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是 Qnity 分拆后缺少直接 AI 半导体材料右尾，Water/数据中心收入未披露订单，正式动量/IV数据也缺失。",
        "- A 最适合的投资者画像：重视质量、现金流、HWT 30%+ EBITDA margin、Water/Healthcare长期替换需求，并愿意买“AI水处理期权但不按AI主链估值”的配置者。",
        "- A 最不适合的投资者画像：只追求高增长大右尾、短线强动量、AI芯片/光互联直接订单、极高beta或强催化的进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常有更直接AI收入化、更硬订单/RPO/backlog、更强价格确认或更高短线弹性。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：DD 不是项目内高增长核心，而是中速质量型材料/水处理资产；在防守、质量和估值消化上可打败一批高反证公司，但面对AI主链、前道设备、光互联、云算力和部分电力/机电强标的，多数思路通常落后。",
        "- 后续最重要跟踪数据：Q2/Q3 net sales、organic sales、HWT和DI分部收入/margin、Water是否恢复中个位数以上、management是否点名microelectronics/industrial water、Water客户项目/backlog/订单、Healthcare项目放量、Building下滑是否收窄、FCF conversion、PFAS/环境现金支出和Qnity分拆后资本回报。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "DD"]),
        base.row(["公司名称", "DuPont de Nemours"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`$7.20-7.45B`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "Water从AI fab/微电子/数据中心水需求转成DD可确认收入的路径不透明；公司未披露Water backlog、AI/DC收入、客户项目或交付时间表。"]),
        base.row(["最大反证", "Qnity已分拆，旧电子材料和先进封装材料不属于DD；Building/DI周期、PFAS/环境现金流和特殊项会抵消Water/Healthcare质量。"]),
        base.row(["近端催化剂", "Q2/Q3收入和Operating EBITDA、HWT margin、Water organic恢复、Healthcare高个位数、DI/Building拖累收窄、FCF conversion和Water项目披露。"]),
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
        base.row(["直接同业", "与DD在特种化学品、水处理、过滤、医疗/工业材料或原DuPont电子材料资金记忆上重叠，优先比较收入兑现、margin、订单、法律尾部和估值。", "Q、CC、ECL、PNR、MMM", "同业证据权重最高；Qnity直接承接旧电子材料时，DD的AI右尾必须明显降权。"]),
        base.row(["相邻替代", "同属材料、工业气体、电子化学品、半导体材料、生命科学/水处理或AI基础设施资金篮子，但产品不完全竞争。", "APD、LIN、ENTG、SHECY、ASGLY、DHR、TMO、TT", "重点比较增长质量、估值消化、下行保护和可见催化；不因DD质量高就忽略成长差距。"]),
        base.row(["上下游", "B处在DD可服务的半导体制造、先进封装、AI芯片、光互联、服务器、云/IDC或数据中心机电链条。", "TSM、ASML、AMAT、NVDA、AVGO、VRT、MSFT、AMZN", "不把下游AI capex直接映射为DD收入；也不把上游水处理材料自动等同更好，核心看利润捕获和订单。"]),
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
                    base.category_short(str(b["category"])),  # type: ignore[index]
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],  # type: ignore[list-item]
                    majority(comparison["ac"], comparison["bc"], comparison["nc"]),  # type: ignore[arg-type]
                    comparison["final"],
                    comparison["reason"],
                ]
            )
        )

    out += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        out.append(base.row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要DD披露Water/微电子/数据中心水处理客户、订单金额、backlog和交付窗口，并证明HWT增长能抵消DI/Building拖累。"
        if comparison["rel"] == "直接同业":
            need = "需要DD在Water/Healthcare/工业材料同业中拿出更高收入增速、利润率和现金流证据，并降低PFAS/周期反证。"
        elif comparison["rel"] == "上下游":
            need = "需要DD证明其膜、树脂、过滤或医疗材料能捕获下游AI/半导体利润池，而非仅小额间接受益。"
        elif comparison["rel"] == "跨赛道":
            need = "需要DD用更硬的利润/现金流兑现或Water订单抵消跨赛道公司的高增长和强动量。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B提高收入确认、利润/现金流质量或估值消化能力，或出现明确订单/指引上修。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要B把右尾叙事转成可确认收入和利润，并降低估值、波动或资产负债表反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/半导体材料_化学品_基板/DD_DuPont_de_Nemours_公司调研_2026-06-23.md`。",
        "- 关键行业资料：`行业调研/AI园区电力_机电_冷却/行业调研_冷却液、水处理、过滤与制冷剂_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体高纯水、气体与化学流体系统_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装湿化学与表面处理材料_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_硅片、光刻胶与前道材料_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；DD不在该日度文件内，已用2026-06-23补充价格/估值快照，但IV、区间涨跌和SOXX压力窗口仍按缺失/保守口径处理。缺少当日价格/估值/IV 的其他公司为 {('、'.join([x for x in missing_fin if x != TARGET]) if [x for x in missing_fin if x != TARGET] else '无')}。",
        f"- 公司 A 日度/补充数据摘录：{daily_snapshot}",
        "- 外部补充行情来源：DD web finance quote，2026-06-23 11:22:17 UTC，价格 `$48.19`、市值约 `$19.89B`；参考链接：`https://finance.yahoo.com/quote/DD`。公司调研文件也记录了2026-06-23约`$48.19`股价和约`$19.9B`市值。",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_dd_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对百分比区间做同号区间修正；对DD的Qnity分拆、Water/Healthcare质量、AI水处理期权、缺失正式日度行情字段做人工校准后建档。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    companies = base.build_companies()
    supplement_dd_finance(companies)
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "dd_tiers": companies[TARGET]["tiers"],
        "dd_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
        "dd_ranks": companies[TARGET]["ranks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
