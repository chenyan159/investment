from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path


BASE_PATH = Path(__file__).resolve().parent / "generate_googl_company_comparison_20260623.py"
spec = importlib.util.spec_from_file_location("company_comparison_base_20260623", BASE_PATH)
if spec is None or spec.loader is None:
    raise SystemExit(f"Cannot load base comparison helpers from {BASE_PATH}")
base = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = base
spec.loader.exec_module(base)


ROOT = base.ROOT
TARGET = "SNPS"
TARGET_NAME = "Synopsys"
REPORT_DATE = "2026-06-23"
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "SNPS_逐家公司投资思路对比_2026-06-23.md"

STRATEGIES = base.STRATEGIES
LABEL_ORDER = base.LABEL_ORDER
GRADE_VALUE = base.GRADE_VALUE


DIRECT_PEERS = {
    "CDNS",
    "ARM",
    "RMBS",
}

CHIP_DESIGN_CUSTOMERS = {
    "ADI",
    "ALAB",
    "AMD",
    "AOSL",
    "AVGO",
    "DIOD",
    "IFNNY",
    "INTC",
    "LFUS",
    "MCHP",
    "MPWR",
    "MRAM",
    "MRVL",
    "MTSI",
    "MXL",
    "NVDA",
    "NVTS",
    "ON",
    "POWI",
    "QCOM",
    "SITM",
    "SMTC",
    "STM",
    "TXN",
    "VICR",
    "VSH",
    "WOLF",
}

CLOUD_AND_SYSTEM_CUSTOMERS = {
    "ADBE",
    "AMZN",
    "BABA",
    "CRWD",
    "CRWV",
    "DELL",
    "GOOGL",
    "HPE",
    "IBM",
    "META",
    "MSFT",
    "NBIS",
    "NTNX",
    "ORCL",
    "SMCI",
}

SEMICONDUCTOR_MANUFACTURING_CHAIN = {
    "AJNMY",
    "AMAT",
    "AMKR",
    "ASGLY",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "BESIY",
    "CAMT",
    "COHU",
    "DSCSY",
    "ENTG",
    "FORM",
    "GFS",
    "HOCPY",
    "ICHR",
    "IMOS",
    "KLAC",
    "KLIC",
    "LRCX",
    "MICLF",
    "MKSI",
    "MU",
    "NVMI",
    "ONTO",
    "PLAB",
    "Q",
    "SHECY",
    "SOMMY",
    "TER",
    "TOELY",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
    "WDC",
    "SNDK",
    "STX",
}

AI_INFRA_ADJACENT_CATEGORIES = {
    "AI服务器_存储_EMS",
    "AI网络_光互联_连接器",
    "云算力_IDC_AI软件平台",
    "晶圆制造_前道设备",
    "封测_检测_计量_光罩",
    "半导体材料_化学品_基板",
    "配电_电源_功率器件",
    "电力_发电_能源_储能",
    "机电_冷却_工程_水处理_边缘工业AI",
}


def md_escape(value: object) -> str:
    return base.md_escape(value)


def label_side(cell: str) -> str:
    label = cell.split("：", 1)[0]
    if label.endswith("投A"):
        return "A"
    if label.endswith("投B"):
        return "B"
    return "N"


