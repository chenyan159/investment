from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_ndsn_company_comparison as framework


TARGET = "NTAP"
TARGET_NAME = "NetApp"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "NTAP_逐家公司投资思路对比_2026-06-23.md"

base = framework.base
STRATS = framework.STRATS
TAG_ORDER = framework.TAG_ORDER
TIER_VAL = framework.TIER_VAL
HIGH_GROWTH_CATS = framework.HIGH_GROWTH_CATS
INFRA_CATS = framework.INFRA_CATS

framework.TARGET = TARGET
framework.TARGET_NAME = TARGET_NAME
framework.OUT_PATH = OUT_PATH


DIRECT_STORAGE_PEERS = {
    "PSTG",
    "DELL",
    "HPE",
    "IBM",
    "NTNX",
}

STORAGE_MEDIA_AND_CONTROLLER = {
    "MU",
    "SNDK",
    "STX",
    "WDC",
    "SIMO",
    "RMBS",
    "MRAM",
}

SERVER_EMS_AND_AI_SYSTEMS = {
    "SMCI",
    "PENG",
    "JBL",
    "FLEX",
    "SANM",
    "CLS",
    "FN",
}

AI_COMPUTE_AND_NETWORK_CHAIN = {
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

SEMICAP_AND_SUPPLY_CHAIN = {
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

    # NTAP calibration from the 2026-06-12 formal assessment and 2026-06-22
    # daily data. The company has hard FY2027 guidance, RPO/deferred revenue,
    # all-flash and Public Cloud evidence, strong FCF, and a visible AI data
    # platform option. It should not be treated like a highest-beta AI chip,
    # optical or NeoCloud name because AI revenue is not separately disclosed
    # and STX/AFX remains a 2026H2/2027 verification item.
    overrides = {
        "NTM兑现优先": 68.0,
        "右尾弹性优先": 60.0,
        "风险调整收益": 54.0,
        "下行保护优先": 84.0,
        "估值消化优先": 64.0,
        "近端催化优先": 62.0,
        "价格确认/动量": 82.0,
        "激进短线": 72.0,
    }
    for strat, score in overrides.items():
        companies[TARGET].setdefault("scores", {})[strat] = score  # type: ignore[index]

    recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_STORAGE_PEERS:
        return "直接同业"
    if ticker in STORAGE_MEDIA_AND_CONTROLLER:
        return "上下游"
    if ticker in SERVER_EMS_AND_AI_SYSTEMS:
        return "相邻替代"
    if ticker in AI_COMPUTE_AND_NETWORK_CHAIN or ticker in CLOUD_AND_IDC_CUSTOMERS or ticker in SEMICAP_AND_SUPPLY_CHAIN:
        return "上下游"
    if category == "AI服务器_存储_EMS":
        return "相邻替代"
    if category in {"AI计算芯片_EDA_IP_custom_ASIC", "AI网络_光互联_连接器", "云算力_IDC_AI软件平台"}:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩"}:
        return "上下游"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict[str, object], diff: float) -> str:
    ticker = str(company["ticker"])
    cat = str(company.get("category", ""))
    rel = relationship(company)

    if winner == "中性":
        if rel == "跨赛道":
            return "业务差异较大且证据互抵"
        return "档位接近，需看下一季订单"

    if winner == "A":
        return {
            "NTM兑现优先": "A有FY2027指引、RPO和all-flash硬锚",
            "右尾弹性优先": "A有AFX/STX和AI数据平台期权",
            "风险调整收益": "A现金流、估值和AI期权更均衡",
            "下行保护优先": "A高FCF、净现金和支持收入更稳",
            "估值消化优先": "A约16x远期PE且FCF质量好",
            "近端催化优先": "A有Q1、AI wins和AFX/STX验证点",
            "价格确认/动量": "A六月初价格已强确认AI存储叙事",
            "激进短线": "A有AI存储叙事和中等IV进攻性",
        }[strat]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}的同业订单或收入兑现更硬",
            "右尾弹性优先": f"{ticker}的同业小基数或产品代际右尾更大",
            "风险调整收益": f"{ticker}的同业增长/估值/现金流组合更好",
            "下行保护优先": f"{ticker}的同业现金流或压力期更稳",
            "估值消化优先": f"{ticker}的同业业绩更能消化估值",
            "近端催化优先": f"{ticker}的同业订单或产品催化更直接",
            "价格确认/动量": f"{ticker}的同业价格确认更强",
            "激进短线": f"{ticker}的同业关注度和beta更高",
        }[strat]

    if ticker in STORAGE_MEDIA_AND_CONTROLLER:
        return {
            "NTM兑现优先": f"{ticker}的存储介质/控制器周期兑现更硬",
            "右尾弹性优先": f"{ticker}的HBM/eSSD/存储周期右尾更大",
            "风险调整收益": f"{ticker}的上行和周期风险组合更优",
            "下行保护优先": f"{ticker}的现金流或估值缓冲更好",
            "估值消化优先": f"{ticker}的利润弹性更能消化估值",
            "近端催化优先": f"{ticker}的财报/价格/供需催化更近",
            "价格确认/动量": f"{ticker}的价格趋势和资金偏好更强",
            "激进短线": f"{ticker}的存储周期beta更适合进攻",
        }[strat]

    if cat in HIGH_GROWTH_CATS or ticker in AI_COMPUTE_AND_NETWORK_CHAIN:
        return {
            "NTM兑现优先": f"{ticker}的直接AI主链兑现更短链",
            "右尾弹性优先": f"{ticker}的直接AI右尾和小基数更大",
            "风险调整收益": f"{ticker}的上行空间更能覆盖风险",
            "下行保护优先": f"{ticker}的需求能见度或现金流更好",
            "估值消化优先": f"{ticker}的高增长更能覆盖估值",
            "近端催化优先": f"{ticker}的产品/订单催化更密集",
            "价格确认/动量": f"{ticker}的价格确认和资金偏好更强",
            "激进短线": f"{ticker}的高beta叙事更适合进攻",
        }[strat]

    if ticker in CLOUD_AND_IDC_CUSTOMERS:
        return {
            "NTM兑现优先": f"{ticker}的云/平台收入兑现更稳",
            "右尾弹性优先": f"{ticker}的AI云或平台右尾更大",
            "风险调整收益": f"{ticker}的规模、现金流和客户粘性更好",
            "下行保护优先": f"{ticker}的现金流和资产质量更强",
            "估值消化优先": f"{ticker}的利润留存更能支撑估值",
            "近端催化优先": f"{ticker}的云订单或AI产品催化更近",
            "价格确认/动量": f"{ticker}的价格确认更强",
            "激进短线": f"{ticker}的市场关注或波动更集中",
        }[strat]

    if cat in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}的电力/机电backlog兑现更清楚",
            "右尾弹性优先": f"{ticker}的AI基础设施瓶颈右尾更直接",
            "风险调整收益": f"{ticker}的订单和现金流赔率更好",
            "下行保护优先": f"{ticker}的防御属性或订单粘性更强",
            "估值消化优先": f"{ticker}用订单兑现消化估值更容易",
            "近端催化优先": f"{ticker}的订单/产能/项目催化更近",
            "价格确认/动量": f"{ticker}的价格趋势更强",
            "激进短线": f"{ticker}的AI电力/冷却beta更强",
        }[strat]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}的需求链收入表证据更硬",
            "右尾弹性优先": f"{ticker}的利润池或需求池右尾更直接",
            "风险调整收益": f"{ticker}的利润捕获或上行更优",
            "下行保护优先": f"{ticker}的需求/现金流韧性更好",
            "估值消化优先": f"{ticker}的增长与估值匹配更好",
            "近端催化优先": f"{ticker}的客户/产能催化更清楚",
            "价格确认/动量": f"{ticker}的资金确认更强",
            "激进短线": f"{ticker}的短线叙事弹性更强",
        }[strat]

    return {
        "NTM兑现优先": f"{ticker}的经营兑现更清楚",
        "右尾弹性优先": f"{ticker}的右尾弹性更大",
        "风险调整收益": f"{ticker}的风险调整后赔率更优",
        "下行保护优先": f"{ticker}的压力期更安全",
        "估值消化优先": f"{ticker}的估值消化更容易",
        "近端催化优先": f"{ticker}的近端催化更明确",
        "价格确认/动量": f"{ticker}的价格确认更强",
        "激进短线": f"{ticker}的短线进攻属性更强",
    }[strat]


