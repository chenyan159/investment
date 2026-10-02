from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_ndsn_company_comparison as framework


TARGET = "NVMI"
TARGET_NAME = "Nova Ltd"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "NVMI_逐家公司投资思路对比_2026-06-23.md"

base = framework.base
STRATS = framework.STRATS
TAG_ORDER = framework.TAG_ORDER
TIER_VAL = framework.TIER_VAL
HIGH_GROWTH_CATS = framework.HIGH_GROWTH_CATS
INFRA_CATS = framework.INFRA_CATS


DIRECT_METROLOGY_PEERS = {"KLAC", "ONTO", "CAMT"}

SEMICAP_ADJACENT = {
    "ACLS",
    "ACMR",
    "AEHR",
    "AEIS",
    "AMAT",
    "ASMIY",
    "ASML",
    "ASMVY",
    "ATEYY",
    "BESIY",
    "COHU",
    "DSCSY",
    "FORM",
    "ICHR",
    "KEYS",
    "KLIC",
    "LRCX",
    "MICLF",
    "MKSI",
    "PLAB",
    "TDY",
    "TER",
    "TMO",
    "TOELY",
    "UCTT",
    "VECO",
}

SEMI_MATERIALS = {
    "AJNMY",
    "ASGLY",
    "AXTI",
    "CC",
    "DD",
    "ENTG",
    "HOCPY",
    "LIN",
    "MRAAY",
    "MTRN",
    "Q",
    "ROG",
    "SHECY",
    "SMTOY",
    "SOMMY",
    "TTDKY",
}

SEMI_CUSTOMERS_AND_AI_DEMAND = {
    "ALAB",
    "AMD",
    "AMKR",
    "ARM",
    "ASX",
    "AVGO",
    "GFS",
    "IMOS",
    "INTC",
    "MRVL",
    "MU",
    "NVDA",
    "QCOM",
    "RMBS",
    "SNDK",
    "STX",
    "TSEM",
    "TSM",
    "UMC",
    "WDC",
}

