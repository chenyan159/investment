from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"D:\investment\基本面")
sys.path.insert(0, str(ROOT / "scripts"))

import generate_cien_company_comparison_20260623 as fw


TARGET = "POET"
TARGET_NAME = "POET Technologies"
REPORT_DATE = "2026-06-23"
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "POET_逐家公司投资思路对比_2026-06-23.md"

STRATEGIES = fw.STRATEGIES
LABEL_ORDER = fw.LABEL_ORDER
GRADE_VALUE = fw.GRADE_VALUE


DIRECT_OPTICAL_ENGINE_PEERS = {
    "AAOI",
    "COHR",
    "LITE",
    "LWLG",
}

OPTICAL_COMPONENT_AND_MODULE_CHAIN = {
    "ANET",
    "APH",
    "BDC",
    "BELFB",
    "CIEN",
    "CRDO",
    "CSCO",
    "GLW",
    "MTSI",
    "NOK",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}

AI_CHIP_AND_NETWORK_CUSTOMER_CHAIN = {
    "ADBE",
    "ALAB",
    "AMD",
    "AMZN",
    "ARM",
    "AVGO",
    "BABA",
    "CDNS",
    "CRWD",
    "CRWV",
    "DELL",
    "DLR",
    "EQIX",
    "GOOGL",
    "HPE",
    "IBM",
    "INTC",
    "META",
    "MRVL",
    "MSFT",
    "MU",
    "NBIS",
    "NTNX",
    "NVDA",
    "ORCL",
    "QCOM",
    "SNPS",
    "TSLA",
}

SERVER_MODULE_AND_EMS_CHAIN = {
    "CLS",
    "FLEX",
    "FN",
    "JBL",
    "PENG",
    "PSTG",
    "RMBS",
    "SANM",
    "SIMO",
    "SMCI",
    "SNDK",
    "STX",
    "WDC",
}

SEMI_AND_PHOTONICS_SUPPLY_CHAIN = {
    "ACLS",
    "ACMR",
    "AMAT",
    "AMKR",
    "ASGLY",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "AXTI",
    "BESIY",
    "CAMT",
    "COHU",
    "DSCSY",
    "FORM",
    "GFS",
    "HOCPY",
    "ICHR",
    "IMOS",
    "KEYS",
    "KLAC",
    "KLIC",
    "LRCX",
    "MICLF",
    "MKSI",
    "MPWR",
    "MRAM",
    "MXL",
    "NVMI",
    "NVTS",
    "ON",
    "ONTO",
    "PLAB",
    "Q",
    "ROG",
    "SHECY",
    "SOMMY",
    "STM",
    "TER",
    "TOELY",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
    "WOLF",
}

INFRA_CATEGORIES = {
    "配电_电源_功率器件",
    "电力_发电_能源_储能",
    "机电_冷却_工程_水处理_边缘工业AI",
}


def md(value: object) -> str:
    return fw.md_escape(value)


def row(cells: list[object]) -> str:
    return "| " + " | ".join(md(c) for c in cells) + " |"


def tag_side(cell: str) -> str:
    label = cell.split("：", 1)[0]
    if label.endswith("投A"):
        return "A"
    if label.endswith("投B"):
        return "B"
    return "N"


def relation_for(b: fw.Company) -> str:
    ticker = b.ticker
    category = b.category
    if ticker in DIRECT_OPTICAL_ENGINE_PEERS:
        return "直接同业"
    if ticker in OPTICAL_COMPONENT_AND_MODULE_CHAIN:
        return "上下游"
    if ticker in AI_CHIP_AND_NETWORK_CUSTOMER_CHAIN:
        return "上下游"
    if ticker in SERVER_MODULE_AND_EMS_CHAIN:
        return "上下游"
    if ticker in SEMI_AND_PHOTONICS_SUPPLY_CHAIN:
        return "相邻替代"
    if category == "AI网络_光互联_连接器":
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    if category in INFRA_CATEGORIES:
        return "相邻替代"
    return "跨赛道"


