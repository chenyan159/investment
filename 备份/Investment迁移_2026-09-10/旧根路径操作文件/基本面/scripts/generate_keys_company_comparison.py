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

base.TARGET = "KEYS"
base.TARGET_NAME = "Keysight Technologies"
base.OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "KEYS_逐家公司投资思路对比_2026-06-23.md"


def relation_for(b) -> str:
    cat = b.category
    if cat == "封测_检测_计量_光罩":
        return "直接同业"
    if b.ticker in {"VIAV", "TDY", "TER", "ATEYY", "COHU", "ONTO", "FORM", "PLAB", "TMO"}:
        return "直接同业"
    if cat in {"AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC", "晶圆制造_前道设备", "半导体材料_化学品_基板"}:
        return "上下游"
    if cat in {"AI服务器_存储_EMS", "云算力_IDC_AI软件平台"}:
        return "上下游"
    if cat in {"配电_电源_功率器件", "电力_发电_能源_储能", "机电_冷却_工程_水处理_边缘工业AI"}:
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
            "NTM兑现优先": "KEYS订单、Q3指引和wireline兑现更清楚",
            "右尾弹性优先": "KEYS受益AI fabric、1.6T和224G验证放量",
            "风险调整收益": "KEYS增长、利润率、现金流和估值较均衡",
            "下行保护优先": "KEYS服务底盘、正FCF和中等IV更稳",
            "估值消化优先": "KEYS可用NTM收入利润增长消化估值",
            "近端催化优先": "KEYS订单、1.6T/224G和Q3财报节点更近",
            "价格确认/动量": "KEYS价格确认完整且基本面同步增强",
            "激进短线": "KEYS AI网络测试叙事和中等IV可交易",
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
        reason = "KEYS在多数思路下更均衡，主要胜在订单可见性、测试平台利润率和现金流质量。"
    elif b_count > a_count:
        final = b.ticker
        reason = f"{b.ticker}在多数思路下胜出，KEYS需要更强AI/wireline订单、利润率或价格确认。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = base.TARGET
            reason = "多数思路打平时，风险调整收益更支持KEYS。"
        elif risk_label.endswith("投B"):
            final = b.ticker
            reason = f"多数思路打平时，风险调整收益更支持{b.ticker}。"
        else:
            ntm_label = decisions["NTM兑现优先"].split("：", 1)[0]
            if ntm_label.endswith("投A"):
                final = base.TARGET
                reason = "多数思路打平，KEYS的NTM兑现路径略更清楚。"
            elif ntm_label.endswith("投B"):
                final = b.ticker
                reason = f"多数思路打平，NTM兑现略偏{b.ticker}。"
            else:
                final = base.TARGET
                reason = "多数思路打平，KEYS的现金流和证据质量略占优。"
    return f"A {a_count} / B {b_count} / 中性 {n_count}", final, reason


