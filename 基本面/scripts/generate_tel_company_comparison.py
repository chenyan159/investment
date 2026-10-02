from __future__ import annotations

from collections import Counter
from pathlib import Path

import generate_cien_company_comparison_20260623 as base


ROOT = Path(__file__).resolve().parents[1]
TARGET = "TEL"
TARGET_NAME = "TE Connectivity"
REPORT_DATE = "2026-06-23"
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "TEL_逐家公司投资思路对比_2026-06-23.md"

STRATEGIES = base.STRATEGIES
LABEL_ORDER = base.LABEL_ORDER
GRADE_VALUE = base.GRADE_VALUE

COMPANY_RESEARCH_PATH = ROOT / "公司调研" / "AI网络_光互联_连接器" / "TEL_TE Connectivity_公司调研_2026-06-11.md"
INDUSTRY_SOURCES = [
    "行业调研/AI网络_光互联_铜互联/行业调研_高速连接器、背板与结构化布线_2026-06-11.md",
    "行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md",
    "行业调研/AI园区电力_机电_冷却/行业调研_液冷小组件与流体控制_2026-06-10.md",
    "行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md",
]


DIRECT_CONNECTIVITY = {"APH", "BDC", "BELFB", "GLW", "SMTOY"}

AI_DEMAND_CHAIN = {
    "AAOI",
    "ADBE",
    "ALAB",
    "AMD",
    "AMZN",
    "ANET",
    "APLD",
    "ARM",
    "AVGO",
    "BABA",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "CRWD",
    "CRWV",
    "CSCO",
    "DELL",
    "DLR",
    "EQIX",
    "FLEX",
    "FN",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "JBL",
    "LITE",
    "LWLG",
    "META",
    "MRVL",
    "MSFT",
    "MTSI",
    "MU",
    "NBIS",
    "NOK",
    "NTAP",
    "NTNX",
    "NVDA",
    "ORCL",
    "PENG",
    "POET",
    "PSTG",
    "QCOM",
    "RMBS",
    "SANM",
    "SIMO",
    "SITM",
    "SMCI",
    "SMTC",
    "SNDK",
    "SNPS",
    "STX",
    "TSM",
    "VIAV",
    "VISN",
    "WDC",
}

POWER_AND_INDUSTRIAL_ADJACENT = {
    "AAON",
    "ABBNY",
    "AEIS",
    "ALLE",
    "ATKR",
    "BE",
    "BWXT",
    "CARR",
    "CAT",
    "CMI",
    "DCI",
    "DOV",
    "EME",
    "ENS",
    "ETN",
    "FIX",
    "FLNC",
    "FTV",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "IESC",
    "IFNNY",
    "JCI",
    "LFUS",
    "MIELY",
    "MOD",
    "MRAAY",
    "MSI",
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
    "ST",
    "TDY",
    "TMO",
    "TT",
    "TTDKY",
    "VICR",
    "VRT",
    "VSH",
}

UTILITY_AND_ENERGY_CUSTOMERS = {"AEP", "CEG", "DTE", "ET", "ETR", "VST"}


