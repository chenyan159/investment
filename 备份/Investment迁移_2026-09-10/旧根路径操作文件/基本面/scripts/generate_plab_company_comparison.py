from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_ndsn_company_comparison as framework


TARGET = "PLAB"
TARGET_NAME = "Photronics"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "PLAB_逐家公司投资思路对比_2026-06-23.md"

base = framework.base
STRATS = framework.STRATS
TAG_ORDER = framework.TAG_ORDER
HIGH_GROWTH_CATS = framework.HIGH_GROWTH_CATS
INFRA_CATS = framework.INFRA_CATS


DIRECT_MASK_PEERS = {"HOCPY"}

MASK_ECOSYSTEM_ADJACENT = {
    "MICLF",
    "SHECY",
    "ASGLY",
    "ENTG",
    "MRAAY",
    "Q",
    "ROG",
    "SOMMY",
    "SMTOY",
    "TTDKY",
    "AMAT",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ATEYY",
    "BESIY",
    "CAMT",
    "COHU",
    "FORM",
    "ICHR",
    "KEYS",
    "KLAC",
    "KLIC",
    "LRCX",
    "MKSI",
    "NDSN",
    "NVMI",
    "ONTO",
    "TDY",
    "TER",
    "TOELY",
    "UCTT",
    "VECO",
}

DOWNSTREAM_SEMI_AND_AI_DEMAND = {
    "ACLS",
    "ACMR",
    "AEHR",
    "AEIS",
    "ALAB",
    "AMD",
    "AMKR",
    "ARM",
    "ASX",
    "AVGO",
    "CDNS",
    "DIOD",
    "GFS",
    "IFNNY",
    "IMOS",
    "INTC",
    "MCHP",
    "MPWR",
    "MRAM",
    "MRVL",
    "MTSI",
    "MU",
    "MXL",
    "NVDA",
    "NVTS",
    "ON",
    "POWI",
    "QCOM",
    "RMBS",
    "SIMO",
    "SITM",
    "SMTC",
    "SNDK",
    "SNPS",
    "STM",
    "STX",
    "TSEM",
    "TSM",
    "TXN",
    "UMC",
    "VICR",
    "VSH",
    "WDC",
    "WOLF",
}

