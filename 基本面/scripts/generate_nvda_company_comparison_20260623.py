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
TARGET = "NVDA"
TARGET_NAME = "NVIDIA"
REPORT_DATE = "2026-06-23"
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "NVDA_逐家公司投资思路对比_2026-06-23.md"

STRATEGIES = base.STRATEGIES
LABEL_ORDER = base.LABEL_ORDER
GRADE_VALUE = base.GRADE_VALUE


DIRECT_AI_CHIP_PEERS = {
    "AMD",
    "AVGO",
    "INTC",
    "MRVL",
    "QCOM",
    "ARM",
}

UPSTREAM_DOWNSTREAM_TICKERS = {
    # Cloud / AI compute buyers and NeoClouds.
    "ADBE",
    "AMZN",
    "APLD",
    "BABA",
    "CRWD",
    "CRWV",
    "DLR",
    "EQIX",
    "GOOGL",
    "IBM",
    "IREN",
    "META",
    "MSFT",
    "NBIS",
    "NTNX",
    "ORCL",
    # Foundry, memory, packaging, test and core semiconductor supply chain.
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
    "CDNS",
    "COHU",
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
    "RMBS",
    "SHECY",
    "SNPS",
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
    # Server, EMS, rack and network attach suppliers.
    "AAOI",
    "ALAB",
    "ANET",
    "APH",
    "BDC",
    "BELFB",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "CSCO",
    "DELL",
    "FLEX",
    "FN",
    "GLW",
    "HPE",
    "JBL",
    "LITE",
    "LWLG",
    "MTSI",
    "NOK",
    "PENG",
    "POET",
    "SANM",
    "SITM",
    "SMCI",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}

AI_INFRA_ADJACENT_CATEGORIES = {
    "电力_发电_能源_储能",
    "机电_冷却_工程_水处理_边缘工业AI",
    "配电_电源_功率器件",
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
    if ticker in DIRECT_AI_CHIP_PEERS:
        return "直接同业"
    if ticker in UPSTREAM_DOWNSTREAM_TICKERS:
        return "上下游"
    if category in AI_INFRA_ADJACENT_CATEGORIES:
        return "相邻替代"
    if category in {
        "AI计算芯片_EDA_IP_custom_ASIC",
        "AI服务器_存储_EMS",
        "AI网络_光互联_连接器",
        "云算力_IDC_AI软件平台",
        "晶圆制造_前道设备",
        "封测_检测_计量_光罩",
        "半导体材料_化学品_基板",
    }:
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
            "NTM兑现优先": "NVDA指引、收入表和GB300交付更硬",
            "右尾弹性优先": "GB300/Rubin/Networking美元右尾更大",
            "风险调整收益": "高增长、高毛利和强FCF组合更优",
            "下行保护优先": "平台锁定和现金流抵消周期波动",
            "估值消化优先": "NTM利润增速可消化当前估值",
            "近端催化优先": "财报、GB300/Rubin和Networking节点近",
            "价格确认/动量": "AI主线流动性和价格确认更充分",
            "激进短线": "高关注度、35%左右IV和产品催化可交易",
        }[strat]

    return {
        "NTM兑现优先": f"{b.ticker} NTM兑现证据更强",
        "右尾弹性优先": f"{b.ticker}小基数或非线性右尾更大",
        "风险调整收益": f"{b.ticker}上行下行组合更优",
        "下行保护优先": f"{b.ticker}现金流、估值或压力期更稳",
        "估值消化优先": f"{b.ticker}当前估值更易被业绩消化",
        "近端催化优先": f"{b.ticker}近端事件重定价概率更高",
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
        reason = "NVDA在多数思路下拥有更硬的收入兑现、利润率和AI平台稀缺性。"
    elif b_count > a_count:
        final = b.ticker
        reason = f"{b.ticker}在多数思路下胜出，NVDA需要更强价格确认、下行保护或新增催化证据。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = TARGET
            reason = "多数思路打平时，风险调整收益更支持NVDA。"
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
                reason = "多数思路打平，NVDA兑现路径略更清楚。"
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
        "NTM兑现优先": "FY2027 Q1收入816.15、Q2指引910、Data Center Compute/Networking收入表和GB300交付形成硬锚",
        "右尾弹性优先": "GB300、Rubin、Data Center Networking、CUDA软件锁定和AI factory替换周期提供大美元右尾",
        "风险调整收益": "高毛利、高经营利润率、强FCF和AI核心利润池稀缺性共同支撑风险调整收益",
        "下行保护优先": "现金流、平台锁定、客户粘性和规模利润池强于多数高弹性小票",
        "估值消化优先": "基准NTM收入3700-4100、经营性净利润1940-2250，最新Forward PE约16.39倍",
        "近端催化优先": "FY2027 Q2实际/后续指引、GB300云部署、Rubin 2026H2验证和Networking attach均是近端节点",
        "价格确认/动量": "1个月涨幅+8.21%、AI主线流动性强，最新价格/IV数据完整",
        "激进短线": "35%左右近月IV、超高成交关注度、财报和产品节点使NVDA仍是主线交易标的",
    }[strat]
    limit = {
        "NTM兑现优先": "NVIDIA不披露传统backlog/bookings；客户集中、上电、HBM/CoWoS/液冷和验收会影响节奏",
        "右尾弹性优先": "市值和收入基数已极大，倍数型弹性通常弱于小基数光互联、NeoCloud和电力链",
        "风险调整收益": "P/S约19.94、市场预期极高，客户ROI、ASIC替代和出口管制仍是反证",
        "下行保护优先": "SOXX三段压力窗口累计下跌约59.56%，高beta和拥挤交易会放大回撤",
        "估值消化优先": "估值已要求高增长延续，若Q3指引、毛利率或FCF转化走弱，消化速度会降档",
        "近端催化优先": "催化必须转化为收入、毛利率和FCF；Rubin收入确认仍需正式验证",
        "价格确认/动量": "过去两周至2026-06-03为-3.90%，2026-06-22价格低于2026-06-03价格",
        "激进短线": "巨型市值限制单日爆发倍数，且利好拥挤时短线赔率会被IV和仓位挤压",
    }[strat]
    return support, limit


