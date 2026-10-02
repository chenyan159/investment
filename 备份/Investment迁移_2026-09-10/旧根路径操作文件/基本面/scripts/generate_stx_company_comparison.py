from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_ndsn_company_comparison as framework


TARGET = "STX"
TARGET_NAME = "Seagate Technology"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "STX_逐家公司投资思路对比_2026-06-23.md"

base = framework.base
STRATS = framework.STRATS
TAG_ORDER = framework.TAG_ORDER
HIGH_GROWTH_CATS = framework.HIGH_GROWTH_CATS
INFRA_CATS = framework.INFRA_CATS


DIRECT_STORAGE_PEERS = {
    "WDC",
    "SNDK",
    "MU",
    "NTAP",
    "PSTG",
    "SIMO",
    "RMBS",
    "MRAM",
}

STORAGE_SYSTEMS_AND_EMS = {
    "CLS",
    "DELL",
    "FLEX",
    "FN",
    "HPE",
    "IBM",
    "JBL",
    "NTNX",
    "PENG",
    "SANM",
    "SMCI",
}

CLOUD_AND_IDC_CUSTOMERS = {
    "ADBE",
    "AMZN",
    "APLD",
    "BABA",
    "CRWD",
    "CRWV",
    "DLR",
    "EQIX",
    "GOOGL",
    "IREN",
    "META",
    "MSFT",
    "NBIS",
    "ORCL",
}

AI_COMPUTE_NETWORK_CHAIN = {
    "AAOI",
    "ADI",
    "ALAB",
    "AMD",
    "ANET",
    "APH",
    "ARM",
    "AVGO",
    "BDC",
    "BELFB",
    "CDNS",
    "CIEN",
    "COHR",
    "CRDO",
    "CSCO",
    "GLW",
    "INTC",
    "LITE",
    "LWLG",
    "MCHP",
    "MRVL",
    "MTSI",
    "MXL",
    "NOK",
    "NVDA",
    "ON",
    "POET",
    "QCOM",
    "SITM",
    "SMTC",
    "SNPS",
    "STM",
    "TEL",
    "TXN",
    "VIAV",
    "VISN",
}

SEMICAP_AND_MANUFACTURING = {
    "ACLS",
    "ACMR",
    "AEHR",
    "AEIS",
    "AMAT",
    "AMKR",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ASX",
    "ATEYY",
    "BESIY",
    "CAMT",
    "COHU",
    "DSCSY",
    "FORM",
    "GFS",
    "ICHR",
    "IMOS",
    "KEYS",
    "KLAC",
    "KLIC",
    "LRCX",
    "MICLF",
    "MKSI",
    "NVMI",
    "ONTO",
    "PLAB",
    "TER",
    "TOELY",
    "TSEM",
    "TSM",
    "UCTT",
    "UMC",
    "VECO",
}

MATERIAL_AND_COMPONENT_CHAIN = {
    "AJNMY",
    "APD",
    "ASGLY",
    "AXTI",
    "CC",
    "DD",
    "DHR",
    "DKILY",
    "ECL",
    "ENTG",
    "HOCPY",
    "LIN",
    "MMM",
    "MRAAY",
    "MTRN",
    "NDSN",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
    "TDK",
    "TTDKY",
}


STX_SCORES = {
    # STX is a high-quality AI storage capacity bottleneck name with hard
    # FY2026Q3/Q4 revenue evidence, Data Center mix, nearline EB and allocation
    # into CY2027. The calibration deliberately penalizes the valuation and
    # pressure-window drawdown: it is not a low-volatility defensive compounder.
    "NTM兑现优先": 83.0,
    "右尾弹性优先": 78.0,
    "风险调整收益": 54.0,
    "下行保护优先": 51.0,
    "估值消化优先": 49.0,
    "近端催化优先": 74.0,
    "价格确认/动量": 80.0,
    "激进短线": 94.0,
}


