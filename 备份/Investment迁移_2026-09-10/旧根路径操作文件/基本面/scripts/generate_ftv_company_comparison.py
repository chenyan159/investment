from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base
import generate_ceg_company_comparison as calibrated


TARGET = "FTV"
TARGET_NAME = "Fortive Corporation"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "FTV_逐家公司投资思路对比_2026-06-23.md"

base.TARGET = TARGET
base.REPORT_DATE = REPORT_DATE
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_TEST_MEASUREMENT_PEERS = {
    "KEYS",
    "TDY",
}

FACILITY_INDUSTRIAL_ADJACENT = {
    "AAON",
    "ALLE",
    "CARR",
    "CAT",
    "DCI",
    "DHR",
    "DOV",
    "ECL",
    "EME",
    "FIX",
    "IESC",
    "JCI",
    "MMM",
    "MOD",
    "MSI",
    "MYRG",
    "NDSN",
    "PH",
    "PNR",
    "RKLB",
    "TMO",
    "TT",
    "VRT",
}

SEMI_TEST_ADJACENT = {
    "AEHR",
    "ATEYY",
    "CAMT",
    "COHU",
    "FORM",
    "KLIC",
    "ONTO",
    "TER",
    "VIAV",
}

ELECTRICAL_POWER_ADJACENT = {
    "ABBNY",
    "AEIS",
    "AEP",
    "ATKR",
    "BE",
    "BWXT",
    "CEG",
    "CMI",
    "DTE",
    "ENS",
    "ETN",
    "ETR",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "NVT",
    "POWI",
    "POWL",
    "PWR",
    "RYCEY",
    "VST",
}

DOWNSTREAM_AI_LOAD = {
    "ADBE",
    "AMZN",
    "APLD",
    "BABA",
    "CRWD",
    "CRWV",
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
    "META",
    "MSFT",
    "NBIS",
    "NTNX",
    "ORCL",
    "PENG",
    "SANM",
    "SMCI",
}

NETWORK_LOAD_CHAIN = {
    "AAOI",
    "ALAB",
    "ANET",
    "APH",
    "AVGO",
    "BDC",
    "BELFB",
    "CIEN",
    "COHR",
    "CRDO",
    "CSCO",
    "GLW",
    "LITE",
    "LWLG",
    "MRVL",
    "MTSI",
    "NOK",
    "POET",
    "SITM",
    "SMTC",
    "TEL",
}

FTV_SCORE_OVERRIDES = {
    # Fortive has good reported Q1/segment evidence and cash generation, but
    # its AI data-center exposure is mostly field-test / facility-software
    # optionality, not a disclosed order/backlog led growth story.
    "NTM兑现优先": 63.5,
    "右尾弹性优先": 43.8,
    "风险调整收益": 54.2,
    "下行保护优先": 86.0,
    "估值消化优先": 58.5,
    "近端催化优先": 60.0,
    "价格确认/动量": 46.0,
    "激进短线": 68.0,
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def md(value: object) -> str:
    text = base.clean(value)
    return text.replace("|", "/").replace("\n", " ")


def table_row(values: list[object]) -> str:
    return "| " + " | ".join(md(value) for value in values) + " |"


def fmt_num(value: object, decimals: int = 2) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.{decimals}f}"
    except Exception:
        return "缺失"


def fmt_b(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"${float(value):.2f}B"
    except Exception:
        return "缺失"


def fmt_pct(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):+.2f}%"
    except Exception:
        return "缺失"


def fmt_iv(value: object) -> str:
    if value is None:
        return "缺失"
    try:
        return f"{float(value):.1f}%"
    except Exception:
        return "缺失"


def category_short(category: str) -> str:
    return category.replace("_", "/") if category else "未分类"


def short_name(company: dict) -> str:
    return f"{company['ticker']} / {company['name']}"