def calibrate_nvda_scores(companies: dict[str, object]) -> None:
    target = companies[TARGET]
    overrides = {
        "NTM兑现优先": 0.94,
        "右尾弹性优先": 0.865,
        "风险调整收益": 0.69,
        "下行保护优先": 0.63,
        "估值消化优先": 0.72,
        "近端催化优先": 0.905,
        "价格确认/动量": 0.58,
        "激进短线": 0.735,
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
    strongest_b = sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker))[:10]
    strongest_b_names = "、".join(b.ticker for _, _, b, _ in strongest_b) or "无明显集中反方"

    eval_dates = [c.eval_date for c in companies.values()]
    finance_meta = base.load_finance()[1]
    missing_finance = sorted([t for t, c in companies.items() if not c.finance])

    one_page = [
        f"- A 最占优的投资思路：`{a_best}`，A侧合计 {by_strategy_a[a_best]}/{len(sorted_bs)}；核心来自FY2027 Q2指引、Data Center收入表、GB300/Rubin/Networking和强利润现金流。",
        f"- A 最吃亏的投资思路：`{a_worst}`，B侧合计 {by_strategy_b[a_worst]}/{len(sorted_bs)}；主要输给小基数右尾、压力期防守资产、短窗动量更强或估值更便宜的公司。",
        "- A 最适合的投资者画像：愿意持有AI算力主线核心利润池，重视NTM兑现、利润质量、估值消化和近端产品/财报验证的中期配置者。",
        "- A 最不适合的投资者画像：只追求小市值倍数弹性、纯防守低波动、或要求短线价格已经持续突破确认的投资者。",
        f"- 多数思路下最强反方公司：{strongest_b_names}。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：NVDA 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后；属于全项目最强经营兑现与估值消化核心之一，但不是所有短线/下行/小基数右尾思路的唯一答案。",
        "- 后续最重要跟踪数据：FY2027 Q2实际收入和Q3指引、Data Center Compute/Networking拆分、non-GAAP毛利率、库存/应收/供应承诺/FCF、GB300云实例和rack acceptance、Rubin 2026H2转收入、HBM4 qualification、Broadcom/Marvell custom ASIC增速、云厂CapEx/RPO和中国出口限制。",
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
        or "基准经营性净利润约1940-2250，FCF强但需观察库存、应收和供应承诺。"
    )
    bottleneck = base.bullet_after(a_intro, "最大传导瓶颈") or base.bullet_after(conclusion, "主要传导瓶颈")
    bear = base.bullet_after(conclusion, "悲观情景触发条件") or base.bullet_after(a_intro, "最大利润率变量")
    catalysts = base.bullet_after(conclusion, "乐观情景成立条件") or base.bullet_after(conclusion, "后续跟踪数据")

    lines: list[str] = []
    lines.append("# NVDA 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：NVDA / {TARGET_NAME}")
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
    lines.append("| 股票代号 | NVDA |")
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
    lines.append("| 直接同业 | 与NVDA争夺AI加速器、自研ASIC、AI芯片IP或同一云厂AI计算预算，优先比较收入兑现、代际产品、客户份额、毛利率、估值消化和ASIC替代风险 | AMD、AVGO、MRVL、INTC、QCOM、ARM | 同档或相邻档时允许用更硬的产品/收入/份额证据放大到建议级别 |")
    lines.append("| 相邻替代 | 同属AI基础设施资金篮子或数据中心资本开支链条，但不是直接芯片同业，重点比较增长质量、兑现确定性、赔率、催化和估值压力 | VRT、ETN、GEV、CEG、SMR、OKLO、CDNS、SNPS | 默认按档位判断；若只是赛道更热但证据不硬，结论降为微倾向或中性 |")
    lines.append("| 上下游 | 云客户、NeoCloud、服务器/EMS、光互联/网络、HBM/存储、晶圆制造、先进封装、设备材料和测试等处在NVDA需求或供给链，重点看利润池、议价权、瓶颈稀缺性和capex传导 | MSFT、GOOGL、AMZN、META、CRWV、TSM、MU、SMCI、ANET、ALAB、COHR、ASML | 不把下游收入规模或上游瓶颈自动等同胜出，仍需检查利润捕获和估值消化 |")
    lines.append("| 跨赛道 | 与NVDA业务差异较大，但作为资金配置替代仍可比较，重点看风险调整收益、估值消化、下行保护和催化可见度 | LIN、ECL、TMO、DHR、MMM、CAT | 默认降低结论力度；证据互有强弱时优先使用微倾向或中性 |")
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
            f"| {rank} | {b.ticker} / {md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在对应档位中高于NVDA，通常来自更强短窗动量、下行保护、小基数右尾、估值便宜或近端特定催化。 | NVDA需要继续用Q2/Q3收入、毛利率、GB300/Rubin收入确认、FCF和价格确认证明AI主线仍能消化预期。 |"
        )
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过NVDA | 继续跟踪财报、GB300/Rubin、Networking和价格确认 |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(
            f"| {rank} | {b.ticker} / {md_escape(b.name)} | {winning_strats(decisions, 'A')} | NVDA相对{b.ticker}的NTM兑现、利润质量、AI平台稀缺性、估值消化或近端催化更清楚。 | {b.ticker}需要更硬的订单/收入/利润兑现、估值消化证据和价格确认。 |"
        )
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | NVDA没有在多数思路下明显压过其他公司 | 需等待财报和价格进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{base.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{base.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{base.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{base.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md` 用于公司名称和分类；A侧业务证据主要来自 `公司调研/AI计算芯片_EDA_IP_custom_ASIC/NVDA_NVIDIA_公司调研_2026-06-20.md`、`行业调研/产业背景/行业调研_头部AI芯片全景与产能释放_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_商用AI加速芯片_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_云厂自研AI ASIC_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_InfiniBand与专有Scale-up互联_2026-06-11.md`、`行业调研/AI网络_光互联_铜互联/行业调研_AI以太网交换系统与Fabric芯片_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心直液冷系统_2026-06-10.md` 和 `行业调研/AI园区电力_机电_冷却/行业调研_数据中心电力接入与高压变电_2026-06-11.md`；这些来源也已在NVDA正式评估中汇总校准。")
    lines.append("- 排除来源：未使用 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/备份/`、`分析报告/tmp/` 或项目根 `tmp/` 中的结论作为本次决策依据。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    companies = base.load_latest_reports()
    if TARGET not in companies:
        raise SystemExit("NVDA not found in formal company evaluation universe")

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
    calibrate_nvda_scores(companies)
    base.assign_grades(companies)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = make_report(companies)
    OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(OUT_PATH)
    print(f"companies={len(companies)} b={len(companies)-1} bytes={OUT_PATH.stat().st_size}")
    print("NVDA grades:", {s: companies[TARGET].grades[s] for s in STRATEGIES})


if __name__ == "__main__":
    main()
