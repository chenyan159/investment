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
TARGET = "ST"
TARGET_NAME = "Sensata Technologies"
REPORT_DATE = "2026-06-23"
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ST_逐家公司投资思路对比_2026-06-23.md"

STRATEGIES = base.STRATEGIES
LABEL_ORDER = base.LABEL_ORDER
GRADE_VALUE = base.GRADE_VALUE


DIRECT_COMPONENT_PEERS = {
    "LFUS",
    "VSH",
    "BELFB",
    "POWI",
    "DIOD",
    "AOSL",
    "IFNNY",
    "MCHP",
    "ON",
    "STM",
    "TXN",
    "ADI",
    "TEL",
    "APH",
}

ELECTRICAL_AND_POWER_ADJACENT = {
    "ABBNY",
    "AEIS",
    "ALLE",
    "ATKR",
    "ETN",
    "HUBB",
    "MIELY",
    "MPWR",
    "MRAAY",
    "NVT",
    "NVTS",
    "POWL",
    "ROG",
    "TTDKY",
    "VICR",
    "WOLF",
}

DATA_CENTER_DEMAND_CHAIN = {
    "ADBE",
    "AMZN",
    "APLD",
    "BABA",
    "CRWD",
    "CRWV",
    "DELL",
    "DLR",
    "EQIX",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "META",
    "MSFT",
    "NBIS",
    "NTNX",
    "ORCL",
    "PENG",
    "SMCI",
}

POWER_UTILITY_AND_ENGINEERING_CHAIN = {
    "AEP",
    "BE",
    "BWXT",
    "CEG",
    "CMI",
    "DTE",
    "EME",
    "ENS",
    "ET",
    "ETR",
    "FIX",
    "FLNC",
    "GEV",
    "GNRC",
    "HTHIY",
    "IESC",
    "MYRG",
    "OKLO",
    "PSIX",
    "PWR",
    "RYCEY",
    "SMR",
    "VRT",
    "VST",
}

AI_HARDWARE_AND_NETWORK_CHAIN = {
    "AAOI",
    "ALAB",
    "AMD",
    "ANET",
    "ARM",
    "AVGO",
    "BDC",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "CSCO",
    "FLEX",
    "FN",
    "JBL",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "MU",
    "NOK",
    "NTAP",
    "NVDA",
    "POET",
    "PSTG",
    "QCOM",
    "RMBS",
    "SANM",
    "SIMO",
    "SITM",
    "SMTC",
    "SNDK",
    "STX",
    "VIAV",
    "VISN",
    "WDC",
}

