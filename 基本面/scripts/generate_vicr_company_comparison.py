from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_txn_company_comparison as framework


TARGET = "VICR"
TARGET_NAME = "Vicor Corporation"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "VICR_逐家公司投资思路对比_2026-06-23.md"

STRATS = framework.STRATS
TAG_ORDER = framework.TAG_ORDER
TIER_VAL = framework.TIER_VAL
HIGH_GROWTH_CATS = framework.HIGH_GROWTH_CATS
INFRA_CATS = framework.INFRA_CATS


DIRECT_POWER_PEERS = {
    "ADI",
    "AEIS",
    "AOSL",
    "DIOD",
    "IFNNY",
    "LFUS",
    "MCHP",
    "MPWR",
    "MRAAY",
    "NVTS",
    "ON",
    "POWI",
    "STM",
    "TTDKY",
    "TXN",
    "VSH",
    "WOLF",
}

ADJACENT_POWER_INFRA = {
    "ABBNY",
    "ATKR",
    "BE",
    "ENS",
    "ENPH",
    "ETN",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "MIELY",
    "NVT",
    "POWL",
    "PSIX",
    "ST",
}

DATA_CENTER_FACILITY = {
    "AAON",
    "CARR",
    "CEG",
    "DKILY",
    "EME",
    "FIX",
    "JCI",
    "MOD",
    "MYRG",
    "PWR",
    "TT",
    "VRT",
    "VST",
}

AI_PLATFORM_AND_SEMI = {
    "ALAB",
    "AMD",
    "ARM",
    "AVGO",
    "CDNS",
    "INTC",
    "MRVL",
    "MTSI",
    "MXL",
    "NVDA",
    "QCOM",
    "RMBS",
    "SIMO",
    "SITM",
    "SMTC",
    "SNPS",
}

SERVER_NETWORK_STORAGE_CHAIN = {
    "AAOI",
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
    "MU",
    "NOK",
    "NTAP",
    "PENG",
    "POET",
    "PSTG",
    "SANM",
    "SMCI",
    "SNDK",
    "STX",
    "TEL",
    "VIAV",
    "VISN",
    "WDC",
}

FABS_EQUIPMENT_MATERIALS_CHAIN = {
    "ACLS",
    "ACMR",
    "AEHR",
    "AMAT",
    "AMKR",
    "ASGLY",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "AXTI",
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
    "KEYS",
    "KLAC",
    "KLIC",
    "LIN",
    "LRCX",
    "MICLF",
    "MKSI",
    "NVMI",
    "ONTO",
    "PLAB",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
    "TER",
    "TOELY",
    "TSEM",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
}

AI_CUSTOMERS_AND_OPERATORS = {
    "AMZN",
    "APLD",
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
}

CROSS_SECTOR = {
    "ADBE",
    "AJNMY",
    "ALLE",
    "AMPX",
    "APD",
    "BABA",
    "BWXT",
    "CAT",
    "CC",
    "CMI",
    "CRWD",
    "DCI",
    "DD",
    "DHR",
    "DOV",
    "DTE",
    "ECL",
    "ET",
    "ETR",
    "FCEL",
    "FTV",
    "HTHIY",
    "IESC",
    "MMM",
    "MSI",
    "MTRN",
    "NDSN",
    "OKLO",
    "PH",
    "PNR",
    "RKLB",
    "RYCEY",
    "SMR",
    "TDY",
    "TMO",
    "TSLA",
}

VICR_SCORES = {
    "NTM兑现优先": 78.0,
    "右尾弹性优先": 84.0,
    "风险调整收益": 43.0,
    "下行保护优先": 57.0,
    "估值消化优先": 44.0,
    "近端催化优先": 76.0,
    "价格确认/动量": 89.0,
    "激进短线": 96.0,
}


def patch_vicr_fields(companies: dict[str, dict]) -> None:
    vicr = companies.get(TARGET)
    if not vicr:
        return
    vicr["bear_growth"] = 36.5
    vicr["base_growth"] = 62.0
    vicr["bull_growth"] = 109.5
    vicr["extreme_growth"] = 182.0
    vicr["base_rev"] = "$620-700M"
    vicr["bull_rev"] = "$780-930M"
    vicr["extreme_rev"] = "$1.00-1.30B"
    vicr["base_profit"] = "基准经营利润 $135-205M、EBITDA $170-245M"
    vicr["base_cash"] = "自由现金流基准为正，但受扩产设备、测试能力和 working capital 占用削弱"


