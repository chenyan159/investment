from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_ndsn_company_comparison as framework


TARGET = "NOK"
TARGET_NAME = "诺基亚"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "NOK_逐家公司投资思路对比_2026-06-23.md"

base = framework.base
STRATS = framework.STRATS
TAG_ORDER = framework.TAG_ORDER
TIER_VAL = framework.TIER_VAL
HIGH_GROWTH_CATS = framework.HIGH_GROWTH_CATS
INFRA_CATS = framework.INFRA_CATS

framework.TARGET = TARGET
framework.TARGET_NAME = TARGET_NAME
framework.OUT_PATH = OUT_PATH


DIRECT_NETWORK_PEERS = {"ANET", "CIEN", "CSCO", "VISN"}

OPTICAL_COMPONENT_CHAIN = {
    "AAOI",
    "APH",
    "BDC",
    "BELFB",
    "COHR",
    "CRDO",
    "GLW",
    "LITE",
    "LWLG",
    "MTSI",
    "POET",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
}

AI_DEMAND_AND_CUSTOMER_CHAIN = {
    "ADBE",
    "ALAB",
    "AMD",
    "AMZN",
    "ARM",
    "AVGO",
    "BABA",
    "CLS",
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
    "MRVL",
    "MSFT",
    "MU",
    "NBIS",
    "NTAP",
    "NTNX",
    "NVDA",
    "ORCL",
    "PENG",
    "PSTG",
    "QCOM",
    "SANM",
    "SMCI",
    "STX",
    "WDC",
}


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def recompute_tiers(companies: dict[str, dict[str, object]]) -> None:
    framework.recompute_tiers(companies)


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target
    framework.apply_global_floors(companies)

    # NOK calibration from the 2026-06-12 formal assessment and 2026-06-22
    # daily data. The positive side is AI & Cloud orders, Optical/IP guidance,
    # Infinera scale, Standards cash flow and strong recent momentum. The
    # limiting side is mature telco/RAN/Fixed exposure, high IV, elevated
    # headline valuation and unproven large AI back-end fabric share.
    overrides = {
        "NTM兑现优先": 69.0,
        "右尾弹性优先": 67.0,
        "风险调整收益": 49.0,
        "下行保护优先": 70.0,
        "估值消化优先": 48.0,
        "近端催化优先": 70.0,
        "价格确认/动量": 76.0,
        "激进短线": 82.0,
    }
    for strat, score in overrides.items():
        companies[TARGET].setdefault("scores", {})[strat] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_NETWORK_PEERS:
        return "直接同业"
    if ticker in OPTICAL_COMPONENT_CHAIN:
        return "上下游"
    if ticker in AI_DEMAND_AND_CUSTOMER_CHAIN:
        return "上下游"
    if category == "AI网络_光互联_连接器":
        return "相邻替代"
    if category in {"AI服务器_存储_EMS", "AI计算芯片_EDA_IP_custom_ASIC", "云算力_IDC_AI软件平台"}:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict[str, object], diff: float) -> str:
    ticker = str(company["ticker"])
    cat = str(company.get("category", ""))
    rel = relationship(company)

    if winner == "中性":
        if rel == "跨赛道":
            return "业务差异较大且档位接近"
        return "档位接近，需看下一季订单"

    if winner == "A":
        return {
            "NTM兑现优先": "A有AI&Cloud订单和Optical/IP指引",
            "右尾弹性优先": "A的Optical/IP与AI-RAN期权更清楚",
            "风险调整收益": "A订单、标准授权和现金流更均衡",
            "下行保护优先": "A有净现金、Standards和运营商底盘",
            "估值消化优先": "A虽贵但业绩兑现证据更硬",
            "近端催化优先": "A的AI&Cloud订单和Infinera协同更近",
            "价格确认/动量": "A近期AI网络资金确认更强",
            "激进短线": "A高IV和AI网络事件弹性更强",
        }[strat]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业收入/订单兑现更硬",
            "右尾弹性优先": f"{ticker}同业份额或产品代际右尾更大",
            "风险调整收益": f"{ticker}同业赔率组合更优",
            "下行保护优先": f"{ticker}同业现金流或防守更强",
            "估值消化优先": f"{ticker}同业增长更能消化估值",
            "近端催化优先": f"{ticker}同业客户/产品催化更直接",
            "价格确认/动量": f"{ticker}同业价格确认更强",
            "激进短线": f"{ticker}同业关注度和beta更高",
        }[strat]

    if cat in HIGH_GROWTH_CATS:
        return {
            "NTM兑现优先": f"{ticker}的AI主链兑现更短链",
            "右尾弹性优先": f"{ticker}的直接AI右尾更大",
            "风险调整收益": f"{ticker}上行空间更能覆盖风险",
            "下行保护优先": f"{ticker}需求能见度或现金流更好",
            "估值消化优先": f"{ticker}高增长更能覆盖估值",
            "近端催化优先": f"{ticker}产品/订单催化更密集",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta更适合短线进攻",
        }[strat]

    if cat in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}的电力/机电订单更清楚",
            "右尾弹性优先": f"{ticker}的AI基础设施右尾更直接",
            "风险调整收益": f"{ticker}订单和估值组合更优",
            "下行保护优先": f"{ticker}防守属性或现金流更稳",
            "估值消化优先": f"{ticker}业绩增速更能消化估值",
            "近端催化优先": f"{ticker}近端订单或项目催化更强",
            "价格确认/动量": f"{ticker}价格确认更强",
            "激进短线": f"{ticker}AI电力/冷却beta更强",
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
    diffs = {strat: a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0) for strat in STRATS}  # type: ignore[union-attr]
    if choice == "A":
        if diffs["价格确认/动量"] > 14:
            return "NOK近期AI网络资金确认强，同时仍有订单和Optical/IP兑现支撑。"
        if diffs["NTM兑现优先"] > 10:
            return "NOK有AI&Cloud订单、Optical/IP指引和Standards现金流支撑。"
        if diffs["下行保护优先"] > 10:
            return "NOK的净现金、专利/软件利润和运营商底盘提供更好缓冲。"
        if diffs["近端催化优先"] > 10:
            return "NOK的AI&Cloud订单延续、Infinera协同和NI margin是更近催化。"
        return "NOK在AI网络兑现、现金流和短线关注之间更均衡。"
    if diffs["右尾弹性优先"] < -18:
        return f"{b['ticker']}的直接AI收入、小基数或平台型右尾明显强于NOK。"
    if diffs["NTM兑现优先"] < -14:
        return f"{b['ticker']}的订单/RPO/backlog或收入确认证据比NOK更硬。"
    if diffs["估值消化优先"] < -12:
        return f"{b['ticker']}的增长和估值匹配度优于NOK。"
    if diffs["下行保护优先"] < -14:
        return f"{b['ticker']}现金流、防御性或压力期表现明显优于NOK。"
    if diffs["价格确认/动量"] < -14:
        return f"{b['ticker']}价格确认和短线资金偏好明显强于NOK。"
    return f"{b['ticker']}在多数投资思路下比NOK更符合项目内资金配置目标。"


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
        key=lambda x: (int(x["ac"]) - int(x["bc"]), a["scores"]["价格确认/动量"] - x["b"]["scores"]["价格确认/动量"]),  # type: ignore[index,operator]
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if int(x["bc"]) >= 5 and int(x["bc"]) - int(x["ac"]) >= 3][:50]
    strong_a_rows = [x for x in strong_a if int(x["ac"]) >= 5 and int(x["ac"]) - int(x["bc"]) >= 3][:50]
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
        "Optical Networks/DCI/coherent line system",
        "IP Networks/DCGW/Data Center Networking",
        "SR Linux/EDA/NSP/Deepfield/WaveSuite软件",
        "Fixed Networks/XGS-PON/25G-50G PON",
        "Radio Networks/AI-RAN/Cloud RAN",
        "Core Software + Technology Standards",
        "Portfolio Businesses",
    ]

    support = {
        "NTM兑现优先": (
            "2026Q1收入€4.497bn，Optical €821m、IP €626m，AI&Cloud订单€1.0bn，NI收入增长指引12-14%、Optical+IP 18-20%",
            "集团基准增速只有5-10%，传统RAN/Fixed和客户验收会抵消AI网络放量",
        ),
        "右尾弹性优先": (
            "Optical/DCI、Infinera、IP DCGW、SR Linux/EDA、AI-RAN和50G PON提供多条右尾",
            "大型AI back-end fabric份额未公开验证，新coherent DSP大规模量产主要在2027H2以后",
        ),
        "风险调整收益": (
            "净现金、Technology Standards高毛利、软件attach和FCF conversion 55-75%给出基本面缓冲",
            "2026-06-22 Forward PE 29.64、EV/EBITDA 28.79、Call IV 87.3%，估值和波动都不低",
        ),
        "下行保护优先": (
            "Core Software/Technology Standards、运营商客户粘性、净现金€3.8bn和多业务组合支撑下行",
            "SOXX三段压力窗口累计-21.58%，且AI网络订单若回落会压库存、应收和capex回收",
        ),
        "估值消化优先": (
            "若基准€21.0-22.0bn收入和€2.2-2.6bn可比经营利润兑现，估值可部分消化",
            "交易货币/财报货币不一致导致P/S校验bad，且当前倍数更像提前反映乐观情景",
        ),
        "近端催化优先": (
            "Q2/Q3 AI&Cloud orders、Optical/IP收入、Infinera协同、NI margin、SR Linux/Deepfield付费案例都可近端验证",
            "如果AI&Cloud订单不能连续，催化会从硬订单变成远期叙事",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+22.83%、过去一月+25.79%，AI网络主题已有明显价格确认",
            "2026-06-22价格14.43低于6月初16.73，高IV意味着部分涨幅可能已经透支",
        ),
        "激进短线": (
            "Call IV 87.3%、Put IV 84.1%，AI网络/AI-RAN/Infinera/订单延续叙事适合高波动进攻",
            "市值约$80.56B且不是纯AI交换/光模块小票，爆发力弱于CRDO、POET、ALAB等小基数标的",
        ),
    }

    daily_snapshot = (
        f"2026-06-22 收盘价 `{framework.fmt_num(fin.get('price'))}` 美元，市值 `{framework.fmt_b(fin.get('market_cap_b'))}`，"
        f"TTM PE `{framework.fmt_num(fin.get('ttm_pe'))}`，Forward PE `{framework.fmt_num(fin.get('forward_pe'))}`，"
        f"P/S `{framework.fmt_num(fin.get('ps'))}`，P/B `{framework.fmt_num(fin.get('pb'))}`，EV/EBITDA `{framework.fmt_num(fin.get('ev_ebitda'))}`，"
        f"Call IV `{framework.fmt_pct(fin.get('call_iv'))}`、Put IV `{framework.fmt_pct(fin.get('put_iv'))}`；"
        f"2026-06-03 过去两周 `{framework.fmt_pct(mom2.get('mom2w'))}`、过去一月 `{framework.fmt_pct(mom1.get('mom1m'))}`；"
        f"2026-06-04 三段 SOXX 压力窗口累计 `{framework.fmt_pct(soxx.get('soxx_cum'))}`。"
    )

    out: list[str] = [
        "# NOK 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：NOK / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04；日度新闻最新文件日期为 2026-06-23。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路相对档位，再逐行做 NOK vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。NOK 的相对优势主要在近端催化、NTM兑现和价格确认：AI网络主题已被资金确认，且Q1 AI&Cloud订单、Optical/IP指引、Infinera协同和软件attach提供近端验证点。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是估值消化、下行保护和相对小基数短线爆发力：Forward PE、EV/EBITDA和IV都不低，SOXX压力窗口不算防御，且NOK仍不是AI back-end fabric默认龙头。",
        "- A 最适合的投资者画像：愿意买AI网络从光传输/DCI向IP data center networking扩张的中短期进攻型资金，同时接受传统运营商业务和高波动估值的配置者。",
        "- A 最不适合的投资者画像：只追求最高确定性AI主链、最低估值消化难度、最强下行保护或最小市值非线性右尾的资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]])}。这些公司通常拥有更直接AI计算/电力/服务器/云平台利润池、更强订单/RPO或更好的估值消化。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：NOK 是项目内AI网络链条的中上档进攻型替代，综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家；它明显强于不少低动量、低右尾或资料不足标的，但面对NVDA/AVGO/MU/ANET/ALAB/VRT/ETN等核心AI主链和电力稀缺公司通常不占优。",
        "- 后续最重要跟踪数据：AI&Cloud收入和订单、Optical Networks/IP Networks单季收入和book-to-bill、Network Infrastructure margin、Infinera协同、capex/库存/应收/FCF conversion、大型AI/data center fabric生产客户、SR Linux/EDA/NSP/Deepfield付费案例、AI-RAN trial转商用、50G PON企业/回传订单。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "NOK"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "€21.0-22.0bn"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "Q1 €1.0bn AI&Cloud订单是否连续，并在NTM内按可验收项目转成收入；NOK是否能从DCI/line system扩到data center fabric，而不是只停留在外围光传输。"]),
        base.row(["最大反证", "AI&Cloud收入仅集团8%，大型AI back-end fabric wins未公开验证；Fixed/RAN可抵消增长，capex扩产可能压库存、应收和FCF。"]),
        base.row(["近端催化剂", "Q2/Q3 AI&Cloud orders、Optical+IP收入增速、Network Infrastructure margin、Infinera协同、SR Linux/EDA/NSP/Deepfield付费案例、AI-RAN trial进展。"]),
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
        base.row(["直接同业", "与NOK在AI网络、光网络、IP路由/交换、运营商/云网络设备或AI data center networking需求池高度重叠，优先比较份额、订单、产品代际、客户质量、margin和同业估值。", "CIEN、ANET、CSCO、VISN", "同业证据权重最高；若B在AI back-end fabric、客户订单或利润兑现上明显强于NOK，可放大到建议或强烈建议。"]),
        base.row(["相邻替代", "同属AI基础设施资金篮子，但与NOK不直接竞争，重点比较资金只能买一个时的增长质量、兑现确定性、估值消化和催化可见度。", "VRT、ETN、GEV、TT、MOD、NVT", "除非档位差明显，否则少用强烈建议；NOK的AI网络动量需要和电力/冷却/配电订单硬度比较。"]),
        base.row(["上下游", "光器件、连接器、光DSP、芯片、服务器、云厂、IDC和存储等与NOK处于同一AI网络/数据中心需求链，重点看利润池位置、议价权和收入确认。", "COHR、LITE、CRDO、APH、TEL、NVDA、AVGO、MSFT、AMZN、DELL", "不把下游AI CapEx直接等同NOK收入；也不把上游瓶颈自动等同胜出，核心看利润捕获和订单硬度。"]),
        base.row(["跨赛道", "半导体材料、前道设备、封测、工业/化工、核电、软件等与NOK业务差异大，但仍可作为资金配置替代。", "ASML、AMAT、LIN、TMO、DHR、RKLB", "默认降低结论力度；若证据互有强弱，优先使用中性或微倾向。"]),
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
        need = "需要NOK证明AI&Cloud订单连续、Optical/IP收入和NI margin超预期，并把data center fabric和软件attach转成可确认收入。"
        if row_obj["relationship"] == "直接同业":
            need = "需要NOK在同业中证明Optical/IP订单、客户份额、产品代际和利润兑现强于B。"
        elif row_obj["relationship"] == "上下游":
            need = "需要NOK证明自己能从上游光器件/芯片或下游云厂CapEx中捕获更高利润，而不是只获得外围传输收入。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), row_obj["key_reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, row_obj in enumerate(strong_a_rows, start=1):
        b = row_obj["b"]
        wins = [strat for strat in STRATS if (base.tag_in_cell(str(row_obj[strat])) or "").endswith("投A")]
        need = "需要B提高收入确认可信度、现金流质量和估值消化能力，或出现明确订单/指引上修。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要B把右尾叙事转成可确认收入和利润，并降低估值、波动或资产负债表反证。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), row_obj["key_reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/AI网络_光互联_连接器/NOK_诺基亚_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/AI网络_光互联_铜互联/行业调研_AI以太网交换系统与Fabric芯片_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_AI Fabric网络操作系统与遥测软件_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_800G_1.6T可插拔光模块_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_光DSP、TIA与CDR芯片_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_宽带接入、PON、DOCSIS 4.0与Wi-Fi 7_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_nok_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用目标无关的最低分校准，对NOK的AI&Cloud订单、Optical/IP指引、Infinera协同、Standards现金流、估值、IV和动量做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
        raise SystemExit("缺少 NOK 正式评估文件")

    framework.relationship = relationship
    framework.reason_for = reason_for
    framework.key_reason = key_reason

    score_companies(companies)
    comparisons = framework.build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "nok_tiers": companies[TARGET]["tiers"],
        "nok_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
        "nok_ranks": companies[TARGET]["ranks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
