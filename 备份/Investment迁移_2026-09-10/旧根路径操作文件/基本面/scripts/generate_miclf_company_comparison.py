from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(r"D:\drive\Investment\基本面")
BASE_SCRIPT = ROOT / "scripts" / "generate_googl_company_comparison_20260623.py"

spec = importlib.util.spec_from_file_location("company_comparison_base", BASE_SCRIPT)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = base
spec.loader.exec_module(base)

base.TARGET = "MICLF"
base.TARGET_NAME = "Mycronic AB"
base.OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MICLF_逐家公司投资思路对比_2026-06-23.md"


DIRECT_TEST_BONDING_PEERS = {
    "AEHR",
    "ASMVY",
    "ATEYY",
    "BESIY",
    "CAMT",
    "COHU",
    "FORM",
    "KEYS",
    "KLIC",
    "NVMI",
    "ONTO",
    "TER",
}

PHOTOMASK_AND_ADVANCED_PACKAGING = {
    "AMAT",
    "ASML",
    "ASMIY",
    "DSCSY",
    "KLAC",
    "LRCX",
    "MKSI",
    "PLAB",
    "TOELY",
    "VECO",
}

CUSTOMERS_AND_DEMAND_CHAIN = {
    "AAOI",
    "ALAB",
    "AMD",
    "AMKR",
    "ANET",
    "APH",
    "ARM",
    "ASX",
    "AVGO",
    "BDC",
    "BELFB",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "DELL",
    "FN",
    "GFS",
    "HPE",
    "IMOS",
    "INTC",
    "LITE",
    "LWLG",
    "MRVL",
    "MU",
    "NVDA",
    "PENG",
    "POET",
    "QCOM",
    "SANM",
    "SMCI",
    "SMTC",
    "SNDK",
    "STX",
    "TSEM",
    "TSM",
    "UMC",
    "WDC",
}

