from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(r"D:\investment\基本面")
BASE_SCRIPT = ROOT / "scripts" / "generate_googl_company_comparison_20260623.py"

spec = importlib.util.spec_from_file_location("company_comparison_base", BASE_SCRIPT)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = base
spec.loader.exec_module(base)

base.TARGET = "KLIC"
base.TARGET_NAME = "Kulicke Soffa"
base.OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "KLIC_逐家公司投资思路对比_2026-06-23.md"


BONDING_DIRECT = {"ASMVY", "BESIY", "COHU", "TER", "ATEYY"}
PACKAGING_TEST_ADJACENT = {
    "AEHR",
    "CAMT",
    "FORM",
    "KEYS",
    "MICLF",
    "ONTO",
    "PLAB",
    "TDY",
    "TMO",
}
OSAT_FOUNDRY_MEMORY_CUSTOMERS = {
    "AMKR",
    "ASX",
    "GFS",
    "IMOS",
    "INTC",
    "MU",
    "SNDK",
    "STX",
    "TSEM",
    "TSM",
    "UMC",
    "WDC",
}
AI_CHIP_NETWORK_SYSTEMS = {
    "AAOI",
    "ALAB",
    "AMD",
    "ANET",
    "ARM",
    "AVGO",
    "BABA",
    "CDNS",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "DELL",
    "FN",
    "GOOGL",
    "HPE",
    "LITE",
    "META",
    "MRAM",
    "MRVL",
    "MSFT",
    "NVDA",
    "ORCL",
    "PENG",
    "QCOM",
    "RMBS",
    "SANM",
    "SIMO",
    "SMCI",
    "SNPS",
}
SEMICAP_ADJACENT = {
    "ACLS",
    "ACMR",
    "AEIS",
    "AMAT",
    "ASMIY",
    "ASML",
    "DSCSY",
    "ICHR",
    "KLAC",
    "LRCX",
    "MKSI",
    "NVMI",
    "TOELY",
    "UCTT",
    "VECO",
}
SEMI_MATERIALS = {
    "AJNMY",
    "ASGLY",
    "AXTI",
    "CC",
    "DD",
    "ENTG",
    "HOCPY",
    "LIN",
    "MTRN",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
}
AI_INFRA_CATS = {
    "云算力_IDC_AI软件平台",
    "AI服务器_存储_EMS",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "配电_电源_功率器件",
    "电力_发电_能源_储能",
    "机电_冷却_工程_水处理_边缘工业AI",
}


def relation_for(b) -> str:
    cat = b.category
    ticker = b.ticker
    if ticker in BONDING_DIRECT:
        return "直接同业"
    if ticker in PACKAGING_TEST_ADJACENT:
        return "相邻替代"
    if ticker in OSAT_FOUNDRY_MEMORY_CUSTOMERS or ticker in AI_CHIP_NETWORK_SYSTEMS:
        return "上下游"
    if ticker in SEMICAP_ADJACENT or ticker in SEMI_MATERIALS:
        return "相邻替代"
    if cat == "封测_检测_计量_光罩":
        return "相邻替代"
    if cat in AI_INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strat: str, label: str, b, relation: str) -> str:
    if label == "中性":
        if relation == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，证据互有强弱"
    side = "A" if label.endswith("投A") else "B"
    if side == "A":
        return {
            "NTM兑现优先": "KLIC Q3指引、Ball高run-rate和TCB ramp更近",
            "右尾弹性优先": "KLIC小基数TCB/先进封装右尾更大",
            "风险调整收益": "KLIC净现金、强增长和先进封装赔率较均衡",
            "下行保护优先": "KLIC净现金和APS服务底盘提供缓冲",
            "估值消化优先": "KLIC若兑现NTM收入利润可消化估值",
            "近端催化优先": "KLIC Q3/Q4指引和TCB订单验证更近",
            "价格确认/动量": "KLIC Q2后价格确认和资金关注更强",
            "激进短线": "KLIC高IV叠加TCB/HBM叙事适合进攻",
        }[strat]
    return {
        "NTM兑现优先": f"{b.ticker} NTM收入/利润兑现证据更强",
        "右尾弹性优先": f"{b.ticker}右尾空间或小基数弹性更大",
        "风险调整收益": f"{b.ticker}上行下行组合更优",
        "下行保护优先": f"{b.ticker}现金流、估值或压力期更稳",
        "估值消化优先": f"{b.ticker}当前估值更易被业绩消化",
        "近端催化优先": f"{b.ticker}近端事件重定价概率更高",
        "价格确认/动量": f"{b.ticker}价格趋势确认更强",
        "激进短线": f"{b.ticker}短线波动和资金关注更强",
    }[strat]