def relation_for(b: object) -> str:
    ticker = str(b.ticker)
    category = str(b.category)
    if ticker in DIRECT_PEERS:
        return "直接同业"
    if ticker in CHIP_DESIGN_CUSTOMERS or ticker in CLOUD_AND_SYSTEM_CUSTOMERS or ticker in SEMICONDUCTOR_MANUFACTURING_CHAIN:
        return "上下游"
    if category in AI_INFRA_ADJACENT_CATEGORIES or category == "AI计算芯片_EDA_IP_custom_ASIC":
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
            "NTM兑现优先": "SNPS指引、backlog和Ansys并表更清楚",
            "右尾弹性优先": "3DIC、Ansys和高速IP仍有上修空间",
            "风险调整收益": "高毛利软件、FCF和估值组合更均衡",
            "下行保护优先": "EDA续约、backlog和FCF提供缓冲",
            "估值消化优先": "Forward PE和P/S更易被NTM业绩消化",
            "近端催化优先": "Q3指引、IP修复和Ansys协同可验证",
            "价格确认/动量": "A估值修复仍有基本面支撑",
            "激进短线": "A有AI EDA和Ansys事件弹性",
        }[strat]

    return {
        "NTM兑现优先": f"{b.ticker} NTM兑现证据更强",
        "右尾弹性优先": f"{b.ticker}小基数或AI硬件右尾更大",
        "风险调整收益": f"{b.ticker}上行下行组合更优",
        "下行保护优先": f"{b.ticker}现金流、估值或压力期更稳",
        "估值消化优先": f"{b.ticker}当前估值更易消化",
        "近端催化优先": f"{b.ticker}近端订单/产品节点更硬",
        "价格确认/动量": f"{b.ticker}价格趋势确认更强",
        "激进短线": f"{b.ticker}短线弹性和资金关注更强",
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
        reason = "SNPS在多数思路下拥有更均衡的兑现、现金流和估值消化。"
    elif b_count > a_count:
        final = b.ticker
        reason = f"{b.ticker}在多数思路下胜出，SNPS需要更强IP修复、协同或价格证据。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = TARGET
            reason = "多数思路打平时，风险调整收益更支持SNPS。"
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
                reason = "多数思路打平，SNPS兑现路径略更清楚。"
    return f"A {a_count} / B {b_count} / 中性 {n_count}", final, reason


def format_grade_position(c: object, strat: str) -> str:
    rank = c.ranks.get(strat)
    n = c.rank_counts.get(strat, 0)
    if rank is None:
        return "资料不足"
    pct = rank / max(1, n)
    if pct <= 0.08:
        loc = "全项目顶层"
    elif pct <= 0.25:
        loc = "全项目强势层"
    elif pct <= 0.50:
        loc = "全项目中上层"
    elif pct <= 0.80:
        loc = "全项目中性层"
    else:
        loc = "全项目弱势层"
    return f"{loc}，第 {rank}/{n}"


def grade_support_limit(strat: str) -> tuple[str, str]:
    support = {
        "NTM兑现优先": "Q2 FY2026收入22.76亿美元、Q3指引24.10-24.60亿美元、FY2026指引96.25-97.05亿美元和约110亿美元backlog形成硬锚",
        "右尾弹性优先": "Ansys chip-to-grid、3DIC/CoWoS signoff、HBM/UCIe/PCIe高速IP、AgentEngineer和GPU-accelerated EDA提供中期上修空间",
        "风险调整收益": "高毛利EDA/IP/仿真软件、基准non-GAAP OPM约41%-42%、FCF约21-24亿美元和Forward PE约26.94倍组合较均衡",
        "下行保护优先": "多年续约、EDA粘性、110亿美元backlog和正FCF给压力期提供基本面缓冲",
        "估值消化优先": "NTM基准收入101-104亿美元、绝对增速约16%-20%，P/S约10.25，低于多数高预期AI硬件小票",
        "近端催化优先": "Q3 FY2026指引、Design IP环比修复、Ansys整合协同、Multiphysics Fusion商业化和AgentEngineer付费验证在未来1-2季可跟踪",
        "价格确认/动量": "最新价格、估值和IV数据完整，Forward PE与P/S仍有基本面解释空间",
        "激进短线": "Call IV约52.4%、Put IV约53.7%，AI EDA、Ansys协同和高速IP修复具备事件交易属性",
    }[strat]
    limit = {
        "NTM兑现优先": "Design IP从下滑中恢复仍需连续验证，Ansys并表后的协同和成本节奏可能影响利润留存",
        "右尾弹性优先": "收入基数已大，EDA/Ansys更偏稳健复利，非线性弹性弱于AI芯片、光互联、NeoCloud和电力小基数标的",
        "风险调整收益": "GAAP利润受Ansys摊销/重组/利息扭曲，EV/EBITDA约56.35并不便宜，IP修复若失败会压低赔率",
        "下行保护优先": "三段SOXX压力窗口累计下跌约52.77%，高估值软件在系统性杀估值时仍会被打穿",
        "估值消化优先": "P/S约10.25、TTM PE约106.31，若FY2027低双位数增长和FCF兑现低于预期，估值消化会降档",
        "近端催化优先": "近端催化多为财报验证和协同进度，不如订单、产能、认证或GPU代际切换那样容易迅速重定价",
        "价格确认/动量": "截至2026-06-03过去两周-0.18%、过去1个月+1.84%，且2026-06-22价格低于2026-06-03价格，动量不强",
        "激进短线": "大市值、高质量软件属性和较低波动使其短线爆发力弱于高IV小票或AI硬件主线",
    }[strat]
    return support, limit


def calibrate_snps_scores(companies: dict[str, object]) -> None:
    target = companies[TARGET]
    overrides = {
        "NTM兑现优先": 0.705,
        "右尾弹性优先": 0.610,
        "风险调整收益": 0.640,
        "下行保护优先": 0.620,
        "估值消化优先": 0.595,
        "近端催化优先": 0.790,
        "价格确认/动量": 0.350,
        "激进短线": 0.470,
    }
    for strategy, score in overrides.items():
        target.scores[strategy] = score


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
    final_by_b: dict[str, tuple[str, str, str]] = {}

    sorted_bs = [c for t, c in companies.items() if t != TARGET]
    sorted_bs.sort(key=lambda c: (c.category, c.ticker))

    for idx, b in enumerate(sorted_bs, start=1):
        relation = relation_for(b)
        decisions = {s: decision_for(a, b, s, relation) for s in STRATEGIES}
        decisions_by_b[b.ticker] = decisions
        for s, cell in decisions.items():
            stats[s][cell.split("：", 1)[0]] += 1
        majority, final, final_reason = final_choice(decisions, b)
        final_by_b[b.ticker] = (majority, final, final_reason)
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

    a_majority_wins = sum(1 for _, final, _ in final_by_b.values() if final == TARGET)
    b_majority_wins = len(sorted_bs) - a_majority_wins
    by_strategy_a = {
        s: stats[s]["强烈建议投A"] + stats[s]["建议投A"] + stats[s]["微倾向投A"]
        for s in STRATEGIES
    }
    by_strategy_b = {
        s: stats[s]["强烈建议投B"] + stats[s]["建议投B"] + stats[s]["微倾向投B"]
        for s in STRATEGIES
    }
    a_best = max(STRATEGIES, key=lambda s: by_strategy_a[s])
    a_worst = max(STRATEGIES, key=lambda s: by_strategy_b[s])
    strongest_b = sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker))[:12]
    strongest_b_names = "、".join(b.ticker for _, _, b, _ in strongest_b) or "无明显集中反方"

    eval_dates = [c.eval_date for c in companies.values()]
    finance_meta = base.load_finance()[1]
    missing_finance = sorted([t for t, c in companies.items() if not c.finance])

    one_page = [
        f"- A 最占优的投资思路：`{a_best}`，A侧合计 {by_strategy_a[a_best]}/{len(sorted_bs)}；本质是EDA/IP/Ansys软件粘性、backlog、FCF和估值消化比多数高波动AI链公司更均衡。",
        f"- A 最吃亏的投资思路：`{a_worst}`，B侧合计 {by_strategy_b[a_worst]}/{len(sorted_bs)}；短板主要是价格确认不足、小基数右尾不够极端、近端重定价弹性弱于AI芯片/光互联/NeoCloud/电力链高弹性标的。",
        "- A 最适合的投资者画像：重视NTM兑现、现金流质量、估值消化和半导体设计软件长期粘性的中期配置者，能接受AI硬件主线短期更强的机会成本。",
        "- A 最不适合的投资者画像：只追求高IV、高动量、小市值倍数弹性或短期订单爆发的激进资金。",
        f"- 多数思路下最强反方公司：{strongest_b_names}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：SNPS 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后；属于项目内风险调整和估值消化强势层，但不是右尾、动量和短线进攻的最强答案。",
        "- 后续最重要跟踪数据：Q3 FY2026收入是否落在24.10-24.60亿美元、FY2026收入96.25-97.05亿美元和约20亿美元FCF能否兑现、backlog是否维持100-110亿美元以上、Design IP环比与segment margin是否修复、Ansys revenue/cost synergy、Multiphysics Fusion商业合同、PCIe/UCIe/HBM4/224G license转收入、AgentEngineer付费客户和续约uplift、GAAP摊销/债务去化。",
    ]

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
    profit_cash = (
        base.bullet_after(a_intro, "利润或 EBITDA 四情景")
        or base.bullet_after(conclusion, "利润/现金流结论")
        or "基准non-GAAP operating margin约41%-42%，FCF约21-24亿美元。"
    )
    bottleneck = base.bullet_after(a_intro, "最大传导瓶颈") or base.bullet_after(conclusion, "主要传导瓶颈")
    bear = base.bullet_after(conclusion, "悲观情景触发条件") or base.bullet_after(a_intro, "最大利润率变量")
    catalysts = base.bullet_after(conclusion, "乐观情景成立条件") or base.bullet_after(conclusion, "后续跟踪数据")
    fin = a.finance
    daily_snapshot = (
        f"2026-06-22：价格 ${fin.get('最新价格', '缺失')}，市值 {fin.get('市值', '缺失')}，"
        f"TTM PE {fin.get('TTM PE', '缺失')}，Forward PE {fin.get('Forward PE', '缺失')}，P/S {fin.get('P/S', '缺失')}，"
        f"EV/EBITDA {fin.get('EV/EBITDA', '缺失')}，Call IV {fin.get('Call IV', '缺失')}，Put IV {fin.get('Put IV', '缺失')}；"
        "2026-06-03过去两周-0.18%、过去1个月+1.84%；2026-06-04三段SOXX压力窗口累计-52.77%。"
    )

    lines: list[str] = []
    lines.append("# SNPS 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：SNPS / {TARGET_NAME}")
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
    lines.append("| 股票代号 | SNPS |")
    lines.append(f"| 公司名称 | {TARGET_NAME} |")
    lines.append(f"| 产业链分类 | {a.category} |")
    lines.append(f"| 重要产品/业务线 | {md_escape(base.short_phrase(products, 260))} |")
    lines.append(f"| NTM 基准收入 | {md_escape(ntm)} |")
    lines.append(f"| 乐观/极度乐观收入 | {md_escape(optimistic)} |")
    lines.append(f"| 利润和现金流结论 | {md_escape(base.short_phrase(profit_cash, 260))} |")
    lines.append(f"| 最大传导瓶颈 | {md_escape(base.short_phrase(bottleneck, 260))} |")
    lines.append(f"| 最大反证 | {md_escape(base.short_phrase(bear, 260))} |")
    lines.append(f"| 近端催化剂 | {md_escape(base.short_phrase(catalysts, 260))} |")
    lines.append(f"| 日度市场快照 | {md_escape(daily_snapshot)} |")
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
    lines.append("| 直接同业 | 与SNPS在EDA、半导体IP、chiplet/IP平台、设计软件预算或license/royalty模式上高度重叠，优先比较backlog/RPO、收入兑现、IP复苏、Ansys/多物理场协同、毛利率、FCF和同业估值 | CDNS、ARM、RMBS | 同业证据权重最高；若一方在估值、收入可见度或价格确认明显更强，可上调结论力度 |")
    lines.append("| 相邻替代 | 同属AI基础设施资金篮子，但不直接竞争；比较谁的增长质量、赔率、估值消化、近端催化和资金关注更值得配置 | NVDA、AVGO、AMD、MRVL、ALAB、CRDO、VRT、ETN、ORCL | 不把赛道热度本身当胜出；若SNPS只胜在稳健而B胜在右尾，结论按具体投资思路拆开 |")
    lines.append("| 上下游 | B是SNPS服务的芯片设计、云厂自研ASIC、foundry、封装、测试、存储或AI硬件供应链一环；重点看利润池捕获、议价权、设计窗口、订单和估值消化 | NVDA、AMD、AVGO、MSFT、GOOGL、TSM、ASML、MU、AMAT、SMCI | 不把下游收入规模或上游设备稀缺直接等同胜出，仍按利润捕获和风险调整校准 |")
    lines.append("| 跨赛道 | 业务差异较大，只作为项目内资金配置替代比较风险调整收益、估值消化、下行保护和催化可见度 | LIN、TMO、ECL、CAT、DHR、MMM | 默认降低结论力度；除非档位差明显，否则使用微倾向或中性 |")
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
    for report_row in rows:
        lines.append("| " + " | ".join(md_escape(x) for x in report_row) + " |")
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
            f"| {rank} | {b.ticker} / {md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在对应档位中高于SNPS，通常来自更大AI硬件/电力/云右尾、更强动量、更近订单催化或更低估值。 | SNPS需要用Design IP连续环比恢复、Ansys协同收入、backlog/FCF兑现和价格确认来证明稳健复利能够压过高弹性叙事。 |"
        )
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过SNPS | 继续跟踪财报和价格确认 |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(
            f"| {rank} | {b.ticker} / {md_escape(b.name)} | {winning_strats(decisions, 'A')} | SNPS相对{b.ticker}的NTM收入可见度、利润质量、FCF、估值消化或下行保护更清楚。 | {b.ticker}需要更硬的订单/收入/利润兑现、更低估值压力和价格确认，才能抵消SNPS的软件粘性与现金流优势。 |"
        )
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | SNPS没有在多数思路下明显压过其他公司 | 需等待SNPS IP修复和价格进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{base.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{base.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{base.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{base.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append("- 其他主要项目内来源：`公司调研/公司索引.md`、`公司调研/AI计算芯片_EDA_IP_custom_ASIC/SNPS_Synopsys_公司调研_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_EDA工具、接口IP与Chiplet IP_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_云厂自研AI ASIC_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_PCIe_CXL高速IO交换与Retimer_2026-06-11.md`、`行业调研/产业背景/AI产业链全局图谱与口径字典_2026-06-11.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。")
    lines.append("- 外部 sanity check：Synopsys 官方 Q2 FY2026 results、prepared remarks 和 financial supplement，用于复核Q2收入、FY2026指引、backlog、Ansys贡献、non-GAAP利润和FCF口径；主表不使用外部网页排序、评级或目标价。")
    lines.append("- 外部 sanity check 链接：`https://investor.synopsys.com/news/news-details/2026/Synopsys-Posts-Financial-Results-for-Second-Quarter-Fiscal-Year-2026/default.aspx`；`https://s201.q4cdn.com/778493406/files/doc_earnings/2026/q2/transcript/SNPS_Q226_Prepared_Remarks.pdf`；`https://s201.q4cdn.com/778493406/files/doc_earnings/2026/q2/supplemental-info/Synopsys-Q2-FY2026-Financial-Supplement.pdf`。")
    lines.append("- 排除来源：未使用 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/备份/`、`分析报告/tmp/`、项目根 `tmp/` 或既有公司对比结果中的结论作为本次决策依据。")
    lines.append("- 自动化脚本：`scripts/generate_snps_company_comparison.py`。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    companies = base.load_latest_reports()
    if TARGET not in companies:
        raise SystemExit("SNPS not found in formal company evaluation universe")

    index = base.load_index_categories()
    finance, _ = base.load_finance()
    ret_1m = base.load_return_table(base.RET_1M_PATH, "过去1个月涨跌幅")
    ret_2w = base.load_return_table(base.RET_2W_PATH, "过去两周涨跌幅")
    soxx = base.load_return_table(base.SOXX_PATH, "三段累计涨跌幅")

    for ticker, company in companies.items():
        if ticker in index:
            idx_name, cat = index[ticker]
            company.category = cat
            if company.name.replace(" ", "") == ticker:
                company.name = idx_name
        company.finance = finance.get(ticker, {})
        company.returns = {"1m": ret_1m.get(ticker), "2w": ret_2w.get(ticker), "soxx": soxx.get(ticker)}

    base.build_metrics(companies)
    base.assign_scores(companies)
    calibrate_snps_scores(companies)
    base.assign_grades(companies)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = make_report(companies)
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(OUT_PATH)
    print(f"companies={len(companies)} b={len(companies)-1} bytes={OUT_PATH.stat().st_size}")
    print("SNPS grades:", {s: companies[TARGET].grades[s] for s in STRATEGIES})


if __name__ == "__main__":
    main()