SEMI_MATERIALS_ADJACENT = {
    "AJNMY",
    "ASGLY",
    "AXTI",
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

AI_INFRA_CATEGORIES = {
    "AI服务器_存储_EMS",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "云算力_IDC_AI软件平台",
    "电力_发电_能源_储能",
    "配电_电源_功率器件",
    "机电_冷却_工程_水处理_边缘工业AI",
}


MICLF_SCORE_OVERRIDES = {
    # The raw parser over-promotes risk-adjusted and valuation because MICLF
    # lacks Forward PE/P/S/EV-EBITDA in the daily snapshot. Keep the real
    # strengths, but do not let missing fields create an artificial S tier.
    "NTM兑现优先": 0.63,
    "右尾弹性优先": 0.60,
    "风险调整收益": 0.60,
    "下行保护优先": 0.67,
    "估值消化优先": 0.61,
    "近端催化优先": 0.78,
    "价格确认/动量": 0.32,
    "激进短线": 0.55,
}


def calibrate_miclf(companies: dict[str, object]) -> None:
    c = companies[base.TARGET]
    for strategy, score in MICLF_SCORE_OVERRIDES.items():
        c.scores[strategy] = score


def relation_for(b) -> str:
    ticker = b.ticker
    cat = b.category
    if ticker in DIRECT_TEST_BONDING_PEERS:
        return "直接同业"
    if ticker in CUSTOMERS_AND_DEMAND_CHAIN:
        return "上下游"
    if ticker in PHOTOMASK_AND_ADVANCED_PACKAGING or ticker in SEMI_MATERIALS_ADJACENT:
        return "相邻替代"
    if cat == "封测_检测_计量_光罩":
        return "相邻替代"
    if cat in {"晶圆制造_前道设备", "半导体材料_化学品_基板"}:
        return "相邻替代"
    if cat in AI_INFRA_CATEGORIES:
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
            "NTM兑现优先": "MICLF有8.75bn指引、4.707bn backlog和PG交付表",
            "右尾弹性优先": "MICLF有GT AI PCB、光模块设备和PG高ASP上限",
            "风险调整收益": "MICLF高利润、26x TTM PE和正现金流较均衡",
            "下行保护优先": "MICLF aftermarket、PG利润和压力窗口韧性更好",
            "估值消化优先": "MICLF估值未明显透支且利润率支撑消化",
            "近端催化优先": "MICLF Q2财报、GT订单和HV光模块验证更近",
            "价格确认/动量": "MICLF压力期韧性好且价格未过热",
            "激进短线": "MICLF小市值叠加光罩、AI PCB和光模块设备期权",
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
        reason = "MICLF在多数思路下胜在PG/GT可见兑现、利润质量、估值消化或下行韧性。"
    elif b_count > a_count:
        final = b.ticker
        reason = f"{b.ticker}在多数思路下胜出，MICLF需要更硬GT/HV订单、产品级收入拆分、现金转换或价格确认。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = base.TARGET
            reason = "多数思路打平时，风险调整收益更支持MICLF。"
        elif risk_label.endswith("投B"):
            final = b.ticker
            reason = f"多数思路打平时，风险调整收益更支持{b.ticker}。"
        else:
            ntm_label = decisions["NTM兑现优先"].split("：", 1)[0]
            if ntm_label.endswith("投A"):
                final = base.TARGET
                reason = "多数思路打平，MICLF的NTM收入兑现略更清楚。"
            elif ntm_label.endswith("投B"):
                final = b.ticker
                reason = f"多数思路打平，NTM兑现略偏{b.ticker}。"
            else:
                final = base.TARGET
                reason = "多数思路打平，MICLF的估值和下行韧性略占优。"
    return f"A {a_count} / B {b_count} / 中性 {n_count}", final, reason


def grade_support_limit(strat: str, c) -> tuple[str, str]:
    support = {
        "NTM兑现优先": "2026Q1收入SEK2.503bn、订单SEK2.529bn、backlog SEK4.707bn，FY2026收入预期上调至SEK8.75bn，PG 13台系统排到2027Q1",
        "右尾弹性优先": "乐观收入SEK9.7-10.6bn、极度乐观SEK10.8-12.0bn；GT订单+260%、AI advanced PCB、MRSI光通信和High Volume光模块提供上限",
        "风险调整收益": "基准EBIT margin 24%-27%、TTM PE 26.11、2026Q1现金流强，SOXX三段压力窗口累计+16.67%，但估值字段不完整",
        "下行保护优先": "aftermarket TTM约SEK1.971bn、PG高毛利、正现金流和压力窗口韧性提供防守属性",
        "估值消化优先": "NTM基准收入SEK8.8-9.4bn、EBITDA SEK2.4-2.9bn，当前TTM PE约26x，盈利质量能部分消化估值",
        "近端催化优先": "2026Q2财报、PG交付表更新、GT order intake/backlog、High Volume光模块重复订单和泰国工厂进度都在1-2季可验证",
        "价格确认/动量": "SOXX压力窗口表现强，价格未明显过热，适合作为防守确认而非强动量确认",
        "激进短线": "小市值设备公司叠加光罩、AI PCB测试、MRSI光通信和photonic interconnect期权，具备一定事件弹性",
    }[strat]
    limit = {
        "NTM兑现优先": "PCB Test、Die Bonding和photonic interconnect产品级收入未拆，GT强订单仍需转收入和验收",
        "右尾弹性优先": "2028定制SLX不进NTM，CPO/photonic interconnect多为低证据远期期权，AI收入化不是线性TAM映射",
        "风险调整收益": "Forward PE、P/S、EV/EBITDA、IV均缺失或不可校验，不能因资料缺失直接给最强结论",
        "下行保护优先": "设备公司季度lumpy、亚洲收入占比高、客户验收/库存/应收会造成现金流波动",
        "估值消化优先": "交易货币与财报货币不一致，P/S缺失；若PG mix回落或GT订单不能续强，估值消化会变慢",
        "近端催化优先": "催化依赖Q2/Q3订单连续性和产品级拆分，若公司继续不披露客户/金额，重定价力度有限",
        "价格确认/动量": "过去两周和一月区间涨跌文件截至2026-06-03且MICLF为0%，最新价格日期为2026-06-19，动量证据偏弱",
        "激进短线": "无干净期权IV，OTC/foreign ordinary流动性和市场关注度弱于AI芯片、光互联、NeoCloud等高beta标的",
    }[strat]
    return support, limit


def finance_snapshot(c) -> str:
    f = c.finance
    return (
        f"2026-06-22金融快照生成时，MICLF价格日期为{f.get('价格日期', '缺失')}，"
        f"最新价格{f.get('最新价格', '缺失')}美元，市值{f.get('市值', '缺失')}，"
        f"TTM PE {f.get('TTM PE', '缺失')}，Forward PE {f.get('Forward PE', '缺失')}，"
        f"P/S {f.get('P/S', '缺失')}，EV/EBITDA {f.get('EV/EBITDA', '缺失')}，"
        f"Call/Put IV {f.get('Call IV', '缺失')}/{f.get('Put IV', '缺失')}；"
        "2026-06-03过去两周0.00%、过去一月0.00%；2026-06-04三段SOXX压力窗口累计+16.67%。"
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
    bear = base.bullet_after(conclusion, "悲观情景触发条件") or "PG交付推迟、GT订单转化慢、光模块和AI PCB capex延迟、并购整合费用和工作资本占用。"
    catalysts = base.bullet_after(conclusion, "后续跟踪数据") or base.bullet_after(conclusion, "乐观情景成立条件")

    lines = []
    lines.append("# MICLF 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{base.REPORT_DATE}")
    lines.append("公司 A：MICLF / Mycronic AB")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(companies) - 1}")
    lines.append(f"公司评估文件日期范围：{min(eval_dates)} 至 {max(eval_dates)}")
    lines.append("日度数据日期：价格/估值/IV 为 2026-06-22 金融快照；MICLF价格日期为 2026-06-19；过去两周和过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。")
    lines.append("")
    lines.append("> 口径说明：本报告读取 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/公司索引.md`、`金融资料/每日金融数据/每日金融数据_2026-06-22.md` 和 `金融资料/区间涨跌/` 三个正式行情文件。未读取、引用或继承 `特征量化/`、Signals、回归、模型比较、`公司排序/`、`简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。")
    if missing_finance:
        lines.append(f"> 金融资料覆盖差异：正式评估公司 {len(companies)} 家，最新金融快照覆盖 {len(companies) - len(missing_finance)} 家；缺少日度金融明细的公司为 {', '.join(missing_finance)}，价格/估值/IV/动量相关档位按资料不足或低置信处理。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.extend(
        [
            f"- A 最占优的投资思路：{'、'.join(a_best)}。MICLF 的相对强项集中在下行保护、估值消化、风险调整收益和可见 NTM 兑现；核心来自 PG 高利润交付、集团 backlog、GT 强订单、aftermarket 稳定器和压力窗口韧性。",
            f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是纯右尾规模不如 AI 芯片/光互联/NeoCloud，日度动量和 IV 资料不足，PCB Test、Die Bonding 和 Photonic Interconnects 缺少产品级收入拆分。",
            "- A 最适合的投资者画像：希望买小中市值半导体/电子设备公司，重视利润率、backlog、估值消化和下行韧性，同时愿意保留 AI advanced PCB、光模块设备和 photomask 高 ASP 期权的中期配置者。",
            "- A 最不适合的投资者画像：只追求最高 AI 右尾、最强价格动量、可交易期权高波动、或要求 AI 数据中心收入已成为公司主体的短线资金。",
            f"- 多数思路下最强反方公司：{strongest_b_names}。",
            f"- 如果只追求更高增长、更好公司，A 的总体位置：MICLF 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后，属于全项目中上偏质量、防守和估值消化更强的设备右尾标的；不是全项目最强增长或最强短线标的。",
            "- 后续最重要跟踪数据：2026Q2报告（财务日历指向 2026-07-14）、PG系统交付表、GT order intake/backlog、GT organic growth和剔除重估后的EBIT margin、High Volume optical modules是否重复订单、PCB Assembly backlog、aftermarket revenue、工作资本/FCF、Cowin DST/ETZ/Surfx/RoBAT/Vanguard整合。",
        ]
    )
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | MICLF |")
    lines.append("| 公司名称 | Mycronic AB |")
    lines.append(f"| 产业链分类 | {a.category} |")
    lines.append(f"| 重要产品/业务线 | {base.md_escape(base.short_phrase(products, 300))} |")
    lines.append(f"| NTM 基准收入 | {base.md_escape(ntm)} |")
    lines.append(f"| 乐观/极度乐观收入 | {base.md_escape(optimistic)} |")
    lines.append(f"| 利润和现金流结论 | {base.md_escape(base.short_phrase(profit_cash, 260))} |")
    lines.append(f"| 最大传导瓶颈 | {base.md_escape(base.short_phrase(bottleneck, 260))} |")
    lines.append(f"| 最大反证 | {base.md_escape(base.short_phrase(bear, 260))} |")
    lines.append(f"| 近端催化剂 | {base.md_escape(base.short_phrase(catalysts, 260))} |")
    lines.append(f"| 日度市场数据 | {base.md_escape(finance_snapshot(a))} |")
    lines.append("")

    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append("建档口径：对同一批 189 家正式评估公司，抽取基准/乐观/极度乐观 NTM 收入增速、经营利润率、FCF/可信度/瓶颈、估值、IV、区间涨跌和 SOXX 压力窗口表现。每个投资思路独立排序，`S` 约为前 8%，`A` 约为 8%-25%，`B` 约为 25%-50%，`C` 约为 50%-80%，`D` 为后 20%；关键日度数据缺失时降权，不因对方资料不足给强烈建议。")
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
    lines.append("| 直接同业 | 同属封测/检测/计量/键合/先进封装设备资金池，或与 MICLF 的 PCB Test、Die Bonding、MRSI、光罩设备在客户预算和订单验证上高度重叠 | KLIC、ASMVY、BESIY、COHU、TER、ATEYY、FORM、CAMT、ONTO、NVMI | 同档时优先比较订单、客户认证、产品级收入、利润率和同业估值；两档以上才给强烈建议 |")
    lines.append("| 相邻替代 | 同属半导体设备、前道设备、材料、光罩/先进封装/光模块设备资金篮子，但产品不直接竞争 | ASML、AMAT、KLAC、LRCX、PLAB、ENTG、LIN、SHECY | 重点比较增长质量、兑现确定性、估值消化和近端催化，避免只因赛道更热胜出 |")
    lines.append("| 上下游 | B 是 MICLF 需求链中的 AI 芯片、HBM、foundry、OSAT、光模块、服务器或云资本开支端 | NVDA、TSM、MU、AVGO、CRDO、COHR、AAOI、DELL、SMCI、AMKR | 区分需求规模和利润捕获；下游收入规模不直接等同 MICLF 订单 |")
    lines.append("| 跨赛道 | 工业、材料、公用事业、软件或其他与 MICLF 业务差异较大的资金替代 | ECL、DHR、CAT、MSI、RKLB、TSLA | 默认降低结论力度；只有增长质量、估值消化、下行保护或价格确认明显拉开才给建议或强烈建议 |")
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
        lines.append(f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在对应档位中高于MICLF，且多数思路下增长、右尾、估值、防守或价格证据更强。 | MICLF需要GT/HV订单连续高位、PCB Test/Die Bonding产品级收入拆分、PG高ASP交付续强、现金转换改善和价格确认刷新。 |")
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过MICLF | 继续跟踪GT/HV订单、PG交付、产品级收入和价格确认 |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'A')} | MICLF相对{b.ticker}的利润质量、估值消化、压力窗口韧性或可见交付证据更清楚。 | {b.ticker}需要更硬的订单/backlog、利润兑现、估值消化证据和价格确认。 |")
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | MICLF没有在多数思路下明显压过其他公司 | 需等待GT/PG收入和价格进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司 A 公司调研文件：`公司调研/封测_检测_计量_光罩/MICLF_Mycronic_AB_公司调研_2026-06-11.md`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{base.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{base.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{base.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{base.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append("- 关键行业资料：`行业调研/晶圆制造_设备_材料_测试/行业调研_高端光罩与先进封装掩模_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_CPO／NPO与交换侧光引擎_2026-06-11.md`、`行业调研/产业背景/AI产业链全局图谱与口径字典_2026-06-11.md`。")
    lines.append(f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {len(companies) - len(missing_finance)}/{len(companies)} 家；缺少当日金融明细的公司为 {('、'.join(missing_finance) if missing_finance else '无')}。")
    lines.append(f"- 公司 A 日度数据摘录：{finance_snapshot(a)}")
    lines.append("- 自动化脚本：`scripts/generate_miclf_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对 MICLF 的 PG/GT/HV/aftermarket、产品级收入缺失、估值字段缺失、SOXX压力窗口和近端Q2验证做人工校准后建档；未读取下游量化目录或现成排序结论。")
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
        raise SystemExit("MICLF not found in formal company evaluation universe")

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
    calibrate_miclf(companies)
    base.assign_grades(companies)

    base.OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = make_report(companies)
    base.OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(base.OUT_PATH)
    print(f"companies={len(companies)} b={len(companies)-1} bytes={base.OUT_PATH.stat().st_size}")
    print("MICLF grades:", {s: companies[base.TARGET].grades[s] for s in base.STRATEGIES})
    print("MICLF ranks:", {s: companies[base.TARGET].ranks[s] for s in base.STRATEGIES})


if __name__ == "__main__":
    main()