def reason_for(strat: str, label: str, b: fw.Company, relation: str) -> str:
    if label == "中性":
        if relation == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，证据互有强弱"

    side = "A" if label.endswith("投A") else "B"
    if side == "A":
        return {
            "NTM兑现优先": "A有订单锚但仍需确认收入",
            "右尾弹性优先": "A小基数叠加EOI/1.6T/ELS右尾",
            "风险调整收益": "A现金跑道好且上行可覆盖部分风险",
            "下行保护优先": "A融资后现金缓冲更厚",
            "估值消化优先": "A若订单兑现收入跃迁更快",
            "近端催化优先": "A的800G交付和Lumilens样品更近",
            "价格确认/动量": "A一月涨幅和关注度更强",
            "激进短线": "A高IV小盘光互联弹性更强",
        }[strat]

    if relation == "直接同业":
        return {
            "NTM兑现优先": f"{b.ticker}同业收入和订单更硬",
            "右尾弹性优先": f"{b.ticker}同业客户或规模右尾更清楚",
            "风险调整收益": f"{b.ticker}同业赔率组合更稳",
            "下行保护优先": f"{b.ticker}现金流或压力期表现更好",
            "估值消化优先": f"{b.ticker}同业估值更能被业绩消化",
            "近端催化优先": f"{b.ticker}同业产品/客户催化更明确",
            "价格确认/动量": f"{b.ticker}同业价格确认更好",
            "激进短线": f"{b.ticker}同业短线关注或爆发更强",
        }[strat]

    if relation == "上下游":
        return {
            "NTM兑现优先": f"{b.ticker}需求链收入兑现更清楚",
            "右尾弹性优先": f"{b.ticker}利润池或客户绑定更强",
            "风险调整收益": f"{b.ticker}上行和下行组合更优",
            "下行保护优先": f"{b.ticker}现金流/客户粘性更稳",
            "估值消化优先": f"{b.ticker}估值与增长匹配更好",
            "近端催化优先": f"{b.ticker}客户/产品节点更可验证",
            "价格确认/动量": f"{b.ticker}资金确认更强",
            "激进短线": f"{b.ticker}短线beta或叙事更强",
        }[strat]

    if relation == "相邻替代":
        return {
            "NTM兑现优先": f"{b.ticker}兑现确定性更强",
            "右尾弹性优先": f"{b.ticker}相邻赛道右尾更大",
            "风险调整收益": f"{b.ticker}风险调整后赔率更优",
            "下行保护优先": f"{b.ticker}防守和估值支撑更好",
            "估值消化优先": f"{b.ticker}业绩更容易消化估值",
            "近端催化优先": f"{b.ticker}近端订单或财报催化更硬",
            "价格确认/动量": f"{b.ticker}价格趋势更强",
            "激进短线": f"{b.ticker}短线进攻属性更好",
        }[strat]

    return {
        "NTM兑现优先": f"{b.ticker}经营兑现更清楚",
        "右尾弹性优先": f"{b.ticker}右尾空间更大",
        "风险调整收益": f"{b.ticker}风险收益组合更好",
        "下行保护优先": f"{b.ticker}压力期更安全",
        "估值消化优先": f"{b.ticker}估值消化更容易",
        "近端催化优先": f"{b.ticker}近端催化更明确",
        "价格确认/动量": f"{b.ticker}价格确认更强",
        "激进短线": f"{b.ticker}短线进攻弹性更强",
    }[strat]