def score_companies(companies: dict[str, dict]) -> None:
    old_target = getattr(base, "TARGET", TARGET)
    base.TARGET = TARGET
    calibrated.score_companies(companies)
    base.TARGET = old_target

    for strategy, score in FTV_SCORE_OVERRIDES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score
    calibrated.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    if ticker in DIRECT_TEST_MEASUREMENT_PEERS:
        return "直接同业"
    if ticker in DOWNSTREAM_AI_LOAD or ticker in NETWORK_LOAD_CHAIN:
        return "上下游"
    if category in {"云算力_IDC_AI软件平台", "AI服务器_存储_EMS", "AI网络_光互联_连接器"}:
        return "上下游"
    if (
        ticker in FACILITY_INDUSTRIAL_ADJACENT
        or ticker in SEMI_TEST_ADJACENT
        or ticker in ELECTRICAL_POWER_ADJACENT
        or category in INFRA_CATS
        or category == "封测_检测_计量_光罩"
    ):
        return "相邻替代"
    return "跨赛道"


def reason_for(strategy: str, winner: str, company: dict, rel: str, diff: float) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    if winner == "A":
        return {
            "NTM兑现优先": "A有Q1收入、分部利润和EPS指引硬锚",
            "右尾弹性优先": "A有Fluke和设施软件小额AI DC期权",
            "风险调整收益": "A现金流质量和经营反证更均衡",
            "下行保护优先": "A自由现金流、低IV和稳定业务更抗压",
            "估值消化优先": "A中个位数增长可部分消化估值",
            "近端催化优先": "A有IOS/AHS季度验证和订单跟踪",
            "价格确认/动量": "A走势更稳且未明显破位",
            "激进短线": "A仅在对手反证更重时胜出",
        }[strategy]

    if winner == "B":
        if ticker in DIRECT_TEST_MEASUREMENT_PEERS:
            return {
                "NTM兑现优先": "B同业测试需求和订单兑现更直接",
                "右尾弹性优先": "B同业产品代际和AI测试右尾更大",
                "风险调整收益": "B同业增长质量更能覆盖估值",
                "下行保护优先": "B同业估值或压力期韧性更好",
                "估值消化优先": "B同业业绩弹性更能消化估值",
                "近端催化优先": "B同业客户/产品催化更明确",
                "价格确认/动量": "B同业价格确认更强",
                "激进短线": "B同业短线资金弹性更高",
            }[strategy]
        if category in HIGH_GROWTH_CATS or ticker in DOWNSTREAM_AI_LOAD or ticker in NETWORK_LOAD_CHAIN:
            return {
                "NTM兑现优先": "B AI主链订单/RPO兑现更短链",
                "右尾弹性优先": "B AI主链右尾和小基数弹性更大",
                "风险调整收益": "B上行空间更能覆盖执行风险",
                "下行保护优先": "B需求能见度或现金流韧性更好",
                "估值消化优先": "B高增长更能消化高倍数",
                "近端催化优先": "B产品/订单催化更密集",
                "价格确认/动量": "B价格确认和资金偏好更强",
                "激进短线": "B高beta和AI关注度更适合进攻",
            }[strategy]
        if category in INFRA_CATS or ticker in ELECTRICAL_POWER_ADJACENT or ticker in FACILITY_INDUSTRIAL_ADJACENT:
            return {
                "NTM兑现优先": "B订单/backlog和交付链更清楚",
                "右尾弹性优先": "B电力/冷却/工程右尾更直接",
                "风险调整收益": "B增长和估值组合更优",
                "下行保护优先": "B订单粘性或利润稳定性更强",
                "估值消化优先": "B用订单利润消化估值更容易",
                "近端催化优先": "B订单/产能/财报催化更近",
                "价格确认/动量": "B价格趋势更强",
                "激进短线": "B电气化或工业AI交易弹性更强",
            }[strategy]
        if category == "封测_检测_计量_光罩" or ticker in SEMI_TEST_ADJACENT:
            return {
                "NTM兑现优先": "B半导体测试兑现链更直接",
                "右尾弹性优先": "B封测/检测右尾更大",
                "风险调整收益": "B周期上行赔率更好",
                "下行保护优先": "B估值或资产质量更稳",
                "估值消化优先": "B复苏利润更能消化估值",
                "近端催化优先": "B半导体周期催化更近",
                "价格确认/动量": "B价格确认更强",
                "激进短线": "B半导体beta更适合短线",
            }[strategy]
        return {
            "NTM兑现优先": "B未来12个月兑现证据更直接",
            "右尾弹性优先": "B极端情景收入弹性更大",
            "风险调整收益": "B上行和下行组合更好",
            "下行保护优先": "B资产质量或估值缓冲更强",
            "估值消化优先": "B当前估值更容易被业绩消化",
            "近端催化优先": "B未来两个季度催化更明确",
            "价格确认/动量": "B价格行为更强",
            "激进短线": "B短线波动和关注度更适合进攻",
        }[strategy]

    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    return {
        "NTM兑现优先": "NTM证据差距有限",
        "右尾弹性优先": "右尾证据互有强弱",
        "风险调整收益": "赔率和风险接近",
        "下行保护优先": "防守证据接近",
        "估值消化优先": "估值消化差距不大",
        "近端催化优先": "近端催化强度接近",
        "价格确认/动量": "价格确认差距有限",
        "激进短线": "短线弹性差距有限",
    }[strategy]