DIRECT_PEER_SCORE_OVERRIDES = {
    # The inherited scoring framework is broad and can under-read storage-cycle
    # peer evidence when a report's strongest facts sit in RPO, guide and NBM
    # language. These overrides keep STX's direct storage rows anchored to the
    # latest formal company-evaluation files rather than generic category priors.
    "SNDK": {
        "NTM兑现优先": 90.0,
        "右尾弹性优先": 92.0,
        "风险调整收益": 60.0,
        "下行保护优先": 60.0,
        "估值消化优先": 70.0,
        "近端催化优先": 72.0,
        "价格确认/动量": 96.0,
        "激进短线": 98.0,
    },
    "WDC": {
        "NTM兑现优先": 84.0,
        "右尾弹性优先": 76.0,
        "风险调整收益": 52.0,
        "下行保护优先": 55.0,
        "估值消化优先": 48.0,
        "近端催化优先": 68.0,
        "价格确认/动量": 92.0,
        "激进短线": 92.0,
    },
}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target
    framework.apply_global_floors(companies)
    for ticker, scores in DIRECT_PEER_SCORE_OVERRIDES.items():
        if ticker not in companies:
            continue
        peer_scores = companies[ticker].setdefault("scores", {})
        for strategy, score in scores.items():
            peer_scores[strategy] = score  # type: ignore[index]
    target = companies[TARGET]
    for strategy, score in STX_SCORES.items():
        target.setdefault("scores", {})[strategy] = score  # type: ignore[index]
    framework.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    if ticker in DIRECT_STORAGE_PEERS:
        return "直接同业"
    if ticker in STORAGE_SYSTEMS_AND_EMS or category == "AI服务器_存储_EMS":
        return "相邻替代"
    if ticker in CLOUD_AND_IDC_CUSTOMERS or ticker in AI_COMPUTE_NETWORK_CHAIN or ticker in SEMICAP_AND_MANUFACTURING:
        return "上下游"
    if ticker in MATERIAL_AND_COMPONENT_CHAIN:
        return "上下游"
    if category in {"云算力_IDC_AI软件平台", "AI计算芯片_EDA_IP_custom_ASIC", "AI网络_光互联_连接器", "晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    if category in HIGH_GROWTH_CATS:
        return "上下游"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict[str, object], diff: float) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    rel = relationship(company)

    if winner == "中性":
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，证据互有强弱"

    if winner == "A":
        return {
            "NTM兑现优先": "A有Q4指引、DC收入和CY2027产能分配",
            "右尾弹性优先": "A有Mozaic 4+和AI冷温对象存储右尾",
            "风险调整收益": "A高FCF和订单可见度覆盖部分高估值",
            "下行保护优先": "A有FCF、长约和高毛利缓冲",
            "估值消化优先": "A可用NTM利润和FCF消化估值",
            "近端催化优先": "A有Q4/FY2027指引和Mozaic客户扩展",
            "价格确认/动量": "A价格已确认AI存储供需重估",
            "激进短线": "A高IV叠加HAMR/AI存储交易弹性",
        }[strat]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}存储同业收入或订单更硬",
            "右尾弹性优先": f"{ticker}的SSD/HBM/软件右尾更大",
            "风险调整收益": f"{ticker}同业增长、估值或现金流组合更优",
            "下行保护优先": f"{ticker}现金流、净现金或压力期更稳",
            "估值消化优先": f"{ticker}利润弹性更能消化估值",
            "近端催化优先": f"{ticker}财报/订单/产品催化更直接",
            "价格确认/动量": f"{ticker}价格趋势确认更强",
            "激进短线": f"{ticker}存储周期beta和关注度更高",
        }[strat]

    if ticker in STORAGE_SYSTEMS_AND_EMS:
        return {
            "NTM兑现优先": f"{ticker}服务器/存储系统订单兑现更近",
            "右尾弹性优先": f"{ticker}的AI系统出货右尾更直接",
            "风险调整收益": f"{ticker}增长和估值组合更好",
            "下行保护优先": f"{ticker}估值或客户项目缓冲更强",
            "估值消化优先": f"{ticker}低倍数或订单更能消化估值",
            "近端催化优先": f"{ticker}服务器/系统催化更明确",
            "价格确认/动量": f"{ticker}价格确认更强",
            "激进短线": f"{ticker}的AI服务器短线弹性更强",
        }[strat]

    if ticker in CLOUD_AND_IDC_CUSTOMERS:
        return {
            "NTM兑现优先": f"{ticker}云/平台收入兑现更稳",
            "右尾弹性优先": f"{ticker}AI云或平台右尾更大",
            "风险调整收益": f"{ticker}规模、现金流和客户粘性更强",
            "下行保护优先": f"{ticker}现金流和资产质量更稳",
            "估值消化优先": f"{ticker}利润留存更能支撑估值",
            "近端催化优先": f"{ticker}云订单或AI产品催化更近",
            "价格确认/动量": f"{ticker}价格趋势确认更强",
            "激进短线": f"{ticker}市场关注或波动更集中",
        }[strat]

    if category in HIGH_GROWTH_CATS or ticker in AI_COMPUTE_NETWORK_CHAIN:
        return {
            "NTM兑现优先": f"{ticker}直接AI主链兑现更短链",
            "右尾弹性优先": f"{ticker}直接AI右尾和小基数更大",
            "风险调整收益": f"{ticker}上行空间更能覆盖风险",
            "下行保护优先": f"{ticker}需求能见度或现金流更好",
            "估值消化优先": f"{ticker}高增长更能覆盖估值",
            "近端催化优先": f"{ticker}产品/订单催化更密集",
            "价格确认/动量": f"{ticker}资金确认和趋势更强",
            "激进短线": f"{ticker}高beta叙事更适合进攻",
        }[strat]

    if category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}电力/机电backlog兑现更清楚",
            "右尾弹性优先": f"{ticker}的AI基础设施瓶颈右尾更直接",
            "风险调整收益": f"{ticker}订单和现金流赔率更好",
            "下行保护优先": f"{ticker}防御属性或订单粘性更强",
            "估值消化优先": f"{ticker}用订单兑现消化估值更容易",
            "近端催化优先": f"{ticker}订单/产能/项目催化更近",
            "价格确认/动量": f"{ticker}价格趋势更强",
            "激进短线": f"{ticker}的AI电力/冷却beta更强",
        }[strat]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}需求链收入表证据更硬",
            "右尾弹性优先": f"{ticker}利润池或需求池右尾更直接",
            "风险调整收益": f"{ticker}利润捕获或上行更优",
            "下行保护优先": f"{ticker}需求/现金流韧性更好",
            "估值消化优先": f"{ticker}增长与估值匹配更好",
            "近端催化优先": f"{ticker}客户/产能催化更清楚",
            "价格确认/动量": f"{ticker}资金确认更强",
            "激进短线": f"{ticker}短线叙事弹性更强",
        }[strat]

    return {
        "NTM兑现优先": f"{ticker}经营兑现更清楚",
        "右尾弹性优先": f"{ticker}右尾弹性更大",
        "风险调整收益": f"{ticker}风险调整后赔率更优",
        "下行保护优先": f"{ticker}压力期更安全",
        "估值消化优先": f"{ticker}估值消化更容易",
        "近端催化优先": f"{ticker}近端催化更明确",
        "价格确认/动量": f"{ticker}价格确认更强",
        "激进短线": f"{ticker}短线进攻属性更强",
    }[strat]