def grade_support_limit(strat: str, c) -> tuple[str, str]:
    support = {
        "NTM兑现优先": "FY2026 Q2收入17.17亿美元、订单20.51亿美元、book-to-bill约1.19x，Q3收入指引17.30-17.50亿美元",
        "右尾弹性优先": "AI fabric/workload emulation、1.6T/224G光电验证、PCIe/CXL和高端仿真测试提供非线性上限",
        "风险调整收益": "基准NTM收入73-76亿美元、non-GAAP经营利润约21.5-23.5亿美元，现金流仍为正",
        "下行保护优先": "传统T&M、校准服务、A&D/6G/NTN/PNT和存量客户提供收入底盘，IV低于高弹性小盘测试股",
        "估值消化优先": "2026-06-22 Forward PE约31.49、P/S约10.48，需要但并非完全依赖极度乐观情景消化",
        "近端催化优先": "Q3指引、Q3/Q4 orders、Commercial Communications和wireline订单语言、1.6T/224G客户验证可连续跟踪",
        "价格确认/动量": "2026-06-22日度快照价格和IV完整；区间动量可与SOXX压力窗口做一致比较",
        "激进短线": "AI网络测试、1.6T/224G、OFC/标准节点和中等IV让短线交易性存在",
    }[strat]
    limit = {
        "NTM兑现优先": "产品级AI收入和backlog美元数未披露，订单转收入需看交付、验收和客户重复采购",
        "右尾弹性优先": "KEYS收入基数较大，CPO/3.2T/PCIe 8.0等多数仍偏远期期权，极度乐观可信度低到中",
        "风险调整收益": "估值已给出测试平台复苏和AI网络增量溢价，客户内制、VIAVI/Teledyne/Anritsu/Rohde竞争仍是反证",
        "下行保护优先": "高端仪器订单周期、AI CapEx推迟和光模块产线压价仍会放大业绩与股价波动",
        "估值消化优先": "P/S和EV/EBITDA不低，若Q3/Q4订单低于收入或毛利率剔除IEEPA后回落，估值消化会变慢",
        "近端催化优先": "催化依赖订单连续性和客户qual转量产，单季订单语言弱化会降低重定价强度",
        "价格确认/动量": "区间涨跌文件截至2026-06-03，正式全项目动量仍需后续行情刷新",
        "激进短线": "相对AEHR、ALAB、CRDO、NBIS、FCEL等高IV小基数标的，KEYS爆发倍数受市值和估值约束",
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
        f"- A 最占优的投资思路：`{a_best}`，A侧合计 {by_strategy_a[a_best]}/{len(sorted_bs)}；核心来自FY2026 Q2订单强度、Q3指引、AI/wireline测试需求和高端仪器/软件利润率。",
        f"- A 最吃亏的投资思路：`{a_worst}`，B侧合计 {by_strategy_b[a_worst]}/{len(sorted_bs)}；主要输给AI芯片、光互联小基数、NeoCloud、电力链或高IV短线标的的更高右尾/动量。",
        "- A 最适合的投资者画像：偏中期基本面、重视订单可见性、毛利率、现金流和AI网络测试确定性，同时不想承担最小盘右尾波动的人。",
        "- A 最不适合的投资者画像：只追求极端短线倍数、只买最低估值周期修复、或要求AI收入分拆和backlog完全披露后才下注的人。",
        f"- 多数思路下最强反方公司：{strongest_b_names}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：KEYS 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后，属于全项目中上到强势的AI测试平台，不是最极端右尾，但质量明显高于纯概念或现金流薄弱标的。",
        "- 后续最重要跟踪数据：Q3/Q4 orders、book-to-bill、Commercial Communications与wireline语言、AI-related revenue是否披露美元数、1.6T/224G订单、剔除IEEPA后毛利率/经营利润率、递延收入、营运资本和FCF转换。",
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
    lines.append("# KEYS 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{base.REPORT_DATE}")
    lines.append(f"公司 A：KEYS / {base.TARGET_NAME}")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(companies) - 1}")
    lines.append(f"公司评估文件日期范围：{min(eval_dates)} 至 {max(eval_dates)}")
    lines.append("日度数据日期：价格/估值/IV 为 2026-06-22；过去两周和过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04；2026-06-23 KEYS/SOXX盘中价只作外部校验，不进入全项目统一档位。")
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
    lines.append("| 股票代号 | KEYS |")
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
    lines.append("| 直接同业 | 同属测试、测量、ATE、探针卡、检测量测、光罩或网络测试工具链，优先比较订单、客户验证、毛利率、产品代际和同业估值 | TER、ATEYY、VIAV、TDY、ONTO、FORM、COHU、PLAB、TMO | 同档或相邻档可用订单/收入兑现和毛利质量放大到建议级别 |")
    lines.append("| 相邻替代 | 同属AI基础设施资金篮子但不直接竞争，重点比较增长质量、兑现确定性、估值消化和催化可见度 | VRT、ETN、GEV、MOD、AAON、PWR、CEG、ALAB | 默认按档位判断，除非增长、估值或催化显著拉开，否则少用强烈建议 |")
    lines.append("| 上下游 | AI芯片、光互联、服务器、云厂、晶圆制造、前道设备和材料是KEYS测试需求链的上下游，重点看利润捕获和需求转测试支出的确定性 | NVDA、AVGO、ANET、CRDO、CIEN、TSM、ASML、AMAT、AMZN、MSFT | 不把客户CapEx或芯片收入直接等同KEYS收入，必须看测试订单转化和估值消化 |")
    lines.append("| 跨赛道 | 业务差异大但仍可作为资金配置替代，比较增长质量、风险调整收益和下行保护 | LIN、ECL、MMM、DHR、CAT | 默认降低结论力度；证据互有强弱时优先微倾向或中性 |")
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
        lines.append(f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在对应档位中高于KEYS，且多数思路下增长、右尾、估值或价格证据更强。 | KEYS需要Q3/Q4 orders继续高于收入、AI/wireline收入披露更硬、剔除IEEPA后利润率保持并刷新价格确认。 |")
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过KEYS | 继续跟踪订单、AI/wireline收入、毛利率和价格确认 |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'A')} | KEYS相对{b.ticker}的订单兑现、测试平台利润率、现金流质量或估值消化更清楚。 | {b.ticker}需要更硬的NTM订单/利润兑现、估值消化证据和价格确认。 |")
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | KEYS没有在多数思路下明显压过其他公司 | 需等待AI/wireline收入、订单和价格进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{base.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{base.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{base.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{base.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md` 用于公司名称和分类；A 侧业务证据补充读取 `公司调研/封测_检测_计量_光罩/KEYS_Keysight_Technologies_公司调研_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_高速互连与光学验证测试_2026-06-11.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_探针卡、ATE与系统级测试_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AI以太网交换系统与Fabric芯片_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_PCIe_CXL高速IO交换与Retimer_2026-06-11.md`；KEYS 评估报告内列出的官方财报/IR来源用于经营数据校准。")
    lines.append("- 外部一致性校验：2026-06-23 对 KEYS 与 SOXX 做过盘中行情 sanity check；因全项目公司没有同一时点批量数据，未用于主表档位、价格/估值/IV和动量判断。")
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
        raise SystemExit("KEYS not found in formal company evaluation universe")

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
    print("KEYS grades:", {s: companies[base.TARGET].grades[s] for s in base.STRATEGIES})


if __name__ == "__main__":
    main()
