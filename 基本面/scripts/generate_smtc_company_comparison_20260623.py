from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path


BASE_PATH = Path(__file__).resolve().parent / "generate_cien_company_comparison_20260623.py"
spec = importlib.util.spec_from_file_location("company_comparison_base_cien_20260623", BASE_PATH)
if spec is None or spec.loader is None:
    raise SystemExit(f"Cannot load base comparison helpers from {BASE_PATH}")
base = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = base
spec.loader.exec_module(base)


ROOT = base.ROOT
TARGET = "SMTC"
TARGET_NAME = "Semtech Corporation"
REPORT_DATE = "2026-06-23"
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "SMTC_逐家公司投资思路对比_2026-06-23.md"

STRATEGIES = base.STRATEGIES
LABEL_ORDER = base.LABEL_ORDER
GRADE_VALUE = base.GRADE_VALUE

DIRECT_PEERS = {
    "CRDO",
    "MTSI",
    "MXL",
    "MRVL",
    "SITM",
}

UPSTREAM_DOWNSTREAM = {
    # Optical modules, lasers, components, cables, connectors and network equipment.
    "AAOI",
    "ANET",
    "APH",
    "BDC",
    "BELFB",
    "CIEN",
    "COHR",
    "CSCO",
    "GLW",
    "LITE",
    "LWLG",
    "NOK",
    "POET",
    "TEL",
    "VIAV",
    "VISN",
    # AI server, storage, EMS and cloud buyers of networking or connectivity capacity.
    "AMZN",
    "BABA",
    "CLS",
    "CRWV",
    "DELL",
    "DLR",
    "EQIX",
    "FLEX",
    "FN",
    "GOOGL",
    "HPE",
    "IREN",
    "JBL",
    "META",
    "MSFT",
    "NBIS",
    "NTAP",
    "NTNX",
    "ORCL",
    "PENG",
    "PSTG",
    "SANM",
    "SMCI",
    # Foundry, EDA/IP, packaging, test, materials and power devices used by data-center semis.
    "ADI",
    "ALAB",
    "AMAT",
    "AMKR",
    "ARM",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "CAMT",
    "CDNS",
    "COHU",
    "ENTG",
    "FORM",
    "GFS",
    "ICHR",
    "IMOS",
    "KLAC",
    "KLIC",
    "LRCX",
    "MKSI",
    "NVMI",
    "ONTO",
    "PLAB",
    "Q",
    "SNPS",
    "TER",
    "TOELY",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
}

AI_INFRA_ADJACENT_CATEGORIES = {
    "AI服务器_存储_EMS",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "云算力_IDC_AI软件平台",
    "配电_电源_功率器件",
    "电力_发电_能源_储能",
    "机电_冷却_工程_水处理_边缘工业AI",
}


def md_escape(value: object) -> str:
    return base.md_escape(value)


def relation_for(b: object) -> str:
    ticker = str(b.ticker)
    category = str(b.category)
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in UPSTREAM_DOWNSTREAM:
        return "上下游"
    if category in AI_INFRA_ADJACENT_CATEGORIES:
        return "相邻替代"
    return "跨赛道"


def strength_label(side: str, diff: int, score_diff: float, relation: str, missing: bool) -> str:
    if missing:
        if abs(score_diff) < 0.08:
            return "中性"
        return f"微倾向投{side}"
    if diff >= 3:
        label = f"强烈建议投{side}"
    elif diff == 2:
        label = f"建议投{side}"
    elif diff == 1:
        label = f"微倾向投{side}"
    else:
        if abs(score_diff) >= 0.12:
            label = f"微倾向投{side}"
        else:
            return "中性"

    if relation == "跨赛道":
        if label.startswith("强烈"):
            label = f"建议投{side}"
        elif label.startswith("建议") and diff <= 2:
            label = f"微倾向投{side}"
    if relation == "直接同业" and label.startswith("微倾向") and abs(score_diff) >= 0.14:
        label = f"建议投{side}"
    return label


