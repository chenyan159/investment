from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_ndsn_company_comparison as framework


TARGET = "ONTO"
TARGET_NAME = "Onto Innovation"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "ONTO_逐家公司投资思路对比_2026-06-23.md"

base = framework.base
STRATS = framework.STRATS
TAG_ORDER = framework.TAG_ORDER
HIGH_GROWTH_CATS = framework.HIGH_GROWTH_CATS
INFRA_CATS = framework.INFRA_CATS


DIRECT_METROLOGY_PEERS = {"KLAC", "NVMI", "CAMT"}

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

    # ONTO calibration from the formal 2026-06-12 assessment and 2026-06-22
    # daily data. ONTO has hard near-term revenue guide, HBM VPA, Dragonfly G5
    # qualification, Semilab contribution and strong HBM/AP optionality. The
    # offsets are high valuation, very high IV, SOXX pressure-window drawdown,
    # customer qualification timing, working-capital absorption and Rigaku
    # financing/strategic-investment complexity.
    overrides = {
        "NTM兑现优先": 86.0,
        "右尾弹性优先": 89.0,
        "风险调整收益": 52.0,
        "下行保护优先": 46.0,
        "估值消化优先": 57.0,
        "近端催化优先": 88.0,
        "价格确认/动量": 82.0,
        "激进短线": 92.0,
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
            "NTM兑现优先": "A有Q2指引、HBM VPA和G5认证",
            "右尾弹性优先": "A有G5/HBM4/Semilab/Rigaku右尾",
            "风险调整收益": "A增长和订单证据抵消部分高估值",
            "下行保护优先": "A净现金和高毛利提供底盘",
            "估值消化优先": "A高增长兑现更能消化倍数",
            "近端催化优先": "A Q2/Q3 G5和Semilab验证很近",
            "价格确认/动量": "A六月价格确认和关注度更强",
            "激进短线": "A高IV叠加HBM量测更适合进攻",
        }[strat]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业收入/订单兑现更硬",
            "右尾弹性优先": f"{ticker}同业量测右尾更大",
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
        if diffs["NTM兑现优先"] > 12:
            return "ONTO有Q2指引、HBM VPA、G5 qualification和Semilab并表，NTM兑现更硬。"
        if diffs["右尾弹性优先"] > 14:
            return "ONTO的HBM4/2.5D封装检测量测、Semilab和Rigaku/X-ray右尾更大。"
        if diffs["近端催化优先"] > 12:
            return "ONTO的Q2/Q3 G5发货、AP >50%和Semilab验证窗口更近。"
        if diffs["价格确认/动量"] > 12:
            return "ONTO的六月价格确认、高IV和HBM设备关注度强于对手。"
        return "ONTO在兑现、先进封装右尾和近端催化之间更均衡。"

    if rel == "直接同业":
        return f"{ticker}在同业规模、订单、估值、现金流或压力期表现上更优。"
    if diffs["右尾弹性优先"] < -18 and str(b.get("category", "")) in HIGH_GROWTH_CATS:
        return f"{ticker}的直接AI主链右尾和利润池大于ONTO的间接设备暴露。"
    if diffs["NTM兑现优先"] < -14:
        return f"{ticker}的订单、RPO、backlog或收入确认链比ONTO更硬。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}增长与估值匹配度优于ONTO，ONTO高倍数已预支乐观。"
    if diffs["下行保护优先"] < -14:
        return f"{ticker}现金流、防御性或压力期表现明显优于ONTO。"
    if diffs["价格确认/动量"] < -14:
        return f"{ticker}价格确认和短线资金偏好明显强于ONTO。"
    return f"{ticker}在多数投资思路下比ONTO更符合项目内资金配置目标。"


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
        key=lambda x: (int(x["ac"]) - int(x["bc"]), a["scores"]["NTM兑现优先"] + a["scores"]["近端催化优先"] - x["b"]["scores"]["NTM兑现优先"] - x["b"]["scores"]["近端催化优先"]),  # type: ignore[index,operator]
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
        "Dragonfly G5/G3 + 3Di/EchoScan先进封装检测量测",
        "Atlas G6/Atlas OCD/Iris先进节点量测",
        "Semilab FAaST/CnCV/MBIR材料与表面电荷量测",
        "JetStep + Firefly panel-level packaging/glass/CPO相邻期权",
        "Discover/Ai Diffract/parts/services装机与软件",
        "Rigaku X-ray/CD-SAXS战略合作",
    ]

    support = {
        "NTM兑现优先": (
            "2026Q1收入2.919亿美元，2026Q2指引3.20-3.30亿美元，2026收入目标>13亿美元且AP增长>50%；HBM VPA超过2.40亿美元覆盖2027扩产",
            "公司不披露标准化bookings/book-to-bill和产品级backlog，G5/3Di还需按季度验收确认",
        ),
        "右尾弹性优先": (
            "Dragonfly G5/3Di承接HBM4、2.5D logic、CoWoS-like和micro-bump/RDL检测；Semilab、Rigaku和panel/glass提供多条期权",
            "极度乐观要求HBM4、CoWoS-like、Atlas/Semilab、panel/Rigaku多线同时兑现，不能只靠行业beta外推",
        ),
        "风险调整收益": (
            "NTM基准收入13.8-15.0亿美元、non-GAAP OM 28%-30%，交易前净现金和高毛利提供质量支撑",
            "2026-06-22 TTM PE 162.56、P/S 16.79、Call IV 82.9%，Rigaku交易和营运资本吸收压低赔率",
        ),
        "下行保护优先": (
            "交易前现金+短投约6.54亿美元、低经营性负债、parts/services和软件有稳定器属性",
            "SOXX压力窗口累计-61.39%，高IV、高估值、客户集中和5亿美元bridge loan使其不是防守标的",
        ),
        "估值消化优先": (
            "基准收入同比约+37%-49%、non-GAAP经营利润3.9-4.5亿美元，若Q2/H2兑现可部分消化Forward PE",
            "当前P/S 16.79、TTM PE 162.56已要求乐观路径；若G5或Semilab只落在基准下沿，倍数压力仍大",
        ),
        "近端催化优先": (
            "2026Q2实际收入、Q3指引、G5发货逐季上升、AP >50%、advanced nodes +25%、Semilab年化>1.30亿美元都在1-2季可验证",
            "缺少新增大额订单和客户名；若财报只重复qualification而无收入/订单金额，催化会被高估值吸收",
        ),
        "价格确认/动量": (
            "2026-06-22价格347.87高于6月初279.98，Call IV 82.9%显示市场关注度和短线弹性很高",
            "区间涨跌正式文件截至2026-06-03仅显示两周+6.41%、一月-4.42%，且高IV意味着拥挤回撤风险",
        ),
        "激进短线": (
            "HBM4/先进封装检测量测、高IV、G5 Q2/Q3发货和价格快速确认，适合更激进的短线进攻",
            "短线依赖乐观叙事延续；任何指引miss、客户验收慢、竞品拿单或融资成本上升都会放大波动",
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
        "# ONTO 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：ONTO / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04；日度新闻最新文件日期为 2026-06-23。",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 ONTO vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。ONTO 的优势集中在激进短线、近端催化、右尾弹性和NTM兑现：HBM VPA、Dragonfly G5 qualification、Q2指引、先进封装>50%增长目标和Semilab并表把AI芯片制造复杂度转成较硬的收入线索。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。短板是下行保护、风险调整收益和估值消化：2026-06-22的高P/S、高TTM PE、高IV、SOXX压力窗口深回撤，以及Rigaku交易后的净现金下降，都会压低防守档位。",
        "- A 最适合的投资者画像：愿意押注HBM4、2.5D/CoWoS-like、advanced packaging inspection/metrology、Semilab材料量测和Rigaku/X-ray长期期权的进攻型半导体设备投资者。",
        "- A 最不适合的投资者画像：优先买低估值、低IV、强现金流防守、完整backlog/RPO披露，或只愿意买直接AI芯片/云平台收入的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]])}。这些公司通常有更直接AI主链利润池、更硬RPO/backlog、更好估值消化、现金流防守或更强价格确认。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：ONTO 对 {final_a}/{n - 1} 家公司多数思路占优，对 {final_b}/{n - 1} 家公司多数思路落后；它是项目内半导体检测量测和先进封装设备链里的前列进攻标的，但并非下行保护或低估值消化型配置。",
        "- 后续最重要跟踪数据：2026Q2实际收入是否高于3.30亿美元、Q3指引、Dragonfly G5发货台数和客户数、HBM VPA交付节奏、advanced packaging收入增速是否维持>50%、advanced nodes memory/logic mix、Semilab季度收入和operating contribution、non-GAAP GM是否维持56%以上、DSO/库存/经营现金流、Rigaku closing和Ai Diffract/X-ray客户qualification、JetStep/Firefly panel/glass订单。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "ONTO"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "13.8-15.0亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "Dragonfly G5/3Di从qualification和VPA转为按季度可确认收入；HBM4、2.5D logic、CoWoS-like和advanced-node客户ramp节奏；precision optics、detector/stage、field service和客户recipe认证。"]),
        base.row(["最大反证", "高估值已前置乐观路径；若G5发货不及预期、AP增速下修、Camtek/KLA/Nova拿单更强、Semilab低于1.20亿美元年化或营运资本继续吸收现金，估值消化会恶化。"]),
        base.row(["近端催化剂", "2026Q2收入和Q3指引、Dragonfly G5发货/客户新增、HBM VPA交付、advanced packaging >50%、Semilab收入、GM/OM、经营现金流、Rigaku/Ai Diffract客户验证。"]),
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
        base.row(["直接同业", "与ONTO在process control、先进封装inspection/metrology、前道/后道量测和HBM良率工具需求池高度重叠，优先比较客户份额、订单/VPA/backlog、产品代际、毛利和估值。", "KLAC、NVMI、CAMT", "同业证据权重最高；若B有更硬订单/规模/估值或ONTO有更硬G5/VPA证据，可在多列给建议或强烈建议。"]),
        base.row(["相邻替代", "同属晶圆制造设备、封测/检测/计量、半导体材料或先进封装资金篮子，但产品不完全相同。", "AMAT、ASML、LRCX、TOELY、ATEYY、TER、FORM、COHU、ENTG、MKSI、Q", "回答资金只能买一个时谁的收入兑现、利润质量、估值消化和近端订单更好；相邻公司若订单更硬可提高判断力度。"]),
        base.row(["上下游", "B位于ONTO需求链或利润池上下游，如AI芯片、HBM/存储、foundry/OSAT、服务器、云厂和光互联。", "NVDA、AMD、AVGO、MU、TSM、AMKR、ASX、MSFT、AMZN、DELL、ANET", "不把下游收入规模直接等同ONTO机会；核心看谁能捕获利润、谁的订单/RPO/backlog和估值消化更清楚。"]),
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
        need = "需要ONTO披露更硬的G5发货、客户、VPA交付、产品线收入、Semilab贡献和现金流，并证明高估值可由基准而非极度乐观情景消化。"
        if row_obj["relationship"] == "直接同业":
            need = "需要ONTO在检测量测同业中证明Dragonfly G5/3Di、Atlas、Semilab订单、客户POR和收入兑现强于B。"
        elif row_obj["relationship"] == "上下游":
            need = "需要ONTO证明自己能从下游AI芯片/HBM/云厂CapEx中捕获足够利润，而不只是间接受益。"
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
        "- 公司 A 公司调研文件：`公司调研/封测_检测_计量_光罩/ONTO_Onto Innovation_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/晶圆制造_设备_材料_测试/行业调研_半导体检测量测设备_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_先进封装设备与混合键合_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_玻璃基板、TGV与玻璃检测_2026-06-11.md`；`行业调研/晶圆制造_设备_材料_测试/行业调研_HBM与存储测试设备_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 外部核对来源：Onto Innovation Q1 2026 results（https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovation-Reports-2026-First-Quarter-Results/default.aspx）；Onto Innovation Dragonfly G5 launch（https://investors.ontoinnovation.com/news/news-details/2026/Onto-Innovation-Launches-Dragonfly-G5-Inspection-System/default.aspx）。外部核对只用于确认公司A关键财务和产品事件，不使用外部网页排序、券商评级或目标价。",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_onto_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用目标无关的最低分校准，对ONTO的Q2指引、HBM VPA、Dragonfly G5 qualification、Semilab、Rigaku/X-ray期权、高估值、高IV、价格动量和SOXX压力窗口做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
        raise SystemExit("缺少 ONTO 正式评估文件")

    score_companies(companies)
    comparisons = framework.build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "onto_tiers": companies[TARGET]["tiers"],
        "onto_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
        "onto_ranks": companies[TARGET]["ranks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