def key_reason(a: dict[str, object], b: dict[str, object], choice: str) -> str:
    diffs = {strat: a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0) for strat in STRATS}  # type: ignore[union-attr]
    if choice == "A":
        if diffs["下行保护优先"] > 12:
            return "NTAP的高FCF、净现金、Support/RPO和较低IV提供更好下行保护。"
        if diffs["NTM兑现优先"] > 10:
            return "NTAP有FY2027收入指引、RPO/deferred revenue和all-flash收入兑现支撑。"
        if diffs["估值消化优先"] > 10:
            return "NTAP约16x远期PE、FCF质量和高毛利服务使估值消化更清楚。"
        if diffs["价格确认/动量"] > 12:
            return "NTAP六月初已被价格确认，且有基本面披露配合。"
        return "NTAP在兑现、现金流、估值和AI数据平台期权之间更均衡。"
    if diffs["右尾弹性优先"] < -18:
        return f"{b['ticker']}的直接AI收入、小基数或平台型右尾明显强于NTAP。"
    if diffs["NTM兑现优先"] < -14:
        return f"{b['ticker']}的订单/RPO/backlog或收入确认证据比NTAP更硬。"
    if diffs["估值消化优先"] < -12:
        return f"{b['ticker']}的增长和估值匹配度优于NTAP。"
    if diffs["下行保护优先"] < -14:
        return f"{b['ticker']}现金流、防御性或压力期表现明显优于NTAP。"
    if diffs["价格确认/动量"] < -14:
        return f"{b['ticker']}价格确认和短线资金偏好明显强于NTAP。"
    return f"{b['ticker']}在多数投资思路下比NTAP更符合项目内资金配置目标。"


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
        key=lambda x: (int(x["ac"]) - int(x["bc"]), a["scores"]["下行保护优先"] - x["b"]["scores"]["下行保护优先"]),  # type: ignore[index,operator]
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
        "Product / all-flash ONTAP systems",
        "Support / installed-base services",
        "Public Cloud storage services",
        "Professional and Other / Keystone STaaS",
        "Hybrid-flash/FAS/StorageGRID residual",
        "AI Data Platform：AFX / AI Data Engine / AIPod / STX-CMX",
    ]

    support = {
        "NTM兑现优先": (
            "FY2027收入指引73.25-75.75亿美元、FY2026 RPO 56.5亿美元、deferred revenue 48.5亿美元、all-flash Q4同比+18%",
            "基准增速约+8%，不是AI芯片式高增；AI/data wins到收入仍需合同、交付和验收",
        ),
        "右尾弹性优先": (
            "AFX、AI Data Engine、NVIDIA DGX SuperPOD/AFX认证、STX/CMX和1,100+ AI/data preparation wins提供右尾",
            "AI收入未单列，STX 2026H2伙伴可用且非独家；极度乐观需要多个千万美元级项目连续确认",
        ),
        "风险调整收益": (
            "2026-06-22 Forward PE 16.06、EV/EBITDA 16.16、FCF margin约27%、净现金和高毛利服务形成均衡赔率",
            "价格已重估为AI存储受益者，SOXX压力窗口累计-49.09%，且Product毛利受NAND/SSD成本压制",
        ),
        "下行保护优先": (
            "Support毛利率约92.5%、Public Cloud毛利率约83.6%、FCF约18.69亿美元、净现金约11亿美元、IV低于多数AI硬件链",
            "企业存储仍有硬件/周期属性，Q4大单和all-flash需求若不可持续，下行不会等同软件/公用事业",
        ),
        "估值消化优先": (
            "FY2027 non-GAAP EPS指引中点约8.85美元，16.06x forward PE和FCF转化给估值消化支撑",
            "P/S 4.48已高于传统硬件公司，若收入只兑现+8%且毛利受组件成本压制，估值消化速度有限",
        ),
        "近端催化优先": (
            "Q1/Q2 FY2027 billings、Product/all-flash、Public Cloud ex-Spot、Keystone TCV/RPO、AI wins金额化和STX/AFX客户案例均可验证",
            "多数AI数据平台催化仍是客户案例和认证，不是已披露大额backlog；催化强度弱于AI服务器/光模块/电力硬订单",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+52.21%、过去一月+61.56%，Q4后价格显著确认AI存储叙事",
            "2026-06-22价格158.31已低于6月初181.08，说明部分短线动量回吐，后续需财报继续确认",
        ),
        "激进短线": (
            "AI-native存储、KV cache、AFX/STX和Public Cloud可形成事件交易；Call IV 46.7%不算低",
            "IV和关注度低于HBM、光互联、NeoCloud和AI服务器高beta标的，短线爆发力不是项目内顶档",
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
        "# NTAP 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：NTAP / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04；日度新闻最新文件日期为 2026-06-23。",
        "",
        f"> 口径说明：本报告按同一批 {n} 家正式公司评估建立 8 个投资思路相对档位，再逐行做 NTAP vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论；既有公司对比结果不作为本报告决策依据。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。NTAP 最容易在下行保护、估值消化和NTM兑现中胜出：FY2027指引、RPO/deferred revenue、all-flash、Support/Public Cloud高毛利和FCF质量较硬。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。短板是激进短线、右尾弹性和近端催化：AI Data Platform、AFX和STX/CMX重要，但尚未披露大额独立收入或backlog。",
        "- A 最适合的投资者画像：希望买AI数据基础设施二层受益、重视现金流和估值消化，同时接受收入增速只是中高个位数到低双位数的质量成长/防守型资金。",
        "- A 最不适合的投资者画像：只追求最高收入增速、最大非线性右尾、明确大额订单/RPO，或短期高beta爆发的进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]])}。这些公司通常拥有更直接AI芯片/服务器/光互联/电力/云平台利润池、更强订单硬度或更高短线beta。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：NTAP 对 {final_a}/{n - 1} 家公司多数思路占优，对 {final_b}/{n - 1} 家公司多数思路落后；它强于很多低兑现、低现金流或纯叙事标的，但面对NVDA/AVGO/MU/ALAB/CRDO/ANET/DELL/HPE/VRT/ETN等核心AI主链和电力稀缺公司通常不占优。",
        "- 后续最重要跟踪数据：季度Product revenue、all-flash array revenue、Public Cloud reported/ex-Spot、Support收入和毛利率、Keystone revenue/TCV/RPO、billings、RPO/unbilled RPO、deferred revenue、AI/data wins的金额化披露、AFX/AI Data Engine客户案例、STX/CMX实际可用和客户采用、Product gross margin、inventory/receivables与FCF转化。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "NTAP"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a["base_rev"] or "73.3-75.8亿美元"]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "从AI/data preparation wins、Google Distributed Cloud、NVIDIA DGX SuperPOD/AFX认证和STX/CMX合作到NTAP NTM可确认收入之间仍有合同、交付、验收、云市场确认和订阅收入递延环节。"]),
        base.row(["最大反证", "AI Data Platform单独收入未披露，STX/CMX非独家且2026H2才进入伙伴可用；Product毛利受NAND/SSD成本和大客户压价影响，Q4强度若不可重复会压估值。"]),
        base.row(["近端催化剂", "FY2027 Q1/Q2 billings和订单、all-flash增速、Public Cloud ex-Spot/marketplace、Keystone TCV/RPO、AI/data wins金额化、AFX/AI Data Engine客户案例、STX/CMX GA和客户部署。"]),
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
        base.row(["直接同业", "与NTAP在企业存储、混合云存储、AI数据平台、HCI/数据管理或企业存储系统需求池高度重叠，优先比较份额、产品代际、客户质量、RPO/backlog、毛利和同业估值。", "PSTG、DELL、HPE、IBM、NTNX", "同业证据权重最高；若B在AI服务器/存储订单或产品代际明显更强，可给建议或强烈建议；若NTAP现金流和估值更稳，也可在下行/估值列胜出。"]),
        base.row(["相邻替代", "同属AI服务器/存储/EMS或AI数据中心硬件资金篮子，但产品不直接竞争，重点看资金只能买一个时的增长质量、兑现确定性和赔率。", "SMCI、PENG、JBL、FLEX、SANM、CLS、FN、VRT、ETN、TT、MOD", "多数情况下按档位差判断；对电力/冷却等更硬订单公司，NTAP需要用现金流和估值消化抵消右尾差距。"]),
        base.row(["上下游", "存储介质/控制器、AI芯片、网络、云厂、服务器和半导体制造链与NTAP处于同一需求链或供给链，重点比较利润池、议价权和收入确认。", "MU、WDC、STX、NVDA、AVGO、ANET、CRDO、MSFT、AMZN、TSM、ASML", "不把云CapEx或STX生态公告直接等同NTAP收入；也不把上游稀缺自动等同胜出，核心看谁能留存利润和兑现业绩。"]),
        base.row(["跨赛道", "半导体材料、工业、化工、能源和软件等与NTAP业务差异大，但仍作为项目内资金配置替代比较风险调整收益、估值消化和下行保护。", "LIN、ECL、DHR、TMO、RKLB、CAT", "默认降低结论力度；若证据互有强弱，优先使用中性或微倾向。"]),
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
        need = "需要NTAP把AI/data wins转成可确认订单、收入和高毛利，并持续披露RPO、billings、all-flash和Public Cloud超预期。"
        if row_obj["relationship"] == "直接同业":
            need = "需要NTAP在企业存储同业中证明all-flash/AFX/Public Cloud/Keystone订单、份额和利润兑现强于B。"
        elif row_obj["relationship"] == "上下游":
            need = "需要NTAP证明自己能从上游AI芯片/存储介质或下游云厂CapEx中捕获更高利润，而不只是间接受益。"
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
        "- 公司 A 公司调研文件：`公司调研/AI服务器_存储_EMS/NTAP_NetApp_公司调研_2026-06-11.md`。",
        "- 关键行业资料：`行业调研/AI服务器_存储_芯片/行业调研_AI-native存储与KV Cache基础设施_2026-06-10.md`；`行业调研/AI服务器_存储_芯片/行业调研_企业级SSD与高速存储控制器_2026-06-10.md`；`行业调研/AI服务器_存储_芯片/行业调研_HDD、对象存储与冷温数据存储_2026-06-11.md`；`行业调研/AI网络_光互联_铜互联/行业调研_网卡、DPU与SmartNIC_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研、IR、SEC、产品公告和财报来源。",
        "- 自动化脚本：`scripts/generate_ntap_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用目标无关的最低分校准，对NTAP的FY2027指引、RPO/deferred revenue、all-flash、Public Cloud、Keystone、AI Data Platform、估值、IV、价格动量和SOXX压力窗口做目标公司校准后建档；未读取下游量化目录或现成排序结论。",
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
        raise SystemExit("缺少 NTAP 正式评估文件")

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
        "ntap_tiers": companies[TARGET]["tiers"],
        "ntap_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
        "ntap_ranks": companies[TARGET]["ranks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
