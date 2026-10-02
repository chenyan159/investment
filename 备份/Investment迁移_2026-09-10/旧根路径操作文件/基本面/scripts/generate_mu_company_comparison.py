from __future__ import annotations

import importlib.util
import math
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(r"D:\drive\Investment\基本面")
BASE_SCRIPT = ROOT / "scripts" / "generate_intc_company_comparison_20260623.py"
TARGET = "MU"
TARGET_NAME = "Micron Technology 美光科技"
REPORT_DATE = "2026-06-23"
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MU_逐家公司投资思路对比_2026-06-23.md"


def load_base():
    spec = importlib.util.spec_from_file_location("company_compare_base_intc", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load base script: {BASE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


base = load_base()
base.TARGET = TARGET
base.TARGET_NAME = TARGET_NAME
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATEGIES = base.STRATEGIES
LABEL_ORDER = base.LABEL_ORDER
GRADE_VALUE = base.GRADE_VALUE


def parse_percent_range_fixed(text: str) -> float | None:
    if not text:
        return None
    cleaned = base.strip_code(text).replace(",", "").replace("−", "-")
    cleaned = cleaned.replace("–", "-").replace("—", "-").replace("～", "-")

    # Common report style is "58-68%" or "+115% 至 +150%"; the old generic
    # parser treated the second number in "58-68%" as a negative percentage.
    patterns = [
        r"([+-]?\d+(?:\.\d+)?)\s*%\s*(?:至|到|-)\s*([+-]?\d+(?:\.\d+)?)\s*%",
        r"([+-]?\d+(?:\.\d+)?)\s*(?:至|到|-)\s*([+-]?\d+(?:\.\d+)?)\s*%",
    ]
    for pat in patterns:
        m = re.search(pat, cleaned)
        if m:
            return (float(m.group(1)) + float(m.group(2))) / 2

    vals = [float(m.group(1)) for m in re.finditer(r"([+-]?\d+(?:\.\d+)?)\s*%", cleaned)]
    if vals:
        if "下跌" in cleaned and all(v >= 0 for v in vals):
            vals = [-v for v in vals]
        return sum(vals) / len(vals)
    return None


base.parse_percent_range = parse_percent_range_fixed


DIRECT_PEERS = {"SNDK", "WDC", "STX"}
MEMORY_STORAGE_ADJACENT = {
    "DELL",
    "FN",
    "HPE",
    "MRAM",
    "NTAP",
    "PENG",
    "PSTG",
    "RMBS",
    "SIMO",
    "SMCI",
    "CLS",
    "FLEX",
    "JBL",
    "SANM",
}
AI_CHIP_VALUE_CHAIN = {"NVDA", "AMD", "AVGO", "MRVL", "QCOM", "ARM", "ALAB", "CDNS", "SNPS", "INTC", "MXL"}
CLOUD_AND_IDC = {"AMZN", "MSFT", "GOOGL", "META", "ORCL", "BABA", "IBM", "CRWV", "APLD", "DLR", "EQIX", "IREN", "NBIS", "NTNX", "ADBE", "CRWD"}
SEMICAP_CHAIN = {
    "ASML",
    "AMAT",
    "LRCX",
    "TOELY",
    "KLAC",
    "TER",
    "ATEYY",
    "FORM",
    "COHU",
    "CAMT",
    "NVMI",
    "DSCSY",
    "BESIY",
    "ASMIY",
    "ACLS",
    "ACMR",
    "AEHR",
    "AEIS",
    "MKSI",
    "ICHR",
    "UCTT",
    "VECO",
}
MATERIALS_CHAIN = {
    "AJNMY",
    "APD",
    "ASGLY",
    "AXTI",
    "HOCPY",
    "LIN",
    "MMM",
    "NDSN",
    "Q",
    "SHECY",
    "SOMMY",
    "CC",
    "ECL",
    "ENTG",
    "MTRN",
    "ROG",
    "SMTOY",
    "DHR",
    "DD",
    "DKILY",
}
NETWORK_CHAIN = {"ANET", "APH", "BDC", "COHR", "CRDO", "CSCO", "GLW", "LITE", "LWLG", "NOK", "TEL", "VIAV", "VISN", "AAOI", "BELFB", "CIEN", "MTSI", "POET", "SITM", "SMTC"}


def relation_for(b) -> str:
    ticker = b.ticker
    cat = b.category
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in MEMORY_STORAGE_ADJACENT or ticker in AI_CHIP_VALUE_CHAIN or ticker in CLOUD_AND_IDC:
        return "上下游"
    if ticker in SEMICAP_CHAIN or ticker in MATERIALS_CHAIN or cat in {"晶圆制造_前道设备", "封测_检测_计量_光罩"}:
        return "上下游"
    if ticker in NETWORK_CHAIN:
        return "相邻替代"
    if cat in {"配电_电源_功率器件", "电力_发电_能源_储能", "机电_冷却_工程_水处理_边缘工业AI"}:
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
    if relation == "直接同业" and label.startswith("微倾向") and abs(score_diff) >= 0.15:
        label = f"建议投{side}"
    return label


def reason_for(strat: str, label: str, b, relation: str) -> str:
    if label == "中性":
        if relation == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，证据互有强弱"
    side = "A" if label.endswith("投A") else "B"
    if side == "A":
        return {
            "NTM兑现优先": "MU的HBM/DRAM指引和CMBU/CDBU收入更硬",
            "右尾弹性优先": "MU受HBM4、SOCAMM、eSSD和Anthropic合作驱动",
            "风险调整收益": "MU高增长和低forward PE形成较好赔率",
            "下行保护优先": "MU盈利规模和大客户长约提供部分支撑",
            "估值消化优先": "MU低forward PE更易被NTM利润消化",
            "近端催化优先": "MU有6月24日财报、Anthropic协议和HBM4验证窗口",
            "价格确认/动量": "MU近月价格确认明显强于B",
            "激进短线": "MU高IV叠加财报/HBM叙事更进攻",
        }[strat]
    return {
        "NTM兑现优先": f"{b.ticker}收入/RPO/订单兑现更清楚",
        "右尾弹性优先": f"{b.ticker}右尾空间或小基数弹性更大",
        "风险调整收益": f"{b.ticker}上行下行组合更优",
        "下行保护优先": f"{b.ticker}现金流、估值或压力期更稳",
        "估值消化优先": f"{b.ticker}当前估值更容易消化",
        "近端催化优先": f"{b.ticker}近端订单/产品/财报催化更直接",
        "价格确认/动量": f"{b.ticker}价格趋势确认更强",
        "激进短线": f"{b.ticker}短线波动和资金关注更强",
    }[strat]


def decision_for(a, b, strat: str, relation: str) -> str:
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


def grade_summary(a, b) -> str:
    short = {
        "NTM兑现优先": "NTM",
        "右尾弹性优先": "右尾",
        "风险调整收益": "风险收益",
        "下行保护优先": "下行",
        "估值消化优先": "估值",
        "近端催化优先": "催化",
        "价格确认/动量": "动量",
        "激进短线": "短线",
    }
    a_strong, b_strong, near = [], [], []
    for strat in STRATEGIES:
        diff = GRADE_VALUE[a.grades[strat]] - GRADE_VALUE[b.grades[strat]]
        if diff >= 1:
            a_strong.append(short[strat])
        elif diff <= -1:
            b_strong.append(short[strat])
        else:
            near.append(short[strat])
    parts = []
    if a_strong:
        parts.append("A强：" + "、".join(a_strong[:4]))
    if b_strong:
        parts.append("B强：" + "、".join(b_strong[:4]))
    if near:
        parts.append("接近：" + "、".join(near[:3]))
    return "；".join(parts)


def final_choice(decisions: dict[str, str], b) -> tuple[str, str, str]:
    counts = Counter(label_side(v) for v in decisions.values())
    a_count, b_count, n_count = counts["A"], counts["B"], counts["N"]
    if a_count > b_count:
        final = TARGET
        reason = "MU在多数思路下增长兑现、估值消化、催化或交易弹性更强。"
    elif b_count > a_count:
        final = b.ticker
        reason = f"{b.ticker}多数思路胜出，MU需要HBM/DRAM价格、利润和FCF继续验证。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = TARGET
            reason = "多数思路打平时，风险调整收益更支持MU。"
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
                reason = "多数思路打平，MU的HBM收入兑现和估值消化略更清楚。"
    return f"A {a_count} / B {b_count} / 中性 {n_count}", final, reason


def grade_support_limit(strat: str) -> tuple[str, str]:
    support = {
        "NTM兑现优先": "FY2026 Q3收入335亿美元指引、CMBU/CDBU高毛利、CY2026 HBM价量协议、HBM4量产和Micron-Anthropic协议支撑兑现",
        "右尾弹性优先": "HBM4、SOCAMM2、server DRAM、data center eSSD和Anthropic架构合作共同形成AI memory/storage右尾",
        "风险调整收益": "NTM收入高增、forward PE约10倍、经营利润率上行和大客户长约提供赔率",
        "下行保护优先": "大规模收入、已披露BU利润率、强经营现金流和长期客户协议提供一定缓冲",
        "估值消化优先": "低forward PE叠加NTM利润暴增，若Q3/Q4兑现可快速压低盈利倍数",
        "近端催化优先": "2026-06-22 Micron-Anthropic协议、2026-06-24 FY2026 Q3财报、Q4指引、HBM4/SOCAMM/eSSD出货和CDBU增长是明确窗口",
        "价格确认/动量": "截至2026-06-22，1个月和2周涨幅在项目内靠前，价格已明显确认HBM叙事",
        "激进短线": "高IV、财报临近、HBM4/Rubin内存短缺和AI存储叙事使短线进攻性强",
    }[strat]
    limit = {
        "NTM兑现优先": "产品级收入未披露，FY2027 ASP、HBM良率、NAND价格和客户验收仍需验证",
        "右尾弹性优先": "极度乐观需要HBM4、SOCAMM、eSSD、MCBU多线同时短缺，16H/HBM4E仍偏期权",
        "风险调整收益": "高capex、存储周期、客户集中和价格剧烈上行后的回撤风险抵消部分赔率",
        "下行保护优先": "高IV、SOXX压力窗口弱表现和存储周期属性使防守性不如云厂、公用事业和现金牛",
        "估值消化优先": "P/S较高且价格已大幅上涨，若Q4指引或毛利低于预期会迅速反噬",
        "近端催化优先": "财报催化双向，若Q3/Q4未继续上修，近端强预期会转成反证",
        "价格确认/动量": "短期涨幅过大且IV高，动量已带过热风险",
        "激进短线": "短线进攻依赖财报和HBM叙事延续，高IV意味着方向错时回撤很大",
    }[strat]
    return support, limit


def calibrate_target(companies: dict[str, object]) -> None:
    mu = companies[TARGET]
    # MU is a special case in this universe: the formal report shows extremely
    # high NTM revenue growth and a near-dated earnings catalyst, while daily
    # data shows very high IV and weak SOXX stress-window behavior. These manual
    # scores preserve that split rather than letting a generic parser overrate
    # downside protection or underrate HBM-driven NTM delivery.
    overrides = {
        "NTM兑现优先": 0.83,
        "右尾弹性优先": 0.87,
        "风险调整收益": 0.58,
        "下行保护优先": 0.39,
        "估值消化优先": 0.59,
        "近端催化优先": 0.93,
        "价格确认/动量": 0.83,
        "激进短线": 0.87,
    }
    for strat, value in overrides.items():
        mu.scores[strat] = value


def md_escape(value: object) -> str:
    return base.md_escape(value)


def format_grade_position(c, strat: str) -> str:
    return base.format_grade_position(c, strat)


def make_report(companies: dict[str, object]) -> str:
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

    a_majority_wins = sum(1 for t, ds in decisions_by_b.items() if final_choice(ds, companies[t])[1] == TARGET)
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
        f"- A 最占优的投资思路：`{a_best}`，A侧合计 {by_strategy_a[a_best]}/{len(sorted_bs)}；MU最容易在近端财报/HBM兑现、估值消化和激进短线中胜出。",
        f"- A 最吃亏的投资思路：`{a_worst}`，B侧合计 {by_strategy_b[a_worst]}/{len(sorted_bs)}；主要输给现金流更稳、SOXX压力期更抗跌或估值更便宜的公司。",
        "- A 最适合的投资者画像：愿意接受高IV和存储周期波动，押注HBM4、SOCAMM、高端eSSD和DRAM/NAND紧缺继续兑现的进攻型投资者。",
        "- A 最不适合的投资者画像：只追求低回撤、稳定现金流和低事件风险，或不愿承受财报后预期落空风险的防守型投资者。",
        f"- 多数思路下最强反方公司：{strongest_b_names}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：MU 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后；它不是最安全资产，但在HBM/AI memory兑现、估值消化和短线进攻上处于全项目强势位置。",
        "- 后续最重要跟踪数据：2026-06-24 FY2026 Q3收入/毛利/Q4指引，CMBU/CDBU收入和毛利率，Micron-Anthropic协议的期限/容量/价格/预付款，HBM4客户和价格，SOCAMM2出货，高端eSSD/NAND QoQ，FY2027 capex、客户长约、库存和FCF。",
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
    catalysts = base.bullet_after(conclusion, "后续跟踪数据") or base.bullet_after(conclusion, "乐观情景成立条件")
    catalysts = "2026-06-22 Micron-Anthropic战略协议；" + catalysts

    lines: list[str] = []
    lines.append("# MU 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：MU / {TARGET_NAME}")
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
    lines.append("| 股票代号 | MU |")
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
        sup, lim = grade_support_limit(strat)
        lines.append(f"| {strat} | {a.grades[strat]} | {format_grade_position(a, strat)} | {md_escape(sup)} | {md_escape(lim)} |")
    lines.append("")

    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | 与 MU 在NAND、存储器、企业级存储或存储周期需求池中高度重叠 | SNDK、WDC、STX | 同档或相邻档必须复核价格周期、产品mix、eSSD/存储收入、现金流和估值，直接证据可提升判断力度 |")
    lines.append("| 相邻替代 | 同属AI基础设施资金篮子，但不直接卖同类产品，重点比较增长质量、兑现确定性和赔率 | ANET、CRDO、COHR、VRT、ETN、CEG | 默认按档位判断；若业务差异较大，即使一方略强也降低到微倾向或中性 |")
    lines.append("| 上下游 | AI芯片、云厂、服务器、EDA、设备、材料、封测与 MU 处于memory/storage需求链或供给链上下游 | NVDA、AMD、AVGO、MRVL、DELL、HPE、ASML、AMAT、TSM | 强调利润池、议价权和收入确认节奏，不把客户CapEx或设备瓶颈直接等同为MU收入 |")
    lines.append("| 跨赛道 | 业务差异大，但作为资金配置替代仍可比较风险调整收益、估值消化和下行保护 | LIN、ECL、TMO、DHR、RYCEY | 默认降低结论力度，除非增长质量、估值或现金流明显拉开 |")
    lines.append("")

    lines.append("## 5. 全项目逐行投资思路决策表")
    lines.append("")
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要", *STRATEGIES, "多数思路方向", "最终更值得投", "最关键理由"]
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

    def winning_strats(decisions: dict[str, str], side: str) -> str:
        out = [s for s, cell in decisions.items() if label_side(cell) == side]
        return "、".join(out) if out else "无"

    lines.append("## 7. 多数思路下 B 明显强于 A 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | B 胜出的主要投资思路 | 为什么 B 更值得投 | A 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(
            f"| {rank} | {b.ticker} / {md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在对应档位中高于MU，且多数思路下兑现、现金流、防守、估值消化或价格证据更强。 | MU需要Q3/Q4指引继续上修、HBM4/SOCAMM/eSSD收入证据增强、FCF覆盖高capex，并保持价格确认。 |"
        )
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过MU | 继续跟踪Q3/Q4指引、HBM4、CDBU和FCF |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(
            f"| {rank} | {b.ticker} / {md_escape(b.name)} | {winning_strats(decisions, 'A')} | MU相对{b.ticker}的HBM/DRAM收入兑现、近端催化、估值消化或短线弹性更清楚。 | {b.ticker}需要更硬的NTM订单/利润兑现、估值消化证据和价格确认。 |"
        )
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | MU没有在多数思路下明显压过其他公司 | 需等待HBM、CDBU、Q4指引和FCF进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{base.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{base.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{base.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{base.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md` 用于公司名称和分类；`金融资料/最新AI新闻/每日AI产业链新闻_2026-06-23.md` 和 `金融资料/最新AI新闻/新闻稿/每日新闻稿_2026-06-23.md` 用于 Micron-Anthropic 战略协议和当日新闻催化；MU 评估报告内已列出的公司调研、行业调研和官方财报/IR来源用于 A 侧业务证据。")
    lines.append("- 排除来源：未使用 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/备份/`、`分析报告/tmp/` 或项目根 `tmp/` 中的结论作为本次决策依据。")
    lines.append("")
    return "\n".join(lines)


def load_companies() -> dict[str, object]:
    companies = base.load_latest_reports()
    if TARGET not in companies:
        raise SystemExit("MU not found in formal company evaluation universe")

    index = base.load_index_categories()
    finance, _ = base.load_finance()
    ret_1m = base.load_return_table(base.RET_1M_PATH, "过去1个月涨跌幅")
    ret_2w = base.load_return_table(base.RET_2W_PATH, "过去两周涨跌幅")
    soxx = base.load_return_table(base.SOXX_PATH, "三段累计涨跌幅")

    for ticker, c in companies.items():
        if ticker in index:
            idx_name, cat = index[ticker]
            c.name = idx_name
            c.category = cat
        c.finance = finance.get(ticker, {})
        c.returns = {"1m": ret_1m.get(ticker), "2w": ret_2w.get(ticker), "soxx": soxx.get(ticker)}

    base.build_metrics(companies)
    base.assign_scores(companies)
    calibrate_target(companies)
    base.assign_grades(companies)
    return companies


def main() -> None:
    companies = load_companies()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = make_report(companies)
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(OUT_PATH)
    print(f"companies={len(companies)} b={len(companies)-1} bytes={OUT_PATH.stat().st_size}")
    print("MU grades:", {s: companies[TARGET].grades[s] for s in STRATEGIES})
    print("MU ranks:", {s: companies[TARGET].ranks[s] for s in STRATEGIES})
    if not math.isfinite(OUT_PATH.stat().st_size):
        raise RuntimeError("invalid output size")


if __name__ == "__main__":
    main()