INDUSTRIAL_SENSOR_ADJACENT = {
    "AAON",
    "CARR",
    "CAT",
    "DCI",
    "DHR",
    "DKILY",
    "DOV",
    "ECL",
    "FTV",
    "JCI",
    "MOD",
    "MSI",
    "NDSN",
    "PH",
    "PNR",
    "TDY",
    "TMO",
    "TT",
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
    if ticker in DIRECT_COMPONENT_PEERS:
        return "直接同业"
    if ticker in DATA_CENTER_DEMAND_CHAIN or ticker in POWER_UTILITY_AND_ENGINEERING_CHAIN:
        return "上下游"
    if ticker in ELECTRICAL_AND_POWER_ADJACENT or ticker in INDUSTRIAL_SENSOR_ADJACENT:
        return "相邻替代"
    if ticker in AI_HARDWARE_AND_NETWORK_CHAIN:
        return "上下游"
    if category == "配电_电源_功率器件":
        return "相邻替代"
    if category in {"电力_发电_能源_储能", "机电_冷却_工程_水处理_边缘工业AI", "AI服务器_存储_EMS", "云算力_IDC_AI软件平台"}:
        return "上下游"
    if category in {"AI网络_光互联_连接器", "AI计算芯片_EDA_IP_custom_ASIC"}:
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
            return "业务差异大且证据互抵"
        return "档位接近，证据互有强弱"

    side = "A" if label.endswith("投A") else "B"
    if side == "A":
        return {
            "NTM兑现优先": "ST指引、FCF和低估值兑现更稳",
            "右尾弹性优先": "ST有液冷传感和保护件小基数期权",
            "风险调整收益": "ST估值低、FCF正且反证已部分计价",
            "下行保护优先": "ST现金流和低倍数提供缓冲",
            "估值消化优先": "ST Forward PE/P/S更容易消化",
            "近端催化优先": "ST有Q2指引和data center验证节点",
            "价格确认/动量": "ST近月涨幅已有价格确认",
            "激进短线": "ST低估值重估和DC期权可交易",
        }[strat]

    return {
        "NTM兑现优先": f"{b.ticker} NTM收入/订单兑现更硬",
        "右尾弹性优先": f"{b.ticker} AI右尾或小基数弹性更大",
        "风险调整收益": f"{b.ticker}上行下行组合更优",
        "下行保护优先": f"{b.ticker}现金流、资产或压力期更稳",
        "估值消化优先": f"{b.ticker}估值更易由高增长消化",
        "近端催化优先": f"{b.ticker}订单/RPO/产品节点更近",
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
        reason = "ST多数胜出主要靠低估值、FCF和价格确认，而非更强AI右尾。"
    elif b_count > a_count:
        final = b.ticker
        reason = f"{b.ticker}多数思路更强，通常拥有更硬增长、订单/RPO、AI右尾或防守质量。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = TARGET
            reason = "多数思路打平时，风险调整收益更支持ST。"
        elif risk_label.endswith("投B"):
            final = b.ticker
            reason = f"多数思路打平时，风险调整收益更支持{b.ticker}。"
        else:
            valuation_label = decisions["估值消化优先"].split("：", 1)[0]
            if valuation_label.endswith("投A"):
                final = TARGET
                reason = "多数思路打平，估值消化略支持ST。"
            elif valuation_label.endswith("投B"):
                final = b.ticker
                reason = f"多数思路打平，估值消化略支持{b.ticker}。"
            else:
                final = b.ticker
                reason = f"多数思路打平且风格差异大，优先选择成长证据更清晰的{b.ticker}。"
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
        "NTM兑现优先": "2026Q1收入9.348亿美元，Q2指引9.50-9.80亿美元，NTM基准38.5-40.2亿美元，FCF预计5.0-5.8亿美元",
        "右尾弹性优先": "液冷flow/pressure/temp sensing、两个hyperscaler specs、Dynapower UPS/BESS和800VDC/HVDC保护件提供小基数期权",
        "风险调整收益": "2026-06-22 Forward PE 12.78、P/S 2.02、EV/EBITDA 12.62，且核心传感/保护业务仍有正FCF",
        "下行保护优先": "低倍数、FCF、三分部现金生成和高可靠传感/保护件粘性提供基本缓冲",
        "估值消化优先": "低Forward PE、低P/S、调整后经营利润率18.8%-19.5%和现金流可消化当前市值",
        "近端催化优先": "Q2指引兑现、Industrials data center design win/order措辞、flow sensor验证、ADCE H2趋势可跟踪",
        "价格确认/动量": "截至2026-06-03过去两周+12.17%、过去1个月+26.93%，已有周期修复和期权重估迹象",
        "激进短线": "Call IV约47.5%、Put IV约48.4%，低估值重估叠加data center sensing/electrical protection叙事可交易",
    }[strat]
    limit = {
        "NTM兑现优先": "汽车仍占过半、工业/HVAC短周期偏弱，且公司不披露data center revenue、backlog、book-to-bill或RPO",
        "右尾弹性优先": "AI/DC直接收入低个位数，规格导入和validation尚未变成客户、订单金额、交付时间和收入确认",
        "风险调整收益": "净杠杆约2.6x、2025 Dynapower impairment和汽车/工业周期使低估值有合理折价",
        "下行保护优先": "2026-06-04三段SOXX压力窗口累计-65.37%，说明系统性杀估值时回撤并不防守",
        "估值消化优先": "GAAP TTM PE受impairment扭曲至高位，若低个位数增长和19% margin不能持续，低倍数未必扩张",
        "近端催化优先": "催化多是验证和措辞变化，不如GPU、光互联、NeoCloud或电力设备订单那样能快速重定价",
        "价格确认/动量": "2026-06-22价格51.70低于2026-06-03收盘53.55，近月强势后已有回落",
        "激进短线": "ST不是纯AI主线，高beta、资金关注和非线性收入弹性弱于AI芯片、光互联和小市值电力链",
    }[strat]
    return support, limit


def calibrate_st_scores(companies: dict[str, object]) -> None:
    target = companies[TARGET]
    overrides = {
        "NTM兑现优先": 0.505,
        "右尾弹性优先": 0.485,
        "风险调整收益": 0.530,
        "下行保护优先": 0.455,
        "估值消化优先": 0.580,
        "近端催化优先": 0.720,
        "价格确认/动量": 0.720,
        "激进短线": 0.580,
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
    a_best = max(STRATEGIES, key=lambda s: by_strategy_a[s] - by_strategy_b[s])
    a_worst = max(STRATEGIES, key=lambda s: by_strategy_b[s] - by_strategy_a[s])
    strongest_b = sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker))[:12]
    strongest_b_names = "、".join(b.ticker for _, _, b, _ in strongest_b) or "无明显集中反方"

    eval_dates = [c.eval_date for c in companies.values()]
    finance_meta = base.load_finance()[1]
    missing_finance = sorted([t for t, c in companies.items() if not c.finance])

    one_page = [
        f"- A 最占优的投资思路：`{a_best}`，A侧合计 {by_strategy_a[a_best]}/{len(sorted_bs)}；ST 的相对优势主要在低估值、现金流和近月价格确认，不在极端AI右尾。",
        f"- A 最吃亏的投资思路：`{a_worst}`，B侧合计 {by_strategy_b[a_worst]}/{len(sorted_bs)}；短板是汽车/工业低增、AI/DC直接收入很小，且没有订单金额、backlog或RPO硬锚。",
        "- A 最适合的投资者画像：愿意买低倍数、正FCF、传统汽车/工业传感和电气保护底盘，同时保留液冷/UPS/BESS/800VDC小期权的中期资金。",
        "- A 最不适合的投资者画像：只追求最强AI收入、订单爆发、RPO可见度、高IV短线弹性或公用事业式防守的资金。",
        f"- 多数思路下最强反方公司：{strongest_b_names}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：ST 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后；它是估值消化和价格确认较好的周期修复/期权标的，但不是项目内增长质量或右尾最强的公司。",
        "- 后续最重要跟踪数据：2026Q2实际收入是否落在9.50-9.80亿美元、Q3指引、Industrials organic growth、data center design win/order/revenue披露、flow sensor validation、PDU/CDU/UPS/HVDC平台认证、Dynapower backlog/毛利/现金流、ADCE H2订单、Automotive market outgrowth、FCF conversion和net leverage。",
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
    )
    bottleneck = base.bullet_after(a_intro, "最大传导瓶颈") or base.bullet_after(conclusion, "主要传导瓶颈")
    bear = base.bullet_after(conclusion, "悲观情景触发条件") or base.bullet_after(a_intro, "最大利润率变量")
    catalysts = base.bullet_after(conclusion, "乐观情景成立条件") or base.bullet_after(conclusion, "后续跟踪数据")
    fin = a.finance
    daily_snapshot = (
        f"2026-06-22：价格 ${fin.get('最新价格', '缺失')}，市值 {fin.get('市值', '缺失')}，"
        f"TTM PE {fin.get('TTM PE', '缺失')}，Forward PE {fin.get('Forward PE', '缺失')}，P/S {fin.get('P/S', '缺失')}，"
        f"EV/EBITDA {fin.get('EV/EBITDA', '缺失')}，Call IV {fin.get('Call IV', '缺失')}，Put IV {fin.get('Put IV', '缺失')}；"
        "2026-06-03过去两周+12.17%、过去1个月+26.93%；2026-06-04三段SOXX压力窗口累计-65.37%。"
    )

    lines: list[str] = []
    lines.append("# ST 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：ST / {TARGET_NAME}")
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
    lines.append("| 股票代号 | ST |")
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
    lines.append("| 直接同业 | 与 ST 在传感器、车规/工业电气保护、功率/分立器件、连接器或高可靠保护件需求池重叠，优先看同一客户群中的收入兑现、认证、margin和估值 | LFUS、VSH、BELFB、POWI、DIOD、AOSL、IFNNY、TEL、APH | 同档或相邻档时可用产品代际、客户认证和估值差放大到建议级别 |")
    lines.append("| 相邻替代 | 同属数据中心电力、配电、电源、工业电气或传感控制资金篮子，但产品不完全互替 | ETN、HUBB、NVT、ABBNY、MIELY、MPWR、AAON、CARR、JCI、MOD | 重点回答资金只能买一个时，谁的增长质量、订单可见度和估值消化更好 |")
    lines.append("| 上下游 | 云/IDC、服务器、AI硬件、MEP工程、电力、公用事业或发电公司与 ST 处于需求链上下游 | MSFT、AMZN、GOOGL、DELL、SMCI、VRT、PWR、EME、CEG、VST | 不把下游capex规模直接等同ST收入，重点看ST能否捕获利润池和确认订单 |")
    lines.append("| 跨赛道 | 半导体设备、材料、EDA、软件或其他业务差异较大的公司，仍作为项目资金配置替代比较 | ASML、TSM、CDNS、SNPS、LIN、TMO、DHR | 默认降低结论力度；只有增长质量、估值消化或风险调整收益明显拉开才给建议/强烈建议 |")
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
        need = "ST需要披露data center revenue、客户/订单金额、backlog或RPO，并证明汽车/工业周期不再拖累。"
        if relation_for(b) == "直接同业":
            need = "ST需要在直接同业中证明更强传感/保护件design-win、认证壁垒、margin和估值消化。"
        elif relation_for(b) == "上下游":
            need = "ST需要证明其零部件能比上下游公司更有效捕获AI数据中心利润池，并进入可确认收入。"
        lines.append(
            f"| {rank} | {b.ticker} / {md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在多数思路下拥有比ST更硬的增长、订单、右尾、动量或防守证据。 | {need} |"
        )
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过ST | 继续跟踪ST订单、收入和价格确认 |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        need = f"{b.ticker}需要更硬的NTM订单/利润兑现、估值消化证据、现金流改善或价格确认。"
        lines.append(
            f"| {rank} | {b.ticker} / {md_escape(b.name)} | {winning_strats(decisions, 'A')} | ST相对{b.ticker}的低估值、FCF、价格确认或下行赔率更清楚。 | {need} |"
        )
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | ST没有在多数思路下明显压过其他公司 | 需等待估值消化、订单和价格进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{base.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{base.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{base.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{base.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append(f"- 公司 A 日度数据摘录：{daily_snapshot}")
    lines.append("- 其他主要来源：`公司调研/公司索引.md`；`公司调研/配电_电源_功率器件/ST_Sensata Technologies_公司调研_2026-06-12.md`；`行业调研/AI园区电力_机电_冷却/行业调研_液冷小组件与流体控制_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`；`行业调研/AI园区电力_机电_冷却/行业调研_数据中心UPS与电池储能_2026-06-11.md`；以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。")
    lines.append("- 排除来源：未使用 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/备份/`、`分析报告/tmp/` 或项目根 `tmp/` 中的结论作为本次决策依据。")
    lines.append("- 自动化脚本：`scripts/generate_st_company_comparison.py`；脚本复用项目内正式评估与金融资料解析函数，并对 ST 做专门档位校准。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    companies = base.load_latest_reports()
    if TARGET not in companies:
        raise SystemExit("ST not found in formal company evaluation universe")

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
    calibrate_st_scores(companies)
    base.assign_grades(companies)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = make_report(companies)
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(OUT_PATH)
    print(f"companies={len(companies)} b={len(companies) - 1} bytes={OUT_PATH.stat().st_size}")
    print("ST grades:", {s: companies[TARGET].grades[s] for s in STRATEGIES})


if __name__ == "__main__":
    main()