def relation_for(b: base.Company) -> str:
    cat = b.category
    if b.ticker in DIRECT_CONNECTIVITY:
        return "直接同业"
    if b.ticker in AI_DEMAND_CHAIN:
        return "上下游"
    if b.ticker in UTILITY_AND_ENERGY_CUSTOMERS:
        return "上下游"
    if b.ticker in POWER_AND_INDUSTRIAL_ADJACENT:
        return "相邻替代"
    if cat == "AI网络_光互联_连接器":
        return "相邻替代"
    if cat in {"AI服务器_存储_EMS", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
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
            "NTM兑现优先": "TEL订单、Q3指引和DDN收入兑现更清楚",
            "右尾弹性优先": "TEL DDN、224G和rack power仍有上修",
            "风险调整收益": "TEL现金流、低杠杆和估值消化更均衡",
            "下行保护优先": "TEL FCF、设计导入和低估值倍数更抗压",
            "估值消化优先": "TEL forward PE和FCF更易消化估值",
            "近端催化优先": "TEL Q3指引、DDN高增和订单B2B更近",
            "价格确认/动量": "TEL两周和一月价格确认更顺",
            "激进短线": "TEL AI连接器重估和中等IV仍有进攻性",
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
        final = f"A（{TARGET}）"
        reason = "TEL在多数思路下以DDN兑现、现金流、估值消化和连接器平台壁垒胜出。"
    elif b_count > a_count:
        final = f"B（{b.ticker}）"
        reason = f"{b.ticker}在多数思路下胜出，TEL需要更强DDN订单、AI/DC收入拆分或价格确认。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = f"A（{TARGET}）"
            reason = "多数思路打平时，风险调整收益更支持TEL。"
        elif risk_label.endswith("投B"):
            final = f"B（{b.ticker}）"
            reason = f"多数思路打平时，风险调整收益更支持{b.ticker}。"
        else:
            ntm_label = decisions["NTM兑现优先"].split("：", 1)[0]
            if ntm_label.endswith("投B"):
                final = f"B（{b.ticker}）"
                reason = f"多数思路打平，NTM兑现略偏{b.ticker}。"
            else:
                final = f"A（{TARGET}）"
                reason = "多数思路打平，TEL兑现路径略更清楚。"
    return f"A {a_count} / B {b_count} / 中性 {n_count}", final, reason


def grade_support_limit(strat: str, c: base.Company) -> tuple[str, str]:
    support = {
        "NTM兑现优先": "Q2 FY2026收入47.44亿美元、订单约53亿美元、B2B约1.12、Q3收入指引约50亿美元，NTM基准201-208亿美元",
        "右尾弹性优先": "DDN organic +46.1%、AI/Cloud FY2025约14亿美元并有30亿美元以上中期轨迹，224G/448G、rack power和Energy提供上修",
        "风险调整收益": "Forward PE约16.86x、P/S约3.32x、FCF质量高、杠杆健康，DDN增长与Transportation底盘组合较均衡",
        "下行保护优先": "连接器设计导入、客户认证、交通/工业/能源多元收入和FCF提供缓冲",
        "估值消化优先": "NTM收入201-208亿美元、基准FCF约26-31亿美元，16.86x forward PE低于多数高热AI硬件标的",
        "近端催化优先": "Q3收入/EPS指引、Q2订单+25%、DDN高增、Energy/Richards协同和AI/Cloud订单跟踪",
        "价格确认/动量": "过去1个月+5.28%、两周+8.44%，价格已经给出一定基本面确认",
        "激进短线": "AI数据中心高速连接、rack power、电网接入和45%-48% IV支持事件弹性",
    }[strat]
    limit = {
        "NTM兑现优先": "Transportation仍约半数收入且automotive有机-3.8%，DDN客户级backlog和AI收入拆分未披露",
        "右尾弹性优先": "TEL体量较大，DDN仍约15%收入；CPO/448G/800VDC大额NTM收入证据偏早",
        "风险调整收益": "SOXX压力窗口累计-50.44%，若DDN放缓或Transportation继续拖累，AI重估会回撤",
        "下行保护优先": "IV不低于传统防御资产，且2025-2026压力窗口回撤显示仍是周期硬件链",
        "估值消化优先": "若DDN增速从高位下滑、Energy并购协同不顺或交通继续弱，估值会从成长工业向普通工业回归",
        "近端催化优先": "缺少客户级AI订单、DDN backlog、224G/rack power金额披露，催化强度弱于小基数AI链",
        "价格确认/动量": "区间涨跌数据截至2026-06-03，2026-06-22价格低于6月初高点，需后续金融资料刷新",
        "激进短线": "相对光模块、AI芯片、存储、核能和小盘高IV标的，TEL短线爆发性不是顶档",
    }[strat]
    return support, limit


def grade_summary(a: base.Company, b: base.Company) -> str:
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
    parts = []
    if a_strong:
        parts.append("A强：" + "、".join(a_strong[:4]))
    if b_strong:
        parts.append("B强：" + "、".join(b_strong[:4]))
    if near:
        parts.append("接近：" + "、".join(near[:3]))
    return "；".join(parts)


def winning_strats(decisions: dict[str, str], side: str) -> str:
    out = [s for s, cell in decisions.items() if base.label_side(cell) == side]
    return "、".join(out) if out else "无"


def make_report(companies: dict[str, base.Company]) -> str:
    a = companies[TARGET]
    rows = []
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
                grade_summary(a, b),
                *[decisions[s] for s in STRATEGIES],
                majority,
                final,
                final_reason,
            ]
        )
        diff = counts["B"] - counts["A"]
        if diff >= 3 and counts["B"] >= 5:
            b_rank_rows.append((diff, counts["B"], b, decisions))
        if -diff >= 3 and counts["A"] >= 5:
            a_rank_rows.append((-diff, counts["A"], b, decisions))

    a_majority_wins = sum(1 for b, ds in decisions_by_b.items() if final_choice(ds, companies[b])[1].startswith("A"))
    b_majority_wins = len(sorted_bs) - a_majority_wins

    by_strategy_a = {s: stats[s]["强烈建议投A"] + stats[s]["建议投A"] + stats[s]["微倾向投A"] for s in STRATEGIES}
    by_strategy_b = {s: stats[s]["强烈建议投B"] + stats[s]["建议投B"] + stats[s]["微倾向投B"] for s in STRATEGIES}
    a_best = max(STRATEGIES, key=lambda s: by_strategy_a[s])
    a_worst = max(STRATEGIES, key=lambda s: by_strategy_b[s])
    strongest_b = sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker))[:8]
    strongest_b_names = "、".join(f"{b.ticker}" for _, _, b, _ in strongest_b) or "无明显集中反方"

    eval_dates = [c.eval_date for c in companies.values()]
    finance_meta = base.load_finance()[1]
    missing_finance = sorted([t for t, c in companies.items() if not c.finance])
    missing_returns = sorted([t for t, c in companies.items() if c.returns.get("1m") is None or c.returns.get("2w") is None])

    a_intro = base.section_between(a.text, "1. 一页结论")
    conclusion = base.section_between(a.text, "8. 结论")
    products = base.bullet_after(a_intro, "重要产品/业务线")
    ntm = a.scenarios.get("基准", {}).get("NTM 公司收入", "") or a.scenarios.get("基准", {}).get("NTM收入", "")
    optimistic = " / ".join(
        filter(
            None,
            [
                a.scenarios.get("乐观", {}).get("NTM 公司收入", "") or a.scenarios.get("乐观", {}).get("NTM收入", ""),
                a.scenarios.get("极度乐观", {}).get("NTM 公司收入", "") or a.scenarios.get("极度乐观", {}).get("NTM收入", ""),
            ],
        )
    )
    profit_cash = base.bullet_after(conclusion, "利润/现金流结论") or base.bullet_after(a_intro, "利润或 EBITDA 四情景")
    bottleneck = base.bullet_after(conclusion, "主要传导瓶颈") or base.bullet_after(a_intro, "最大传导瓶颈")
    bear = base.bullet_after(conclusion, "悲观情景触发条件") or "DDN增速放缓、Transportation继续拖累、Energy reported growth剥离并购后弱化、库存和应收占用压低FCF。"
    catalysts = base.bullet_after(conclusion, "后续跟踪数据") or base.bullet_after(conclusion, "乐观情景成立条件")

    one_page = [
        f"- A 最占优的投资思路：`{a_best}`，A侧合计 {by_strategy_a[a_best]}/{len(sorted_bs)}；核心来自低forward PE、强FCF、DDN收入化、订单B2B和高质量连接器设计导入。",
        f"- A 最吃亏的投资思路：`{a_worst}`，B侧合计 {by_strategy_b[a_worst]}/{len(sorted_bs)}；主要输给小基数AI芯片、光模块、存储、云算力和核能/电力高beta标的的右尾与短线爆发。",
        "- A 最适合的投资者画像：希望配置高质量工业连接器龙头，同时获得AI数据中心高速互联、rack power和电网接入增量的中期资金。",
        "- A 最不适合的投资者画像：只追求纯AI算力最高收入增速、最高IV、最强短线爆发或完全防御低回撤的人。",
        f"- 多数思路下最强反方公司：{strongest_b_names}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：按本报告最终二选一口径，TEL 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后；TEL属于全项目估值消化和质量较强、增长和短线弹性中等的AI基础设施连接器资产。",
        "- 后续最重要跟踪数据：FY2026 Q3收入/EPS、DDN单季收入和organic growth、订单和book-to-bill、Industrial margin、Transportation automotive是否恢复、Energy organic growth/Richards协同、224G/448G/rack power客户金额、FCF和库存应收。"
    ]

    lines: list[str] = []
    lines.append("# TEL 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：TEL / {TARGET_NAME}")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(companies) - 1}")
    lines.append(f"公司评估文件日期范围：{min(eval_dates)} 至 {max(eval_dates)}")
    lines.append("日度数据日期：价格/估值/IV 为 2026-06-22；过去两周和过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。")
    lines.append("")
    lines.append("> 口径说明：本报告读取 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/公司索引.md`、TEL正式公司调研、评估报告列示的行业调研口径，以及 `金融资料/每日金融数据/每日金融数据_2026-06-22.md` 和 `金融资料/区间涨跌/` 三个正式行情文件。未读取、引用或继承 `特征量化/`、Signals、回归、模型比较或 `公司排序/` 的现成排序结果；`备份/` 与 `tmp/` 不作为决策输入。")
    if missing_finance:
        lines.append(f"> 金融资料覆盖差异：正式评估公司 {len(companies)} 家，最新金融快照覆盖 {len(companies) - len(missing_finance)} 家；缺少日度金融明细的公司为 {', '.join(missing_finance)}，价格/估值/IV相关档位按资料不足或低置信处理。")
    if missing_returns:
        lines.append(f"> 区间涨跌覆盖差异：{len(missing_returns)} 家公司缺少过去两周或过去1个月区间涨跌，价格确认/动量列对这些公司保守处理。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.extend(one_page)
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | TEL |")
    lines.append(f"| 公司名称 | {TARGET_NAME} |")
    lines.append(f"| 产业链分类 | {a.category} |")
    lines.append(f"| 重要产品/业务线 | {base.md_escape(base.short_phrase(products, 300))} |")
    lines.append(f"| NTM 基准收入 | {base.md_escape(ntm)} |")
    lines.append(f"| 乐观/极度乐观收入 | {base.md_escape(optimistic)} |")
    lines.append(f"| 利润和现金流结论 | {base.md_escape(base.short_phrase(profit_cash, 260))} |")
    lines.append(f"| 最大传导瓶颈 | {base.md_escape(base.short_phrase(bottleneck, 260))} |")
    lines.append(f"| 最大反证 | {base.md_escape(base.short_phrase(bear, 260))} |")
    lines.append(f"| 近端催化剂 | {base.md_escape(base.short_phrase(catalysts, 260))} |")
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
    lines.append("| 直接同业 | 与TEL在连接器、结构化布线、铜互联、光纤/线缆、电源连接或高可靠连接需求池高度重叠，优先比较订单、design win、产品代际、利润留存和同业估值 | APH、BDC、BELFB、GLW、SMTOY | 判断力度最高；同档时优先用DDN/AI连接器收入化、订单和估值消化决定微倾向 |")
    lines.append("| 相邻替代 | 同属AI基础设施、电力/机电、工业质量或数据中心物理基础设施资金篮子，重点比较增长质量、兑现确定性、估值消化和近端催化 | VRT、ETN、NVT、HUBB、GEV、PWR、TT、PH | 默认按档位判断，避免只因电力或冷却叙事更热就压过TEL；强烈建议需两档以上差距或硬证据 |")
    lines.append("| 上下游 | AI芯片、服务器、云、网络、光模块、存储、utility/数据中心电力需求与TEL DDN/Energy/rack power处在同一需求链，重点看利润池、议价权和订单可收入化 | NVDA、AVGO、ANET、CIEN、COHR、CRDO、DELL、MSFT、CEG | 不把下游收入规模直接等同于TEL机会；若对手本身掌握更大利润池或更强订单，允许B胜出 |")
    lines.append("| 跨赛道 | 半导体设备材料、化工、公用事业和部分传统工业与TEL业务差异较大，但作为资金配置替代仍可比较 | ASML、AMAT、LIN、ECL、TMO、MMM | 默认降低结论力度；证据互有强弱时优先中性或微倾向 |")
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

    lines.append("## 7. 多数思路下 B 明显强于 A 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | B 胜出的主要投资思路 | 为什么 B 更值得投 | A 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(
            f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在对应档位中高于TEL，且多数思路下增长、右尾、估值或价格证据更强。 | TEL需要看到DDN/AI Cloud收入继续高增、224G/rack power客户订单金额、Transportation恢复和价格确认改善。 |"
        )
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过TEL | 继续跟踪DDN订单、margin和价格确认 |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(
            f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'A')} | TEL相对{b.ticker}的DDN收入化、现金流、估值消化、客户设计导入或订单可见度更清楚。 | {b.ticker}需要更硬的NTM订单/利润兑现、估值消化证据和价格确认。 |"
        )
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | TEL没有在多数思路下明显压过其他公司 | 需等待TEL订单和价格进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append(f"- 公司 A 调研文件：`{COMPANY_RESEARCH_PATH.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{base.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{base.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{base.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{base.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append("- 其他主要来源：" + "；".join(f"`{p}`" for p in INDUSTRY_SOURCES) + "；B侧公司业务、产品、客户、订单、竞争和风险证据主要通过各公司最新正式评估报告吸收。")
    lines.append("- 排除来源：未使用 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/备份/`、`分析报告/tmp/`、项目根 `tmp/` 或公司调研/行业调研备份目录中的结论作为本次决策依据。")
    lines.append("- 口径说明：本报告是项目内横截面二选一研究，不是绝对买卖建议；日度价格、估值和IV为日期敏感数据，应以后续金融资料刷新。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    companies = base.load_latest_reports()
    if TARGET not in companies:
        raise SystemExit("TEL not found in formal company evaluation universe")

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
    print("TEL grades:", {s: companies[TARGET].grades[s] for s in STRATEGIES})


if __name__ == "__main__":
    main()
