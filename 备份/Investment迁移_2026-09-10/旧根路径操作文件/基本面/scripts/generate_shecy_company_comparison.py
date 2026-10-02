from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_entg_company_comparison as framework


TARGET = "SHECY"
TARGET_NAME = "Shin-Etsu Chemical 信越化学"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "SHECY_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_MATERIAL_PEERS = {
    "AJNMY",
    "ASGLY",
    "AXTI",
    "DD",
    "DKILY",
    "ENTG",
    "HOCPY",
    "MTRN",
    "Q",
    "ROG",
    "SMTOY",
    "SOMMY",
}
MATERIAL_ADJACENT = {
    "APD",
    "CC",
    "DHR",
    "ECL",
    "LIN",
    "MMM",
    "NDSN",
    "TMO",
}
SEMI_DOWNSTREAM_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "封测_检测_计量_光罩",
    "晶圆制造_前道设备",
    "云算力_IDC_AI软件平台",
}
POWER_THERMAL_RELATED = {
    "ABBNY",
    "AEIS",
    "ATKR",
    "BE",
    "CEG",
    "ETN",
    "GEV",
    "HUBB",
    "IFNNY",
    "MPWR",
    "NVT",
    "POWL",
    "VRT",
    "VST",
}


SHECY_SCORES = {
    # The project-wide model under-ranks large high-quality Japanese materials
    # names because it rewards pure growth. SHECY gets explicit calibration for
    # high evidence quality, net cash and FCF, while keeping growth/short-term
    # aggression below AI main-chain leaders.
    "NTM兑现优先": 70.0,
    "右尾弹性优先": 63.0,
    "风险调整收益": 60.0,
    "下行保护优先": 78.0,
    "估值消化优先": 60.0,
    "近端催化优先": 59.0,
    # 2026-06-03 interval files showed positive momentum, but 2026-06-22
    # price had pulled back from the 2026-06-03 close, so do not over-credit.
    "价格确认/动量": 54.0,
    "激进短线": 60.0,
}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    framework.score_companies(companies)
    target = companies[TARGET]
    for strategy, score in SHECY_SCORES.items():
        target.setdefault("scores", {})[strategy] = score  # type: ignore[index]
    framework.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    if ticker in DIRECT_MATERIAL_PEERS:
        return "直接同业"
    if ticker in MATERIAL_ADJACENT or category == "半导体材料_化学品_基板":
        return "相邻替代"
    if category in SEMI_DOWNSTREAM_CATS:
        return "上下游"
    if ticker in POWER_THERMAL_RELATED:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, b: dict[str, object], rel: str) -> str:
    ticker = str(b.get("ticker", ""))
    category = str(b.get("category", ""))
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A分部数据和材料订单线索更稳",
            "右尾弹性优先": "A硅片/光刻材料右尾更清楚",
            "风险调整收益": "A净现金、FCF和反证更均衡",
            "下行保护优先": "A净现金和多元材料底盘更稳",
            "估值消化优先": "A电子材料利润可消化估值",
            "近端催化优先": "A有Isesaki/wafer/PVC验证点",
            "价格确认/动量": "A材料重估仍有价格支撑",
            "激进短线": "A材料题材优于弱弹性B",
        }[strategy]

    if tag.endswith("投B"):
        if rel == "直接同业":
            return {
                "NTM兑现优先": "B同业订单或分部增速更硬",
                "右尾弹性优先": "B同业小基数或材料右尾更大",
                "风险调整收益": "B同业估值/上行组合更优",
                "下行保护优先": "B同业现金流或低波动更稳",
                "估值消化优先": "B同业增长更能覆盖倍数",
                "近端催化优先": "B客户/新品节点更近",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业短线弹性更高",
            }[strategy]
        if category in HIGH_GROWTH_CATS:
            return {
                "NTM兑现优先": "B直接AI收入兑现更短链",
                "右尾弹性优先": "B直接AI右尾和弹性更大",
                "风险调整收益": "B上行空间更能覆盖风险",
                "下行保护优先": "B需求能见度或现金流更强",
                "估值消化优先": "B高增长更能消化估值",
                "近端催化优先": "B订单/RPO/产品催化更硬",
                "价格确认/动量": "B资金趋势确认更强",
                "激进短线": "B高beta叙事更适合进攻",
            }[strategy]
        if category in INFRA_CATS or ticker in POWER_THERMAL_RELATED:
            return {
                "NTM兑现优先": "B订单/backlog兑现更清楚",
                "右尾弹性优先": "B AI电力机电右尾更直接",
                "风险调整收益": "B订单和估值组合更优",
                "下行保护优先": "B现金流或防御属性更强",
                "估值消化优先": "B backlog更能覆盖估值",
                "近端催化优先": "B项目/FID/产能催化更近",
                "价格确认/动量": "B价格趋势确认更强",
                "激进短线": "B事件弹性和关注度更高",
            }[strategy]
        return {
            "NTM兑现优先": "B收入兑现证据更强",
            "右尾弹性优先": "B右尾空间更大",
            "风险调整收益": "B风险收益组合更优",
            "下行保护优先": "B下行缓冲更强",
            "估值消化优先": "B增长更能消化估值",
            "近端催化优先": "B近端催化更明确",
            "价格确认/动量": "B价格确认更强",
            "激进短线": "B短线弹性更强",
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

    score_diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
    tier_diff = TIER_VAL[at] - TIER_VAL[bt]  # type: ignore[index,operator]
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
    return f"{tag}：{reason_for(strategy, tag, b, rel)}"


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
        float(a["scores"]["NTM兑现优先"]) * 0.8
        + float(a["scores"]["风险调整收益"]) * 0.9
        + float(a["scores"]["下行保护优先"]) * 0.6
        + float(a["scores"]["估值消化优先"]) * 0.6
        - float(b["scores"]["NTM兑现优先"]) * 0.8
        - float(b["scores"]["风险调整收益"]) * 0.9
        - float(b["scores"]["下行保护优先"]) * 0.6
        - float(b["scores"]["估值消化优先"]) * 0.6
    )
    return "A" if quality_weight >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if float(a["scores"]["风险调整收益"]) - float(b["scores"]["风险调整收益"]) > 10:
            return "SHECY的净现金、FCF和材料质量使风险调整收益更好。"
        if float(a["scores"]["下行保护优先"]) - float(b["scores"]["下行保护优先"]) > 10:
            return "SHECY资产负债表和多元材料底盘提供更好下行保护。"
        if float(a["scores"]["NTM兑现优先"]) - float(b["scores"]["NTM兑现优先"]) > 8:
            return "SHECY电子材料和PVC修复路径比B的NTM兑现更清楚。"
        return "SHECY在质量、现金流和材料壁垒上略胜，B的右尾不足以覆盖反证。"

    if float(b["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]) > 18:
        return f"{b['ticker']}的直接AI收入、小基数或平台型右尾明显强于SHECY。"
    if float(b["scores"]["NTM兑现优先"]) - float(a["scores"]["NTM兑现优先"]) > 12:
        return f"{b['ticker']}的订单/RPO/backlog或收入兑现比SHECY更硬。"
    if float(b["scores"]["近端催化优先"]) - float(a["scores"]["近端催化优先"]) > 12:
        return f"{b['ticker']}的近端订单、产能或产品催化更明确。"
    if float(b["scores"]["价格确认/动量"]) - float(a["scores"]["价格确认/动量"]) > 12:
        return f"{b['ticker']}的价格确认和资金趋势明显强于SHECY。"
    return f"{b['ticker']}在多数投资思路下比SHECY更符合项目内资金配置目标。"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong, b_strong, close = [], [], []
    for strategy in STRATS:
        diff = float(a["scores"][strategy]) - float(b["scores"][strategy])  # type: ignore[index]
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
    rows: list[dict[str, object]] = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        cells = [cell_for(a, b, strategy, rel) for strategy in STRATS]
        a_count, b_count, neutral = direction_counts(cells)
        final = final_choice(a, b, cells)
        rows.append(
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
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return sorted(rows, key=lambda item: (rel_order.get(str(item["rel"]), 9), str(item["ticker"])))


def fmt_num(value: object, precision: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{precision}f}"
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
        return f"{float(value):.2f}%"
    except Exception:
        return "缺失"


def majority(a_count: int, b_count: int, neutral: int) -> str:
    return f"A {a_count} / B {b_count} / 中性 {neutral}"


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = sorted(str(company["date"]) for company in companies.values())
    date_range = f"{company_dates[0]} 至 {company_dates[-1]}"

    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][base.tag_in_cell(cell)] += 1
    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]

    strong_b = sorted(
        comparisons,
        key=lambda row: (
            int(row["bc"]) - int(row["ac"]),
            float(row["b"]["scores"]["右尾弹性优先"]) - float(a["scores"]["右尾弹性优先"]),  # type: ignore[index]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda row: (
            int(row["ac"]) - int(row["bc"]),
            float(a["scores"]["风险调整收益"]) - float(row["b"]["scores"]["风险调整收益"]),  # type: ignore[index]
        ),
        reverse=True,
    )
    strong_b_rows = [row for row in strong_b if int(row["bc"]) >= 5 and int(row["bc"]) - int(row["ac"]) >= 3][:45]
    strong_a_rows = [row for row in strong_a if int(row["ac"]) >= 5 and int(row["ac"]) - int(row["bc"]) >= 3][:45]
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker].get("fin") or not companies[ticker].get("fin", {}).get("price")  # type: ignore[union-attr]
    ]

    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {
        strategy: f"第 {a['ranks'][strategy]}/{n}，{a['tiers'][strategy]} 档"  # type: ignore[index]
        for strategy in STRATS
    }

    fin = a["fin"]  # type: ignore[assignment]
    mom2 = a["mom2"]  # type: ignore[assignment]
    mom1 = a["mom1"]  # type: ignore[assignment]
    soxx = a["soxx"]  # type: ignore[assignment]
    price = fin.get("price")
    close_0603 = mom2.get("latest_close")
    post_interval = "缺失"
    if price is not None and close_0603:
        post_interval = fmt_pct((float(price) / float(close_0603) - 1) * 100)
    daily_snapshot = (
        f"2026-06-22收盘价 `{fmt_num(fin.get('price'))}`，市值 `{fmt_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `{fmt_num(fin.get('ttm_pe'))}`，Forward PE `{fmt_num(fin.get('forward_pe'))}`，"
        f"源字段P/S `{fmt_num(fin.get('ps'), 4)}`（交易货币/财报货币不一致，P/S校验bad；公司调研口径约`5.3x`），"
        f"P/B `{fmt_num(fin.get('pb'))}`，EV/EBITDA `{fmt_num(fin.get('ev_ebitda'))}`，"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`，Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03过去两周 `{fmt_pct(mom2.get('mom2w'))}`，过去一月 `{fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04三段SOXX压力窗口累计 `{fmt_pct(soxx.get('soxx_cum'))}`；"
        f"从2026-06-03收盘到2026-06-22收盘约 `{post_interval}`。"
    )

    product_names = []
    for product in a["products"]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])
        if len(product_names) >= 8:
            break

    support = {
        "NTM兑现优先": (
            "FY2026净销售`2.574万亿日元`、营业利润`6,352亿日元`；NTM基准收入`2.70-2.78万亿日元`，电子材料订单和PVC修复提供兑现锚",
            "FY2027正式收入/利润指引缺失，产品级backlog/bookings和客户名单不披露，基准增速仅`+5%-+8%`",
        ),
        "右尾弹性优先": (
            "300mm高端硅片、EUV/ArF光刻胶、mask blanks、封装胶材/TIM和QST GaN形成材料长右尾",
            "大集团基数和PVC/普通化工稀释明显，极度乐观`+13%-+18%`可信度低，远不如直接AI主链",
        ),
        "风险调整收益": (
            "FY2026 OCF`7,126亿日元`、基准FCF仍为正，净现金资产负债表和高壁垒材料组合降低永久损失风险",
            "2026-06-22 TTM PE`28.82x`且Forward PE缺失；若电子材料订单未转收入，估值缺少快速消化支撑",
        ),
        "下行保护优先": (
            "净现金、高流动性、分部多元、电子材料客户认证和PVC现金流底盘提供缓冲",
            "SOXX三段压力窗口累计`-25.75%`不算顶级防御，PVC/烧碱和半导体库存仍有周期反证",
        ),
        "估值消化优先": (
            "基准营业利润`6,900-7,300亿日元`、利润增速高于收入增速，电子材料mix与PVC利润修复可部分覆盖估值",
            "Forward PE缺失，ADR P/S字段因币种不一致不可直接用；当前P/S约`5x`已反映材料溢价",
        ),
        "近端催化优先": (
            "Isesaki光刻材料基地、300mm客户追加订单/新LTA兴趣、silicone提价和PVC提价可在1-2季验证",
            "缺少明确财报指引上修、产品级订单金额和客户认证时间表，近端催化弱于订单/RPO型公司",
        ),
        "价格确认/动量": (
            "截至2026-06-03两周`+9.95%`、一月`+7.36%`，材料重估已有阶段性价格确认",
            "2026-06-22价格`22.77`低于6月3日收盘`24.20`约`-5.91%`，动量已回吐且OTC/ADR流动性需折扣",
        ),
        "激进短线": (
            "材料长右尾、光刻/硅片/TIM/QST叙事和净现金质量使其强于弱题材材料股",
            "无期权链/IV、OTC ADR流动性弱、短线爆发力和资金关注度低于高beta AI芯片/光互联/电力股",
        ),
    }

    lines: list[str] = []
    lines += [
        "# SHECY 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：SHECY / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV为2026-06-22；两周/一月区间涨跌为2026-06-03；SOXX压力窗口为2026-06-04。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 SHECY vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；SHECY 的 AI 暴露只按高端硅片、光刻材料、mask blanks、封装材料/TIM 和QST GaN等可收入化材料链处理，不把AI数据中心CapEx直接并入公司收入。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。SHECY 的相对优势集中在风险调整收益、下行保护和NTM质量：净现金、正FCF、高壁垒材料认证和分部利润质量，使它比多数弱盈利、高估值或订单不透明公司更适合稳健配置。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是近端催化、激进短线和右尾弹性：SHECY不是直接AI芯片/服务器/光模块公司，FY2027指引和产品级订单缺失，OTC ADR也没有可用近月IV。",
        "- A 最适合的投资者画像：重视半导体材料稀缺性、现金流、净现金、低永久损失概率和中期电子材料修复的配置者；可作为AI硬件组合中的低beta材料底仓。",
        "- A 最不适合的投资者画像：只追求1-2个季度订单/RPO爆发、直接AI收入高增长、价格强趋势和高IV短线进攻的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(row['ticker']) for row in strong_b_rows[:10]])}。这些公司通常具备更直接AI收入、更高右尾、更硬订单/RPO/backlog或更强价格确认。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：SHECY是项目内高质量、稳健型半导体材料龙头，但不是全项目增长冠军；它能压过多数低质量、弱现金流或估值难消化公司，面对NVDA/AVGO/MU/TSM/高端光互联/NeoCloud/强电力机电等直接AI主链通常落后。",
        "- 后续最重要跟踪数据：Electronics Materials收入YoY和利润率、300mm wafer客户追加订单和新LTA、Isesaki光刻材料利用率、photoresist环比、Infrastructure Materials利润率和北美PVC/烧碱价格、silicone提价接受度、TIM/underfill客户design-in、QST GaN客户pilot、FY2027正式指引和FCF。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "SHECY"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`2.70-2.78万亿日元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "公司不披露产品级backlog/bookings或客户名单，300mm wafer、photoresist、mask blanks和TIM从客户需求到收入确认仍需LTA、库存、良率、认证和交付节奏验证。"]),
        base.row(["最大反证", "AI相关产品约15%仍被PVC/Functional/普通材料大基数稀释；FY2027正式指引缺失，且6月22日价格已从6月初回落。"]),
        base.row(["近端催化剂", "300mm wafer追加订单与新LTA兴趣、Isesaki光刻材料爬坡、PVC/烧碱提价、silicone全线提价、FY2027指引、TIM/underfill或QST GaN客户验证。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        lines.append(base.row([strategy, a["tiers"][strategy], rank_text[strategy], support[strategy][0], support[strategy][1]]))  # type: ignore[index]

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与SHECY在半导体材料、硅片/基板、光刻材料、mask blanks、封装材料、TIM、有机硅或电子化学品需求池重叠，优先比较客户认证、收入兑现、分部利润率、产品代际和估值。", "Q、ENTG、HOCPY、ASGLY、SOMMY、AJNMY、DKILY、DD、ROG", "同业证据权重最高；若B在订单、分部增速、客户认证或估值消化上明显更强，可直接压过SHECY。"]),
        base.row(["相邻替代", "同属材料、工业气体、工业化学品、生命科学工具或AI基础设施资金篮子，但产品不完全竞争；回答资金只能买一个时谁的增长质量和赔率更好。", "APD、LIN、ECL、NDSN、DHR、TMO、VRT、ETN、GEV", "默认看增长质量、现金流、估值消化和近端催化；不因材料属性或AI主题相近而自动胜出。"]),
        base.row(["上下游", "B处于SHECY材料需求链的晶圆制造、前道设备、封测、AI芯片、光互联、服务器、云算力、功率/电力或热管理下游。", "TSM、ASML、AMAT、NVDA、MU、ANET、SMCI、MSFT、VRT", "不把下游AI收入规模等同于SHECY机会，重点看SHECY能否实际捕获材料端利润池。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "RKLB、TSLA、CRWD、MSI、CAT", "默认降低结论力度；除非档位差明显，否则优先微倾向或中性。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]

    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    lines.append(base.row(headers))
    lines.append(base.row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for index, comparison in enumerate(comparisons, start=1):
        b = comparison["b"]
        lines.append(
            base.row(
                [
                    index,
                    base.short_name(b),  # type: ignore[arg-type]
                    base.category_short(str(b.get("category", ""))),  # type: ignore[union-attr]
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],  # type: ignore[list-item]
                    majority(int(comparison["ac"]), int(comparison["bc"]), int(comparison["nc"])),
                    comparison["final"],
                    comparison["reason"],
                ]
            )
        )

    lines += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        lines.append(base.row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    lines += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要SHECY把先进硅片、光刻材料、mask blanks、TIM/underfill从订单线索转成分部增速、产品收入和利润率上修。"
        if comparison["rel"] == "直接同业":
            need = "需要SHECY在直接材料同业中证明更高客户份额、更强LTA/订单、更快收入确认和更低估值反证。"
        elif comparison["rel"] == "上下游":
            need = "需要SHECY证明能实际捕获下游AI芯片/晶圆制造/云算力利润池，而不是只有间接受益。"
        elif comparison["rel"] == "跨赛道":
            need = "需要SHECY用更强现金流、价格确认和估值消化抵消跨赛道标的的高增长或防守属性。"
        lines.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    lines += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B提高NTM收入确认、利润/现金流质量和估值消化能力，或给出明确订单/指引上修。"
        if float(b["scores"]["右尾弹性优先"]) > float(a["scores"]["右尾弹性优先"]):  # type: ignore[index]
            need = "需要B把右尾叙事转成可确认收入和利润，并降低估值、波动或资产负债表反证。"
        lines.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/半导体材料_化学品_基板/SHECY_Shin-Etsu_Chemical_信越化学_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/晶圆制造_设备_材料_测试/行业调研_硅片、光刻胶与前道材料_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_高端光罩与先进封装掩模_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_先进封装材料与热界面材料_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_液冷小组件与流体控制_2026-06-10.md`；`行业调研/产业背景/AI产业链瓶颈与反证指标总表_2026-06-10.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV或正式金融行的公司为 {('、'.join(missing_fin) if missing_fin else '无')}。新增评估日期晚于金融快照或金融源缺失的公司，在估值、价格确认和激进短线列按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 外部核验来源：[Shin-Etsu Chemical Investors](https://www.shinetsu.co.jp/en/ir/)；[Shin-Etsu Financial Data](https://www.shinetsu.co.jp/en/ir/ir-data/ir-results/)；[Yahoo Finance SHECY quote](https://finance.yahoo.com/quote/SHECY/)；[OTC Markets SHECY quote](https://www.otcmarkets.com/stock/SHECY/quote)。外部来源只用于核验公司IR入口和2026-06-22 SHECY报价口径，逐行判断仍以项目正式评估和金融资料为主。",
        "- 自动化脚本：`scripts/generate_shecy_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，应用项目已有强公司校准，并对SHECY的半导体材料质量、净现金/FCF、PVC周期、FY2027指引缺失、OTC ADR缺IV和6月22日价格回吐做人工校准后建档。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    base.TARGET = "ALLE"
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 SHECY 正式评估文件")
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
                "shecy_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "shecy_scores": {strategy: round(float(a.get("scores", {}).get(strategy, 0)), 2) for strategy in STRATS},
                "shecy_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
