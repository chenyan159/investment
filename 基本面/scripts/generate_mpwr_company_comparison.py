from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_cien_company_comparison_20260623 as base


TARGET = "MPWR"
TARGET_NAME = "Monolithic Power Systems"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MPWR_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.TARGET_NAME = TARGET_NAME
base.OUT_PATH = OUT_PATH

STRATEGIES = base.STRATEGIES
LABEL_ORDER = base.LABEL_ORDER
GRADE_VALUE = base.GRADE_VALUE

DIRECT_POWER_PEERS = {
    "ADI",
    "AOSL",
    "DIOD",
    "IFNNY",
    "LFUS",
    "MCHP",
    "NVTS",
    "ON",
    "POWI",
    "STM",
    "TXN",
    "VICR",
    "VSH",
    "WOLF",
}

POWER_COMPONENT_ADJACENT = {
    "ABBNY",
    "AEIS",
    "ATKR",
    "ETN",
    "HUBB",
    "MIELY",
    "MRAAY",
    "NVT",
    "POWL",
    "ST",
    "TTDKY",
}

AI_PLATFORM_CHAIN = {
    "ALAB",
    "AMD",
    "AMZN",
    "ANET",
    "APLD",
    "ARM",
    "AVGO",
    "BABA",
    "CDNS",
    "CIEN",
    "COHR",
    "CRDO",
    "CRWV",
    "CSCO",
    "DELL",
    "FN",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "JBL",
    "LITE",
    "META",
    "MRVL",
    "MSFT",
    "MU",
    "NBIS",
    "NVDA",
    "ORCL",
    "QCOM",
    "SANM",
    "SMCI",
    "SNPS",
    "TSM",
}

DATA_CENTER_INFRA_ADJACENT = {
    "AAON",
    "BE",
    "CARR",
    "CEG",
    "EME",
    "ENS",
    "EQIX",
    "FIX",
    "GEV",
    "JCI",
    "MOD",
    "PWR",
    "TT",
    "VRT",
    "VST",
}


def relation_for(b: base.Company) -> str:
    ticker = b.ticker
    cat = b.category
    if ticker in DIRECT_POWER_PEERS:
        return "直接同业"
    if ticker in AI_PLATFORM_CHAIN:
        return "上下游"
    if ticker in POWER_COMPONENT_ADJACENT or ticker in DATA_CENTER_INFRA_ADJACENT:
        return "相邻替代"
    if cat in {"AI服务器_存储_EMS", "AI计算芯片_EDA_IP_custom_ASIC", "AI网络_光互联_连接器", "云算力_IDC_AI软件平台"}:
        return "上下游"
    if cat in {"配电_电源_功率器件", "电力_发电_能源_储能", "机电_冷却_工程_水处理_边缘工业AI"}:
        return "相邻替代"
    return "跨赛道"


def reason_for(strat: str, label: str, b: base.Company, relation: str) -> str:
    if label == "中性":
        if relation == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，证据互有强弱"
    side = "A" if label.endswith("投A") else "B"
    if side == "A":
        return {
            "NTM兑现优先": "MPWR ED/Comms已确认高增且Q2指引清楚",
            "右尾弹性优先": "MPWR AI近端供电和48V/800V期权更直接",
            "风险调整收益": "MPWR增长、毛利和现金流质量更均衡",
            "下行保护优先": "MPWR净现金和55%+毛利提供底盘",
            "估值消化优先": "MPWR NTM增长可部分消化高估值",
            "近端催化优先": "MPWR Q2/Q3、ED/Comms和产能验证更近",
            "价格确认/动量": "MPWR阶段价格确认仍较好",
            "激进短线": "MPWR AI供电叙事、IV和催化共振更强",
        }[strat]
    return {
        "NTM兑现优先": f"{b.ticker} NTM兑现证据更硬",
        "右尾弹性优先": f"{b.ticker}右尾空间或小基数弹性更大",
        "风险调整收益": f"{b.ticker}上行下行组合更优",
        "下行保护优先": f"{b.ticker}现金流、估值或压力期更稳",
        "估值消化优先": f"{b.ticker}当前估值更易被业绩消化",
        "近端催化优先": f"{b.ticker}近端事件重定价概率更高",
        "价格确认/动量": f"{b.ticker}价格趋势确认更强",
        "激进短线": f"{b.ticker}短线波动和资金关注更强",
    }[strat]


