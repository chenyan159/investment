from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_alle_company_comparison as base


TARGET = "BABA"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "BABA_逐家公司投资思路对比_2026-06-23.md"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL

DIRECT_PEERS = {"AMZN", "GOOGL", "MSFT", "ORCL", "IBM", "CRWV", "NBIS", "APLD", "IREN"}
ADJACENT_PEERS = {"META", "ADBE", "CRWD", "NTNX", "EQIX", "DLR"}
UPSTREAM_CATS = {
    "AI服务器_存储_EMS",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "半导体材料_化学品_基板",
    "电力_发电_能源_储能",
    "封测_检测_计量_光罩",
    "机电_冷却_工程_水处理_边缘工业AI",
    "晶圆制造_前道设备",
    "配电_电源_功率器件",
}
CROSS_TICKERS = {"RKLB", "TSLA", "CAT", "MSI", "ALLE", "FTV", "DHR", "TMO", "ECL", "MMM"}


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
    base.score_companies(companies)

    # Alibaba calibration: the generic model rewards high-beta hardware names
    # more than cheap platform companies. BABA's edge is valuation digestion and
    # risk-adjusted optionality from AI cloud + ecommerce cash flow; its weak
    # columns are price confirmation and aggressive short-term trading.
    overrides = {
        "NTM兑现优先": 63.0,
        "右尾弹性优先": 61.0,
        "风险调整收益": 56.0,
        "下行保护优先": 66.5,
        "估值消化优先": 74.0,
        "近端催化优先": 62.0,
        "价格确认/动量": 28.0,
        "激进短线": 64.0,
    }
    target = companies[TARGET]
    for strategy, score in overrides.items():
        target["scores"][strategy] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in ADJACENT_PEERS or category == "云算力_IDC_AI软件平台":
        return "相邻替代"
    if ticker in CROSS_TICKERS:
        return "跨赛道"
    if category in UPSTREAM_CATS:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A电商底盘和AI云收入更可见",
            "右尾弹性优先": "A有AI云/MaaS/Qwen体系右尾",
            "风险调整收益": "A低估值与平台资产赔率更好",
            "下行保护优先": "A低估值和电商现金流更稳",
            "估值消化优先": "A当前倍数消化难度更低",
            "近端催化优先": "A云AI/MaaS和快商数据更近",
            "价格确认/动量": "A低估值修复承接略好",
            "激进短线": "A中概AI关注度仍可交易",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B订单/指引兑现更硬",
            "右尾弹性优先": "B小基数或硬件右尾更大",
            "风险调整收益": "B上行与反证组合更好",
            "下行保护优先": "B压力期或现金流更稳",
            "估值消化优先": "B增长更能覆盖估值",
            "近端催化优先": "B近端订单/产品节点更硬",
            "价格确认/动量": "B价格趋势更强",
            "激进短线": "B高beta更适合短攻",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"价格确认/动量", "激进短线"}:
        return "价格和短线弹性接近"
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
    weighted = (
        a["scores"]["NTM兑现优先"] * 0.9
        + a["scores"]["风险调整收益"]
        + a["scores"]["估值消化优先"] * 1.1
        + a["scores"]["近端催化优先"] * 0.5
        - b["scores"]["NTM兑现优先"] * 0.9
        - b["scores"]["风险调整收益"]
        - b["scores"]["估值消化优先"] * 1.1
        - b["scores"]["近端催化优先"] * 0.5
    )
    return "A" if weighted >= 0 else "B"


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 12:  # type: ignore[index,operator]
            return "BABA 的低前瞻倍数和平台现金流更容易消化估值。"
        if a["scores"]["风险调整收益"] - b["scores"]["风险调整收益"] > 10:  # type: ignore[index,operator]
            return "BABA 以低估值叠加AI云期权，风险调整后赔率略好。"
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "BABA 的电商底盘和Cloud AI收入表证据更清楚。"
        return "BABA 在估值、平台底盘和AI云可选性之间更均衡。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的小基数或直接AI硬件/电力右尾明显强于 BABA。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和资金偏好明显强于 BABA。"
    if b["scores"]["下行保护优先"] - a["scores"]["下行保护优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的压力期韧性或现金流安全性强于 BABA。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的订单/RPO/指引兑现比 BABA 更硬。"
    return f"{b['ticker']} 在多数投资思路下比 BABA 更符合当前配置目标。"


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
                "summary": grade_diff_summary(a, b),
                "reason": key_reason(a, b, final),
            }
        )
    return output