def label_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    at = a.get("tiers", {}).get(strategy, "资料不足")
    bt = b.get("tiers", {}).get(strategy, "资料不足")
    if "资料不足" in (at, bt):
        return "中性"
    diff = a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0)
    tier_gap = tier_value(at) - tier_value(bt)
    abs_diff = abs(diff)
    if abs_diff < 4:
        return "中性"
    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 25, 13, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 23, 11, 4
    else:
        strong_cut, suggest_cut, micro_cut = 19, 9, 4
    if diff > 0:
        if tier_gap >= 2 and abs_diff >= strong_cut:
            return "强烈建议投A"
        if tier_gap >= 1 and abs_diff >= suggest_cut:
            return "建议投A"
        if abs_diff >= micro_cut:
            return "微倾向投A"
    else:
        if tier_gap <= -2 and abs_diff >= strong_cut:
            return "强烈建议投B"
        if tier_gap <= -1 and abs_diff >= suggest_cut:
            return "建议投B"
        if abs_diff >= micro_cut:
            return "微倾向投B"
    return "中性"


def cell_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    label = label_for(strategy, a, b, rel)
    diff = a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0)
    winner = "A" if "投A" in label else "B" if "投B" in label else "中性"
    return f"{label}：{reason_for(strategy, winner, b, rel, diff)}"


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in row_obj[strategy])
    b_count = sum(1 for strategy in STRATS if "投B" in row_obj[strategy])
    neutral = 8 - a_count - b_count
    return a_count, b_count, neutral


def final_choice(row_obj: dict, a: dict, b: dict) -> str:
    weights = {
        "NTM兑现优先": 1.15,
        "风险调整收益": 1.15,
        "估值消化优先": 1.05,
        "下行保护优先": 0.95,
        "右尾弹性优先": 0.85,
        "近端催化优先": 0.80,
        "价格确认/动量": 0.45,
        "激进短线": 0.45,
    }
    label_score = {
        "强烈建议投A": 2.0,
        "建议投A": 1.35,
        "微倾向投A": 0.55,
        "中性": 0.0,
        "微倾向投B": -0.55,
        "建议投B": -1.35,
        "强烈建议投B": -2.0,
    }
    score = 0.0
    for strategy in STRATS:
        label = base.tag_in_cell(row_obj[strategy])
        score += weights[strategy] * label_score.get(label, 0.0)
    if score == 0:
        score = a.get("scores", {}).get("风险调整收益", 0) - b.get("scores", {}).get("风险调整收益", 0)
    return "A" if score >= 0 else "B"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["下行保护优先"] > 18:
            return "FTV 的自由现金流、低IV和工业/医疗底盘提供更强下行保护。"
        if diffs["风险调整收益"] > 10:
            return "FTV 的经营质量、现金流和反证强度更均衡，B 的上行不足以覆盖风险。"
        if diffs["估值消化优先"] > 10:
            return "FTV 估值不便宜但有中个位数增长和现金流支撑，消化难度低于对手。"
        return "FTV 在稳健兑现、现金流和风险控制上略胜，对手缺少更硬收入化证据。"

    if diffs["右尾弹性优先"] < -18:
        return f"{b['ticker']} 的增长右尾和重定价弹性明显大于 FTV。"
    if diffs["NTM兑现优先"] < -14:
        return f"{b['ticker']} 的 NTM 订单、收入或利润兑现链条更短。"
    if diffs["近端催化优先"] < -14:
        return f"{b['ticker']} 的未来两个季度订单、产品或财报催化更密集。"
    if diffs["估值消化优先"] < -12:
        return f"{b['ticker']} 当前估值更容易被未来业绩消化。"
    if diffs["价格确认/动量"] < -14:
        return f"{b['ticker']} 的价格确认和资金偏好强于 FTV。"
    return f"{b['ticker']} 在该资金配置口径下的增长质量、催化或估值组合更优。"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong = [s for s in STRATS if tier_value(a.get("tiers", {}).get(s)) > tier_value(b.get("tiers", {}).get(s))]
    b_strong = [s for s in STRATS if tier_value(a.get("tiers", {}).get(s)) < tier_value(b.get("tiers", {}).get(s))]
    close = [s for s in STRATS if tier_value(a.get("tiers", {}).get(s)) == tier_value(b.get("tiers", {}).get(s))]
    parts = []
    if a_strong:
        parts.append("A强:" + "、".join(a_strong[:3]))
    if b_strong:
        parts.append("B强:" + "、".join(b_strong[:3]))
    if close:
        parts.append("接近:" + "、".join(close[:2]))
    return "；".join(parts) if parts else "档位接近"