def key_reason(a: dict[str, object], b: dict[str, object], choice: str) -> str:
    diffs = {
        strat: float(a.get("scores", {}).get(strat, 0)) - float(b.get("scores", {}).get(strat, 0))  # type: ignore[union-attr]
        for strat in STRATS
    }
    if choice == "A":
        if diffs["NTM兑现优先"] > 12:
            return "STX的Q4指引、Data Center收入、nearline EB和CY2027产能分配使NTM兑现更硬。"
        if diffs["右尾弹性优先"] > 14:
            return "STX的Mozaic 4+、HAMR和AI冷温对象存储右尾比B更可收入化。"
        if diffs["近端催化优先"] > 12:
            return "STX有FY2027合同、Mozaic客户扩展、Q4指引和高容量盘mix可在近端验证。"
        if diffs["价格确认/动量"] > 12:
            return "STX价格已明显确认AI存储供需重估，且有基本面同步支撑。"
        return "STX在AI存储容量层兑现、FCF和HAMR路线之间更均衡。"
    if diffs["估值消化优先"] < -14:
        return f"{b['ticker']}估值和利润弹性更好，STX的高P/S和高forward PE削弱赔率。"
    if diffs["下行保护优先"] < -14:
        return f"{b['ticker']}现金流、防御性或压力期表现明显优于STX。"
    if diffs["右尾弹性优先"] < -18:
        return f"{b['ticker']}的直接AI收入、小基数或平台型右尾明显强于STX。"
    if diffs["NTM兑现优先"] < -14:
        return f"{b['ticker']}的订单/RPO/backlog或收入确认证据比STX更硬。"
    if diffs["价格确认/动量"] < -14:
        return f"{b['ticker']}价格确认和短线资金偏好明显强于STX。"
    return f"{b['ticker']}在多数投资思路下比STX更符合项目内资金配置目标。"


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
        key=lambda x: (int(x["bc"]) - int(x["ac"]), x["b"]["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (int(x["ac"]) - int(x["bc"]), a["scores"]["NTM兑现优先"] - x["b"]["scores"]["NTM兑现优先"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if int(x["bc"]) >= 5 and int(x["bc"]) - int(x["ac"]) >= 3][:55]
    strong_a_rows = [x for x in strong_a if int(x["ac"]) >= 5 and int(x["ac"]) - int(x["bc"]) >= 3][:55]
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
    close_0603 = mom2.get("latest_close")
    post_interval = "缺失"
    if fin.get("price") is not None and close_0603:
        post_interval = fmt_pct((float(fin["price"]) / float(close_0603) - 1) * 100)  # type: ignore[index]

    product_names = [
        "Data Center nearline HDD + systems",
        "Mozaic 3+ 30/32/36TB HAMR",
        "Mozaic 4+ 40/44TB HAMR",
        "Legacy high-capacity PMR/ePMR/SMR nearline",
        "Exos systems / CORVAULT / JBOD",
        "Edge IoT / NAS / surveillance / consumer",
        "Mozaic 5 / 50TB 与 100TB roadmap",
    ]

    support = {
        "NTM兑现优先": (
            "FY2026Q3收入`$3.112B`、Data Center `$2.500B`占80%、Q4指引`$3.45B +/- $0.10B`、nearline `175EB`、capacity几乎分配至CY2027",
            "产品级Mozaic收入未单列，Q4/FY2027仍需交付、验收、应收和HAMR良率验证",
        ),
        "右尾弹性优先": (
            "Mozaic 4+ 40/44TB已在两家hyperscale cloud provider production，AI checkpoint、数据湖、日志和长期留存推高冷温容量需求",
            "极度乐观要求更多CSP qualification、44TB良率/可靠性、客户不延期和WD/Toshiba不快速追赶",
        ),
        "风险调整收益": (
            "基准NTM收入`$15.0-16.0B`、non-GAAP净利润约`$4.8-5.8B`、FCF约`$4.0-5.0B`，订单可见度强",
            "2026-06-22 Forward PE `40.39`、P/S `22.28`、Call/Put IV约90%，价格已大幅反映FY2027/FY2028利润预期",
        ),
        "下行保护优先": (
            "Q3 FCF `$953M`、gross debt下降、BTO/长约和高容量盘客户粘性提供经营缓冲",
            "SOXX三段压力窗口累计`-58.72%`，高IV和存储周期属性使其不是低回撤防守资产",
        ),
        "估值消化优先": (
            "若NTM利润和FCF按基准兑现，STX可用高毛利Data Center收入逐步消化部分高估值",
            "当前Forward PE和P/S均高，估值已经要求FY2027继续高增长和Mozaic 4+顺利扩展",
        ),
        "近端催化优先": (
            "FY2026Q4收入/EPS指引、FY2027 BTO合同、Mozaic 4+客户扩展、40/44TB mix和FCF均可在1-2季验证",
            "催化双向；若指引只是正常兑现、客户扩展慢或毛利率见顶，强预期会转为反证",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周`+25.25%`、过去一月`+29.41%`，2026-06-22价格较6月初继续上涨约`{post}`".format(post=post_interval),
            "短期涨幅大且IV高，动量确认同时带来追高和事件回撤风险",
        ),
        "激进短线": (
            "Call IV `90.1%`、Put IV `90.2%`，AI存储、HAMR、Mozaic 4+和高容量HDD短缺形成短线交易弹性",
            "短线进攻高度依赖财报/指引和AI存储新闻流延续，方向错时回撤会很大",
        ),
    }

    daily_snapshot = (
        f"2026-06-22 收盘价 `{fmt_num(fin.get('price'))}` 美元，市值 `{fmt_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `{fmt_num(fin.get('ttm_pe'))}`，Forward PE `{fmt_num(fin.get('forward_pe'))}`，"
        f"P/S `{fmt_num(fin.get('ps'))}`，P/B `{fmt_num(fin.get('pb'))}`，EV/EBITDA `{fmt_num(fin.get('ev_ebitda'))}`，"
        f"Call IV `{fmt_pct(fin.get('call_iv'))}`、Put IV `{fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03 过去两周 `{fmt_pct(mom2.get('mom2w'))}`、过去一月 `{fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04 三段 SOXX 压力窗口累计 `{fmt_pct(soxx.get('soxx_cum'))}`；"
        f"从2026-06-03收盘到2026-06-22收盘约 `{post_interval}`。"
    )

    out: list[str] = [
        "# STX 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：STX / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 STX vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或项目根 `tmp/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。STX 的优势集中在 NTM兑现、价格确认/动量和激进短线：Q4指引、Data Center收入、nearline EB、CY2027 capacity allocation、Mozaic 4+和高IV共同支撑。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是高估值、高IV和SOXX压力窗口回撤，导致下行保护和估值消化明显弱于低倍数现金流、云平台、公用事业或部分存储同业。",
        "- A 最适合的投资者画像：愿意承受高波动，押注AI/cloud数据留存、nearline HDD短缺、HAMR/Mozaic路线和STX高FCF继续兑现的成长进攻型资金。",
        "- A 最不适合的投资者画像：只追求低回撤、低估值、稳定股息或不愿承受财报/指引落空风险的防守型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]])}。这些公司通常在更低估值、更强下行保护、更直接AI主链右尾或更大订单/RPO上压过STX。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：STX 对 {final_a}/{n - 1} 家公司多数思路占优，对 {final_b}/{n - 1} 家公司多数思路落后；它是项目内AI存储容量层最强标的之一，但不是全项目最便宜或最安全的资产。",
        "- 后续最重要跟踪数据：FY2026Q4收入/EPS和毛利率，FY2027收入指引，Data Center revenue、nearline EB、revenue/TB，Mozaic 4+客户数和40/44TB shipment mix，purchase order cancellation fees，库存、应收、DSO、FCF，WD/Toshiba高容量进度，QLC SSD替代速度，hyperscaler/NeoCloud CapEx和上电节奏。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "STX"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or "`$15.0-16.0B`"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a.get('bull_rev')}；极度乐观：{a.get('extreme_rev')}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a.get('base_margin')}；利润/现金流：{a.get('base_profit')}；{a.get('base_cash')}"]),
        base.row(["最大传导瓶颈", "AI/cloud数据增长能否转成hyperscaler冷温对象容量预算、30/40/44TB qualification、可交付EB和季度收入确认；Mozaic 4+良率和可靠性是核心。"]),
        base.row(["最大反证", "nearline lead time缩短、Data Center sequential growth停滞、FY2027指引弱、Mozaic 4+客户数不扩、HAMR field reliability异常、云CapEx/NeoCloud融资下修、QLC SSD更快替代warm tier。"]),
        base.row(["近端催化剂", "FY2026Q4收入/EPS和毛利率、FY2027 BTO合同、Mozaic 4+客户扩展、40/44TB shipment mix、nearline EB、FCF、WD/Toshiba高容量进展。"]),
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
        base.row(["直接同业", "与STX在HDD、NAND/eSSD、AI存储、企业存储系统、存储控制器或数据平台需求池中有明显重叠，优先比较收入兑现、订单/供应分配、产品代际、客户质量、毛利率和估值。", "WDC、SNDK、MU、NTAP、PSTG、SIMO、RMBS", "同业证据权重最高；若对手有更低估值、更强RPO/订单或更大SSD/HBM右尾，可直接在对应投资思路压过STX。"]),
        base.row(["相邻替代", "同属AI服务器、存储系统、EMS、数据中心物理基础设施或AI基础设施资金篮子，但不直接竞争HDD介质；重点比较增长质量、兑现确定性和赔率。", "DELL、HPE、SMCI、PENG、JBL、FLEX、SANM、VRT、ETN", "默认按档位差判断；若B的服务器/电力订单更硬，STX需用高FCF和存储供需稀缺抵消。"]),
        base.row(["上下游", "B位于STX需求链或供应链上下游，如云厂、AI芯片、网络、半导体制造、设备材料和关键元件；重点看利润池、议价权和收入确认。", "MSFT、AMZN、GOOGL、META、NVDA、AVGO、TSM、ASML、TDK、HOYA相关材料链", "不把下游云CapEx自动等同STX收入，也不把STX产能短缺自动等同上游/下游胜出；核心看谁能留存利润并兑现。"]),
        base.row(["跨赛道", "业务差异大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "工业、化工、生命科学、航天、软件和部分能源公司", "默认降低结论力度；若证据互有强弱，优先使用中性或微倾向。"]),
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
    for index, row_obj in enumerate(strong_b_rows, start=1):
        b = row_obj["b"]
        wins = [strat for strat in STRATS if (base.tag_in_cell(str(row_obj[strat])) or "").endswith("投B")]
        need = "需要STX证明Mozaic 4+多客户扩展、FY2027收入指引、毛利率和FCF继续超预期，并缓解高估值和高IV反证。"
        if row_obj["relationship"] == "直接同业":
            need = "需要STX在存储同业中证明HAMR/Mozaic收入、Data Center增长、FCF和估值消化强于B。"
        elif row_obj["relationship"] == "上下游":
            need = "需要STX证明自己能从云CapEx、AI芯片和数据增长中捕获更高利润，而不只是间接受益。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), row_obj["key_reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, row_obj in enumerate(strong_a_rows, start=1):
        b = row_obj["b"]
        wins = [strat for strat in STRATS if (base.tag_in_cell(str(row_obj[strat])) or "").endswith("投A")]
        need = "需要B提高NTM收入确认、订单/RPO、利润和现金流质量，或用更低估值/更强价格确认反超。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要B把更大的右尾叙事转成可确认收入和利润，并降低估值、波动或资产负债表反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), row_obj["key_reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/AI服务器_存储_EMS/STX_Seagate_Technology_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/AI服务器_存储_芯片/行业调研_HDD、对象存储与冷温数据存储_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_AI-native存储与KV Cache基础设施_2026-06-10.md`；`行业调研/AI服务器_存储_芯片/行业调研_企业级SSD与高速存储控制器_2026-06-10.md`；`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`；`行业调研/产业背景/AI产业链瓶颈与反证指标总表_2026-06-10.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`分析报告/公司排序/`、`分析报告/简单排序/`、项目根 `tmp/` 或 `特征量化/`。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研、IR、SEC、产品公告和财报来源。",
        "- 自动化脚本：`scripts/generate_stx_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用既有正式脚本的最低分校准，对STX的Q4指引、Data Center收入、nearline EB、Mozaic 4+、FCF、高估值、高IV、价格动量和SOXX压力窗口做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 STX 正式评估文件")

    framework.TARGET = TARGET
    framework.TARGET_NAME = TARGET_NAME
    framework.OUT_PATH = OUT_PATH
    framework.relationship = relationship
    framework.reason_for = reason_for
    framework.key_reason = key_reason

    score_companies(companies)
    comparisons = framework.build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8", newline="\n")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "stx_tiers": companies[TARGET]["tiers"],
        "stx_scores": {k: round(float(v), 2) for k, v in companies[TARGET]["scores"].items()},
        "stx_ranks": companies[TARGET]["ranks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