def decision_for(a: base.Company, b: base.Company, strat: str, relation: str) -> str:
    ga = a.grades[strat]
    gb = b.grades[strat]
    sa = a.scores.get(strat)
    sb = b.scores.get(strat)
    missing = ga == "资料不足" or gb == "资料不足"
    score_diff = (sa if sa is not None else 0.5) - (sb if sb is not None else 0.5)
    diff = GRADE_VALUE.get(ga, 0) - GRADE_VALUE.get(gb, 0)
    if diff > 0 or (diff == 0 and score_diff > 0.04):
        label = base.strength_label("A", diff, score_diff, relation, missing)
    elif diff < 0 or (diff == 0 and score_diff < -0.04):
        label = base.strength_label("B", -diff, score_diff, relation, missing)
    else:
        label = "中性"
    return f"{label}：{reason_for(strat, label, b, relation)}"


def final_choice(decisions: dict[str, str], b: base.Company) -> tuple[str, str, str]:
    counts = Counter(base.label_side(v) for v in decisions.values())
    a_count, b_count, n_count = counts["A"], counts["B"], counts["N"]
    if a_count > b_count:
        final = TARGET
        reason = "MPWR在多数思路下兑现、利润质量或AI供电稀缺性更强。"
    elif b_count > a_count:
        final = b.ticker
        reason = f"{b.ticker}在多数思路下胜出，MPWR需要更强订单、估值消化或价格证据。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = TARGET
            reason = "多数思路打平时，风险调整收益更支持MPWR。"
        elif risk_label.endswith("投B"):
            final = b.ticker
            reason = f"多数思路打平时，风险调整收益更支持{b.ticker}。"
        else:
            ntm_label = decisions["NTM兑现优先"].split("：", 1)[0]
            if ntm_label.endswith("投A"):
                final = TARGET
                reason = "多数思路打平，MPWR的NTM兑现路径略更清楚。"
            elif ntm_label.endswith("投B"):
                final = b.ticker
                reason = f"多数思路打平，NTM兑现略偏{b.ticker}。"
            else:
                final = "中性"
                reason = "多数思路和核心兑现证据均接近。"
    return f"A {a_count} / B {b_count} / 中性 {n_count}", final, reason


def grade_support_limit(strat: str, c: base.Company) -> tuple[str, str]:
    support = {
        "NTM兑现优先": "2026Q1收入804.2M、Q2指引890M-910M、ED同比97.7%、Comms同比55.5%",
        "右尾弹性优先": "AI/server power、48V/54V IBC、Intelli-Module、800V/HVDC和Z-Axis提供上限",
        "风险调整收益": "基准NTM收入3.75B-3.95B、55%+毛利、强经营现金流和净现金",
        "下行保护优先": "高毛利、现金及短投1.367B、汽车/工业底盘和盈利质量较强",
        "估值消化优先": "NTM基准增速34%-42%，乐观增速45%-56%，经营杠杆可兑现",
        "近端催化优先": "Q2实际收入/Q3指引、ED/Comms分部、库存天数和6B产能目标可连续验证",
        "价格确认/动量": "区间资料显示过去1个月+6.72%、过去两周+8.80%，基本面有同步支撑",
        "激进短线": "AI供电、48V/800V架构、76%附近IV和高端模块叙事具进攻性",
    }[strat]
    limit = {
        "NTM兑现优先": "公司不披露backlog/bookings/客户名，订单覆盖仍不可审计",
        "右尾弹性优先": "800V/HVDC和Z-Axis仍偏样品/认证，极度乐观不能进基准",
        "风险调整收益": "Forward PE约50.7、P/S约25.6，估值已要求较高兑现",
        "下行保护优先": "SOXX压力窗口累计约-74.3%，高估值和高IV削弱防御属性",
        "估值消化优先": "当前价格已经透支部分乐观，需要连续超指引验证",
        "近端催化优先": "客户平台节奏、socket share和库存周转若转弱会迅速反证",
        "价格确认/动量": "区间涨跌资料截至2026-06-03，需结合后续日度行情刷新",
        "激进短线": "相比小市值光互联/电力右尾票，短线爆发性不是最高",
    }[strat]
    return support, limit