def decision_for(a: fw.Company, b: fw.Company, strat: str, relation: str) -> str:
    ga = a.grades[strat]
    gb = b.grades[strat]
    sa = a.scores.get(strat)
    sb = b.scores.get(strat)
    missing = ga == "资料不足" or gb == "资料不足"
    score_diff = (sa if sa is not None else 0.5) - (sb if sb is not None else 0.5)
    diff = GRADE_VALUE.get(ga, 0) - GRADE_VALUE.get(gb, 0)
    if diff > 0 or (diff == 0 and score_diff > 0.04):
        label = fw.strength_label("A", diff, score_diff, relation, missing)
    elif diff < 0 or (diff == 0 and score_diff < -0.04):
        label = fw.strength_label("B", -diff, score_diff, relation, missing)
    else:
        label = "中性"
    return f"{label}：{reason_for(strat, label, b, relation)}"


def grade_summary(a: fw.Company, b: fw.Company) -> str:
    short_names = {
        "NTM兑现优先": "NTM",
        "右尾弹性优先": "右尾",
        "风险调整收益": "风险收益",
        "下行保护优先": "下行",
        "估值消化优先": "估值",
        "近端催化优先": "催化",
        "价格确认/动量": "动量",
        "激进短线": "短线",
    }
    a_strong: list[str] = []
    b_strong: list[str] = []
    near: list[str] = []
    for strat in STRATEGIES:
        diff = GRADE_VALUE[a.grades[strat]] - GRADE_VALUE[b.grades[strat]]
        if diff >= 1:
            a_strong.append(short_names[strat])
        elif diff <= -1:
            b_strong.append(short_names[strat])
        else:
            near.append(short_names[strat])
    parts = []
    if a_strong:
        parts.append("A强：" + "、".join(a_strong[:4]))
    if b_strong:
        parts.append("B强：" + "、".join(b_strong[:4]))
    if near:
        parts.append("接近：" + "、".join(near[:3]))
    return "；".join(parts)


def final_choice(decisions: dict[str, str], b: fw.Company) -> tuple[str, str, str]:
    counts = Counter(tag_side(v) for v in decisions.values())
    a_count, b_count, n_count = counts["A"], counts["B"], counts["N"]
    if a_count > b_count:
        if a_count >= 5:
            reason = "POET在右尾、催化或短线弹性上明显占优，但仍需订单转收入验证。"
        else:
            reason = "POET更适合高弹性进攻，胜在小基数和光互联期权。"
        return f"A {a_count} / B {b_count} / 中性 {n_count}", TARGET, reason

    if b_count > a_count:
        reason = f"{b.ticker}在多数思路下胜出，POET需要把订单、样品和产能转成收入与毛利。"
        if decisions["下行保护优先"].split("：", 1)[0].endswith("投B"):
            reason = f"{b.ticker}的兑现、估值或下行保护优于POET的高波动期权。"
        return f"A {a_count} / B {b_count} / 中性 {n_count}", b.ticker, reason

    risk_label = decisions["风险调整收益"].split("：", 1)[0]
    if risk_label.endswith("投A"):
        return f"A {a_count} / B {b_count} / 中性 {n_count}", TARGET, "多数思路打平时，风险调整收益略偏POET。"
    if risk_label.endswith("投B"):
        return f"A {a_count} / B {b_count} / 中性 {n_count}", b.ticker, f"多数思路打平时，风险调整收益更支持{b.ticker}。"
    ntm_label = decisions["NTM兑现优先"].split("：", 1)[0]
    if ntm_label.endswith("投B"):
        return f"A {a_count} / B {b_count} / 中性 {n_count}", b.ticker, f"多数思路打平，NTM兑现更支持{b.ticker}。"
    return f"A {a_count} / B {b_count} / 中性 {n_count}", TARGET, "多数思路打平，POET右尾和催化略更值得押注。"


