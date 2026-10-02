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

base.TARGET = "MRAM"
base.TARGET_NAME = "Everspin Technologies"
base.REPORT_DATE = "2026-06-23"
base.OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MRAM_逐家公司投资思路对比_2026-06-23.md"


MEMORY_STORAGE_DIRECT = {
    "MU",
    "RMBS",
    "SIMO",
    "SNDK",
    "STX",
    "WDC",
}

MRAM_SUPPLY_AND_DEMAND_CHAIN = {
    "AMAT",
    "ASML",
    "ASMIY",
    "GFS",
    "INTC",
    "MCHP",
    "STM",
    "TER",
    "TOELY",
    "TSM",
    "TSEM",
    "TXN",
    "UMC",
}

STORAGE_SYSTEM_DOWNSTREAM = {
    "CLS",
    "DELL",
    "FLEX",
    "FN",
    "HPE",
    "JBL",
    "NTAP",
    "PENG",
    "PSTG",
    "SANM",
    "SMCI",
}

SEMI_AND_AI_ADJACENT_CATEGORIES = {
    "AI服务器_存储_EMS",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "云算力_IDC_AI软件平台",
    "晶圆制造_前道设备",
    "封测_检测_计量_光罩",
    "半导体材料_化学品_基板",
}

INFRA_CATEGORIES = {
    "电力_发电_能源_储能",
    "配电_电源_功率器件",
    "机电_冷却_工程_水处理_边缘工业AI",
}


MRAM_SCORE_OVERRIDES = {
    # MRAM has real NTM revenue acceleration from product run-rate plus the
    # Amentum contract, but the formal evaluation is explicit that backlog is
    # not disclosed and that AI GPU/HBM capex should not be mapped directly to
    # MRAM revenue. Keep the growth/right-tail strength, but take it out of the
    # all-project S tier for right-tail because the extreme scenario is low
    # confidence and depends on several simultaneous transmission links.
    "NTM兑现优先": 0.664,
    "右尾弹性优先": 0.780,
    "风险调整收益": 0.482,
    "下行保护优先": 0.140,
    "估值消化优先": 0.465,
    "近端催化优先": 0.799,
    "价格确认/动量": 0.465,
    "激进短线": 0.776,
}


def calibrate_mram(companies: dict[str, object]) -> None:
    c = companies[base.TARGET]
    for strategy, score in MRAM_SCORE_OVERRIDES.items():
        c.scores[strategy] = score


def relation_for(b) -> str:
    ticker = b.ticker
    category = b.category
    if ticker in MEMORY_STORAGE_DIRECT:
        return "直接同业"
    if ticker in MRAM_SUPPLY_AND_DEMAND_CHAIN or ticker in STORAGE_SYSTEM_DOWNSTREAM:
        return "上下游"
    if category in SEMI_AND_AI_ADJACENT_CATEGORIES:
        return "相邻替代"
    if category in INFRA_CATEGORIES:
        return "跨赛道"
    return "跨赛道"


def reason_for(strat: str, label: str, b, relation: str) -> str:
    if label == "中性":
        if relation == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，证据互有强弱"
    side = "A" if label.endswith("投A") else "B"
    if side == "A":
        return {
            "NTM兑现优先": "MRAM有产品run-rate和40M合同支撑",
            "右尾弹性优先": "MRAM小基数、Amentum和UNISYST上限更大",
            "风险调整收益": "MRAM上行能覆盖部分估值/执行风险",
            "下行保护优先": "对手更弱或资料不足，MRAM现金债务压力较轻",
            "估值消化优先": "MRAM若兑现73-86M收入可部分消化估值",
            "近端催化优先": "MRAM Q2指引、Amentum和xSPI验证更近",
            "价格确认/动量": "MRAM一月反弹有一定基本面同步",
            "激进短线": "MRAM高IV、小市值和合同催化适合进攻",
        }[strat]
    return {
        "NTM兑现优先": f"{b.ticker} NTM收入/利润兑现更硬",
        "右尾弹性优先": f"{b.ticker}右尾规模或收入化更强",
        "风险调整收益": f"{b.ticker}上行下行组合更优",
        "下行保护优先": f"{b.ticker}现金流、估值或压力期更稳",
        "估值消化优先": f"{b.ticker}估值更容易被业绩消化",
        "近端催化优先": f"{b.ticker}近端订单/产品催化更强",
        "价格确认/动量": f"{b.ticker}价格趋势确认更强",
        "激进短线": f"{b.ticker}短线资金关注和爆发力更强",
    }[strat]