def reason_for(strat: str, label: str, b: object, relation: str) -> str:
    if label == "中性":
        if relation == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，证据互有强弱"

    side = "A" if label.endswith("投A") else "B"
    if side == "A":
        return {
            "NTM兑现优先": "SMTC Q2指引、data center和LoRa收入锚更硬",
            "右尾弹性优先": "1.6T、CopperEdge、HieFo和LoRa+右尾更大",
            "风险调整收益": "高毛利增长与FCF改善组合更优",
            "下行保护优先": "LoRa和半导体现金流给A一定底线",
            "估值消化优先": "NTM EBITDA扩张可部分消化估值",
            "近端催化优先": "Q2/Q3、1.6T、CopperEdge和LoRa节点更近",
            "价格确认/动量": "近期价格确认强且基本面同步上修",
            "激进短线": "高IV、光互联和active copper叙事更适合进攻",
        }[strat]

    return {
        "NTM兑现优先": f"{b.ticker} NTM兑现证据更强",
        "右尾弹性优先": f"{b.ticker}右尾空间或小基数弹性更大",
        "风险调整收益": f"{b.ticker}上行下行组合更优",
        "下行保护优先": f"{b.ticker}现金流、估值或压力期更稳",
        "估值消化优先": f"{b.ticker}当前估值更易被业绩消化",
        "近端催化优先": f"{b.ticker}近端事件重定价概率更高",
        "价格确认/动量": f"{b.ticker}价格趋势确认更强",
        "激进短线": f"{b.ticker}短线波动和资金关注更强",
    }[strat]


def decision_for(a: object, b: object, strat: str, relation: str) -> str:
    ga = a.grades[strat]
    gb = b.grades[strat]
    sa = a.scores.get(strat)
    sb = b.scores.get(strat)
    missing = ga == "资料不足" or gb == "资料不足"
    score_diff = (sa if sa is not None else 0.5) - (sb if sb is not None else 0.5)
    diff = GRADE_VALUE.get(ga, 0) - GRADE_VALUE.get(gb, 0)
    if diff > 0 or (diff == 0 and score_diff > 0.04):
        label = strength_label("A", diff, score_diff, relation, missing)
    elif diff < 0 or (diff == 0 and score_diff < -0.04):
        label = strength_label("B", -diff, score_diff, relation, missing)
    else:
        label = "中性"
    return f"{label}：{reason_for(strat, label, b, relation)}"


def label_side(cell: str) -> str:
    label = cell.split("：", 1)[0]
    if label.endswith("投A"):
        return "A"
    if label.endswith("投B"):
        return "B"
    return "N"


def grade_summary(a: object, b: object) -> str:
    a_strong: list[str] = []
    b_strong: list[str] = []
    near: list[str] = []
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
    for strat in STRATEGIES:
        diff = GRADE_VALUE[a.grades[strat]] - GRADE_VALUE[b.grades[strat]]
        if diff >= 1:
            a_strong.append(short_names[strat])
        elif diff <= -1:
            b_strong.append(short_names[strat])
        else:
            near.append(short_names[strat])
    parts: list[str] = []
    if a_strong:
        parts.append("A强：" + "、".join(a_strong[:4]))
    if b_strong:
        parts.append("B强：" + "、".join(b_strong[:4]))
    if near:
        parts.append("接近：" + "、".join(near[:3]))
    return "；".join(parts)


def final_choice(decisions: dict[str, str], b: object) -> tuple[str, str, str]:
    counts = Counter(label_side(v) for v in decisions.values())
    a_count, b_count, n_count = counts["A"], counts["B"], counts["N"]
    if a_count > b_count:
        final = TARGET
        reason = "SMTC在多数思路下更适合高增长光互联/LoRa兑现和近端催化配置。"
    elif b_count > a_count:
        final = b.ticker
        reason = f"{b.ticker}在多数思路下胜出，SMTC需要更硬收入、利润或估值消化证据。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = TARGET
            reason = "多数思路打平时，风险调整收益更支持SMTC。"
        elif risk_label.endswith("投B"):
            final = b.ticker
            reason = f"多数思路打平时，风险调整收益更支持{b.ticker}。"
        else:
            ntm_label = decisions["NTM兑现优先"].split("：", 1)[0]
            if ntm_label.endswith("投B"):
                final = b.ticker
                reason = f"多数思路打平，NTM兑现略偏{b.ticker}。"
            else:
                final = TARGET
                reason = "多数思路打平，SMTC近端收入锚略更清楚。"
    return f"A {a_count} / B {b_count} / 中性 {n_count}", final, reason


def format_grade_position(c: object, strat: str) -> str:
    return base.format_grade_position(c, strat)