def score_companies(companies: dict[str, dict]) -> None:
    # Reuse the latest project-wide scoring and floors, then replace only VICR.
    framework.framework.score_companies(companies)
    patch_vicr_fields(companies)
    for strategy, score in VICR_SCORES.items():
        companies[TARGET].setdefault("scores", {})[strategy] = score
    framework.framework.recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_POWER_PEERS:
        return "直接同业"
    if ticker in ADJACENT_POWER_INFRA or ticker in DATA_CENTER_FACILITY or ticker in AI_PLATFORM_AND_SEMI:
        return "相邻替代"
    if ticker in SERVER_NETWORK_STORAGE_CHAIN or ticker in FABS_EQUIPMENT_MATERIALS_CHAIN or ticker in AI_CUSTOMERS_AND_OPERATORS:
        return "上下游"
    if ticker in CROSS_SECTOR:
        return "跨赛道"
    if category in {"配电_电源_功率器件", "电力_发电_能源_储能", "机电_冷却_工程_水处理_边缘工业AI", "AI计算芯片_EDA_IP_custom_ASIC"}:
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI网络_光互联_连接器", "云算力_IDC_AI软件平台", "晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "直接同业":
            return "AI供电同业证据互有强弱"
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，增长与估值互抵"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "VICR Q2上修、backlog和book-to-bill更硬",
            "右尾弹性优先": "VICR VPD/Power-on-Package与IP授权右尾更大",
            "风险调整收益": "VICR上行弹性可抵消部分估值风险",
            "下行保护优先": "VICR正经营利润和订单底盘略优",
            "估值消化优先": "VICR高增长路径可部分消化估值",
            "近端催化优先": "VICR Q2实际、新license和backlog验证更近",
            "价格确认/动量": "VICR两周和一月价格确认更强",
            "激进短线": "VICR高IV、AI供电和IP催化更适合进攻",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业收入或订单兑现更硬",
            "右尾弹性优先": f"{ticker}同业AI电源/功率右尾更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}同业现金流或估值缓冲更厚",
            "估值消化优先": f"{ticker}同业估值更容易消化",
            "近端催化优先": f"{ticker}同业产品或订单催化更近",
            "价格确认/动量": f"{ticker}同业价格趋势更强",
            "激进短线": f"{ticker}同业beta和关注度更适合短攻",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}订单、RPO或收入确认链更硬",
            "右尾弹性优先": f"{ticker} AI主链或瓶颈利润池更大",
            "风险调整收益": f"{ticker}上行与下行组合更优",
            "下行保护优先": f"{ticker}现金流、规模或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更适合短线",
        }[strategy]

    if rel == "相邻替代" or category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}收入、订单或交付可见度更强",
            "右尾弹性优先": f"{ticker}右尾或利润池弹性更直接",
            "风险调整收益": f"{ticker}增长与估值组合更好",
            "下行保护优先": f"{ticker}现金流或压力期表现更安全",
            "估值消化优先": f"{ticker}订单兑现更能消化估值",
            "近端催化优先": f"{ticker}近端订单或产品催化更强",
            "价格确认/动量": f"{ticker}趋势和资金偏好更强",
            "激进短线": f"{ticker}主题beta和波动更适合进攻",
        }[strategy]

    if category in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker} AI链兑现证据更硬",
            "右尾弹性优先": f"{ticker}小基数或AI收入弹性更大",
            "风险调整收益": f"{ticker}增长赔率更能覆盖风险",
            "下行保护优先": f"{ticker}需求能见度或现金流更好",
            "估值消化优先": f"{ticker}高增速更能消化估值",
            "近端催化优先": f"{ticker}产品/订单催化更密集",
            "价格确认/动量": f"{ticker}价格趋势更强",
            "激进短线": f"{ticker}高波动更适合短线进攻",
        }[strategy]

    return {
        "NTM兑现优先": f"{ticker}未来12个月兑现证据更直接",
        "右尾弹性优先": f"{ticker}极端情景上行更大",
        "风险调整收益": f"{ticker}风险调整赔率更好",
        "下行保护优先": f"{ticker}估值或资产质量更安全",
        "估值消化优先": f"{ticker}当前估值更易消化",
        "近端催化优先": f"{ticker}未来两个季度催化更明确",
        "价格确认/动量": f"{ticker}价格行为更强",
        "激进短线": f"{ticker}短线关注度和波动更强",
    }[strategy]