def grade_support_limit(strat: str) -> tuple[str, str]:
    support = {
        "NTM兑现优先": ">$5M 800G订单、Lumilens $50M初始PO和2026H2交付窗口提供收入锚",
        "右尾弹性优先": "TTM收入仅约$1.41M，EOI/1.6T/ELS/optical I/O一旦转量产弹性极大",
        "风险调整收益": "融资后现金跑道强，理论上能吸收研发、产线和客户认证周期",
        "下行保护优先": "现金/短投和低债务降低短期流动性风险",
        "估值消化优先": "若$22M-$50M基准收入兑现，收入基数会出现数量级跃迁",
        "近端催化优先": "800G订单交付、Lumilens late-2026样品、Lessengers/LITEON进展和Q2/Q3财报可验证",
        "价格确认/动量": "2026-06-03过去一月+110.40%，2026-06-22仍有高IV和主题关注",
        "激进短线": "小盘、高IV、AI光互联、EOI/ELS和1.6T叙事叠加，适合高风险进攻",
    }[strat]
    limit = {
        "NTM兑现优先": "基准仍亏损，收入确认依赖qualification、验收、Lumilens条件和Malaysia良率",
        "右尾弹性优先": "极度乐观可信度低，Celestial/Marvell取消PO证明订单可撤销",
        "风险调整收益": "P/S约1478x、Forward PE不适用、经营现金流仍为负，执行反证很重",
        "下行保护优先": "SOXX三段压力窗口累计-88.77%，Call/Put IV约122%，不是防守资产",
        "估值消化优先": "当前市值已提前定价多年订单，NTM利润仍难覆盖固定费用",
        "近端催化优先": "真正生产ramp多在2027，短期财报可能仍显示小收入和高亏损",
        "价格确认/动量": "6月22日价格12.09低于6月3日15.38，涨幅已有回吐",
        "激进短线": "同样的高IV和高关注也意味着短线回撤风险极高",
    }[strat]
    return support, limit


def calibrate_poet_scores(companies: dict[str, fw.Company]) -> None:
    a = companies[TARGET]
    overrides = {
        "NTM兑现优先": 0.50,
        "右尾弹性优先": 0.94,
        "风险调整收益": 0.34,
        "下行保护优先": 0.24,
        "估值消化优先": 0.22,
        "近端催化优先": 0.80,
        "价格确认/动量": 0.55,
        "激进短线": 0.82,
    }
    for strat, score in overrides.items():
        a.scores[strat] = score


def fmt_raw(value: str, default: str = "缺失") -> str:
    return value if value and value != "缺失" else default


def daily_snapshot(a: fw.Company) -> str:
    fin = a.finance
    call_iv = fmt_raw(fin.get("Call IV", ""))
    put_iv = fmt_raw(fin.get("Put IV", ""))
    ret_2w = a.returns.get("2w")
    ret_1m = a.returns.get("1m")
    soxx = a.returns.get("soxx")
    def pct(v: float | None) -> str:
        if v is None:
            return "缺失"
        sign = "+" if v > 0 else ""
        return f"{sign}{v:.2f}%"

    return (
        f"2026-06-22 收盘价 `{fmt_raw(fin.get('最新价格', ''))}` 美元，市值 `{fmt_raw(fin.get('市值', ''))}`，"
        f"TTM PE `{fmt_raw(fin.get('TTM PE', ''))}`，Forward PE `{fmt_raw(fin.get('Forward PE', ''))}`，"
        f"P/S `{fmt_raw(fin.get('P/S', ''))}`，P/B `{fmt_raw(fin.get('P/B', ''))}`，EV/EBITDA `{fmt_raw(fin.get('EV/EBITDA', ''))}`，"
        f"Call IV `{call_iv}`、Put IV `{put_iv}`；2026-06-03 过去两周 `{pct(ret_2w)}`、过去1个月 `{pct(ret_1m)}`；"
        f"2026-06-04 三段 SOXX 压力窗口累计 `{pct(soxx)}`。"
    )


def short_text(value: str, max_len: int = 220) -> str:
    return fw.short_phrase(value, max_len)