AI_SYSTEM_AND_CLOUD_CHAIN = {
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
    "MTSI",
    "NBIS",
    "NOK",
    "NTAP",
    "NTNX",
    "ORCL",
    "PENG",
    "POET",
    "PSTG",
    "SANM",
    "SITM",
    "SMCI",
    "SMTC",
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

    # NVMI calibration from the formal 2026-06-12 assessment and 2026-06-22
    # daily data. Nova has hard near-term guide, high margin, service quality
    # and differentiated Metrion/AncoScene/Sentronics exposure. The limits are
    # no backlog/bookings/product-family disclosure, high valuation, high IV and
    # weak SOXX pressure-window behavior.
    overrides = {
        "NTM兑现优先": 80.0,
        "右尾弹性优先": 84.0,
        "风险调整收益": 50.0,
        "下行保护优先": 52.0,
        "估值消化优先": 49.0,
        "近端催化优先": 75.0,
        "价格确认/动量": 78.0,
        "激进短线": 86.0,
    }
    for strat, score in overrides.items():
        companies[TARGET].setdefault("scores", {})[strat] = score  # type: ignore[index]

    framework.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_METROLOGY_PEERS:
        return "直接同业"
    if ticker in SEMICAP_ADJACENT or category in {"晶圆制造_前道设备", "封测_检测_计量_光罩"}:
        return "相邻替代"
    if ticker in SEMI_MATERIALS or category == "半导体材料_化学品_基板":
        return "相邻替代"
    if ticker in SEMI_CUSTOMERS_AND_AI_DEMAND or ticker in AI_SYSTEM_AND_CLOUD_CHAIN:
        return "上下游"
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
            return "业务差异较大且档位接近"
        return "档位接近，证据互有强弱"

    if winner == "A":
        return {
            "NTM兑现优先": "A有Q2指引和record产品线支撑",
            "右尾弹性优先": "A有Metrion/AncoScene/HBM4右尾",
            "风险调整收益": "A利润率和现金流质量较均衡",
            "下行保护优先": "A高毛利服务和现金流提供底盘",
            "估值消化优先": "A收入利润兑现更能支撑高倍数",
            "近端催化优先": "A有Q2/Q3指引和产品线record验证",
            "价格确认/动量": "A近期价格和高IV资金确认更强",
            "激进短线": "A量测右尾和高波动更适合进攻",
        }[strat]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业订单或收入覆盖更硬",
            "右尾弹性优先": f"{ticker}同业封装/量测右尾更大",
            "风险调整收益": f"{ticker}同业估值和反证组合更优",
            "下行保护优先": f"{ticker}同业规模或现金流更稳",
            "估值消化优先": f"{ticker}同业增长更能消化估值",
            "近端催化优先": f"{ticker}同业订单/产品节点更近",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业短线弹性或关注度更高",
        }[strat]

    if rel == "相邻替代":
        return {
            "NTM兑现优先": f"{ticker}相邻设备/材料兑现更清楚",
            "右尾弹性优先": f"{ticker}相邻赛道右尾更大",
            "风险调整收益": f"{ticker}估值与反证组合更优",
            "下行保护优先": f"{ticker}现金流或估值缓冲更强",
            "估值消化优先": f"{ticker}业绩增长更能消化倍数",
            "近端催化优先": f"{ticker}近端订单/产能催化更明确",
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
            "NTM兑现优先": f"{ticker}订单/backlog兑现更硬",
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
        if diffs["右尾弹性优先"] > 14:
            return "NVMI的材料/化学/先进封装量测右尾明显强于对手。"
        if diffs["NTM兑现优先"] > 12:
            return "NVMI有Q2指引、Q1超预期和record产品线，NTM兑现更硬。"
        if diffs["近端催化优先"] > 12:
            return "NVMI的Q2/Q3指引、Metrion/AncoScene和Sentronics验证窗口更近。"
        if diffs["价格确认/动量"] > 12:
            return "NVMI近期价格确认和高IV资金关注强于对手。"
        return "NVMI在兑现、量测右尾和高毛利质量之间更均衡。"

    if rel == "直接同业":
        return f"{ticker}在同业订单、规模、估值或直接封装/量测证据上更优。"
    if diffs["右尾弹性优先"] < -18 and str(b.get("category", "")) in HIGH_GROWTH_CATS:
        return f"{ticker}的直接AI主链右尾和利润池大于NVMI的间接设备暴露。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker}的订单、RPO、backlog或收入确认链比NVMI更硬。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}增长与估值匹配度优于NVMI，NVMI高倍数已预支乐观。"
    if diffs["下行保护优先"] < -14:
        return f"{ticker}现金流、防御性或压力期表现明显优于NVMI。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}价格确认和短线资金偏好明显强于NVMI。"
    return f"{ticker}在多数投资思路下比NVMI更符合项目内资金配置目标。"


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
        key=lambda x: (int(x["ac"]) - int(x["bc"]), a["scores"]["右尾弹性优先"] - x["b"]["scores"]["右尾弹性优先"]),  # type: ignore[index,operator]
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
        "光学/尺寸/集成量测",
        "材料量测：Metrion、VeraFlex、ELIPSON",
        "化学量测：AncoScene/ancosys",
        "先进封装/后道量测：Sentronics",
        "服务/软件/recipe/数据",
    ]

    support = {
        "NTM兑现优先": (
            "2026Q1收入2.353亿美元超指引，2026Q2指引2.45-2.55亿美元；memory、Metrion、AncoScene和服务均给出record信号",
            "不披露backlog、bookings、book-to-bill和产品族收入，全年覆盖率主要由指引和管理层措辞推断",
        ),
        "右尾弹性优先": (
            "HBM4/GAA/背面供电/混合键合会提高材料、化学和后道量测强度，小基数产品线具备非线性上行",
            "极度乐观要求Metrion、AncoScene、Sentronics和集成量测多线同时成为POR，当前证据不足以进基准",
        ),
        "风险调整收益": (
            "GAAP毛利率约57.7%、经营利润率约30%，服务收入和轻资本开支支撑现金流质量",
            "2026-06-22 TTM PE 72.89、Forward PE 45.07、P/S 20.55、Call IV 64.6%，赔率被高估值压缩",
        ),
        "下行保护优先": (
            "高毛利、盈利、服务收入和正经营现金流提供基本面底盘",
            "三段SOXX压力窗口累计-70.22%，高IV、高PS和客户/地区集中使其不是防守标的",
        ),
        "估值消化优先": (
            "NTM基准收入10.5-11.2亿美元、毛利率57%-59%、经营利润率29%-32%，若Q2/Q3上修可部分消化估值",
            "当前估值已要求乐观兑现，若只落在基准下沿或产品线record不可持续，估值消化压力大",
        ),
        "近端催化优先": (
            "2026Q2实际收入、Q3指引、Metrion/AncoScene是否连续record、Sentronics占比和服务20%+增速都在1-2季可验证",
            "缺少大额订单或客户名单硬锚，催化依赖财报措辞和指引上修",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+7.29%、过去一月+7.19%，2026-06-22价格583.10高于6月初530.04，高IV显示关注度",
            "价格已较强，叠加高估值和历史压力窗口深回撤，不能把动量等同低风险",
        ),
        "激进短线": (
            "Call IV 64.6%、HBM/GAA/AP量测叙事、Q2/Q3财报验证和高端设备稀缺性提供短线进攻弹性",
            "短线回报依赖高波动和乐观叙事延续，任何指引miss、毛利率回落或订单不透明都会放大回撤",
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
        "# NVMI 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：NVMI / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04；日度新闻最新文件日期为 2026-06-23。",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 NVMI vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。NVMI 的优势集中在近端催化、NTM兑现和右尾弹性：Metrion、AncoScene、Sentronics、服务收入和Q2指引把AI芯片制造复杂度转成可跟踪的量测收入线索。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。短板是下行保护、估值消化以及与更高beta标的相比的激进短线胜率：2026-06-22的P/S、Forward PE、IV和SOXX压力窗口回撤都显示市场已经预支较多乐观。",
        "- A 最适合的投资者画像：愿意押注HBM/GAA/先进封装良率复杂度继续抬高材料/化学/后道量测价值，并能承受高估值、高IV和订单不透明的进攻型半导体设备投资者。",
        "- A 最不适合的投资者画像：优先要低估值、低回撤、清晰backlog/RPO、大型平台现金流防守或只买直接AI数据中心收入的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]])}。这些公司通常有更直接AI主链利润池、更硬订单/RPO/backlog、更好估值消化或更强下行保护。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：NVMI 对 {final_a}/{n - 1} 家公司多数思路占优，对 {final_b}/{n - 1} 家公司多数思路落后；它是项目内半导体设备链中右尾和催化较强的高质量进攻标的，但面对NVDA/AVGO/TSM/MU/ALAB/CRDO/ANET/部分AI电力与云平台公司时，综合风险收益不一定占优。",
        "- 后续最重要跟踪数据：2026Q2实际收入是否高于2.55亿美元、Q3指引、Metrion和AncoScene是否连续record、Sentronics/AP收入占比是否升向10%+、服务收入是否继续20%+、毛利率是否守住57%-59%、递延收入/RPO、应收和经营现金流、客户/地区集中、是否首次披露backlog/bookings/book-to-bill或产品族订单。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "NVMI"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "10.5-11.2亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "从HBM/GAA/先进封装需求到Nova收入，需要经过客户POR/qualification、工具交付、验收和服务附着；公司不披露backlog、bookings、B/B或产品族收入。"]),
        base.row(["最大反证", "高估值和高IV已预支乐观；客户和地区集中、出口管制、KLA/Onto/Camtek/ASML/Applied竞争、以及e-beam/内置传感/实验室抽检替代都可能压制收入和倍数。"]),
        base.row(["近端催化剂", "2026Q2实际收入和Q3指引、Metrion/AncoScene连续record、Sentronics/AP贡献、服务收入20%+、毛利率守住57%-59%、经营现金流回升、是否披露更多订单或产品线证据。"]),
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
        base.row(["直接同业", "与NVMI在半导体process control、前道/先进封装inspection/metrology、材料/化学/光学量测需求池高度重叠，优先比较客户份额、工具代际、订单、毛利和估值。", "KLAC、ONTO、CAMT", "同业证据权重最高；若B有更硬订单/规模/产品代际，可在多列压过NVMI；若NVMI材料/化学量测证据更强，可在右尾和催化列胜出。"]),
        base.row(["相邻替代", "同属晶圆制造设备、封测/检测/计量、半导体材料或先进封装资金篮子，但产品不完全相同。", "AMAT、ASML、LRCX、TOELY、ATEYY、TER、FORM、ENTG、MKSI、Q", "回答资金只能买一个时谁的收入兑现、利润质量、估值消化和近端订单更好；相邻公司若订单更硬可提高判断力度。"]),
        base.row(["上下游", "B位于NVMI需求链或利润池上下游，如AI芯片、HBM/存储、foundry/OSAT、服务器、云厂和光互联。", "NVDA、AMD、AVGO、MU、TSM、AMKR、ASX、MSFT、AMZN、DELL、ANET", "不把下游收入规模直接等同NVMI机会；核心看谁能捕获利润、谁的订单/RPO/backlog和估值消化更清楚。"]),
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
    for index, row_obj in enumerate(strong_b_rows, start=1):
        b = row_obj["b"]
        wins = [strat for strat in STRATS if (base.tag_in_cell(str(row_obj[strat])) or "").endswith("投B")]
        need = "需要NVMI披露更硬的订单/backlog/book-to-bill、连续指引上修、产品线收入和毛利率，并证明高估值可由基准业绩而非极度乐观情景消化。"
        if row_obj["relationship"] == "直接同业":
            need = "需要NVMI在检测量测同业中证明Metrion/AncoScene/Sentronics订单、客户POR和收入兑现强于B。"
        elif row_obj["relationship"] == "上下游":
            need = "需要NVMI证明自己能从下游AI芯片/HBM/云厂CapEx中捕获足够利润，而不只是间接受益。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), row_obj["key_reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, row_obj in enumerate(strong_a_rows, start=1):
        b = row_obj["b"]
        wins = [strat for strat in STRATS if (base.tag_in_cell(str(row_obj[strat])) or "").endswith("投A")]
        need = "需要B拿出同等强度的收入确认、订单/backlog、毛利率和近端催化，或显著改善估值/现金流反证。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "需要B在保持下行保护的同时补足增长右尾、价格确认和近端催化。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), row_obj["key_reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/晶圆制造_前道设备/NVMI_Nova_Ltd_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体检测量测设备_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_AI芯片前道制造设备_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_HBM与存储测试设备_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_nvmi_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用目标无关的最低分校准，对NVMI的Q2指引、Metrion/AncoScene/Sentronics、服务收入、毛利率、高估值、高IV、价格动量和SOXX压力窗口做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
    framework.TARGET_NAME = TARGET_NAME
    framework.OUT_PATH = OUT_PATH
    framework.relationship = relationship
    framework.reason_for = reason_for
    framework.key_reason = key_reason

    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 NVMI 正式评估文件")

    score_companies(companies)
    comparisons = framework.build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "nvmi_tiers": companies[TARGET]["tiers"],
        "nvmi_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
        "nvmi_ranks": companies[TARGET]["ranks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