def build_comparisons(companies: dict[str, dict]) -> list[dict]:
    a = companies[TARGET]
    rows = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        row_obj = {
            "ticker": ticker,
            "name": b["name"],
            "classification": category_short(str(b.get("category", ""))),
            "relationship": rel,
            "grade_diff": grade_diff_summary(a, b),
        }
        for strategy in STRATS:
            row_obj[strategy] = cell_for(strategy, a, b, rel)
        ac, bc, nc = direction_counts(row_obj)
        row_obj["majority"] = f"A {ac} / B {bc} / 中性 {nc}"
        row_obj["ac"] = ac
        row_obj["bc"] = bc
        row_obj["nc"] = nc
        choice = final_choice(row_obj, a, b)
        row_obj["final_choice"] = choice
        row_obj["key_reason"] = key_reason(a, b, row_obj, choice)
        rows.append(row_obj)

    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return sorted(rows, key=lambda item: (rel_order.get(item["relationship"], 9), item["ticker"]))


def strongest(rows: list[dict], final: str, limit: int = 45) -> list[dict]:
    selected = [row for row in rows if row["final_choice"] == final]
    if final == "B":
        selected.sort(key=lambda row: (row["bc"] - row["ac"], row["bc"], -row["nc"]), reverse=True)
    else:
        selected.sort(key=lambda row: (row["ac"] - row["bc"], row["ac"], -row["nc"]), reverse=True)
    return selected[:limit]