def final_choice(decisions: dict[str, str], b) -> tuple[str, str, str]:
    counts = Counter(base.label_side(v) for v in decisions.values())
    a_count, b_count, n_count = counts["A"], counts["B"], counts["N"]
    if a_count > b_count:
        final = base.TARGET
        reason = "KLIC在多数思路下胜在NTM兑现、TCB/先进封装右尾、近端催化或价格确认。"
    elif b_count > a_count:
        final = b.ticker
        reason = f"{b.ticker}在多数思路下胜出，KLIC需要更硬TCB订单、利润留存、现金转换或下行保护证据。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = base.TARGET
            reason = "多数思路打平时，风险调整收益更支持KLIC。"
        elif risk_label.endswith("投B"):
            final = b.ticker
            reason = f"多数思路打平时，风险调整收益更支持{b.ticker}。"
        else:
            ntm_label = decisions["NTM兑现优先"].split("：", 1)[0]
            if ntm_label.endswith("投A"):
                final = base.TARGET
                reason = "多数思路打平，KLIC的近端收入兑现略更清楚。"
            elif ntm_label.endswith("投B"):
                final = b.ticker
                reason = f"多数思路打平，NTM兑现略偏{b.ticker}。"
            else:
                final = base.TARGET
                reason = "多数思路打平，KLIC的TCB期权和净现金略占优。"
    return f"A {a_count} / B {b_count} / 中性 {n_count}", final, reason


def grade_support_limit(strat: str, c) -> tuple[str, str]:
    support = {
        "NTM兑现优先": "FY2026 Q2收入2.426亿美元、Q3指引3.10亿美元正负0.20亿美元，NTM基准收入11.5-13.0亿美元",
        "右尾弹性优先": "Advanced Solutions/TCB从小基数ramp，TCB产能规划支持约4亿美元年系统销售，极度乐观收入16.5-19.0亿美元",
        "风险调整收益": "NTM基准增速约50%-69%，净现金资产负债表、APS服务底盘和TCB右尾同时存在",
        "下行保护优先": "FY2026 Q2末现金及短投约4.879亿美元、无明显金融债，APS和装机服务提供一定底盘",
        "估值消化优先": "2026-06-22价格124.22美元、市值约65.0亿美元、Forward PE约29.32、P/S约8.46，需要但可由高增长消化",
        "近端催化优先": "FY2026 Q3实际收入/Q4指引、Advanced Solutions单季收入、TCB repeat orders和Ball持续性是近端验证点",
        "价格确认/动量": "截至2026-06-03过去1个月上涨25.56%、两周上涨7.08%，2026-06-22高IV显示资金关注仍高",
        "激进短线": "小中市值、约71.5% IV、HBM/TCB/先进封装叙事和Q3/Q4财报节点提供短线进攻性",
    }[strat]
    limit = {
        "NTM兑现优先": "公司不披露backlog/bookings/book-to-bill，Ball高run-rate能否延续和TCB验收仍需确认",
        "右尾弹性优先": "TCB客户POR、重复订单和收入确认未完全披露，BESI/ASMPT等竞争者证据也强",
        "风险调整收益": "估值已重估，FY2026 H1经营现金流仅约134万美元，应收和库存占用放大执行风险",
        "下行保护优先": "SOXX压力窗口三段累计跌幅约-52.57%，高IV和周期设备属性削弱防守档位",
        "估值消化优先": "P/S和TTM PE不低，若Advanced Solutions利润留存慢或Ball回落，估值消化会变慢",
        "近端催化优先": "催化高度依赖Q3/Q4连续兑现；若公司仍不披露TCB订单或Advanced Solutions停在低基数，重定价会减弱",
        "价格确认/动量": "区间涨跌文件截至2026-06-03，之后涨幅可能已透支部分Q2/Q3和TCB预期",
        "激进短线": "相对ALAB、CRDO、NBIS、FCEL等更高beta标的，KLIC短线爆发仍受后道设备周期和估值约束",
    }[strat]
    return support, limit