def cell_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    label = framework.label_for(strategy, a, b, rel)
    return f"{label}：{reason_for(strategy, label, b, rel)}"


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in row_obj[strategy])
    b_count = sum(1 for strategy in STRATS if "投B" in row_obj[strategy])
    neutral = 8 - a_count - b_count
    return a_count, b_count, neutral


def final_choice(row_obj: dict) -> str:
    return framework.final_choice(row_obj)


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    ticker = str(b["ticker"])
    if choice == "中性":
        return "VICR的AI供电/IP右尾与对手估值、防守或兑现优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice == "A":
        if diffs["NTM兑现优先"] > 10:
            return "VICR由Q2上修、3亿美元backlog和book-to-bill>2支撑NTM兑现。"
        if diffs["右尾弹性优先"] > 10:
            return "VICR的VPD/Power-on-Package、royalty/IP和小基数收入右尾更大。"
        if diffs["近端催化优先"] > 10:
            return "VICR未来1-2季可用Q2实际、新OEM license、backlog和产品mix连续验证。"
        if diffs["价格确认/动量"] > 10:
            return "VICR近期价格确认和IV显示资金对AI供电右尾已有验证。"
        return "VICR在增长兑现、右尾弹性和近端催化之间的组合略优。"

    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、资产质量或压力期韧性明显强于VICR。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}的业绩增速或估值组合比VICR更容易消化。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量、估值压力和反证组合优于VICR。"
    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的订单/RPO/backlog或收入兑现比VICR更硬。"
    if diffs["右尾弹性优先"] < -16:
        return f"{ticker}的AI主链、小基数或电力设备右尾明显大于VICR。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}的价格确认和短线资金偏好明显强于VICR。"
    return f"{ticker}在多数投资思路下比VICR更符合项目内资金配置目标。"


def build_comparisons(companies: dict[str, dict]) -> list[dict]:
    a = companies[TARGET]
    rows = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        row_obj = {
            "ticker": ticker,
            "name": b["name"],
            "classification": framework.base.category_short(str(b.get("category", ""))),
            "relationship": rel,
            "grade_diff": framework.grade_diff_summary(a, b),
        }
        for strategy in STRATS:
            row_obj[strategy] = cell_for(strategy, a, b, rel)
        ac, bc, nc = direction_counts(row_obj)
        row_obj["majority"] = f"A {ac} / B {bc} / 中性 {nc}"
        row_obj["ac"] = ac
        row_obj["bc"] = bc
        row_obj["nc"] = nc
        row_obj["final_choice"] = final_choice(row_obj)
        row_obj["key_reason"] = key_reason(a, b, row_obj, row_obj["final_choice"])
        rows.append(row_obj)
    return sorted(rows, key=framework.comparison_sort_key)


def fmt_num(value, decimals: int = 2) -> str:
    return framework.fmt_num(value, decimals)


def fmt_b(value) -> str:
    return framework.fmt_b(value)


def fmt_pct(value) -> str:
    return framework.fmt_pct(value)


def majority_rows(rows: list[dict], final: str, limit: int = 45) -> list[dict]:
    selected = [row for row in rows if row["final_choice"] == final]
    if final == "B":
        selected.sort(key=lambda x: (x["bc"] - x["ac"], x["bc"], -x["nc"]), reverse=True)
    else:
        selected.sort(key=lambda x: (x["ac"] - x["bc"], x["ac"], -x["nc"]), reverse=True)
    return selected[:limit]