def render_report(companies: dict[str, dict], comparisons: list[dict]) -> str:
    a = companies[TARGET]
    latest_dates = sorted({company["date"] for company in companies.values() if company.get("date")})
    date_range = f"{latest_dates[0]} 至 {latest_dates[-1]}" if latest_dates else "缺失"
    missing_fin = sorted([ticker for ticker, company in companies.items() if not company.get("fin")])
    fin = a.get("fin", {})
    mom2 = a.get("mom2", {})
    mom1 = a.get("mom1", {})
    soxx = a.get("soxx", {})

    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {fmt_iv(fin.get('call_iv'))}，"
        f"Put IV {fmt_iv(fin.get('put_iv'))}；2026-06-03 过去两周 {fmt_pct(mom2.get('mom2w'))}，"
        f"过去一月 {fmt_pct(mom1.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    stats: dict[str, Counter] = {strategy: Counter() for strategy in STRATS}
    for row_obj in comparisons:
        for strategy in STRATS:
            stats[strategy][base.tag_in_cell(row_obj[strategy])] += 1
    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy], reverse=True)[:2]
    a_worst = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy])[:2]
    strong_b = strongest(comparisons, "B", 45)
    strong_a = strongest(comparisons, "A", 45)
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = len(comparisons) - final_a

    product_names = []
    for product in a.get("products", [])[:6]:
        if product:
            product_names.append(str(product[0]).split("：")[0])
    file_list = "；".join([f"{ticker}:{Path(companies[ticker]['path']).name}" for ticker in sorted(companies)])

    support = {
        "NTM兑现优先": (
            "中上但非顶档",
            "2026Q1持续经营收入10.694亿美元、核心增长5.3%；IOS/AHS分部收入和利润已披露；FY2026调整EPS 2.90-3.00美元",
            "未披露backlog/RPO/book-to-bill，AI/DC增量不能替代分部级正常增长",
        ),
        "右尾弹性优先": (
            "偏弱到中位",
            "Fluke、Fluke Networks、设施资产软件和安全/EHSQ可受AI数据中心commissioning、布线验收和O&M复杂度带动",
            "当前没有AI/DC客户订单、项目金额或收入确认时间表；Ralliant高端测试业务已排除",
        ),
        "风险调整收益": (
            "中上",
            "IOS高利润、recurring软件/服务属性和TTM FCF约9.537亿美元支撑基本面质量",
            "估值不是深度低估，收入增速低于AI主链，毛利率同比下降显示成本压力",
        ),
        "下行保护优先": (
            "强势档",
            "自由现金流质量强、业务分散、医疗流程/AHS稳定，Call IV 44.6%低于多数高beta AI标的",
            "SOXX压力窗口累计-30.60%，并非低回撤公用事业型防守资产",
        ),
        "估值消化优先": (
            "中上",
            "Forward PE 19.15、P/S 4.44与中个位数增长和现金流质量大致匹配",
            "若只兑现基准中个位数增长，估值消化速度慢于高增长AI主链和部分低估值工业公司",
        ),
        "近端催化优先": (
            "偏中性",
            "后续季度可验证IOS/AHS核心增长、毛利率、FCF、Fluke/Accruent数据中心客户线索和Ralliant边界",
            "缺少明确大额订单、认证、产能或客户项目节点，催化密度低于订单驱动型公司",
        ),
        "价格确认/动量": (
            "偏弱",
            "2026-06-03两周和一月均+2.66%，价格未明显破位",
            "相对项目内高动量AI链条较弱，2026-06-22金融快照的关注度和IV也不突出",
        ),
        "激进短线": (
            "弱势档",
            "若出现AI/DC设施软件或现场测试订单披露，可有事件交易弹性",
            "短线beta、右尾叙事、价格爆发力和IV吸引力均弱于AI主链/电气设备/核能小票",
        ),
    }

    lines: list[str] = []
    lines.append("# FTV 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{REPORT_DATE}")
    lines.append(f"公司 A：FTV / {TARGET_NAME}")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(comparisons)}")
    lines.append(f"公司评估文件日期范围：{date_range}")
    lines.append("日度数据日期：2026-06-22 金融数据；2026-06-03 区间涨跌；2026-06-04 SOXX 压力窗口")
    lines.append("")
    lines.append("> 口径说明：本报告只使用公司评估、公司调研、行业调研和金融资料等上游资料；未读取、引用或继承 `特征量化/`、公司排序结果、备份目录或临时结果。每一行是 FTV 与一家项目内公司 B 的二选一判断。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.append(f"- A 最占优的投资思路：`{'`、`'.join(a_best)}`。FTV 的相对优势来自自由现金流、业务分散、IOS高利润仪器/软件服务和医疗流程稳定性。")
    lines.append(f"- A 最吃亏的投资思路：`{'`、`'.join(a_worst)}`。FTV 不是AI主链高beta标的，缺少可量化AI/DC订单、backlog、客户项目和明确收入确认时间表。")
    lines.append("- A 最适合的投资者画像：偏稳健、重视现金流、估值消化和压力窗口韧性，同时愿意把AI数据中心暴露只当作小额加分项的配置者。")
    lines.append("- A 最不适合的投资者画像：追求最高收入增速、非线性右尾、近端订单催化、强价格动量或激进短线弹性的进攻型资金。")
    lines.append("- 多数思路下最强反方公司：" + "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]]) + "。")
    lines.append(f"- 如果只追求更高增长、更好公司，A 的总体位置：FTV 是高质量但偏低beta的工业/医疗/设施软件组合，不是项目内增长冠军；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家。")
    lines.append("- 后续最重要跟踪数据：IOS/AHS核心收入增长、毛利率和调整EBITDA margin、FCF conversion、是否披露AI/DC客户订单/RPO/backlog、Fluke/Fluke Networks现场测试项目、Accruent/eMaint/ServiceChannel/Gordian大型设施客户、AHS更新周期和Ralliant分拆后费用吸收。")
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | FTV |")
    lines.append(f"| 公司名称 | {TARGET_NAME} |")
    lines.append(f"| 产业链分类 | {a.get('category', '机电_冷却_工程_水处理_边缘工业AI')} |")
    lines.append(f"| 重要产品/业务线 | {'；'.join(product_names)} |")
    lines.append(f"| NTM 基准收入 | {a.get('base_rev') or '43.5-45.0 亿美元'} |")
    lines.append(f"| 乐观/极度乐观收入 | 乐观：{a.get('bull_rev')}；极度乐观：{a.get('extreme_rev')} |")
    lines.append(f"| 利润和现金流结论 | 基准经营利润率：{a.get('base_margin')}；利润/EBITDA：{a.get('base_profit')}；现金流：{a.get('base_cash')} |")
    lines.append("| 最大传导瓶颈 | AI数据中心需求到FTV可确认收入之间缺少客户项目、订单、RPO/backlog和交付时间表；Ralliant分拆后高端高速测试、电网监测和高功率电源机会不再归入FTV。 |")
    lines.append("| 最大反证 | 2026Q1毛利率同比下降，AHS利润率低于IOS；设施软件受hyperscaler自建、系统集成商和实施周期约束；AI/DC工具在客户capex中占比小。 |")
    lines.append("| 近端催化剂 | IOS/AHS季度核心增长、毛利率修复、Fluke/Fluke Networks现场测试订单、Accruent/ServiceChannel设施软件客户、AHS医院更新周期和FCF conversion。 |")
    lines.append(f"| 日度数据 | {daily_snapshot} |")
    lines.append("")
    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append("| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for strategy in STRATS:
        tier = a.get("tiers", {}).get(strategy, "资料不足")
        position = f"{support[strategy][0]}；评分排名 {a.get('ranks', {}).get(strategy)}/{a.get('rank_total', {}).get(strategy)}"
        lines.append(f"| {strategy} | {tier} | {position} | {support[strategy][1]} | {support[strategy][2]} |")
    lines.append("")
    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | 只在测试测量、工业仪器和高端检测业务有较强重叠时使用，优先看产品代际、客户、订单、利润率、估值和收入兑现。 | KEYS、TDY | 同业证据权重最高；若一方有更硬订单/客户/产品代际，可以给建议或强烈建议。 |")
    lines.append("| 相邻替代 | 同属工业设施、机电、冷却、工程、电气设备、半导体测试或AI基础设施工具链资金篮子，但产品不直接竞争。 | DHR、TMO、JCI、DOV、TT、VRT、ETN、CEG、AEHR、TER | 默认比较增长质量、订单可见度、估值消化和现金流，不因赛道更热自动胜出。 |")
    lines.append("| 上下游 | B 是云/IDC/服务器/网络/AI主链需求端或资本开支链，FTV 只是其设施测试、资产软件、安全和维护工具的供应侧。 | MSFT、AMZN、GOOGL、EQIX、DLR、DELL、SMCI、ANET、CIEN、COHR | 降低产品指标硬比，重点看谁捕获利润池、谁的收入确认链更短、谁的估值风险更可控。 |")
    lines.append("| 跨赛道 | 半导体材料、前道设备、软件平台、能源化工等与FTV业务差异大，但作为资金配置替代仍比较。 | NVDA、ASML、TSM、LIN、APD、CDNS 等 | 默认降低结论力度，只有增长质量、估值消化、风险收益或右尾明显拉开时给建议/强烈建议。 |")
    lines.append("")
    lines.append("## 5. 全项目逐行投资思路决策表")
    lines.append("")
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    lines.append(table_row(headers))
    lines.append(table_row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for idx, row_obj in enumerate(comparisons, 1):
        values = [
            idx,
            f"{row_obj['ticker']} / {row_obj['name']}",
            row_obj["classification"],
            row_obj["relationship"],
            row_obj["grade_diff"],
        ] + [row_obj[strategy] for strategy in STRATS] + [
            row_obj["majority"],
            row_obj["final_choice"],
            row_obj["key_reason"],
        ]
        lines.append(table_row(values))
    lines.append("")
    lines.append("## 6. 投资思路统计")
    lines.append("")
    lines.append("| 投资思路 | 强烈建议投A | 建议投A | 微倾向投A | 中性 | 微倾向投B | 建议投B | 强烈建议投B | A侧合计 | B侧合计 |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for strategy in STRATS:
        c = stats[strategy]
        a_total = c["强烈建议投A"] + c["建议投A"] + c["微倾向投A"]
        b_total = c["微倾向投B"] + c["建议投B"] + c["强烈建议投B"]
        lines.append(
            f"| {strategy} | {c['强烈建议投A']} | {c['建议投A']} | {c['微倾向投A']} | {c['中性']} | "
            f"{c['微倾向投B']} | {c['建议投B']} | {c['强烈建议投B']} | {a_total} | {b_total} |"
        )
    lines.append("")
    lines.append("## 7. 多数思路下 B 明显强于 A 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | B 胜出的主要投资思路 | 为什么 B 更值得投 | A 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for idx, row_obj in enumerate(strong_b, 1):
        wins = [strategy for strategy in STRATS if "投B" in row_obj[strategy]]
        catchup = "FTV 需要披露可量化AI/DC订单、RPO/backlog、客户项目和更高IOS organic增长，并维持FCF和毛利率修复。"
        if row_obj["relationship"] == "跨赛道":
            catchup = "FTV 需要证明其增长和利润扩张能接近该跨赛道标的，或用更强现金流/估值缓冲抵消右尾差距。"
        lines.append(f"| {idx} | {row_obj['ticker']} / {row_obj['name']} | {'、'.join(wins[:5])} | {row_obj['key_reason']} | {catchup} |")
    lines.append("")
    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for idx, row_obj in enumerate(strong_a, 1):
        wins = [strategy for strategy in STRATS if "投A" in row_obj[strategy]]
        catchup = "B 需要拿出更清晰的NTM收入/利润兑现、订单或客户合同，并证明估值和现金流能承受压力窗口。"
        lines.append(f"| {idx} | {row_obj['ticker']} / {row_obj['name']} | {'、'.join(wins[:5])} | {row_obj['key_reason']} | {catchup} |")
    lines.append("")
    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。")
    lines.append(f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告，同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。")
    lines.append(f"- 公司全集最新正式评估文件清单：{file_list}")
    lines.append(f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家，缺失日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}。")
    lines.append("- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。")
    lines.append("- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。")
    lines.append("- 其他主要来源：`公司调研/公司索引.md`、`公司调研/机电_冷却_工程_水处理_边缘工业AI/FTV_Fortive_Corporation_公司调研_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_DCIM、能控与AI工厂数字孪生_2026-06-10.md`、`行业调研/晶圆制造_设备_材料_测试/行业调研_高速互连与光学验证测试_2026-06-11.md`、`行业调研/AI园区电力_机电_冷却/行业调研_数据中心土建、MEP与预制化交付_2026-06-10.md`。")
    lines.append(f"- FTV 日度数据快照：{daily_snapshot}")
    lines.append("- 生成脚本：`scripts/generate_ftv_company_comparison.py`。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    score_companies(companies)
    comparisons = build_comparisons(companies)
    report = render_report(companies, comparisons)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(report, encoding="utf-8")
    a = companies[TARGET]
    print(json.dumps({
        "target": TARGET,
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "ftv_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
        "ftv_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
        "size": OUT_PATH.stat().st_size,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