AI_SYSTEM_AND_CLOUD_DEMAND = {
    "AAOI",
    "ADBE",
    "AMZN",
    "ANET",
    "APH",
    "APLD",
    "BABA",
    "BDC",
    "BELFB",
    "CIEN",
    "CLS",
    "COHR",
    "CRDO",
    "CRWD",
    "CRWV",
    "CSCO",
    "DELL",
    "DLR",
    "EQIX",
    "FLEX",
    "FN",
    "GLW",
    "GOOGL",
    "HPE",
    "IBM",
    "IREN",
    "JBL",
    "LITE",
    "LWLG",
    "META",
    "MSFT",
    "NBIS",
    "NOK",
    "NTAP",
    "NTNX",
    "ORCL",
    "PENG",
    "POET",
    "PSTG",
    "SANM",
    "SMCI",
    "TEL",
    "VIAV",
    "VISN",
}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target
    framework.apply_global_floors(companies)

    # PLAB calibration from the formal 2026-06-12 assessment and 2026-06-22
    # daily data. The durable positives are low valuation, large net cash,
    # IC/FPD product revenue disclosure, high-end FPD strength, and small-cap
    # high-end mask optionality. The offsets are flat Q3 guidance, high-end IC
    # design-release delay, short backlog, FY2026 capex pressure, high IV, and
    # severe recent price drawdown.
    overrides = {
        "NTM兑现优先": 59.0,
        "右尾弹性优先": 63.0,
        "风险调整收益": 54.0,
        "下行保护优先": 66.0,
        "估值消化优先": 67.0,
        "近端催化优先": 59.0,
        "价格确认/动量": 21.0,
        "激进短线": 60.0,
    }
    for strat, score in overrides.items():
        companies[TARGET].setdefault("scores", {})[strat] = score  # type: ignore[index]

    framework.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_MASK_PEERS:
        return "直接同业"
    if ticker in MASK_ECOSYSTEM_ADJACENT:
        return "相邻替代"
    if ticker in DOWNSTREAM_SEMI_AND_AI_DEMAND or ticker in AI_SYSTEM_AND_CLOUD_DEMAND:
        return "上下游"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "相邻替代"
    if category in HIGH_GROWTH_CATS:
        return "上下游"
    if category in INFRA_CATS:
        return "跨赛道"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict[str, object], diff: float) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    rel = relationship(company)

    if winner == "中性":
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，证据互有强弱"

    if winner == "A":
        return {
            "NTM兑现优先": "A有分产品收入表和Q3指引硬锚",
            "右尾弹性优先": "A有高端IC/FPD和先进封装mask期权",
            "风险调整收益": "A低估值、净现金和右尾组合较均衡",
            "下行保护优先": "A净现金和低债务提供安全垫",
            "估值消化优先": "A低P/S和Forward PE更易消化",
            "近端催化优先": "A有Allen/Korea/G8.6验证节点",
            "价格确认/动量": "A低位修复但仍需确认",
            "激进短线": "A高IV和光罩AI期权可交易",
        }[strat]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业收入和订单兑现更硬",
            "右尾弹性优先": f"{ticker}高端blank/mask右尾更大",
            "风险调整收益": f"{ticker}同业赔率组合更优",
            "下行保护优先": f"{ticker}同业规模和现金流更稳",
            "估值消化优先": f"{ticker}增长质量更能消化估值",
            "近端催化优先": f"{ticker}同业产品/产能节点更清楚",
            "价格确认/动量": f"{ticker}价格确认更强",
            "激进短线": f"{ticker}同业交易弹性更强",
        }[strat]

    if rel == "相邻替代":
        return {
            "NTM兑现优先": f"{ticker}相邻设备/材料兑现更清楚",
            "右尾弹性优先": f"{ticker}相邻赛道右尾更大",
            "风险调整收益": f"{ticker}估值与反证组合更优",
            "下行保护优先": f"{ticker}现金流或压力期更稳",
            "估值消化优先": f"{ticker}业绩增长更能消化倍数",
            "近端催化优先": f"{ticker}订单/产品催化更明确",
            "价格确认/动量": f"{ticker}价格趋势确认更强",
            "激进短线": f"{ticker}短线事件弹性更高",
        }[strat]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}需求链收入确认更短链",
            "右尾弹性优先": f"{ticker}直接AI利润池右尾更大",
            "风险调整收益": f"{ticker}上行空间更能覆盖风险",
            "下行保护优先": f"{ticker}需求能见度或现金流更好",
            "估值消化优先": f"{ticker}增长与估值匹配更好",
            "近端催化优先": f"{ticker}客户/产品催化更密集",
            "价格确认/动量": f"{ticker}资金确认更充分",
            "激进短线": f"{ticker}AI主链beta更适合进攻",
        }[strat]

    if category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}项目/backlog兑现更硬",
            "右尾弹性优先": f"{ticker}AI电力/冷却右尾更直接",
            "风险调整收益": f"{ticker}订单和估值组合更好",
            "下行保护优先": f"{ticker}现金流或合同底盘更稳",
            "估值消化优先": f"{ticker}用项目兑现消化估值更清楚",
            "近端催化优先": f"{ticker}项目/订单催化更近",
            "价格确认/动量": f"{ticker}价格确认更强",
            "激进短线": f"{ticker}主题交易弹性更强",
        }[strat]

    return {
        "NTM兑现优先": f"{ticker}经营兑现证据更强",
        "右尾弹性优先": f"{ticker}右尾空间更大",
        "风险调整收益": f"{ticker}风险收益组合更优",
        "下行保护优先": f"{ticker}下行缓冲更强",
        "估值消化优先": f"{ticker}估值更容易消化",
        "近端催化优先": f"{ticker}近端催化更明确",
        "价格确认/动量": f"{ticker}价格确认更强",
        "激进短线": f"{ticker}短线弹性更强",
    }[strat]