def grade_support_limit(strat: str, c: object) -> tuple[str, str]:
    support = {
        "NTM兑现优先": "Q1收入$291M、Q2指引$328M、data center +35% QoQ目标和LoRa all-time-high目标",
        "右尾弹性优先": "1.6T optical、CopperEdge ACC、HieFo光子器件和LoRa+构成多条非线性上行线",
        "风险调整收益": "基准收入+24%-36%、EBITDA和FCF扩张，但需要估值和执行折扣",
        "下行保护优先": "LoRa、TVS和部分IoT/legacy业务提供底座，Q1 FCF为正",
        "估值消化优先": "基准EBITDA $310M-$365M、FCF $150M-$210M，可部分解释高倍数",
        "近端催化优先": "Q2 FY2027、H2 1.6T module ramp、CopperEdge客户进展、LoRa季度收入节点集中",
        "价格确认/动量": "最新金融快照显示SMTC价格与近端趋势强，光互联主题同步升温",
        "激进短线": "Call/Put IV约98%、小中市值、光互联和active copper资金关注度高",
    }[strat]
    limit = {
        "NTM兑现优先": "1.6T/CopperEdge/HieFo分产品收入未披露，IoT剥离和低毛利业务仍会扰动",
        "右尾弹性优先": "极度乐观需要多客户量产、扩产、认证和毛利同时兑现，当前可信度低",
        "风险调整收益": "Forward PE约45倍、P/S约14.9倍、EV/EBITDA约99倍，高IV放大回撤",
        "下行保护优先": "SOXX压力窗口弱、TTM EPS为负且估值支撑不足，不能当防御资产",
        "估值消化优先": "当前估值已经要求data center和LoRa持续超预期，悲观情景缓冲有限",
        "近端催化优先": "若Q2 data center或Q3指引不继续加速，催化会快速转成反证",
        "价格确认/动量": "区间涨跌文件日期为2026-06-03，需用后续行情刷新；涨幅也可能过热",
        "激进短线": "高波动适合进攻但也意味止损风险高，不能忽略客户认证和营运资本反证",
    }[strat]
    return support, limit


def winning_strats(decisions: dict[str, str], side: str) -> str:
    out = [s for s, cell in decisions.items() if label_side(cell) == side]
    return "、".join(out) if out else "无"


