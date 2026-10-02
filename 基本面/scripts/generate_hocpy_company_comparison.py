from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "HOCPY"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "HOCPY_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_PEERS = {
    "ASGLY",  # AGC: EUV blanks / specialty glass overlap
    "SHECY",  # Shin-Etsu: photomask blanks / synthetic quartz adjacency
    "GLW",  # specialty glass / optical material overlap
    "PLAB",  # downstream photomask / mask supply-chain overlap
}
MATERIAL_ADJACENT = {
    "AJNMY",
    "AXTI",
    "CC",
    "DD",
    "DKILY",
    "ENTG",
    "LIN",
    "MRAAY",
    "MMM",
    "MTRN",
    "NDSN",
    "Q",
    "ROG",
    "SMTOY",
    "SOMMY",
    "TMO",
}
OPTICAL_DOWNSTREAM = {
    "AAOI",
    "ANET",
    "APH",
    "AVGO",
    "BDC",
    "BELFB",
    "CIEN",
    "COHR",
    "CRDO",
    "CSCO",
    "FN",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "MXL",
    "NOK",
    "POET",
    "SMTC",
    "TEL",
    "VIAV",
}
STORAGE_DOWNSTREAM = {"MU", "SNDK", "STX", "WDC", "NTAP", "PSTG", "DELL", "HPE", "SMCI", "PENG"}
SEMI_DOWNSTREAM_CATS = {
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "AI服务器_存储_EMS",
    "封测_检测_计量_光罩",
    "晶圆制造_前道设备",
    "云算力_IDC_AI软件平台",
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
    old_target = base.TARGET
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target

    # HOYA is a quality compounder with real EUV/HDD/CUPO bottleneck exposure.
    # The generic model over-rewards the bad P/S field in the daily snapshot
    # and overstates short-term aggression despite missing IV / OTC ADR liquidity.
    hocpy = companies[TARGET]
    overrides = {
        "NTM兑现优先": 72.0,
        "右尾弹性优先": 72.0,
        "风险调整收益": 56.0,
        "下行保护优先": 80.0,
        "估值消化优先": 56.0,
        "近端催化优先": 64.0,
        "价格确认/动量": 36.0,
        "激进短线": 65.0,
    }
    for strategy, score in overrides.items():
        hocpy["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in OPTICAL_DOWNSTREAM or ticker in STORAGE_DOWNSTREAM or category in SEMI_DOWNSTREAM_CATS:
        return "上下游"
    if ticker in MATERIAL_ADJACENT or category == "半导体材料_化学品_基板" or category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A的EUV/HDD与Life Care锚更稳",
            "右尾弹性优先": "A有EUV/HDD瓶颈右尾",
            "风险调整收益": "A净现金和高ROIC更均衡",
            "下行保护优先": "A净现金、Life Care和高OPM更稳",
            "估值消化优先": "A利润质量可支撑较高倍数",
            "近端催化优先": "A FY26 IT/HDD验证更近",
            "价格确认/动量": "A价格跌幅相对更可控",
            "激进短线": "A瓶颈材料重估弹性略强",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B订单/RPO或收入兑现更硬",
            "右尾弹性优先": "B右尾更大或基数更小",
            "风险调整收益": "B上行赔率或估值缓冲更好",
            "下行保护优先": "B低波动/现金流/压力期更稳",
            "估值消化优先": "B估值更容易被增长消化",
            "近端催化优先": "B近端订单/产品催化更硬",
            "价格确认/动量": "B价格确认和资金趋势更强",
            "激进短线": "B高IV/高beta和事件弹性更强",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"风险调整收益", "下行保护优先", "估值消化优先"}:
        return "质量、估值和安全边际接近"
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
    return "A" if a["scores"]["风险调整收益"] >= b["scores"]["风险调整收益"] else "B"  # type: ignore[index,operator]


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 12:  # type: ignore[index,operator]
            return "HOCPY 的EUV/HDD增长和Life Care现金流让NTM兑现更硬。"
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 10:  # type: ignore[index,operator]
            return "HOCPY 的净现金、30% OPM和医疗/镜片底座提供更好防守。"
        return "HOCPY 的质量和关键材料稀缺性略强，B 的右尾或估值证据不足以反超。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 16:  # type: ignore[index,operator]
        return f"{b['ticker']} 的直接AI右尾、收入斜率或小基数弹性明显强于 HOCPY。"
    if b["scores"]["估值消化优先"] - a["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 更容易用增长或低估值消化当前价格。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 12:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和短线资金偏好强于 HOCPY。"
    return f"{b['ticker']} 在多数投资思路下比 HOCPY 更符合项目内资金配置目标。"


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    output = []
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
                "summary": base.grade_diff_summary(a, b),
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
        key=lambda x: (x["ac"] - x["bc"], a["scores"]["NTM兑现优先"] - x["b"]["scores"]["NTM兑现优先"]),  # type: ignore[index,operator]
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
        f"2026-06-22 金融快照；HOCPY价格日期 {fin.get('price_date', '缺失')}，价格 {fmt_num(fin.get('price'))} 美元，"
        f"市值 {fmt_b(fin.get('market_cap_b'))}，TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S 源字段 {fmt_num(fin.get('ps'), precision=4)}（交易货币/财报货币不一致，估值重算bad，不作为低估值证据），"
        f"P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = []
    for product in a["products"][:8]:  # type: ignore[index]
        product_names.append(str(product[0]).split("：")[0])

    support = {
        "NTM兑现优先": (
            "FY25收入`9477.49亿日元`、OPM`30.1%`，NTM基准收入`1.00-1.035万亿日元`；LSI/EUV和HDD基板有Q4强增长",
            "公司未给FY26集团量化指引，不披露backlog/booking；FY26受产能、客户认证和折旧限制",
        ),
        "右尾弹性优先": (
            "EUV/DUV mask blanks、3.5寸nearline HDD glass substrates、CUPO光学材料是AI制造/存储/光互联瓶颈",
            "极度乐观收入`1.13-1.21万亿日元`仍要求多线同时兑现；新加坡/越南大扩产主要FY28以后贡献",
        ),
        "风险调整收益": (
            "净现金、FY25 ROIC`21.1%`、FY25 FCF`2709亿日元`和IT OPM`52.5%`支撑质量溢价",
            "2026-06-22 Forward PE`39.29`、P/B`8.92`，SOXX压力窗口累计`-39.34%`，估值/回撤抵消质量优势",
        ),
        "下行保护优先": (
            "Life Care收入底座、医疗/镜片需求、净现金和高利润率让经营韧性好于多数高beta AI硬件",
            "高估值、IT周期和历史压力窗口回撤较大，使其防守性弱于公用事业、低IV现金流和部分成熟云巨头",
        ),
        "估值消化优先": (
            "高毛利IT mix、Life Care现金流和回购/分红能支撑较高质量倍数",
            "Forward PE接近`39x`，项目内日度P/S字段有币种异常；NTM基准增速仅中高个位数，不易快速消化估值",
        ),
        "近端催化优先": (
            "FY26Q1/Q2 IT收入和OPM、EUV/LSI增速、HDD第二客户H2 2026、CUPO是否继续被管理层强调可验证",
            "缺少明确订单、客户认证、backlog和产能释放的近端量化时间表，强催化更多在FY28扩产前后",
        ),
        "价格确认/动量": (
            "过去两周小涨`+0.75%`，说明并非完全破位；质量型材料叙事仍有支撑",
            "过去一月`-3.11%`，2026-06-22价格低于2026-06-03收盘；无IV且OTC ADR流动性需折扣",
        ),
        "激进短线": (
            "若EUV/HDD订单或客户路线突然披露，瓶颈材料叙事可能触发重估",
            "无期权链、低短线催化密度、OTC ADR、估值高且动量弱，不适合高beta短线进攻",
        ),
    }

    out: list[str] = []
    out += [
        "# HOCPY 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：HOCPY / HOYA Corporation",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22金融快照；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 HOCPY vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。HOCPY 最像“高质量材料瓶颈 + Life Care 现金流”的中期配置标的，而不是纯AI高beta右尾标的。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是估值已经高、日度动量弱、无期权链、OTC ADR流动性折扣，以及FY26缺少可量化订单/backlog催化。",
        "- A 最适合的投资者画像：愿意持有高ROIC、净现金、EUV/HDD关键材料瓶颈，接受中个位数到低双位数增长和较高估值的中期质量配置者。",
        "- A 最不适合的投资者画像：只追求直接AI收入爆发、小市值右尾、高IV短线进攻、价格强确认或1-2季度硬订单重定价的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]]) if strong_b_rows else '无'}。这些公司通常有更高收入斜率、更直接AI订单/RPO、更便宜估值或更强价格确认。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：HOCPY 属于项目内质量较高但增长/催化/估值弹性不顶级的中上材料标的；在NTM兑现和质量上可打，但多数高增长AI主链和更便宜周期修复标的会在右尾、估值消化或短线列压过它。",
        "- 后续最重要跟踪数据：FY26Q1/Q2 IT收入和OPM、LSI/EUV blanks增速是否高于10%-15%、3.5寸HDD glass substrates和第二客户H2 2026进度、CUPO绝对收入或客户线索、FY26-FY28 capex/折旧/FCF、新加坡EUV blank和越南HDD substrate扩产、Life Care中国内窥镜与MiYOSMART iQ增长。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "HOCPY"]),
        base.row(["公司名称", "HOYA Corporation"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "`1.00-1.035万亿日元`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "EUV/DUV mask blanks 与 HDD glass substrates 需求强，但FY26受现有产能、客户认证、交付节奏、折旧和demand materialization限制；FY28扩产不应提前计入NTM。"]),
        base.row(["最大反证", "公司不披露backlog、booking、产品绝对收入和CUPO子项；Forward PE约39x，P/S日度字段有币种异常，价格动量弱于AI主链。"]),
        base.row(["近端催化剂", "FY26Q1/Q2 IT分部收入和OPM、LSI/EUV增速、3.5寸HDD第二客户H2 2026、CUPO管理层措辞、capex/折旧/FCF更新。"]),
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
        base.row(["直接同业", "与HOCPY在EUV/DUV blank、photomask材料、特种玻璃/光学材料或光罩生态中高度重叠，优先比较份额、客户认证、收入兑现、利润率和同业估值。", "ASGLY、SHECY、GLW、PLAB", "同业证据权重最高；若对方订单、份额、估值消化或动量明显更强，会直接压低HOCPY结论。"]),
        base.row(["相邻替代", "同属半导体材料、先进材料、工业气体或AI基础设施资金篮子，但产品不直接竞争；回答资金只能买一个时谁的增长质量和赔率更好。", "DD、ENTG、AXTI、LIN、Q、ROG、VRT、ETN", "默认看增长质量、估值消化、订单可见度和下行保护；不因赛道更热自动胜出。"]),
        base.row(["上下游", "一方处在HOCPY材料所服务的先进节点、光罩、封测、存储、AI光互联、服务器或云资本开支链条。", "TSM、ASML、NVDA、MU、WDC、STX、ANET、CRDO、AMZN", "不把下游收入规模直接等同于HOCPY机会，重点看利润捕获、议价权、订单硬度和估值。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化。", "RKLB、TSLA、BWXT、MSI、CAT", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
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
    if not strong_b_rows:
        out.append(base.row(["-", "无", "无", "本次没有达到多数思路明显强于A阈值的公司。", "无"]))
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要 HOCPY 把EUV/HDD/CUPO转成可量化订单、收入和利润上修，同时证明高估值可被消化。"
        if comparison["rel"] == "直接同业":
            need = "需要 HOCPY 在EUV blanks、HDD substrates或CUPO上拿出强于同业的份额、客户、订单和利润率证据。"
        elif comparison["rel"] == "上下游":
            need = "需要 HOCPY 证明材料端利润捕获能接近下游AI芯片、存储、光互联或云公司的成长斜率。"
        elif comparison["rel"] == "跨赛道":
            need = "需要 HOCPY 用更强现金流、估值消化和价格确认抵消跨赛道标的的高增长或防守质量。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    if not strong_a_rows:
        out.append(base.row(["-", "无", "无", "本次没有达到多数思路明显强于B阈值的公司。", "无"]))
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提高收入确认可信度、现金流质量和估值消化能力，或拿出更强价格确认。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要 B 把右尾叙事转成可确认收入/利润，并降低估值、IV或现金流反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/半导体材料_化学品_基板/HOCPY_HOYA_Corporation_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_高端光罩与先进封装掩模_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_HDD、对象存储与冷温数据存储_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_玻璃基板、TGV与玻璃检测_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_封装基板、中介层与RDL_2026-06-10.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 外部核验来源：HOYA IR financial results page `https://www.hoya.com/en/investor/kessan/`；HOYA IR library `https://www.hoya.com/en/investor/library/`。外部核验仅用于确认FY25Q4披露材料存在和日期，正式判断仍以项目内正式评估、公司调研、行业调研和金融资料为主。",
        "- 自动化脚本：`scripts/generate_hocpy_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对HOCPY的EUV/HDD/CUPO瓶颈、Life Care现金流、高估值、P/S币种异常、无IV和弱价格确认做人工校准后建档。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    old_target = base.TARGET
    base.TARGET = "ALLE"
    companies = base.build_companies()
    base.TARGET = old_target
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "hocpy_tiers": companies[TARGET]["tiers"],
        "hocpy_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