def key_reason(a: dict[str, object], b: dict[str, object], choice: str) -> str:
    diffs = {
        strat: a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0)  # type: ignore[union-attr,operator]
        for strat in STRATS
    }
    ticker = str(b["ticker"])
    rel = relationship(b)
    if choice == "A":
        if diffs["估值消化优先"] > 12:
            return "PLAB低P/S、低EV/EBITDA和净现金使估值消化优于对手。"
        if diffs["下行保护优先"] > 12:
            return "PLAB现金与短投厚、债务极低，能承受扩产和周期波动。"
        if diffs["右尾弹性优先"] > 12:
            return "PLAB高端IC/FPD、8nm以下能力和先进封装mask提供小盘右尾。"
        if diffs["NTM兑现优先"] > 10:
            return "PLAB有FY2026 Q2分产品收入表和Q3收入指引作为兑现锚。"
        return "PLAB在低估值、净现金和高端光罩期权之间更均衡。"

    if rel == "直接同业":
        return f"{ticker}在光罩/blank同业中增长、利润率、订单或规模质量强于PLAB。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker}的订单、RPO、backlog或收入确认链比PLAB更硬。"
    if diffs["右尾弹性优先"] < -16:
        return f"{ticker}的直接AI主链或小基数右尾明显大于PLAB的间接光罩暴露。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}增长、估值和下行组合优于PLAB。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}价格确认和短线资金偏好明显强于PLAB。"
    if diffs["近端催化优先"] < -14:
        return f"{ticker}近端订单、产品或财报重定价节点比PLAB更明确。"
    return f"{ticker}在多数投资思路下比PLAB更符合项目内资金配置目标。"


def fmt_num(value: object, decimals: int = 2) -> str:
    return framework.fmt_num(value, decimals)


def fmt_b(value: object) -> str:
    return framework.fmt_b(value)