def make_report(companies) -> str:
    a = companies[base.TARGET]
    rows = []
    stats = {s: Counter() for s in base.STRATEGIES}
    b_rank_rows = []
    a_rank_rows = []
    decisions_by_b = {}

    sorted_bs = [c for t, c in companies.items() if t != base.TARGET]
    sorted_bs.sort(key=lambda c: (c.category, c.ticker))

    for idx, b in enumerate(sorted_bs, start=1):
        relation = relation_for(b)
        decisions = {s: base.decision_for(a, b, s, relation) for s in base.STRATEGIES}
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
                *[decisions[s] for s in base.STRATEGIES],
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

    a_majority_wins = sum(1 for b, ds in decisions_by_b.items() if final_choice(ds, companies[b])[1] == base.TARGET)
    b_majority_wins = len(sorted_bs) - a_majority_wins
    by_strategy_a = {s: stats[s]["强烈建议投A"] + stats[s]["建议投A"] + stats[s]["微倾向投A"] for s in base.STRATEGIES}
    by_strategy_b = {s: stats[s]["强烈建议投B"] + stats[s]["建议投B"] + stats[s]["微倾向投B"] for s in base.STRATEGIES}
    a_best = max(base.STRATEGIES, key=lambda s: by_strategy_a[s])
    a_worst = max(base.STRATEGIES, key=lambda s: by_strategy_b[s])
    strongest_b = sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker))[:10]
    strongest_b_names = "、".join(f"{b.ticker}" for _, _, b, _ in strongest_b) or "无明显集中反方"

    eval_dates = [c.eval_date for c in companies.values()]
    finance_meta = base.load_finance()[1]
    missing_finance = sorted([t for t, c in companies.items() if not c.finance])

    one_page = [
        f"- A 最占优的投资思路：`{a_best}`，A侧合计 {by_strategy_a[a_best]}/{len(sorted_bs)}；核心来自Q3指引强、Ball Bonding高run-rate、Advanced Solutions/TCB ramp和先进封装右尾。",
        f"- A 最吃亏的投资思路：`{a_worst}`，B侧合计 {by_strategy_b[a_worst]}/{len(sorted_bs)}；主要输给更强下行保护、现金流更稳、估值更低，或AI主链/电力链/云算力更高右尾和更强动量公司。",
        "- A 最适合的投资者画像：愿意承担后道设备周期和高IV，换取TCB/先进封装从小基数放量、Q3/Q4继续上修和净现金资产负债表保护的中高风险投资者。",
        "- A 最不适合的投资者画像：只要稳定现金流和低估值防守、不能接受backlog/bookings不披露，或要求AI收入已成为主体后才下注的人。",
        f"- 多数思路下最强反方公司：{strongest_b_names}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：KLIC 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后，属于全项目中上偏强的先进封装设备右尾标的；强项是NTM兑现、右尾和催化，短板是下行保护、现金转换和估值重估后的容错率。",
        "- 后续最重要跟踪数据：FY2026 Q3实际收入和Q4指引、Advanced Solutions收入/毛利/经营亏损是否改善、TCB客户数和repeat orders、Ball Bonding收入持续性、APS增速、应收/库存/经营现金流、前三大客户占比和BESI/ASMPT等竞品订单。"
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

    lines = []
    lines.append("# KLIC 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{base.REPORT_DATE}")
    lines.append(f"公司 A：KLIC / {base.TARGET_NAME}")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(companies) - 1}")
    lines.append(f"公司评估文件日期范围：{min(eval_dates)} 至 {max(eval_dates)}")
    lines.append("日度数据日期：价格/估值/IV 为 2026-06-22；过去两周和过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。")
    lines.append("")
    lines.append("> 口径说明：本报告读取 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/公司索引.md`、`金融资料/每日金融数据/每日金融数据_2026-06-22.md` 和 `金融资料/区间涨跌/` 三个正式行情文件。未使用下游量化、Signals、回归、模型比较或 `公司排序/` 的现成排序结果；`备份/` 与 `tmp/` 不作为决策输入。")
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
    lines.append("| 股票代号 | KLIC |")
    lines.append(f"| 公司名称 | {base.TARGET_NAME} |")
    lines.append(f"| 产业链分类 | {a.category} |")
    lines.append(f"| 重要产品/业务线 | {base.md_escape(base.short_phrase(products, 260))} |")
    lines.append(f"| NTM 基准收入 | {base.md_escape(ntm)} |")
    lines.append(f"| 乐观/极度乐观收入 | {base.md_escape(optimistic)} |")
    lines.append(f"| 利润和现金流结论 | {base.md_escape(base.short_phrase(profit_cash, 240))} |")
    lines.append(f"| 最大传导瓶颈 | {base.md_escape(base.short_phrase(bottleneck, 240))} |")
    lines.append(f"| 最大反证 | {base.md_escape(base.short_phrase(bear, 240))} |")
    lines.append(f"| 近端催化剂 | {base.md_escape(base.short_phrase(catalysts, 240))} |")
    lines.append("")

    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append("| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for strat in base.STRATEGIES:
        sup, lim = grade_support_limit(strat, a)
        lines.append(f"| {strat} | {a.grades[strat]} | {base.format_grade_position(a, strat)} | {base.md_escape(sup)} | {base.md_escape(lim)} |")
    lines.append("")

    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | 同属后道键合、封装组装设备或相近测试设备资金池，优先比较订单、客户POR、收入兑现、产品代际、毛利率和同业估值 | ASMVY、BESIY、COHU、TER、ATEYY | 同档或相邻档可用TCB/键合订单、客户验证和利润留存放大到建议级别 |")
    lines.append("| 相邻替代 | 同属半导体设备、封测检测、先进封装或AI基础设施资金篮子，但不直接卖同一设备，重点比较增长质量、兑现确定性和赔率 | CAMT、FORM、ONTO、KEYS、AMAT、ASML、VRT、ETN | 默认按档位判断，除非增长、估值或催化显著拉开，否则少用强烈建议 |")
    lines.append("| 上下游 | OSAT、foundry、存储、AI芯片、光互联和服务器客户链与KLIC存在需求传导，重点看客户CapEx能否变成KLIC订单和利润 | AMKR、ASX、TSM、MU、NVDA、AVGO、ANET、SMCI | 不把下游收入规模直接等同KLIC机会，必须看TCB/Ball订单、验收和收入确认 |")
    lines.append("| 跨赛道 | 工业、材料、公用事业或其他业务差异较大公司，作为资金配置替代比较风险调整收益和下行保护 | LIN、ECL、DHR、MMM、CAT | 默认降低结论力度；证据互有强弱时优先微倾向或中性 |")
    lines.append("")

    lines.append("## 5. 全项目逐行投资思路决策表")
    lines.append("")
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要", *base.STRATEGIES, "多数思路方向", "最终更值得投", "最关键理由"]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---:" if h == "序号" else "---" for h in headers]) + " |")
    for row in rows:
        lines.append("| " + " | ".join(base.md_escape(x) for x in row) + " |")
    lines.append("")

    lines.append("## 6. 投资思路统计")
    lines.append("")
    stat_headers = ["投资思路", *base.LABEL_ORDER, "A侧合计", "B侧合计"]
    lines.append("| " + " | ".join(stat_headers) + " |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for strat in base.STRATEGIES:
        counter = stats[strat]
        a_total = counter["强烈建议投A"] + counter["建议投A"] + counter["微倾向投A"]
        b_total = counter["强烈建议投B"] + counter["建议投B"] + counter["微倾向投B"]
        vals = [str(counter[label]) for label in base.LABEL_ORDER]
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
        lines.append(f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在对应档位中高于KLIC，且多数思路下增长、右尾、估值、防守或价格证据更强。 | KLIC需要Q3/Q4继续上修、Advanced Solutions放量并转正、TCB订单/客户POR披露、现金转换改善和价格确认延续。 |")
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过KLIC | 继续跟踪TCB订单、Advanced Solutions利润、现金流和价格确认 |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'A')} | KLIC相对{b.ticker}的NTM兑现、TCB/先进封装右尾、近端催化或价格确认更清楚。 | {b.ticker}需要更硬的订单/利润兑现、估值消化证据和价格确认。 |")
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | KLIC没有在多数思路下明显压过其他公司 | 需等待TCB订单、利润和价格进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{base.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{base.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{base.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{base.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md` 用于公司名称和分类；KLIC 评估报告内列出的公司调研、行业调研和官方财报/IR来源用于 A 侧业务证据。")
    lines.append("- 排除来源：未使用下游量化、Signals、回归、模型比较、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/备份/`、`分析报告/tmp/` 或项目根 `tmp/` 中的结论作为本次决策依据。")
    lines.append("")
    return "\n".join(lines)


base.relation_for = relation_for
base.reason_for = reason_for
base.final_choice = final_choice
base.grade_support_limit = grade_support_limit


def main() -> None:
    companies = base.load_latest_reports()
    if base.TARGET not in companies:
        raise SystemExit("KLIC not found in formal company evaluation universe")

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

    base.OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = make_report(companies)
    base.OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(base.OUT_PATH)
    print(f"companies={len(companies)} b={len(companies)-1} bytes={base.OUT_PATH.stat().st_size}")
    print("KLIC grades:", {s: companies[base.TARGET].grades[s] for s in base.STRATEGIES})


if __name__ == "__main__":
    main()