def final_choice(decisions: dict[str, str], b) -> tuple[str, str, str]:
    counts = Counter(base.label_side(v) for v in decisions.values())
    a_count, b_count, n_count = counts["A"], counts["B"], counts["N"]
    if a_count > b_count:
        final = base.TARGET
        reason = "MRAM在该组合下胜在小基数增速、正式合同、近端验证和短线弹性。"
    elif b_count > a_count:
        final = b.ticker
        reason = f"{b.ticker}在多数思路下胜出，MRAM需要更硬订单、收入确认、利润和估值消化证据。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = base.TARGET
            reason = "多数思路打平时，风险调整收益略支持MRAM。"
        elif risk_label.endswith("投B"):
            final = b.ticker
            reason = f"多数思路打平时，风险调整收益更支持{b.ticker}。"
        else:
            ntm_label = decisions["NTM兑现优先"].split("：", 1)[0]
            if ntm_label.endswith("投A"):
                final = base.TARGET
                reason = "多数思路打平，MRAM的NTM兑现略更清楚。"
            elif ntm_label.endswith("投B"):
                final = b.ticker
                reason = f"多数思路打平，NTM兑现略偏{b.ticker}。"
            else:
                final = b.ticker
                reason = f"多数思路打平且MRAM下行保护弱，最终略偏{b.ticker}。"
    return f"A {a_count} / B {b_count} / 中性 {n_count}", final, reason


def grade_support_limit(strat: str, c) -> tuple[str, str]:
    support = {
        "NTM兑现优先": "2026Q1 product sales 14.1M、Q2 revenue guide 15.5-16.5M、Amentum 40M/约2.5年合同，NTM基准73-86M",
        "右尾弹性优先": "乐观/极度乐观收入92-112M/118-144M，小收入基数、Amentum、HR xSPI、UNISYST和Microchip second-source提供上限",
        "风险调整收益": "TTM收入仅56.94M，若产品run-rate和Amentum兑现，经营杠杆可从接近盈亏平衡转正",
        "下行保护优先": "公司无大额金融债，产品毛利历史50%+，Amentum是正式合同而非纯概念",
        "估值消化优先": "NTM基准收入较TTM约+28%-51%，若Non-GAAP转正可部分解释P/S和Forward PE",
        "近端催化优先": "Q2实际收入/指引、Amentum milestone、128/256Mb xSPI qualification、UNISYST Q4 samples都是1-2季验证点",
        "价格确认/动量": "2026-06-03过去一月+32.95%，价格曾对产品收入和合同催化作出反应",
        "激进短线": "市值约599M、Call/Put IV约140%、高可靠MRAM/国防合同/UNISYST叙事具备事件交易弹性",
    }[strat]
    limit = {
        "NTM兑现优先": "公司不披露backlog/bookings，产品收入只能用指引、design wins和客户评论校准，Amentum确认节奏仍需折扣",
        "右尾弹性优先": "MRAM不是2026 AI GPU/HBM主链，UNISYST和D-MRAM更多是2027+期权，极度乐观可信度低",
        "风险调整收益": "P/S 10.51、Forward PE 54.90、TTM PE 2553和140%+ IV使下行风险很高",
        "下行保护优先": "SOXX三段压力窗口累计-86.38%，小市值高IV和盈利薄弱使其不是防守标的",
        "估值消化优先": "当前估值已经要求Amentum、product GM、license/IP和费用控制同时兑现，Microchip setup还可能消耗现金",
        "近端催化优先": "缺少客户订单额、backlog、Amentum收入确认表和UNISYST付费客户，催化可能只停留在样品/资格认证",
        "价格确认/动量": "2026-06-03过去两周-1.28%，2026-06-22价格25.53低于6月初28.57，短线确认并不连续",
        "激进短线": "高IV意味着期权市场已计入大波动，若Q2或milestone不兑现，回撤会被迅速放大",
    }[strat]
    return support, limit