def build_report(companies: dict[str, fw.Company]) -> str:
    a = companies[TARGET]
    sorted_bs = [c for t, c in companies.items() if t != TARGET]
    sorted_bs.sort(key=lambda c: (c.category, c.ticker))

    stats: dict[str, Counter] = {s: Counter() for s in STRATEGIES}
    rows: list[list[object]] = []
    b_rank_rows: list[tuple[int, int, fw.Company, dict[str, str], str]] = []
    a_rank_rows: list[tuple[int, int, fw.Company, dict[str, str], str]] = []
    final_by_b: dict[str, str] = {}

    for idx, b in enumerate(sorted_bs, start=1):
        relation = relation_for(b)
        decisions = {s: decision_for(a, b, s, relation) for s in STRATEGIES}
        for s, cell in decisions.items():
            stats[s][cell.split("：", 1)[0]] += 1
        majority, final, final_reason = final_choice(decisions, b)
        final_by_b[b.ticker] = final
        counts = Counter(tag_side(v) for v in decisions.values())
        rows.append(
            [
                idx,
                f"{b.ticker} / {b.name}",
                b.category,
                relation,
                grade_summary(a, b),
                *[decisions[s] for s in STRATEGIES],
                majority,
                final,
                final_reason,
            ]
        )
        diff = counts["B"] - counts["A"]
        if diff >= 3:
            b_rank_rows.append((diff, counts["B"], b, decisions, final_reason))
        elif -diff >= 3:
            a_rank_rows.append((-diff, counts["A"], b, decisions, final_reason))

    by_strategy_a = {s: stats[s]["强烈建议投A"] + stats[s]["建议投A"] + stats[s]["微倾向投A"] for s in STRATEGIES}
    by_strategy_b = {s: stats[s]["强烈建议投B"] + stats[s]["建议投B"] + stats[s]["微倾向投B"] for s in STRATEGIES}
    a_best = sorted(STRATEGIES, key=lambda s: by_strategy_a[s] - by_strategy_b[s], reverse=True)[:3]
    a_worst = sorted(STRATEGIES, key=lambda s: by_strategy_b[s] - by_strategy_a[s], reverse=True)[:3]
    strongest_b = sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker))[:12]
    strongest_a = sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker))[:12]
    strongest_b_names = "、".join(x[2].ticker for x in strongest_b) or "无明显集中反方"
    strongest_a_names = "、".join(x[2].ticker for x in strongest_a) or "无明显集中胜方"
    a_final_count = sum(1 for final in final_by_b.values() if final == TARGET)
    b_final_count = len(sorted_bs) - a_final_count
    eval_dates = [c.eval_date for c in companies.values()]
    finance_meta = fw.load_finance()[1]
    missing_finance = sorted([t for t, c in companies.items() if not c.finance])

    intro = fw.section_between(a.text, "1. 一页结论")
    conclusion = fw.section_between(a.text, "8. 结论")
    products = fw.bullet_after(intro, "重要产品/业务线")
    ntm = a.scenarios.get("基准", {}).get("NTM 公司收入", "") or a.scenarios.get("基准", {}).get("NTM收入", "")
    optimistic = " / ".join(
        filter(
            None,
            [
                a.scenarios.get("乐观", {}).get("NTM 公司收入", "") or a.scenarios.get("乐观", {}).get("NTM收入", ""),
                a.scenarios.get("极度乐观", {}).get("NTM 公司收入", "")
                or a.scenarios.get("极度乐观", {}).get("NTM收入", ""),
            ],
        )
    )
    profit_cash = fw.bullet_after(conclusion, "利润/现金流结论") or fw.bullet_after(intro, "利润或 EBITDA 四情景")
    bottleneck = fw.bullet_after(conclusion, "主要传导瓶颈") or fw.bullet_after(intro, "最大传导瓶颈")
    bear = fw.bullet_after(conclusion, "悲观情景触发条件") or fw.bullet_after(intro, "最大传导瓶颈")
    catalysts = fw.bullet_after(conclusion, "乐观情景成立条件") or fw.bullet_after(conclusion, "后续跟踪数据")
    snapshot = daily_snapshot(a)

    lines: list[str] = []
    lines.append("# POET 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：POET / {TARGET_NAME}")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(companies) - 1}")
    lines.append(f"公司评估文件日期范围：{min(eval_dates)} 至 {max(eval_dates)}")
    lines.append("日度数据日期：价格/估值/IV 为 2026-06-22；过去两周和过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04；日度新闻最新文件日期为 2026-06-23。")
    lines.append("")
    lines.append("> 口径说明：本报告读取 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/公司索引.md`、POET正式公司调研、正式光互联行业调研和 `金融资料/` 正式行情文件。未读取、引用或继承 `特征量化/`、Signals、回归、模型比较、`公司排序/`、`简单排序/`、`分析报告/备份/`、`分析报告/tmp/` 或项目根 `tmp/` 的结论；既有公司对比结果不作为本报告决策依据。")
    if missing_finance:
        lines.append(f"> 金融资料覆盖差异：正式评估公司 {len(companies)} 家，最新金融快照覆盖 {len(companies) - len(missing_finance)} 家；缺少日度金融明细的公司为 {', '.join(missing_finance)}，价格/估值/IV/动量相关档位按资料不足或保守口径处理。")
    lines.append("")

    lines.append("## 1. 一页结论")
    lines.append("")
    lines.append(f"- A 最占优的投资思路：{'、'.join(a_best)}。POET 的优势不是当前利润质量，而是小收入基数、Lumilens EOI、1.6T/ELS/optical interposer 的大右尾，以及高IV/高关注带来的短线进攻属性。")
    lines.append(f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是估值、下行保护和风险调整收益：2026-06-22 P/S 为 {a.finance.get('P/S', '缺失')}，PE不适用，SOXX三段压力窗口累计 {a.returns.get('soxx')}%，且基准情景仍亏损。")
    lines.append("- A 最适合的投资者画像：能承受高波动、愿意用小仓位押 AI 光互联架构变化和客户认证突破的进攻型投资者。")
    lines.append("- A 最不适合的投资者画像：要求 NTM 利润兑现、估值可用PE/FCF消化、压力期回撤可控或低IV防守属性的资金。")
    lines.append(f"- 多数思路下最强反方公司：{strongest_b_names}。这些公司通常有更硬的收入/RPO/backlog、利润现金流、平台客户或更可消化的估值。")
    lines.append(f"- 多数思路下 POET 明显强于 B 的代表：{strongest_a_names}。这些比较主要发生在对方更缺右尾、动量或近端催化时。")
    lines.append(f"- 如果只追求更高增长、更好公司，A 的总体位置：POET 对 {a_final_count}/{len(sorted_bs)} 家公司多数思路占优，对 {b_final_count}/{len(sorted_bs)} 家公司落后；它是全项目最强右尾/短线期权之一，但不是综合质量、估值消化或下行保护的一线公司。")
    lines.append("- 后续最重要跟踪数据：2026Q2/Q3 收入、合同负债、应收与库存；`>$5M` Infinity订单交付确认；Lumilens样品、付款、qualification和production ramp；Lessengers/LITEON是否转生产PO；Malaysia产线良率；是否再出现客户取消或披露/治理争议；产品毛利和经营现金流。")
    lines.append("")

    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append(row(["项目", "内容"]))
    lines.append(row(["---", "---"]))
    lines.append(row(["股票代号", "POET"]))
    lines.append(row(["公司名称", TARGET_NAME]))
    lines.append(row(["产业链分类", a.category]))
    lines.append(row(["重要产品/业务线", short_text(products, 260)]))
    lines.append(row(["NTM 基准收入", ntm]))
    lines.append(row(["乐观/极度乐观收入", optimistic]))
    lines.append(row(["利润和现金流结论", short_text(profit_cash, 240)]))
    lines.append(row(["最大传导瓶颈", short_text(bottleneck, 240)]))
    lines.append(row(["最大反证", short_text(bear, 240)]))
    lines.append(row(["近端催化剂", short_text(catalysts, 240)]))
    lines.append(row(["日度市场数据", snapshot]))
    lines.append("")

    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append(row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]))
    lines.append(row(["---", "---", "---", "---", "---"]))
    for strat in STRATEGIES:
        support, limit = grade_support_limit(strat)
        lines.append(row([strat, a.grades[strat], fw.format_grade_position(a, strat), support, limit]))
    lines.append("")

    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append(row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]))
    lines.append(row(["---", "---", "---", "---"]))
    lines.append(row(["直接同业", "与POET在800G/1.6T optical engine、light source、硅光/PIC或光模块需求池高度重叠，优先比较订单、客户认证、产品代际、毛利和估值。", "AAOI、COHR、LITE、LWLG", "同业证据权重最高；如果对手已有规模收入或客户绑定，POET的右尾不能直接压过对方兑现证据。"]))
    lines.append(row(["相邻替代", "同属AI基础设施或半导体/光子供应链资金篮子，但不直接争同一订单，重点比较增长质量、估值消化、催化和风险调整收益。", "TSM、AMAT、ASML、TER、VRT、ETN", "除非档位差明显，否则降低强烈结论；POET高右尾需和对方硬订单/利润质量对比。"]))
    lines.append(row(["上下游", "AI芯片、网络系统、云厂、服务器/EMS、连接器、DSP/SerDes和模块客户链条，重点看利润池位置、议价权和收入确认路径。", "NVDA、AVGO、MRVL、ANET、CIEN、MSFT、DELL、FN", "不把下游AI CapEx直接等同POET收入；也不把上游平台规模自动等同胜出，核心看利润捕获和订单硬度。"]))
    lines.append(row(["跨赛道", "业务差异较大但作为资金配置替代仍可比较，默认看增长质量、估值消化、下行保护和催化可见度。", "LIN、TMO、DHR、RKLB、工业/化工/公用事业公司", "默认降低结论力度；若证据互有强弱，优先微倾向或中性。"]))
    lines.append("")

    lines.append("## 5. 全项目逐行投资思路决策表")
    lines.append("")
    headers = [
        "序号",
        "公司B",
        "公司B分类",
        "可比关系",
        "档位差摘要",
        *STRATEGIES,
        "多数思路方向",
        "最终更值得投",
        "最关键理由",
    ]
    lines.append(row(headers))
    lines.append(row(["---:" if h == "序号" else "---" for h in headers]))
    for item in rows:
        lines.append(row(item))
    lines.append("")

    lines.append("## 6. 投资思路统计")
    lines.append("")
    lines.append(row(["投资思路", *LABEL_ORDER, "A侧合计", "B侧合计"]))
    lines.append(row(["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    for strat in STRATEGIES:
        counter = stats[strat]
        a_total = counter["强烈建议投A"] + counter["建议投A"] + counter["微倾向投A"]
        b_total = counter["强烈建议投B"] + counter["建议投B"] + counter["微倾向投B"]
        lines.append(row([strat, *[counter[label] for label in LABEL_ORDER], a_total, b_total]))
    lines.append("")

    def winning_strats(decisions: dict[str, str], side: str) -> str:
        out = [s for s, cell in decisions.items() if tag_side(cell) == side]
        return "、".join(out) if out else "无"

    lines.append("## 7. 多数思路下 B 明显强于 A 的公司")
    lines.append("")
    lines.append(row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]))
    lines.append(row(["---:", "---", "---", "---", "---"]))
    for rank, (_, _, b, decisions, final_reason) in enumerate(sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        need = "POET需要把Lumilens、800G、1.6T/ELS从公告/样品转成可确认收入、毛利、合同负债或repeat PO，并证明估值可以被NTM业绩消化。"
        if relation_for(b) == "直接同业":
            need = "POET需要在同业中证明客户认证、生产订单、量产良率和毛利率优于B，而不是只保留技术期权。"
        lines.append(row([rank, f"{b.ticker} / {b.name}", winning_strats(decisions, "B"), final_reason, need]))
    if not b_rank_rows:
        lines.append(row([1, "无", "无", "没有公司在多数思路下显著压过POET", "继续跟踪订单和价格确认"]))
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append(row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]))
    lines.append(row(["---:", "---", "---", "---", "---"]))
    for rank, (_, _, b, decisions, final_reason) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        need = f"{b.ticker}需要更明确的AI相关订单、收入加速、估值消化和价格确认，或证明其右尾不弱于POET的EOI/1.6T/ELS期权。"
        lines.append(row([rank, f"{b.ticker} / {b.name}", winning_strats(decisions, "A"), final_reason, need]))
    if not a_rank_rows:
        lines.append(row([1, "无", "无", "POET没有在多数思路下明显压过其他公司", "需等待POET订单和价格进一步确认"]))
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司 A 公司调研文件：`公司调研/AI网络_光互联_连接器/POET_POET Technologies_公司调研_2026-06-11.md`。")
    lines.append("- 关键行业资料：`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_CPO／NPO与交换侧光引擎_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_Optical Interposer与新型光引擎_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_封装内光IO与Optical_Chiplet_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_硅光材料、光子材料与电光聚合物_2026-06-11.md`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{fw.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{fw.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{fw.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{fw.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append(f"- 公司 A 日度数据摘录：{snapshot}")
    lines.append("- 其他主要来源：`公司调研/公司索引.md` 用于公司名称和分类；各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源用于 B 侧业务证据。")
    lines.append("- 排除来源：未使用 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/备份/`、`分析报告/tmp/` 或项目根 `tmp/` 中的结论作为本次决策依据。")
    lines.append("- 自动化脚本：`scripts/generate_poet_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对POET的低基数右尾、强现金跑道、极高估值、负利润、订单条件性和高波动做目标公司校准后建档；未读取下游量化目录或现成排序结论。")
    lines.append("")
    lines.append("### 公司全集最新正式评估文件清单")
    lines.append("")
    lines.append(row(["股票代号", "公司名称", "评估日期", "正式评估文件"]))
    lines.append(row(["---", "---", "---", "---"]))
    for ticker in sorted(companies):
        c = companies[ticker]
        lines.append(row([ticker, c.name, c.eval_date, f"`{c.eval_path.relative_to(ROOT).as_posix()}`"]))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    fw.TARGET = TARGET
    companies = fw.load_latest_reports()
    if TARGET not in companies:
        raise SystemExit("缺少 POET 正式评估文件")

    index = fw.load_index_categories()
    finance, _ = fw.load_finance()
    ret_1m = fw.load_return_table(fw.RET_1M_PATH, "过去1个月涨跌幅")
    ret_2w = fw.load_return_table(fw.RET_2W_PATH, "过去两周涨跌幅")
    soxx = fw.load_return_table(fw.SOXX_PATH, "三段累计涨跌幅")

    for ticker, company in companies.items():
        if ticker in index:
            idx_name, category = index[ticker]
            company.category = category
            if company.name.replace(" ", "") == ticker:
                company.name = idx_name
        company.finance = finance.get(ticker, {})
        company.returns = {"1m": ret_1m.get(ticker), "2w": ret_2w.get(ticker), "soxx": soxx.get(ticker)}

    fw.build_metrics(companies)
    fw.assign_scores(companies)
    calibrate_poet_scores(companies)
    fw.assign_grades(companies)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = build_report(companies)
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(OUT_PATH)
    print(f"companies={len(companies)} b={len(companies) - 1} bytes={OUT_PATH.stat().st_size}")
    print("POET grades:", {s: companies[TARGET].grades[s] for s in STRATEGIES})
    print("POET ranks:", {s: companies[TARGET].ranks[s] for s in STRATEGIES})


if __name__ == "__main__":
    main()