def make_report(companies: dict[str, object]) -> str:
    a = companies[TARGET]
    rows: list[list[str]] = []
    stats: dict[str, Counter] = {s: Counter() for s in STRATEGIES}
    b_rank_rows: list[tuple[int, int, object, dict[str, str]]] = []
    a_rank_rows: list[tuple[int, int, object, dict[str, str]]] = []
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
        counts = Counter(label_side(v) for v in decisions.values())
        rows.append(
            [
                str(idx),
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
        f"- A 最占优的投资思路：`{a_best}`，A侧合计 {by_strategy_a[a_best]}/{len(sorted_bs)}；优势集中在 data center optical、LoRa 和近端收入/订单催化。",
        f"- A 最吃亏的投资思路：`{a_worst}`，B侧合计 {by_strategy_b[a_worst]}/{len(sorted_bs)}；主要输给现金流更稳、估值更低或压力期表现更好的公司。",
        "- A 最适合的投资者画像：愿意承担高波动，重点买 AI 光互联/active copper 和 LoRa 兑现弹性的成长型投资者。",
        "- A 最不适合的投资者画像：要求低回撤、低估值、稳定盈利或只买现金流防御资产的投资者。",
        f"- 多数思路下最强反方公司：{strongest_b_names}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：SMTC 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后，属于全项目进攻成长强势档，但不是风险调整或下行保护顶档。",
        "- 后续最重要跟踪数据：Q2 FY2027实际data center收入、Q3指引、Signal Integrity毛利率、LoRa季度收入、CopperEdge客户数量、1.6T product revenue/backlog、HieFo扩产和FCF/营运资本。",
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
    bear = base.bullet_after(conclusion, "悲观情景触发条件") or base.bullet_after(a_intro, "最大反证")
    catalysts = base.bullet_after(conclusion, "乐观情景成立条件") or base.bullet_after(conclusion, "后续跟踪数据")

    lines: list[str] = []
    lines.append("# SMTC 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：SMTC / {TARGET_NAME}")
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
    lines.append("| 股票代号 | SMTC |")
    lines.append(f"| 公司名称 | {TARGET_NAME} |")
    lines.append(f"| 产业链分类 | {a.category} |")
    lines.append(f"| 重要产品/业务线 | {md_escape(base.short_phrase(products, 260))} |")
    lines.append(f"| NTM 基准收入 | {md_escape(ntm)} |")
    lines.append(f"| 乐观/极度乐观收入 | {md_escape(optimistic)} |")
    lines.append(f"| 利润和现金流结论 | {md_escape(base.short_phrase(profit_cash, 240))} |")
    lines.append(f"| 最大传导瓶颈 | {md_escape(base.short_phrase(bottleneck, 240))} |")
    lines.append(f"| 最大反证 | {md_escape(base.short_phrase(bear, 240))} |")
    lines.append(f"| 近端催化剂 | {md_escape(base.short_phrase(catalysts, 240))} |")
    lines.append("")

    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append("| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for strat in STRATEGIES:
        sup, lim = grade_support_limit(strat, a)
        lines.append(f"| {strat} | {a.grades[strat]} | {format_grade_position(a, strat)} | {md_escape(sup)} | {md_escape(lim)} |")
    lines.append("")

    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | 同属数据中心连接/信号完整性/高速模拟和网络半导体需求池，优先比较设计赢单、客户量产、毛利、产品代际和估值消化 | CRDO、MTSI、MXL、MRVL、SITM | 同档或相邻档可以用更明确的收入兑现和产品代际证据放大到建议级别 |")
    lines.append("| 相邻替代 | 同属 AI 基础设施资金篮子，但产品不直接竞争，重点比较增长质量、兑现确定性、估值消化和短线资金偏好 | NVDA、AVGO、ALAB、VRT、ETN、GEV | 默认按全项目档位判断，除非增长质量或估值明显拉开，否则少用强烈建议 |")
    lines.append("| 上下游 | 光模块、连接器、网络设备、云/IDC、晶圆制造、封测和材料等处于同一需求链，重点看利润池位置、议价权和传导瓶颈 | COHR、LITE、AAOI、CIEN、ANET、TSM、AMAT、AMZN | 不把下游收入规模或上游瓶颈自动等同为胜出，强调利润捕获和订单转收入 |")
    lines.append("| 跨赛道 | 化工材料、工业设备、部分公用事业/航天等与 SMTC 业务差异大，但仍可作为资金配置替代 | LIN、ECL、TMO、CAT、RKLB | 默认降低结论力度；证据互有强弱时优先微倾向或中性 |")
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
        lines.append("| " + " | ".join(md_escape(x) for x in row) + " |")
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

    lines.append("## 7. 多数思路下 B 明显强于 A 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | B 胜出的主要投资思路 | 为什么 B 更值得投 | A 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(
            f"| {rank} | {b.ticker} / {md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在对应档位中高于SMTC，且多数思路下增长、估值、下行保护或价格证据更强。 | SMTC需要Q2/Q3 data center继续加速、1.6T/CopperEdge显性收入、LoRa保持$50M+季度run-rate并降低估值压力。 |"
        )
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过SMTC | 继续跟踪收入和价格确认 |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(
            f"| {rank} | {b.ticker} / {md_escape(b.name)} | {winning_strats(decisions, 'A')} | SMTC相对{b.ticker}的AI光互联/LoRa收入兑现、右尾或近端催化更清楚。 | {b.ticker}需要更硬的NTM订单/利润兑现、估值消化证据和价格确认。 |"
        )
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | SMTC没有在多数思路下明显压过其他公司 | 需等待订单和价格进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{base.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{base.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{base.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{base.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md` 用于公司名称和分类；SMTC 评估报告内已列出的公司调研、行业调研和官方财报/IR来源用于 A 侧业务证据。")
    lines.append("- 排除来源：未使用 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/备份/`、`分析报告/tmp/` 或项目根 `tmp/` 中的结论作为本次决策依据。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    companies = base.load_latest_reports()
    if TARGET not in companies:
        raise SystemExit("SMTC not found in formal company evaluation universe")

    index = base.load_index_categories()
    finance, _ = base.load_finance()
    ret_1m = base.load_return_table(base.RET_1M_PATH, "过去1个月涨跌幅")
    ret_2w = base.load_return_table(base.RET_2W_PATH, "过去两周涨跌幅")
    soxx = base.load_return_table(base.SOXX_PATH, "三段累计涨跌幅")

    for ticker, c in companies.items():
        if ticker in index:
            idx_name, cat = index[ticker]
            c.category = cat
            if c.name.replace(" ", "") == ticker or c.name == ticker:
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
    print("SMTC grades:", {s: companies[TARGET].grades[s] for s in STRATEGIES})


if __name__ == "__main__":
    main()