def finance_snapshot(c) -> str:
    f = c.finance
    return (
        f"2026-06-22金融快照：价格日期{f.get('价格日期', '缺失')}，"
        f"最新价格{f.get('最新价格', '缺失')}美元，市值{f.get('市值', '缺失')}，"
        f"TTM PE {f.get('TTM PE', '缺失')}，Forward PE {f.get('Forward PE', '缺失')}，"
        f"P/S {f.get('P/S', '缺失')}，EV/EBITDA {f.get('EV/EBITDA', '缺失')}，"
        f"Call/Put IV {f.get('Call IV', '缺失')}/{f.get('Put IV', '缺失')}；"
        "2026-06-03过去两周-1.28%、过去一月+32.95%；"
        "2026-06-04三段SOXX压力窗口累计-86.38%。"
    )


def make_report(companies: dict[str, object]) -> str:
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
    a_best = sorted(base.STRATEGIES, key=lambda s: by_strategy_a[s] - by_strategy_b[s], reverse=True)[:3]
    a_worst = sorted(base.STRATEGIES, key=lambda s: by_strategy_a[s] - by_strategy_b[s])[:3]
    strongest_b = sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker))[:12]
    strongest_b_names = "、".join(f"{b.ticker}" for _, _, b, _ in strongest_b) or "无明显集中反方"

    eval_dates = [c.eval_date for c in companies.values()]
    finance_meta = base.load_finance()[1]
    missing_finance = sorted([t for t, c in companies.items() if not c.finance])
    missing_price = sorted([t for t, c in companies.items() if (not c.finance) or c.metrics.get("price") is None])

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
    profit_cash = base.bullet_after(conclusion, "利润/现金流结论") or a.scenarios.get("基准", {}).get("EBITDA/净利润", "")
    bottleneck = base.bullet_after(conclusion, "主要传导瓶颈") or base.bullet_after(a_intro, "最大传导瓶颈")
    bear = base.bullet_after(conclusion, "悲观情景触发条件") or "产品收入跌回12-14M/q、Amentum确认后移、渠道库存反复、GM跌破50%、litigation/G&A和Microchip setup吞噬现金。"
    catalysts = base.bullet_after(conclusion, "后续跟踪数据") or base.bullet_after(conclusion, "乐观情景成立条件")

    lines = []
    lines.append("# MRAM 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{base.REPORT_DATE}")
    lines.append("公司 A：MRAM / Everspin Technologies")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(companies) - 1}")
    lines.append(f"公司评估文件日期范围：{min(eval_dates)} 至 {max(eval_dates)}")
    lines.append("日度数据日期：价格/估值/IV 为 2026-06-22 金融快照；过去两周和过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。")
    lines.append("")
    lines.append("> 口径说明：本报告读取 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/公司索引.md`、`金融资料/每日金融数据/每日金融数据_2026-06-22.md` 和 `金融资料/区间涨跌/` 三个正式行情文件。未读取、引用或继承 `特征量化/`、Signals、回归、模型比较、`公司排序/`、`简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。")
    if missing_finance:
        lines.append(f"> 金融资料覆盖差异：正式评估公司 {len(companies)} 家，最新金融快照覆盖 {len(companies) - len(missing_finance)} 家；缺少日度金融明细的公司为 {', '.join(missing_finance)}，价格/估值/IV/动量相关档位按资料不足或低置信处理。")
    if missing_price:
        lines.append(f"> 价格字段缺失或不可用公司：{', '.join(missing_price)}；这些公司在价格确认、估值消化、下行保护和激进短线中自动降权。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.extend(
        [
            f"- A 最占优的投资思路：{'、'.join(a_best)}。MRAM 的优势集中在小基数收入增长、Amentum 正式合同、HR xSPI/UNISYST 右尾和高 IV 短线事件弹性。",
            f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是估值已经较贵、历史压力窗口回撤大、盈利薄、缺少 backlog/bookings，且 MRAM 不是 2026 AI GPU/HBM 主链。",
            "- A 最适合的投资者画像：能承受高波动和小市值回撤、愿意用中期事件催化押注高可靠 MRAM 产品/国防合同/UNISYST 样品兑现的进攻型资金。",
            "- A 最不适合的投资者画像：要求大市值防守、稳定现金流、低 IV、估值快速消化或只买 AI 主链订单/RPO最硬公司的资金。",
            f"- 多数思路下最强反方公司：{strongest_b_names}。",
            f"- 如果只追求更高增长、更好公司，A 的总体位置：MRAM 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后；它是全项目里右尾和短线更强、但下行保护和估值消化明显偏弱的小市值存储半导体标的。",
            "- 后续最重要跟踪数据：2026Q2实际收入和Q3指引、product sales是否维持16M/q以上、Amentum milestone revenue/billing、product GM、operating expenses excluding litigation、AR/inventory/distributor mix、128/256Mb qualification、UNISYST Q4 samples、Microchip bring-up现金支出和客户订单证据。",
        ]
    )
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | MRAM |")
    lines.append("| 公司名称 | Everspin Technologies |")
    lines.append(f"| 产业链分类 | {a.category} |")
    lines.append(f"| 重要产品/业务线 | {base.md_escape(base.short_phrase(products, 320))} |")
    lines.append(f"| NTM 基准收入 | {base.md_escape(ntm)} |")
    lines.append(f"| 乐观/极度乐观收入 | {base.md_escape(optimistic)} |")
    lines.append(f"| 利润和现金流结论 | {base.md_escape(base.short_phrase(profit_cash, 280))} |")
    lines.append(f"| 最大传导瓶颈 | {base.md_escape(base.short_phrase(bottleneck, 280))} |")
    lines.append(f"| 最大反证 | {base.md_escape(base.short_phrase(bear, 280))} |")
    lines.append(f"| 近端催化剂 | {base.md_escape(base.short_phrase(catalysts, 280))} |")
    lines.append(f"| 日度市场数据 | {base.md_escape(finance_snapshot(a))} |")
    lines.append("")

    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append("建档口径：对同一批正式评估公司，抽取基准/乐观/极度乐观 NTM 收入增速、经营利润率、毛利率、FCF/现金流、可信度、反证、估值、IV、区间涨跌和 SOXX 压力窗口表现。每个投资思路独立排序，`S` 约为前 8%，`A` 约为 8%-25%，`B` 约为 25%-50%，`C` 约为 50%-80%，`D` 为后 20%；日度价格或估值缺失时按资料不足/低置信处理。MRAM 右尾从通用模型的 S 档人工下调至 A 档，因为极度乐观需要 Amentum、xSPI、license/IP、UNISYST 和费用控制同时成立，且 MRAM 不是 2026 AI 主链收入。")
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
    lines.append("| 直接同业 | 与 MRAM 在非易失存储、存储控制器、内存接口、企业存储或存储介质资金池中高度重叠，优先比较产品收入兑现、客户/订单、毛利率、利润杠杆和同业估值 | MU、SNDK、WDC、STX、SIMO、RMBS | 同档时必须复核谁真正吃到同一存储/内存需求池；两档以上才给强烈建议 |")
    lines.append("| 相邻替代 | 同属 AI 服务器、半导体、光互联、软件/云算力或设备材料资金篮子，但产品不直接竞争 | NVDA、AVGO、ALAB、CRDO、COHR、ASML、AMAT、NBIS、CRWV | 重点比较增长质量、兑现确定性、估值消化和右尾赔率，避免把赛道热度直接当胜负 |")
    lines.append("| 上下游 | B 是 MRAM 的供应链、制造链、客户系统链或数据中心存储/服务器需求链相关公司 | MCHP、GFS、TSM、TER、DELL、HPE、SMCI、PENG、NTAP、PSTG | 区分下游收入规模和 MRAM 利润捕获；Microchip/晶圆制造对 MRAM 更像执行和产能变量 |")
    lines.append("| 跨赛道 | 电力、冷却、工业、材料、医疗工具、软件或与 MRAM 业务差异较大的公司，但仍是项目资金配置替代 | CEG、VST、ETN、VRT、LIN、ECL、DHR、TMO | 默认降低结论力度；证据互有强弱时优先中性或微倾向 |")
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
        lines.append(f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在对应档位中高于MRAM，且多数思路下收入兑现、右尾收入化、估值消化、防守或价格证据更强。 | MRAM需要Amentum收入确认、product sales持续超过16-18M/q、xSPI 128/256Mb量产订单、UNISYST付费客户、GM维持50%+且FCF改善。 |")
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过MRAM | 继续跟踪Amentum、product sales、xSPI和UNISYST兑现 |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'A')} | MRAM相对{b.ticker}的NTM小基数增长、正式合同、近端验证或高波动进攻弹性更清楚。 | {b.ticker}需要更硬的订单/backlog、收入利润兑现、估值消化证据和价格确认。 |")
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | MRAM没有在多数思路下明显压过其他公司 | 需等待合同收入、产品收入和价格进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司 A 公司调研文件：`公司调研/AI服务器_存储_EMS/MRAM_Everspin_Technologies_公司调研_2026-06-11.md`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{base.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{base.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{base.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{base.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append("- 关键行业资料：`行业调研/AI服务器_存储_芯片/行业调研_片上SRAM、MRAM与近存计算_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_特种晶圆代工_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_企业级SSD与高速存储控制器_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_CXL内存扩展与内存池化_2026-06-10.md`、`行业调研/产业背景/AI产业链全局图谱与口径字典_2026-06-11.md`。")
    lines.append(f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {len(companies) - len(missing_finance)}/{len(companies)} 家；缺少当日金融明细的公司为 {('、'.join(missing_finance) if missing_finance else '无')}；价格字段缺失或不可用公司为 {('、'.join(missing_price) if missing_price else '无')}。")
    lines.append(f"- 公司 A 日度数据摘录：{finance_snapshot(a)}")
    lines.append("- 自动化脚本：`scripts/generate_mram_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对 MRAM 的 product run-rate、Amentum合同、HR xSPI/UNISYST、Microchip second-source、估值、IV、压力窗口和动量做人工校准后建档；未读取下游量化目录或现成排序结论。")
    lines.append("- 排除来源：未使用 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/备份/`、`分析报告/tmp/` 或项目根 `tmp/` 中的结论作为本次决策依据。")
    lines.append("")
    return "\n".join(lines)


base.relation_for = relation_for
base.reason_for = reason_for
base.final_choice = final_choice
base.grade_support_limit = grade_support_limit


def main() -> None:
    companies = base.load_latest_reports()
    if base.TARGET not in companies:
        raise SystemExit("MRAM not found in formal company evaluation universe")

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
    calibrate_mram(companies)
    base.assign_grades(companies)

    base.OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = make_report(companies)
    base.OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(base.OUT_PATH)
    print(f"companies={len(companies)} b={len(companies)-1} bytes={base.OUT_PATH.stat().st_size}")
    print("MRAM grades:", {s: companies[base.TARGET].grades[s] for s in base.STRATEGIES})
    print("MRAM ranks:", {s: companies[base.TARGET].ranks[s] for s in base.STRATEGIES})


if __name__ == "__main__":
    main()