def make_report(companies: dict[str, base.Company]) -> str:
    a = companies[TARGET]
    rows: list[list[str]] = []
    stats: dict[str, Counter] = {s: Counter() for s in STRATEGIES}
    b_rank_rows = []
    a_rank_rows = []
    decisions_by_b: dict[str, dict[str, str]] = {}

    sorted_bs = [c for t, c in companies.items() if t != TARGET]
    sorted_bs.sort(key=lambda c: (c.category, c.ticker))

    for idx, b in enumerate(sorted_bs, start=1):
        relation = relation_for(b)
        decisions = {s: decision_for(a, b, s, relation) for s in STRATEGIES}
        decisions_by_b[b.ticker] = decisions
        for s, cell in decisions.items():
            stats[s][cell.split("：", 1)[0]] += 1
        majority, final, final_reason = final_choice(decisions, b)
        counts = Counter(base.label_side(v) for v in decisions.values())
        rows.append(
            [
                str(idx),
                f"{b.ticker} / {b.name}",
                b.category,
                relation,
                base.grade_summary(a, b),
                *[decisions[s] for s in STRATEGIES],
                majority,
                final,
                final_reason,
            ]
        )
        diff = counts["B"] - counts["A"]
        if diff >= 3:
            b_rank_rows.append((diff, counts["B"], b, decisions))
        if -diff >= 3:
            a_rank_rows.append((-diff, counts["A"], b, decisions))

    a_majority_wins = sum(1 for b, ds in decisions_by_b.items() if final_choice(ds, companies[b])[1] == TARGET)
    b_majority_wins = len(sorted_bs) - a_majority_wins
    by_strategy_a = {s: stats[s]["强烈建议投A"] + stats[s]["建议投A"] + stats[s]["微倾向投A"] for s in STRATEGIES}
    by_strategy_b = {s: stats[s]["强烈建议投B"] + stats[s]["建议投B"] + stats[s]["微倾向投B"] for s in STRATEGIES}
    a_best = max(STRATEGIES, key=lambda s: by_strategy_a[s])
    a_worst = max(STRATEGIES, key=lambda s: by_strategy_b[s])
    strongest_b = sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker))[:10]
    strongest_b_names = "、".join(f"{b.ticker}" for _, _, b, _ in strongest_b) or "无明显集中反方"

    eval_dates = [c.eval_date for c in companies.values()]
    finance_meta = base.load_finance()[1]
    missing_finance = sorted([t for t, c in companies.items() if not c.finance])

    one_page = [
        f"- A 最占优的投资思路：`{a_best}`，A侧合计 {by_strategy_a[a_best]}/{len(sorted_bs)}；核心来自 Q2 指引、ED/Comms 高增、55%+毛利和强现金流。",
        f"- A 最吃亏的投资思路：`{a_worst}`，B侧合计 {by_strategy_b[a_worst]}/{len(sorted_bs)}；主要输给防御型公用事业/现金流资产、低估值周期底部票和更极端小基数右尾票。",
        "- A 最适合的投资者画像：偏中期基本面，愿意为 AI 服务器近端供电稀缺性、利润质量和可兑现增长支付高估值的投资者。",
        "- A 最不适合的投资者画像：只追求低估值防御、极端短线爆发，或要求客户订单/backlog完全透明的人。",
        f"- 多数思路下最强反方公司：{strongest_b_names}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：MPWR 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后，属于全项目高质量成长层，但估值和压力期表现限制其成为所有思路的绝对首选。",
        "- 后续最重要跟踪数据：2026Q2实际收入和Q3指引、Enterprise Data与Communications收入、Non-GAAP GM、库存/DIO/经营现金流、6B产能目标、48V/54V模块量产客户、800V/HVDC和Z-Axis客户认证。"
    ]

    a_intro = base.section_between(a.text, "1. 一页结论")
    conclusion = base.section_between(a.text, "8. 结论")
    products = base.bullet_after(a_intro, "重要产品/业务线")
    ntm = a.scenarios.get("基准", {}).get("NTM 公司收入", "")
    optimistic = " / ".join(
        filter(
            None,
            [
                a.scenarios.get("乐观", {}).get("NTM 公司收入", ""),
                a.scenarios.get("极度乐观", {}).get("NTM 公司收入", ""),
            ],
        )
    )
    profit_cash = base.bullet_after(conclusion, "利润/现金流结论") or base.bullet_after(a_intro, "利润或 EBITDA 四情景")
    bottleneck = base.bullet_after(conclusion, "主要传导瓶颈") or base.bullet_after(a_intro, "最大传导瓶颈")
    bear = base.bullet_after(conclusion, "悲观情景触发条件") or base.bullet_after(a_intro, "最大传导瓶颈")
    catalysts = base.bullet_after(conclusion, "乐观情景成立条件") or base.bullet_after(conclusion, "后续跟踪数据")

    lines: list[str] = []
    lines.append("# MPWR 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：MPWR / {TARGET_NAME}")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(companies) - 1}")
    lines.append(f"公司评估文件日期范围：{min(eval_dates)} 至 {max(eval_dates)}")
    lines.append("日度数据日期：价格/估值/IV 为 2026-06-22；过去两周和过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。")
    lines.append("")
    lines.append("> 口径说明：本报告读取 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/公司索引.md`、`金融资料/每日金融数据/每日金融数据_2026-06-22.md` 和 `金融资料/区间涨跌/` 三个正式行情文件。未读取、引用或继承 `特征量化/`、Signals、回归、模型比较或 `公司排序/` 的现成排序结果；`备份/` 与 `tmp/` 不作为决策输入。")
    if missing_finance:
        lines.append(f"> 金融资料覆盖差异：正式评估公司 {len(companies)} 家，最新金融快照覆盖 {len(companies) - len(missing_finance)} 家；缺少日度金融明细的公司为 {', '.join(missing_finance)}，价格/估值/IV/动量相关档位按资料不足或低置信处理。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.extend(one_page)
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | MPWR |")
    lines.append(f"| 公司名称 | {TARGET_NAME} |")
    lines.append(f"| 产业链分类 | {a.category} |")
    lines.append(f"| 重要产品/业务线 | {base.md_escape(base.short_phrase(products, 240))} |")
    lines.append(f"| NTM 基准收入 | {base.md_escape(ntm)} |")
    lines.append(f"| 乐观/极度乐观收入 | {base.md_escape(optimistic)} |")
    lines.append(f"| 利润和现金流结论 | {base.md_escape(base.short_phrase(profit_cash, 220))} |")
    lines.append(f"| 最大传导瓶颈 | {base.md_escape(base.short_phrase(bottleneck, 220))} |")
    lines.append(f"| 最大反证 | {base.md_escape(base.short_phrase(bear, 220))} |")
    lines.append(f"| 近端催化剂 | {base.md_escape(base.short_phrase(catalysts, 220))} |")
    lines.append("")

    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append("| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for strat in STRATEGIES:
        sup, lim = grade_support_limit(strat, a)
        lines.append(f"| {strat} | {a.grades[strat]} | {base.format_grade_position(a, strat)} | {base.md_escape(sup)} | {base.md_escape(lim)} |")
    lines.append("")

    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | 同属模拟/电源管理/功率器件或高密度供电方案，优先比较AI server socket、产品代际、毛利率、订单/指引和同业估值 | ADI、TXN、VICR、POWI、ON、STM、IFNNY | 同档或相邻档可放大公司证据，尤其看谁真正吃到AI供电需求池 |")
    lines.append("| 相邻替代 | 同属AI基础设施或数据中心电力资金篮子，但利润池和产品不同，重点比较增长质量、估值消化和催化可见度 | VRT、ETN、POWL、GEV、FIX、TT、EQIX | 默认按档位判断，除非增长和估值显著拉开，否则少用强烈建议 |")
    lines.append("| 上下游 | GPU/ASIC、服务器、云厂、光互联和网络公司与MPWR处于需求链上下游，重点看利润捕获、议价权和客户平台节奏 | NVDA、AMD、AVGO、MRVL、DELL、SMCI、AMZN、MSFT、ANET、CRDO | 不把下游收入规模自动等同为胜出，也不把上游瓶颈自动等同为高赔率 |")
    lines.append("| 跨赛道 | 半导体材料、前道设备、封测、化工、工业等与MPWR业务差异大，但仍可作为资金配置替代 | ASML、AMAT、LIN、ECL、TMO | 默认降低结论力度；若证据互有强弱，优先微倾向或中性 |")
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
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---:" if h == "序号" else "---" for h in headers]) + " |")
    for row in rows:
        lines.append("| " + " | ".join(base.md_escape(x) for x in row) + " |")
    lines.append("")

    lines.append("## 6. 投资思路统计")
    lines.append("")
    stat_headers = ["投资思路", *LABEL_ORDER, "A侧合计", "B侧合计"]
    lines.append("| " + " | ".join(stat_headers) + " |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for strat in STRATEGIES:
        counter = stats[strat]
        a_total = counter["强烈建议投A"] + counter["建议投A"] + counter["微倾向投A"]
        b_total = counter["强烈建议投B"] + counter["建议投B"] + counter["微倾向投B"]
        vals = [str(counter[label]) for label in LABEL_ORDER]
        lines.append(f"| {strat} | " + " | ".join(vals) + f" | {a_total} | {b_total} |")
    lines.append("")

    def winning_strats(decisions: dict[str, str], side: str) -> str:
        out = [s for s, cell in decisions.items() if base.label_side(cell) == side]
        return "、".join(out) if out else "无"

    lines.append("## 7. 多数思路下 B 明显强于 A 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | B 胜出的主要投资思路 | 为什么 B 更值得投 | A 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(
            f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在对应档位中高于MPWR，且多数思路下增长、右尾、估值、防御或价格证据更强。 | MPWR需要披露更硬客户订单/backlog、Q2/Q3连续超指引、库存下降且毛利率维持55%+，并刷新价格确认。 |"
        )
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过MPWR | 继续跟踪订单和价格确认 |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(
            f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'A')} | MPWR相对{b.ticker}的NTM收入兑现、AI供电稀缺性、利润质量或近端催化更清楚。 | {b.ticker}需要更硬的NTM订单/利润兑现、估值消化证据和价格确认。 |"
        )
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | MPWR没有在多数思路下明显压过其他公司 | 需等待MPWR订单和价格进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{base.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{base.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{base.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{base.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md` 用于公司名称和分类；MPWR 评估报告内已列出的公司调研、行业调研和官方财报/IR来源用于 A 侧业务证据；其他公司 B 的最新正式评估用于各自 NTM、利润、现金流、反证和催化判断。")
    lines.append("- 排除来源：未使用 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/备份/`、`分析报告/tmp/` 或项目根 `tmp/` 中的结论作为本次决策依据。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    companies = base.load_latest_reports()
    if TARGET not in companies:
        raise SystemExit("MPWR not found in formal company evaluation universe")

    index = base.load_index_categories()
    finance, _ = base.load_finance()
    ret_1m = base.load_return_table(base.RET_1M_PATH, "过去1个月涨跌幅")
    ret_2w = base.load_return_table(base.RET_2W_PATH, "过去两周涨跌幅")
    soxx = base.load_return_table(base.SOXX_PATH, "三段累计涨跌幅")

    for ticker, c in companies.items():
        if ticker in index:
            idx_name, cat = index[ticker]
            c.category = cat
            if c.name.replace(" ", "") == ticker:
                c.name = idx_name
        c.finance = finance.get(ticker, {})
        c.returns = {"1m": ret_1m.get(ticker), "2w": ret_2w.get(ticker), "soxx": soxx.get(ticker)}

    base.build_metrics(companies)
    base.assign_scores(companies)
    base.assign_grades(companies)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = make_report(companies)
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(OUT_PATH)
    print(f"companies={len(companies)} b={len(companies)-1} bytes={OUT_PATH.stat().st_size}")
    print("MPWR grades:", {s: companies[TARGET].grades[s] for s in STRATEGIES})


if __name__ == "__main__":
    main()