def fmt_num(value: object, suffix: str = "") -> str:
    if value is None:
        return "缺失"
    if isinstance(value, float):
        return f"{value:.2f}{suffix}"
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
        key=lambda x: (
            x["bc"] - x["ac"],
            x["b"]["scores"]["右尾弹性优先"] + x["b"]["scores"]["价格确认/动量"] - a["scores"]["右尾弹性优先"] - a["scores"]["价格确认/动量"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            x["ac"] - x["bc"],
            a["scores"]["估值消化优先"] + a["scores"]["风险调整收益"] - x["b"]["scores"]["估值消化优先"] - x["b"]["scores"]["风险调整收益"],  # type: ignore[index,operator]
        ),
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
        f"2026-06-22 价格 {fmt_num(fin.get('price'))} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'))}，Forward PE {fmt_num(fin.get('forward_pe'))}，"
        f"P/S {fmt_num(fin.get('ps'))}（交易/财报币种不一致，作为低估值方向性参考），"
        f"P/B {fmt_num(fin.get('pb'))}，EV/EBITDA {fmt_num(fin.get('ev_ebitda'))}，"
        f"Call IV {fmt_pct(fin.get('call_iv'))}，Put IV {fmt_pct(fin.get('put_iv'))}；"
        f"2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}、过去一月 {fmt_pct(mom1.get('mom1m'))}；"
        f"2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    product_names = [str(product[0]).split("，")[0] for product in a["products"][:7]]  # type: ignore[index]
    support = {
        "NTM兑现优先": (
            "FY2026收入RMB 1,023.7bn、like-for-like约+11%；Cloud Q4 +38%、外部云+40%、AI-related RMB 9.0bn/季度，NTM基准收入RMB 1,115-1,155bn",
            "中国消费和广告需求偏弱，quick commerce补贴、云CAPEX转收入和客户验收仍会压制利润留存",
        ),
        "右尾弹性优先": (
            "Cloud AI、MaaS/Model Studio、Qwen企业/商户Agent、T-Head/Zhenwu和AIDC效率改善共同构成右尾",
            "集团体量大、AI收入仍嵌在Cloud/All others，T-Head/MaaS拆分证据多为B/C级，非线性弹性不如硬件小基数公司",
        ),
        "风险调整收益": (
            "Forward PE 11.39、P/B 1.56，电商现金流底盘叠加AI云高增，若FCF修复则赔率较好",
            "FY2026 FCF为-RMB 46.6bn，NTM仍受CAPEX、quick commerce、Qwen获客和中概风险约束",
        ),
        "下行保护优先": (
            "核心电商/CMR、AIDC改善和低估值提供一定缓冲，业务线分散度高于单一硬件链",
            "SOXX压力窗口累计-61.65%，Call IV 43.4%，FCF和政策/竞争风险使其不是防守顶档",
        ),
        "估值消化优先": (
            "Forward PE 11.39、TTM PE 16.12，NTM基准non-GAAP净利润RMB 70-95bn，乐观可到RMB 110-150bn",
            "估值消化依赖Cloud EBITA率、quick commerce亏损收窄和CAPEX不继续吞噬经营现金流",
        ),
        "近端催化优先": (
            "AI-related cloud revenue、MaaS/模型应用ARR、Cloud EBITA margin、quick commerce unit economics、AIDC EBITA和CAPEX commentary均可在1-2季验证",
            "多数催化是经营数据连续验证，不是硬订单、客户认证或产品代际单点重定价",
        ),
        "价格确认/动量": (
            "低估值和中概AI关注度可形成修复交易，但需要价格先重新站稳",
            "2026-06-03过去一月-3.26%、两周-5.40%，6月22日价格104.97显著低于6月3日127.21，动量弱",
        ),
        "激进短线": (
            "Qwen/AI云/MaaS和中概平台修复可交易，Call IV 43.4%不算低",
            "价格趋势破弱、集团体量大、业务混合，短线爆发力明显弱于高IV小盘、光互联、AI芯片和电力弹性股",
        ),
    }

    out: list[str] = []
    out += [
        "# BABA 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：BABA / Alibaba 阿里巴巴",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；区间涨跌为 2026-06-03；SOXX 三段压力窗口为 2026-06-04",
        "",
        "> 口径说明：本报告按同一批 189 家正式公司评估建立 8 个投资思路相对档位，再逐行做 BABA vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。BABA 的主要优势不是最高增速，而是低估值、电商现金流底座和 AI 云/MaaS 期权组合，最容易在估值消化和风险调整收益列中胜出。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是价格趋势明显偏弱、短线爆发力不如高 IV 小盘/硬件链，且右尾弹性被集团体量、CAPEX和业务混合摊薄。",
        "- A 最适合的投资者画像：愿意用低估值承接中国平台公司和 AI 云修复，重视未来12个月收入/利润可见度、估值消化和中长期AI optionality，同时能承受中概、竞争和现金流波动的配置者。",
        "- A 最不适合的投资者画像：只追求短期动量、极端右尾、小基数高波动、硬件订单直兑现或压力期绝对防守的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:12]])}。这些公司通常在右尾弹性、价格确认、激进短线、直接AI硬件/电力订单或下行保护上压过 BABA。",
        "- 如果只追求更高增长、更好公司，A 的总体位置：BABA 是全项目中估值消化靠前、兑现中上、风险调整中上的平台型标的；若只追求高增长和价格确认，它落后于AI芯片、光互联、服务器、NeoCloud和电力高弹性链条。",
        "- 后续最重要跟踪数据：AI-related cloud revenue绝对额和云外部占比、MaaS/模型应用ARR、Cloud adjusted EBITA margin、CAPEX与云收入滞后关系、quick commerce unit economics、China E-commerce CMR like-for-like、AIDC EBITA、T-Head外部客户/云实例/收入披露、tokens/GPU-hour与API价格。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "BABA"]),
        base.row(["公司名称", "Alibaba 阿里巴巴"]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "RMB 1,115-1,155bn"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；FCF {a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI云需求已有收入证据，但需求转收入需要GPU/ASIC/HBM、站点电力、液冷、网络、调度和客户验收全部转成可用capacity；收入转利润还取决于利用率、tokens/GPU-hour和价格纪律。"]),
        base.row(["最大反证", "FY2026 FCF为-RMB 46.6bn；quick commerce与Qwen获客支出、Cloud折旧、价格战和中国消费/竞争压力，可能抵消AI云收入高增。"]),
        base.row(["近端催化剂", "AI-related cloud revenue、MaaS/模型应用ARR、Cloud EBITA margin、CAPEX节奏、quick commerce unit economics、China CMR like-for-like、AIDC EBITA、T-Head外部客户和云实例披露。"]),
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
        base.row(["直接同业", "与 BABA 在公有云、AI云、NeoCloud、企业云或平台型AI服务收入池高度重叠，优先比较云收入兑现、客户/RPO、利润率、CAPEX效率和估值相对同业。", "AMZN、MSFT、GOOGL、ORCL、IBM、CRWV、NBIS、APLD、IREN", "同档或相邻档也需看云收入质量、现金流和估值；两档以上可给强结论。"]),
        base.row(["相邻替代", "同属AI平台、AI软件、IDC/云资源或大市值互联网AI资金篮子，但收入模式不完全重叠。", "META、ADBE、CRWD、NTNX、EQIX、DLR", "重点看增长质量、估值消化、近端催化和风险调整，不因赛道更热直接胜出。"]),
        base.row(["上下游", "B 是 BABA/阿里云 AI CapEx 与AI基础设施的芯片、服务器、网络、光互联、电力、冷却、设备、材料或能源供应链参与者。", "NVDA、AMD、AVGO、TSM、MU、SMCI、ANET、VRT、ETN、PWR、CEG", "不把BABA下游收入规模直接等同于更好，也不把上游稀缺直接当胜出；看利润捕获、订单和估值消化。"]),
        base.row(["跨赛道", "业务差异较大，只作为项目内资金配置替代比较。", "RKLB、TSLA、CAT、TMO、DHR、MMM", "默认降低结论力度；除非增长质量、估值消化或风险调整明显拉开，否则使用中性或微倾向。"]),
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
        need = "需要 BABA 证明AI云收入、MaaS ARR、Cloud EBITA和FCF同步改善，且估值修复开始被价格确认。"
        if "价格确认/动量" in wins or "激进短线" in wins:
            need = "需要 BABA 先修复价格趋势，用AI云/快商/AIDC数据触发资金重新定价。"
        if "右尾弹性优先" in wins:
            need = "需要 BABA 把Qwen/MaaS/T-Head从期权变成可确认收入和利润，而不是只停留在叙事。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (base.tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要 B 提供更硬的收入/订单兑现、利润质量和估值消化证据。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要 B 把右尾叙事转成可确认收入、利润和现金流，降低估值或执行反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 181 家，本次公司评估全集为 {n} 家；缺少可用价格/估值的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/云算力_IDC_AI软件平台/BABA_Alibaba阿里巴巴_公司调研_2026-06-20.md`、`行业调研/产业背景/全球AI需求与Token经济框架_2026-06-11.md`、`行业调研/产业背景/AI产业链瓶颈与反证指标总表_2026-06-10.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_云厂自研AI ASIC_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI集群调度与推理运行时_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI云算力外包和NeoCloud与AI数据中心运营商_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_baba_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，并对百分比区间如 `+9%-13%` 做同号区间修正后建档；未读取下游量化目录或现成排序结论。",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    print(
        json.dumps(
            {
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "size": OUT_PATH.stat().st_size,
                "baba_tiers": companies[TARGET]["tiers"],
                "baba_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