def fmt_pct(value: object) -> str:
    return framework.fmt_pct(value)


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(company_dates)} 至 {max(company_dates)}"
    stats = {strat: Counter() for strat in STRATS}
    for comparison in comparisons:
        for strat in STRATS:
            stats[strat][base.tag_in_cell(str(comparison[strat]))] += 1
    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b = sorted(
        comparisons,
        key=lambda x: (
            int(x["bc"]) - int(x["ac"]),
            x["b"]["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            int(x["ac"]) - int(x["bc"]),
            a["scores"]["估值消化优先"] + a["scores"]["下行保护优先"] - x["b"]["scores"]["估值消化优先"] - x["b"]["scores"]["下行保护优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if int(x["bc"]) >= 5 and int(x["bc"]) - int(x["ac"]) >= 3][:45]
    strong_a_rows = [x for x in strong_a if int(x["ac"]) >= 5 and int(x["ac"]) - int(x["bc"]) >= 3][:45]
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "B")
    missing_fin = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker].get("fin") or not companies[ticker]["fin"].get("price")  # type: ignore[union-attr]
    ]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]
    fin = a.get("fin", {})
    mom2 = a.get("mom2", {})
    mom1 = a.get("mom1", {})
    soxx = a.get("soxx", {})

    product_names = [
        "高端IC photomasks，28nm及以下",
        "主流IC photomasks，28nm以上",
        "高端FPD/AMOLED/G8.6 photomasks",
        "主流FPD/成熟LCD photomasks",
        "Allen/Boise/Korea 8nm及以下与multi-beam能力",
        "先进封装/RDL/interposer/硅光mask",
    ]

    support = {
        "NTM兑现优先": (
            "FY2026 Q2收入2.099亿美元，Q3指引2.07-2.15亿美元；IC/FPD和高端/主流拆分均有A类收入锚",
            "基准NTM收入仅8.75-9.25亿美元、同比+2%到+7%；高端IC Q2环比-21%，订单能见度短",
        ),
        "右尾弹性优先": (
            "乐观/极度乐观收入9.60-10.40亿/10.80-12.00亿美元；高端IC、G8.6 AMOLED、8nm以下和先进封装mask提供小盘右尾",
            "AI/HPC只是间接设计迭代暴露，未披露客户、订单或AI收入；极度乐观需多环节同时突破",
        ),
        "风险调整收益": (
            "2026-06-22 Forward PE 16.82、P/S 2.33、EV/EBITDA 6.57，现金与短投6.377亿美元、债务约390万美元",
            "FY2026 capex约3.30亿美元，FCF可能弱于利润；高IV和近期暴跌说明市场仍给周期折价",
        ),
        "下行保护优先": (
            "净现金和低债务是明确安全垫，主流IC/主流FPD提供收入底盘，资产负债表可承受扩产周期",
            "Call IV 75.5%、两周/一月跌幅约-35%，SOXX压力窗口累计-55.95%，短期防守属性不强",
        ),
        "估值消化优先": (
            "低P/S、低EV/EBITDA和净现金降低业绩兑现门槛；只要基准收入和20%左右OPM守住，估值不算透支",
            "估值便宜部分来自低增长和Q2 miss；若高端IC不回到6500-7000万美元/季，估值修复空间受限",
        ),
        "近端催化优先": (
            "FY2026 Q3收入/EPS、Allen qualification masks、Korea 8nm capability、G8.6 AMOLED writer和高端FPD重复订单是近端验证点",
            "Q3指引不是V型反弹；大多数催化仍是qualification/能力验证，缺少已披露量产订单和客户名",
        ),
        "价格确认/动量": (
            "2026-06-22价格34.06美元较2026-06-03的32.11美元已有低位修复，高IV显示市场关注仍在",
            "正式区间文件显示至2026-06-03过去两周-35.56%、一月-35.98%，价格趋势仍被Q2 miss破坏",
        ),
        "激进短线": (
            "75%左右近月IV、小市值、低估值和高端光罩/先进封装mask主题使其有事件交易属性",
            "短线进攻缺少价格确认和强订单催化，Q3若继续平淡，高IV会放大下行而非上行",
        ),
    }

    daily_snapshot = (
        f"2026-06-22 收盘价 `{fmt_num(fin.get('price'))}` 美元，市值 `{fmt_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `{fmt_num(fin.get('ttm_pe'))}`，Forward PE `{fmt_num(fin.get('forward_pe'))}`，"
        f"P/S `{fmt_num(fin.get('ps'))}`，P/B `{fmt_num(fin.get('pb'))}`，EV/EBITDA `{fmt_num(fin.get('ev_ebitda'))}`，"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`、Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03 过去两周 `{fmt_pct(mom2.get('mom2w'))}`、过去一月 `{fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04 三段 SOXX 压力窗口累计 `{fmt_pct(soxx.get('soxx_cum'))}`。"
    )

    out: list[str] = [
        "# PLAB 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：PLAB / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04；日度新闻最新文件日期为 2026-06-23。",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 PLAB vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。PLAB 的优势主要来自低估值、净现金、低债务、IC/FPD分产品收入锚，以及高端光罩/先进封装mask的小盘右尾；它不是AI数据中心直接BOM高增长股。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。短板是Q2高端IC下滑、Q3指引平淡、订单能见度短、近期价格破位和高IV；价格确认/动量尤其不能给高档。",
        "- A 最适合的投资者画像：愿意买低估值、净现金、半导体上游可选期权，并接受高端IC/FPD季度波动的中期逆向或事件型投资者。",
        "- A 最不适合的投资者画像：只追求AI主链直接收入、强RPO/backlog、持续价格突破、低波动防守或1-2个季度订单已经明确爆发的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]]) if strong_b_rows else '无明显集中反方'}。这些公司通常有更直接AI利润池、更硬订单/RPO、更强价格确认或更高近端催化密度。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：PLAB 对 {final_a}/{n - 1} 家公司多数思路占优，对 {final_b}/{n - 1} 家公司多数思路落后；它更像全项目低估值光罩期权和资产负债表安全垫，而不是顶层增长或动量标的。",
        "- 后续最重要跟踪数据：FY2026 Q3收入是否高于2.15亿美元、Q4指引、高端IC是否回到6500-7000万美元/季、Allen qualification masks反馈、Korea 8nm客户认证、高端FPD/G8.6 AMOLED重复订单、IC lead time是否从1-3周拉长、FY2026 capex是否维持约3.30亿美元、毛利率是否回到35%+、FCF是否转正。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "PLAB"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "8.75-9.25亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "AI/HPC设计迭代必须转成客户design release、mask set订单、qualification、工具可用、交付验收和收入确认；FY2026 Q2已验证高端IC会因design release延迟而下滑。"]),
        base.row(["最大反证", "Q2高端IC环比-21%、Q3指引2.07-2.15亿美元且OPM 18%-20%、backlog通常只有1-3周；若高端IC无法恢复，AI叙事不能进入公司收入表。"]),
        base.row(["近端催化剂", "FY2026 Q3/Q4分产品收入、Allen qualification masks、Korea 8nm extension、G8.6 AMOLED writer、高端FPD重复订单、毛利率回到35%+和FCF改善。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strat in STRATS:
        out.append(base.row([strat, a["tiers"][strat], rank_text[strat], support[strat][0], support[strat][1]]))  # type: ignore[index]

    out += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与PLAB在高端光罩、mask blanks、FPD photomask或先进mask需求池高度重叠，优先比较产品收入、客户认证、产能、利润率、订单可见度和估值消化。", "HOCPY", "同业证据权重最高；若B有更硬EUV/blank增长、产能或利润率证据，PLAB低估值也不能直接胜出。"]),
        base.row(["相邻替代", "同属光罩生态、晶圆制造设备、检测量测、先进封装设备或半导体材料资金篮子，但产品不完全相同。", "MICLF、SHECY、ASML、KLAC、ONTO、NVMI、CAMT、TER、ENTG", "回答资金只能买一个时谁的收入兑现、利润质量、估值消化和近端订单更好；若只是相邻景气而非可确认收入，结论降档。"]),
        base.row(["上下游", "B位于PLAB需求链的上游/下游，如AI芯片、foundry/IDM、memory、先进封装、服务器、光互联、云厂和数据中心需求端。", "NVDA、AMD、AVGO、MU、TSM、AMKR、ASX、MSFT、AMZN、DELL、ANET", "不把下游AI收入规模直接等同PLAB机会；核心看谁能捕获利润、谁的订单/RPO/backlog和估值消化更清楚。"]),
        base.row(["跨赛道", "电力、冷却、工业、软件、能源和其他业务差异大的公司，作为项目内资金配置替代比较风险调整收益、估值消化、下行保护和催化可见度。", "VRT、ETN、CEG、GEV、DHR、RKLB、CRWD", "默认降低结论力度；档位接近时优先中性或微倾向，只有增长质量或风险收益明显拉开才给建议/强烈建议。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]

    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    out.append(base.row(headers))
    out.append(base.row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for index, row_obj in enumerate(comparisons, start=1):
        b = row_obj["b"]
        out.append(
            base.row(
                [
                    index,
                    base.short_name(b),  # type: ignore[arg-type]
                    row_obj["classification"],
                    row_obj["relationship"],
                    row_obj["grade_diff"],
                    *[row_obj[strat] for strat in STRATS],
                    row_obj["majority"],
                    row_obj["final_choice"],
                    row_obj["key_reason"],
                ]
            )
        )

    out += ["", "## 6. 投资思路统计", "", base.row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), base.row(["---"] + ["---:"] * 9)]
    for strat in STRATS:
        out.append(base.row([strat] + [stats[strat][tag] for tag in TAG_ORDER] + [a_side[strat], b_side[strat]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    if strong_b_rows:
        for index, row_obj in enumerate(strong_b_rows, start=1):
            b = row_obj["b"]
            wins = [strat for strat in STRATS if (base.tag_in_cell(str(row_obj[strat])) or "").endswith("投B")]
            need = "需要PLAB披露更硬的高端IC/FPD订单、客户qualification、lead time拉长、收入上修、毛利率恢复和FCF改善，证明低估值不是价值陷阱。"
            if row_obj["relationship"] == "直接同业":
                need = "需要PLAB在高端光罩同业中证明merchant mask收入、客户资格、产能利用率、毛利率和估值消化强于B。"
            elif row_obj["relationship"] == "上下游":
                need = "需要PLAB证明自己能从下游AI芯片/HBM/云厂CapEx中捕获足够利润，而不只是间接受益。"
            out.append(base.row([index, base.short_name(b), "、".join(wins), row_obj["key_reason"], need]))  # type: ignore[arg-type]
    else:
        out.append(base.row([1, "无", "无", "没有公司在多数思路下显著压过PLAB", "继续跟踪高端IC、FPD、订单和价格确认"]))

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    if strong_a_rows:
        for index, row_obj in enumerate(strong_a_rows, start=1):
            b = row_obj["b"]
            wins = [strat for strat in STRATS if (base.tag_in_cell(str(row_obj[strat])) or "").endswith("投A")]
            need = "需要B拿出同等强度的收入确认、订单/backlog、现金流、估值消化或更清晰的近端催化。"
            if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
                need = "需要B把右尾叙事转成可确认收入/利润，并降低估值和波动反证。"
            out.append(base.row([index, base.short_name(b), "、".join(wins), row_obj["key_reason"], need]))  # type: ignore[arg-type]
    else:
        out.append(base.row([1, "无", "无", "PLAB没有在多数思路下明显压过其他公司", "需等待估值、现金流和高端光罩订单进一步确认"]))

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/封测_检测_计量_光罩/PLAB_Photronics_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/晶圆制造_设备_材料_测试/行业调研_高端光罩与先进封装掩模_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体检测量测设备_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 外部核对来源：Photronics FY2026 Q2 results（https://photronicsinc.gcs-web.com/news-releases/news-release-details/photronics-reports-second-quarter-2026-results）；Photronics Events & Presentations / FY26 Earnings Presentation（https://photronicsinc.gcs-web.com/events-presentations）；Photronics advanced FPD mask writer announcement（https://photronicsinc.gcs-web.com/news-releases/news-release-details/photronics-receives-advanced-mask-writer-expanding-amoled）。外部核对只用于确认公司A关键财务和产品事件，不使用外部网页排序、券商评级或目标价。",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_plab_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用目标无关的最低分校准，对PLAB的Q2分产品收入、Q3指引、净现金、低债务、低估值、高端IC延迟、G8.6 AMOLED、Allen/Korea qualification、FY2026 capex、高IV和价格破位做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
        "",
        "### 公司全集最新正式评估文件清单",
        "",
        base.row(["股票代号", "公司名称", "评估日期", "正式评估文件"]),
        base.row(["---", "---", "---", "---"]),
    ]
    for ticker in sorted(companies):
        company = companies[ticker]
        out.append(base.row([ticker, company["name"], company["date"], f"`分析报告/公司评估/结果/{company['path'].name}`"]))  # type: ignore[index,union-attr]

    out.append("")
    return "\n".join(out)


def main() -> None:
    base.TARGET = TARGET
    framework.TARGET = TARGET
    framework.OUT_PATH = OUT_PATH
    framework.relationship = relationship
    framework.reason_for = reason_for
    framework.key_reason = key_reason

    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 PLAB 正式评估文件")

    score_companies(companies)
    comparisons = framework.build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "plab_tiers": companies[TARGET]["tiers"],
        "plab_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
        "plab_ranks": companies[TARGET]["ranks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