def render_report(companies: dict[str, dict], comparisons: list[dict]) -> str:
    a = companies[TARGET]
    latest_dates = sorted({company["date"] for company in companies.values() if company.get("date")})
    date_range = f"{latest_dates[0]} 至 {latest_dates[-1]}" if latest_dates else "缺失"
    missing_fin = sorted([ticker for ticker, company in companies.items() if not company.get("fin")])
    missing_price = sorted([ticker for ticker, company in companies.items() if not company.get("fin", {}).get("price")])
    fin = a.get("fin", {})
    m2w = a.get("mom2", {})
    m1m = a.get("mom1", {})
    soxx = a.get("soxx", {})
    daily_snapshot = (
        f"2026-06-23 最新价格 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {fmt_num(fin.get('call_iv'), 1)}%，"
        f"Put IV {fmt_num(fin.get('put_iv'), 1)}%；过去两周 {fmt_pct(m2w.get('mom2w'))}，"
        f"过去1个月 {fmt_pct(m1m.get('mom1m'))}；三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}。"
    )

    stats: dict[str, Counter] = {strategy: Counter() for strategy in STRATS}
    for row_obj in comparisons:
        for strategy in STRATS:
            stats[strategy][framework.tag_in_cell(row_obj[strategy])] += 1

    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b = majority_rows(comparisons, "B", 45)
    strong_a = majority_rows(comparisons, "A", 45)
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "B")
    final_neutral = len(comparisons) - final_a - final_b
    strong_b_names = "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]]) or "无"

    support = {
        "NTM兑现优先": (
            "A档",
            "2026Q1收入113.0M、同比+20.2%；Q2 revenue guidance上修至142M；Q1 backlog约300.6M、同比+75%、环比+70%、book-to-bill>2，NTM基准收入620-700M。",
            "产品级客户和VPD收入拆分不透明，backlog转收入仍受CHiP fab测试/良率、客户验收、第二供应和license持续性约束。",
        ),
        "右尾弹性优先": (
            "A档",
            "VPD/Power-on-Package、NBM/48V、royalty/IP和800VDC远期期权使极度乐观收入可达1.00-1.30B，且高毛利产品/授权可放大利润。",
            "极度乐观依赖2-3个高端AI XPU平台导入、IP集中授权和first fab高利用；800VDC当前不能进入NTM基准。",
        ),
        "风险调整收益": (
            "C档",
            "基准毛利率54%-58%、经营利润率22%-29%，收入增速可观；但风险收益主要来自高右尾而非安全垫。",
            "2026-06-23 Forward PE约58.95、P/S约35.52、EV/EBITDA约203.13，估值已经要求VPD/IP持续兑现，客户集中和授权波动放大反证。",
        ),
        "下行保护优先": (
            "C档",
            "Q1已盈利、gross margin 55.2%、backlog和royalty提供底盘，SOXX三段压力窗口累计-53.05%不算最差。",
            "高估值、高IV、产品集中、royalty时点波动、扩产和working capital占用使压力期防守弱于公用事业、大型平台和低估值现金流公司。",
        ),
        "估值消化优先": (
            "C档",
            "若NTM基准收入620-700M、经营利润135-205M兑现，能解释部分高倍数；乐观情景可快速降低销售倍数压力。",
            "P/S约35.52和Forward PE约58.95已经内含乐观预期，若Q2/Q3或backlog回落，估值消化会迅速失败。",
        ),
        "近端催化优先": (
            "A档",
            "Q2实际收入是否接近/超过142M、product/royalty split、backlog/book-to-bill、新OEM license、lead customer和Gen4/Gen5 VPD表述都在1-2季可验证。",
            "催化质量取决于新增license是否持续、VPD客户是否多元化，以及first fab利用率是否不被良率和field support成本侵蚀。",
        ),
        "价格确认/动量": (
            "A档",
            "2026-06-23过去两周+18.00%、过去1个月+24.82%，价格已经明显验证AI供电/IP右尾，且IV维持高位。",
            "涨幅后短线可能透支；若Q2实际、Q3指引或授权持续性低于预期，动量会反向放大估值回撤。",
        ),
        "激进短线": (
            "A档",
            "Call IV约109.2%、Put IV约106.1%，叠加VPD/AI近负载供电、新OEM license、ITC/IP和backlog催化，短线进攻属性强。",
            "高波动也意味着反证杀伤大；相比亏损小盘/核能/NeoCloud，VICR仍需要真实收入确认配合。",
        ),
    }

    product_names = [
        "VPD / Power-on-Package / current multiplier",
        "NBM / 48V-to-12V / FPA bus conversion",
        "Royalty/IP licensing",
        "Brick Products / ATE / semicap / A&D",
        "BCM / HVDC-to-48V / 800VDC bus conversion",
    ]

    lines: list[str] = [
        "# VICR 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：VICR / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：2026-06-23（价格/估值/IV、过去两周/过去1个月区间涨跌、SOXX三段压力窗口均为该日期。）",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 VICR vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。VICR 的优势集中在Q2指引上修、3亿美元级backlog、book-to-bill>2、VPD/Power-on-Package和royalty/IP的高毛利右尾，以及2026-06-23前两周和一个月的价格确认。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是估值已非常高、客户/产品级收入拆分不足、royalty持续性与license时点有波动，且扩产、良率、field support和working capital会削弱下行保护。",
        "- A 最适合的投资者画像：愿意为AI近负载高电流供电、VPD/IP授权和小基数高毛利放量支付高估值的进攻型成长资金；更适合右尾、近端催化、动量和激进短线，而不是纯防守或低估值策略。",
        "- A 最不适合的投资者画像：优先买低估值、稳定现金流、公用事业/大型平台防守，或要求客户名、订单、产品级收入和授权合同全部透明的资金；这类资金会更偏向NVDA/AVGO/MSFT/META/ETN/VRT/CEG/GEV/ABB等更成熟或更确定的标的。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常在AI主链收入、现金流/下行保护、估值消化、订单/RPO或电力基础设施确定性上压过VICR。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：VICR 是项目内高右尾、高动量但风险调整和估值消化存在明显约束的AI电源链标的，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它能压过大量缺右尾、缺近端催化或价格弱的公司，但面对顶级AI主链、大型云平台、电力设备和低估值现金流公司时必须按投资思路拆开。",
        "- 后续最重要跟踪数据：Q2 2026 actual revenue、product/royalty split、gross margin、backlog、book-to-bill、Advanced/Brick mix；lead computing customer、Gen4/Gen5 VPD、alternate source、second fab的管理层表述；新增OEM/hyperscaler license；ITC/exclusion order；OCP/NVIDIA/Rubin/Kyber/800VDC公开架构是否出现Vicor具体design-in。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        framework.base.row(["项目", "内容"]),
        framework.base.row(["---", "---"]),
        framework.base.row(["股票代号", "VICR"]),
        framework.base.row(["公司名称", TARGET_NAME]),
        framework.base.row(["产业链分类", a.get("category", "配电_电源_功率器件")]),
        framework.base.row(["重要产品/业务线", "；".join(product_names)]),
        framework.base.row(["NTM 基准收入", a.get("base_rev") or "$620-700M"]),
        framework.base.row(["乐观/极度乐观收入", f"{a.get('bull_rev') or '$780-930M'} / {a.get('extreme_rev') or '$1.00-1.30B'}"]),
        framework.base.row(["利润和现金流结论", "基准经营利润 $135-205M、EBITDA $170-245M；基准毛利率54%-58%、经营利润率22%-29%；自由现金流基准为正但受扩产设备、测试能力和working capital占用削弱。"]),
        framework.base.row(["最大传导瓶颈", "从高性能计算和AI供电需求到Vicor可确认收入的中间环节：客户命名、量产设计导入、第二供应、CHiP fab测试/良率、backlog转收入周期和royalty合同确认。"]),
        framework.base.row(["最大反证", "Q2 actual或Q3 guide低于142M路径；backlog从300M明显回落；royalty新license只是一次性低持续；VPD lead customer延迟或客户转向MPS/Infineon/TI/ADI方案；CHiP fab设备、测试、良率或field reliability出问题。"]),
        framework.base.row(["近端催化剂", "Q2实际收入、product/royalty split、gross margin、backlog、book-to-bill、新OEM license、lead computing customer和Gen4/Gen5 VPD表述、ITC/IP进展。"]),
        framework.base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        framework.base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        framework.base.row(["---", "---", "---", "---", "---"]),
    ]

    for strategy in STRATS:
        tier = a.get("tiers", {}).get(strategy, "资料不足")
        rank = a.get("ranks", {}).get(strategy)
        total = a.get("rank_total", {}).get(strategy) or len(companies)
        position = f"第 {rank}/{total}，{support[strategy][0]}" if rank else support[strategy][0]
        lines.append(framework.base.row([strategy, tier, position, support[strategy][1], support[strategy][2]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        framework.base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        framework.base.row(["---", "---", "---", "---"]),
        framework.base.row(["直接同业", "与VICR在高密度电源模块、AI server供电、功率器件、模拟/电源管理、48V/800V架构或IP/模块替代关系上重叠；优先比较客户socket、产品代际、订单/backlog、毛利率、license和同业估值。", "MPWR、TXN、ADI、ON、IFNNY、POWI、AEIS、NVTS、AOSL、WOLF", "判断力度最高；同档或相邻档时，若对手在订单、估值或现金流上明显更强，可压过VICR的右尾。"]),
        framework.base.row(["相邻替代", "同属AI半导体、电力设备、配电/冷却或数据中心设施资金篮子，但产品不直接替代。", "NVDA、AVGO、MRVL、ALAB、ETN、HUBB、VRT、NVT、GEV、BE", "重点回答资金只能买一个时，谁的增长质量、估值消化、近端催化和风险调整更好。"]),
        framework.base.row(["上下游", "B位于VICR需求链上下游，如GPU/ASIC、服务器、光互联、云厂、晶圆制造、封测、设备或材料。", "MSFT、AMZN、GOOGL、META、DELL、ANET、MU、TSM、ASML、AMAT、ENTG", "不把下游capex或上游设备收入直接等同VICR收入，重点看利润池位置、议价权、客户平台节奏和收入确认链条。"]),
        framework.base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "TMO、DHR、LIN、CAT、RKLB、CRWD、ADBE", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
        framework.base.row(["序号", "公司B", "公司B分类", "可比关系", "档位差摘要", *STRATS, "多数思路方向", "最终更值得投", "最关键理由"]),
        framework.base.row(["---:", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(comparisons, start=1):
        lines.append(
            framework.base.row(
                [
                    index,
                    f"{row_obj['ticker']} / {row_obj['name']}",
                    row_obj["classification"],
                    row_obj["relationship"],
                    row_obj["grade_diff"],
                    *[row_obj[strategy] for strategy in STRATS],
                    row_obj["majority"],
                    "VICR" if row_obj["final_choice"] == "A" else row_obj["ticker"] if row_obj["final_choice"] == "B" else "中性",
                    row_obj["key_reason"],
                ]
            )
        )

    lines += [
        "",
        "## 6. 投资思路统计",
        "",
        framework.base.row(["投资思路", *TAG_ORDER, "A侧合计", "B侧合计"]),
        framework.base.row(["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]),
    ]
    for strategy in STRATS:
        c = stats[strategy]
        lines.append(framework.base.row([strategy, *[c[tag] for tag in TAG_ORDER], a_side[strategy], b_side[strategy]]))

    lines += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        framework.base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        framework.base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(strong_b, start=1):
        wins = [strategy for strategy in STRATS if "投B" in row_obj[strategy]]
        need = "VICR需要披露更硬的VPD客户/订单、持续性royalty、Q2/Q3超预期、backlog不回落，并证明高估值能被利润和现金流兑现消化。"
        if row_obj["relationship"] == "直接同业":
            need = "VICR需要在AI供电同业中证明VPD socket、license、毛利率和backlog转收入强于B，且估值没有过度透支。"
        elif row_obj["relationship"] == "上下游":
            need = "VICR需要证明云厂/AI主链capex能明确落到自己的VPD、NBM、royalty和高毛利产品收入，而不是只停留在行业TAM。"
        lines.append(framework.base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], need]))

    lines += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        framework.base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        framework.base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(strong_a, start=1):
        wins = [strategy for strategy in STRATS if "投A" in row_obj[strategy]]
        catchup = "B需要拿出更硬的NTM订单/利润兑现、右尾收入化、估值消化证据或价格确认，才能压过VICR的AI供电/IP催化。"
        if "下行保护优先" in wins:
            catchup = "B需要把防守或估值优势转成更高增长和近端催化，否则难以压过VICR的右尾和价格确认。"
        lines.append(framework.base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], catchup]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/配电_电源_功率器件/VICR_Vicor_Corporation_公司调研_2026-06-12.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未使用备份、临时结果、现成排序或下游量化结论。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-23.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家；缺少日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}；价格缺失或不可用公司为：{('、'.join(missing_price) if missing_price else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-23.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-23.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI园区电力_机电_冷却/行业调研_机柜级供电与服务器电源架构_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_中压直流、800VDC与固态变压器_2026-06-10.md`、`行业调研/AI园区电力_机电_冷却/行业调研_功率半导体与高压保护器件_2026-06-10.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- VICR 日度数据快照：{daily_snapshot}",
        "- 自动化脚本：`scripts/generate_vicr_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对VICR的Q2上修、backlog、book-to-bill、VPD/Power-on-Package、royalty/IP、800V远期期权、高估值、IV、区间涨跌和SOXX压力窗口做目标公司校准后建档；未读取下游量化目录、现成排序结论、临时结果、备份结论或既有公司对比成品。",
        "",
        "### 公司全集最新正式评估文件清单",
        "",
        framework.base.row(["股票代号", "公司名称", "评估日期", "正式评估文件"]),
        framework.base.row(["---", "---", "---", "---"]),
    ]
    for ticker in sorted(companies):
        company = companies[ticker]
        lines.append(framework.base.row([ticker, company["name"], company["date"], f"`分析报告/公司评估/结果/{Path(company['path']).name}`"]))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    framework.base.TARGET = TARGET
    companies = framework.base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 VICR 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    a = companies[TARGET]
    print(
        json.dumps(
            {
                "target": TARGET,
                "out": str(OUT_PATH),
                "companies": len(companies),
                "comparisons": len(comparisons),
                "vicr_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "vicr_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "vicr_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
