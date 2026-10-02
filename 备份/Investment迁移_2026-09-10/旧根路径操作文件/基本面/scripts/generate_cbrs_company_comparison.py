from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_ndsn_company_comparison as framework


TARGET = "CBRS"
TARGET_NAME = "Cerebras Systems Inc"
REPORT_DATE = "2026-06-30"
ROOT = Path(r"D:\drive\Investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "CBRS_逐家公司投资思路对比_2026-06-30.md"

base = framework.base
STRATS = framework.STRATS
TAG_ORDER = framework.TAG_ORDER
HIGH_GROWTH_CATS = framework.HIGH_GROWTH_CATS
INFRA_CATS = framework.INFRA_CATS

base.FIN_PATH = ROOT.parent / "金融资料" / "每日金融数据" / "每日金融数据_2026-06-29.md"
base.MOM2W_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去两周_2026-06-23.md"
base.MOM1M_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价区间涨跌幅_过去1个月_2026-06-23.md"
base.SOXX_PATH = ROOT.parent / "金融资料" / "区间涨跌" / "公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md"


DIRECT_AI_ACCELERATOR_PEERS = {
    "NVDA",
    "AMD",
    "AVGO",
    "INTC",
    "MRVL",
    "ARM",
    "QCOM",
}

AI_CHIP_ADJACENT = {
    "ADI",
    "ALAB",
    "CDNS",
    "MCHP",
    "MXL",
    "ON",
    "SNPS",
    "STM",
    "TXN",
    "CRDO",
    "SITM",
    "SMTC",
    "MTSI",
    "POET",
    "LWLG",
    "LITE",
    "COHR",
}

CLOUD_AND_AI_CAPACITY_CUSTOMERS = {
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
}

SERVER_NETWORK_STORAGE_CHAIN = {
    "AAOI",
    "ANET",
    "APH",
    "BDC",
    "BELFB",
    "CIEN",
    "CLS",
    "CSCO",
    "DELL",
    "FLEX",
    "FN",
    "GLW",
    "HPE",
    "JBL",
    "MU",
    "NOK",
    "NTAP",
    "PENG",
    "PSTG",
    "RMBS",
    "SANM",
    "SIMO",
    "SMCI",
    "SNDK",
    "STX",
    "TEL",
    "VIAV",
    "VISN",
    "WDC",
}

FOUNDRY_PACKAGING_EQUIPMENT_CHAIN = {
    "ACLS",
    "ACMR",
    "AEHR",
    "AEIS",
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
    "CC",
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
    "LRCX",
    "MICLF",
    "MKSI",
    "MRAAY",
    "MRAM",
    "MTRN",
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

POWER_COOLING_INFRA_ALTS = {
    "AAON",
    "ABBNY",
    "AEP",
    "ALLE",
    "AMPX",
    "APD",
    "ATKR",
    "BE",
    "BWXT",
    "CARR",
    "CAT",
    "CEG",
    "CMI",
    "DCI",
    "DD",
    "DHR",
    "DKILY",
    "DOV",
    "DTE",
    "ECL",
    "EME",
    "ENS",
    "ET",
    "ETN",
    "ETR",
    "FCEL",
    "FIX",
    "FLNC",
    "FTV",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "IESC",
    "IFNNY",
    "JCI",
    "LFUS",
    "LIN",
    "MIELY",
    "MMM",
    "MOD",
    "MPWR",
    "MSI",
    "MYRG",
    "NDSN",
    "NVT",
    "OKLO",
    "PH",
    "PNR",
    "POWI",
    "POWL",
    "PSIX",
    "PWR",
    "RYCEY",
    "SMR",
    "ST",
    "TDY",
    "TE",
    "TMO",
    "TSLA",
    "TT",
    "TTDKY",
    "VICR",
    "VRT",
    "VSH",
    "VST",
    "WOLF",
}


CBRS_EXTERNAL_MARKET = {
    "price_date": "2026-06-30",
    "price": 216.16,
    "market_cap_b": 51.0,
    "ps": 100.0,
    "ttm_pe": None,
    "forward_pe": None,
    "pb": None,
    "ev_ebitda": None,
    "call_iv": None,
    "put_iv": None,
    "ttm_revenue_b": 0.51,
    "source_timestamp": "2026-06-30 UTC；项目日度表未覆盖，外部公开报价补充",
    "valuation_check": "source_conflict",
    "notes": (
        "项目2026-06-29金融快照未覆盖CBRS；外部源显示6月30日价格约213-216美元，"
        "Google/TradingView/Robinhood市值口径约49-61B且互不一致，Barchart/其他源也有差异；"
        "因此估值和动量列按高不确定性处理。"
    ),
}

CBRS_MOMENTUM_PROXY = {
    "latest_trade_date": "2026-06-30",
    "latest_close": 216.16,
    "base_trade_date": "上市后数据不足",
    "base_close": None,
    "mom1m": None,
    "mom2w": None,
}

CBRS_SCORES = {
    "NTM兑现优先": 85.0,
    "右尾弹性优先": 96.0,
    "风险调整收益": 54.0,
    "下行保护优先": 38.0,
    "估值消化优先": 42.0,
    "近端催化优先": 88.0,
    "价格确认/动量": 45.0,
    "激进短线": 86.0,
}


def install_cbrs_market_snapshot(companies: dict[str, dict[str, object]]) -> None:
    company = companies.get(TARGET)
    if not company:
        return
    existing_fin = dict(company.get("fin", {}) or {})
    existing_fin.update(CBRS_EXTERNAL_MARKET)
    company["fin"] = existing_fin
    company["mom1"] = {**CBRS_MOMENTUM_PROXY, "mom1m": None}
    company["mom2"] = {**CBRS_MOMENTUM_PROXY, "mom2w": None}
    company["soxx"] = {"soxx1": None, "soxx2": None, "soxx3": None, "soxx_cum": None}


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    install_cbrs_market_snapshot(companies)
    old_target = getattr(base, "TARGET", "ALLE")
    base.TARGET = "ALLE"
    base.score_companies(companies)
    base.TARGET = old_target
    framework.apply_global_floors(companies)
    target = companies[TARGET]
    for strat, score in CBRS_SCORES.items():
        target.setdefault("scores", {})[strat] = score  # type: ignore[index]
    framework.recompute_tiers(companies)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    if ticker in DIRECT_AI_ACCELERATOR_PEERS:
        return "直接同业"
    if ticker in AI_CHIP_ADJACENT:
        return "相邻替代"
    if ticker in CLOUD_AND_AI_CAPACITY_CUSTOMERS:
        return "上下游"
    if ticker in SERVER_NETWORK_STORAGE_CHAIN or ticker in FOUNDRY_PACKAGING_EQUIPMENT_CHAIN:
        return "上下游"
    if ticker in POWER_COOLING_INFRA_ALTS:
        return "相邻替代"
    if category in {"AI计算芯片_EDA_IP_custom_ASIC"}:
        return "相邻替代"
    if category in {"云算力_IDC_AI软件平台", "AI服务器_存储_EMS", "AI网络_光互联_连接器"}:
        return "上下游"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    if category in INFRA_CATS:
        return "相邻替代"
    return "跨赛道"


def reason_for(strat: str, winner: str, company: dict[str, object]) -> str:
    ticker = str(company.get("ticker", ""))
    category = str(company.get("category", ""))
    rel = relationship(company)

    if winner == "中性":
        if rel == "跨赛道":
            return "业务差异大且证据互抵"
        if strat in {"估值消化优先", "价格确认/动量"}:
            return "日度口径或估值证据不足"
        return "档位接近需继续验证"

    if winner == "A":
        return {
            "NTM兑现优先": "A有Q1收入、FY2026指引和OpenAI RPO硬锚",
            "右尾弹性优先": "A的OpenAI 750MW和AWS解耦推理右尾更大",
            "风险调整收益": "A右尾巨大且现金充足但仍需折扣",
            "下行保护优先": "A有IPO后现金但仍非防守资产",
            "估值消化优先": "A可用高增长消化部分高P/S",
            "近端催化优先": "A有Q2/Q3、OpenAI、AWS和模型API验证点",
            "价格确认/动量": "A高关注反弹但波动仍大",
            "激进短线": "A高beta IPO和AI推理叙事更适合进攻",
        }[strat]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业收入/订单兑现更硬",
            "右尾弹性优先": f"{ticker}的AI平台右尾证据更硬",
            "风险调整收益": f"{ticker}生态、份额或现金流更稳",
            "下行保护优先": f"{ticker}盈利和交易历史更能防守",
            "估值消化优先": f"{ticker}利润或估值口径更可验证",
            "近端催化优先": f"{ticker}产品/订单催化更明确",
            "价格确认/动量": f"{ticker}价格确认数据更完整",
            "激进短线": f"{ticker}短线流动性或趋势更清楚",
        }[strat]

    if ticker in CLOUD_AND_AI_CAPACITY_CUSTOMERS or category == "云算力_IDC_AI软件平台":
        return {
            "NTM兑现优先": f"{ticker}云/平台收入兑现更稳",
            "右尾弹性优先": f"{ticker}的AI云需求池或平台右尾更大",
            "风险调整收益": f"{ticker}规模、现金流和客户粘性更强",
            "下行保护优先": f"{ticker}现金流和资产质量更稳",
            "估值消化优先": f"{ticker}利润留存更能支撑估值",
            "近端催化优先": f"{ticker}云订单或AI产品催化更近",
            "价格确认/动量": f"{ticker}价格趋势数据更完整",
            "激进短线": f"{ticker}市场关注或波动更可交易",
        }[strat]

    if ticker in SERVER_NETWORK_STORAGE_CHAIN or category in {"AI服务器_存储_EMS", "AI网络_光互联_连接器"}:
        return {
            "NTM兑现优先": f"{ticker}硬件订单/客户兑现更近",
            "右尾弹性优先": f"{ticker}AI服务器/网络/存储右尾更可收入化",
            "风险调整收益": f"{ticker}增长与估值组合更优",
            "下行保护优先": f"{ticker}现金流或价格历史更稳",
            "估值消化优先": f"{ticker}估值和收入表更可验证",
            "近端催化优先": f"{ticker}订单/产品催化更清楚",
            "价格确认/动量": f"{ticker}价格确认更强",
            "激进短线": f"{ticker}的AI硬件beta更可交易",
        }[strat]

    if ticker in FOUNDRY_PACKAGING_EQUIPMENT_CHAIN or category in {"晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return {
            "NTM兑现优先": f"{ticker}供应链收入确认更成熟",
            "右尾弹性优先": f"{ticker}半导体周期或先进封装右尾更硬",
            "风险调整收益": f"{ticker}利润池或估值组合更均衡",
            "下行保护优先": f"{ticker}资产质量和交易历史更稳",
            "估值消化优先": f"{ticker}估值消化证据更完整",
            "近端催化优先": f"{ticker}设备/产能催化更直接",
            "价格确认/动量": f"{ticker}价格趋势数据更完整",
            "激进短线": f"{ticker}周期beta或订单弹性更清楚",
        }[strat]

    if ticker in POWER_COOLING_INFRA_ALTS or category in INFRA_CATS:
        return {
            "NTM兑现优先": f"{ticker}电力/机电订单兑现更清楚",
            "右尾弹性优先": f"{ticker}的AI基础设施瓶颈右尾更可见",
            "风险调整收益": f"{ticker}订单、估值或现金流组合更好",
            "下行保护优先": f"{ticker}现金流/公用事业/订单粘性更稳",
            "估值消化优先": f"{ticker}用订单兑现消化估值更容易",
            "近端催化优先": f"{ticker}订单/项目催化更近",
            "价格确认/动量": f"{ticker}价格确认更完整",
            "激进短线": f"{ticker}的AI电力/冷却beta更强",
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


def cell_for(strat: str, a: dict[str, object], b: dict[str, object], rel: str) -> str:
    label = framework.label_for(strat, a, b, rel)
    winner = "A" if "投A" in label else "B" if "投B" in label else "中性"
    return f"{label}：{reason_for(strat, winner, b)}"


def grade_diff_summary(a: dict[str, object], b: dict[str, object]) -> str:
    a_strong: list[str] = []
    b_strong: list[str] = []
    close: list[str] = []
    for strat in STRATS:
        diff = a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0)  # type: ignore[union-attr,operator]
        label = strat.replace("优先", "").replace("/动量", "动量")
        if diff >= 8:
            a_strong.append(label)
        elif diff <= -8:
            b_strong.append(label)
        else:
            close.append(label)

    def joined(items: list[str]) -> str:
        return "无" if not items else "、".join(items[:3]) + ("等" if len(items) > 3 else "")

    return f"A强：{joined(a_strong)}；B强：{joined(b_strong)}；接近：{joined(close)}"


def key_reason(a: dict[str, object], b: dict[str, object], choice: str) -> str:
    diffs = {strat: a.get("scores", {}).get(strat, 0) - b.get("scores", {}).get(strat, 0) for strat in STRATS}  # type: ignore[union-attr]
    ticker = str(b.get("ticker", ""))
    if choice == "A":
        if diffs["右尾弹性优先"] > 18:
            return "CBRS的OpenAI 750MW、25B级RPO、AWS和高速推理API带来更大非线性右尾。"
        if diffs["NTM兑现优先"] > 12:
            return "CBRS有Q1收入、FY2026指引、OpenAI容量和RPO转收入路径，NTM增速更硬。"
        if diffs["近端催化优先"] > 12:
            return "CBRS未来1-2季有cloud/services、毛利修复、OpenAI/AWS和模型API连续验证点。"
        if diffs["激进短线"] > 14:
            return "CBRS高波动IPO、AI推理叙事和反弹弹性更适合激进进攻。"
        return "CBRS在高增长、订单可见性和近端验证之间优于B，但仍需承担执行和估值风险。"
    if diffs["下行保护优先"] < -14:
        return f"{ticker}现金流、盈利、交易历史或防御属性明显优于CBRS。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}估值口径更清楚，CBRS刚上市且高P/S/市值源冲突削弱消化确定性。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}上行与下行组合更均衡，CBRS仍有数据中心、毛利和客户集中反证。"
    if diffs["价格确认/动量"] < -12:
        return f"{ticker}价格确认数据更完整，CBRS上市后波动大且项目日度表缺失。"
    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}收入、订单或利润兑现链条比CBRS更成熟。"
    return f"{ticker}在多数投资思路下比CBRS更符合项目内资金配置目标。"


def build_comparisons(companies: dict[str, dict[str, object]]) -> list[dict[str, object]]:
    a = companies[TARGET]
    rows: list[dict[str, object]] = []
    for ticker in sorted(t for t in companies if t != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        row_obj: dict[str, object] = {
            "ticker": ticker,
            "name": b["name"],
            "classification": base.category_short(str(b.get("category", ""))),
            "relationship": rel,
            "grade_diff": grade_diff_summary(a, b),
            "b": b,
        }
        for strat in STRATS:
            row_obj[strat] = cell_for(strat, a, b, rel)
        ac, bc, nc = framework.direction_counts(row_obj)
        row_obj["majority"] = f"A {ac} / B {bc} / 中性 {nc}"
        row_obj["ac"] = ac
        row_obj["bc"] = bc
        row_obj["nc"] = nc
        choice = framework.final_choice(row_obj, a, b)
        row_obj["final_choice"] = choice
        row_obj["key_reason"] = key_reason(a, b, choice)
        rows.append(row_obj)

    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return sorted(rows, key=lambda x: (rel_order.get(str(x["relationship"]), 9), str(x["ticker"])))


def fmt_num(value: object, decimals: int = 2) -> str:
    return framework.fmt_num(value, decimals)


def fmt_b(value: object) -> str:
    return framework.fmt_b(value)


def fmt_pct(value: object) -> str:
    return framework.fmt_pct(value)


def tag(cell: object) -> str | None:
    return base.tag_in_cell(str(cell))


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(company_dates)} 至 {max(company_dates)}"
    stats = {strat: Counter() for strat in STRATS}
    for row_obj in comparisons:
        for strat in STRATS:
            stats[strat][tag(row_obj[strat])] += 1
    a_side = {s: sum(stats[s][label] for label in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][label] for label in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "A")
    final_b = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "B")
    strong_b = sorted(
        comparisons,
        key=lambda x: (
            int(x["bc"]) - int(x["ac"]),
            x["b"]["scores"]["风险调整收益"] - a["scores"]["风险调整收益"],  # type: ignore[index,operator]
            x["b"]["scores"]["下行保护优先"] - a["scores"]["下行保护优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_a = sorted(
        comparisons,
        key=lambda x: (
            int(x["ac"]) - int(x["bc"]),
            a["scores"]["右尾弹性优先"] - x["b"]["scores"]["右尾弹性优先"],  # type: ignore[index,operator]
            a["scores"]["近端催化优先"] - x["b"]["scores"]["近端催化优先"],  # type: ignore[index,operator]
        ),
        reverse=True,
    )
    strong_b_rows = [x for x in strong_b if int(x["bc"]) >= 5 and int(x["bc"]) - int(x["ac"]) >= 3][:45]
    strong_a_rows = [x for x in strong_a if int(x["ac"]) >= 5 and int(x["ac"]) - int(x["bc"]) >= 3][:45]
    missing_daily = [
        ticker
        for ticker in sorted(companies)
        if not companies[ticker].get("fin") or not companies[ticker]["fin"].get("price")  # type: ignore[union-attr]
    ]
    rank_text = {s: f"第 {a['ranks'][s]}/{n}，{a['tiers'][s]} 档" for s in STRATS}  # type: ignore[index]

    support = {
        "NTM兑现优先": (
            "2026Q1收入193.4M，FY2026 core revenue指引855-865M，OpenAI MRA/RPO约25B提供硬锚",
            "Q2 core GM指引36-38%，RPO前24个月仅约16%确认，数据中心上电和验收仍是瓶颈",
        ),
        "右尾弹性优先": (
            "OpenAI 750MW低延迟推理容量、AWS Trainium prefill+CS-3 decode、WSE-3/CS-3和Kimi/Gemma高速API构成大右尾",
            "极度乐观需OpenAI提前、AWS多区域商业化、非OpenAI客户和毛利修复同时成立",
        ),
        "风险调整收益": (
            "NTM基准收入1.55-2.10B、IPO后现金/投资约3.3B，若cloud利用率提升，上行很大",
            "外部市值/估值口径冲突且大多显示高P/S；FCF仍流出，客户集中和租赁承诺压制赔率",
        ),
        "下行保护优先": (
            "现金储备给扩张期时间，OpenAI长约/RPO降低需求真空风险",
            "刚上市交易历史短，价格曾从386高点跌至160低点附近，Q2毛利压力和数据中心成本使防守性弱",
        ),
        "估值消化优先": (
            "若NTM收入进入1.55-2.10B且2027 run-rate继续上台阶，高增长可消化部分高估值",
            "项目日度估值表未覆盖；外部源市值约49-61B且冲突，按2025收入看P/S极高，估值消化证据不足",
        ),
        "近端催化优先": (
            "未来1-2季可验证Q2/Q3 core revenue、core GM、OpenAI容量、RPO转收入、AWS商业状态和非OpenAI API用量",
            "若Q3/Q4 cloud revenue不连续增长或GM低于38%，催化会直接转为反证",
        ),
        "价格确认/动量": (
            "6月30日外部报价显示从6月26日160.81低点强反弹至约213-216，市场关注度高",
            "项目区间涨跌/SOXX文件未覆盖CBRS；上市后先冲高至386.34再大幅回撤，趋势确认不稳定",
        ),
        "激进短线": (
            "高beta IPO、AI推理、OpenAI/AWS、模型API和低延迟叙事叠加，短线弹性强",
            "无干净IV口径，波动极高，毛利/锁定期/数据源冲突容易放大反向波动",
        ),
    }

    daily_snapshot = (
        "项目金融快照 `每日金融数据_2026-06-29.md` 未覆盖CBRS；"
        "外部补充 2026-06-30 报价约 213-216 美元，Google Finance 显示日内区间约 182.10-220.57、"
        "市值约48.97B，TradingView显示市值约51.01B、历史高点386.34、低点160.81、波动率21.41%，"
        "Robinhood显示市值约60.68B。源间市值/PE口径冲突，因此估值和动量列均按高不确定性处理。"
    )

    out: list[str] = [
        "# CBRS 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：CBRS / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：项目价格/估值/IV主文件为 2026-06-29；项目两周/一月涨跌与SOXX压力窗口为 2026-06-23；CBRS未被上述日度文件覆盖，另用2026-06-30外部公开报价作补充且标记为高不确定性。",
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 CBRS vs 公司 B 的二选一判断。未读取、引用或继承 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/tmp/`、`分析报告/备份/` 或既有公司对比结果；外部报价仅用于弥补CBRS未进入项目日度金融表的价格/估值缺口。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。CBRS 的强项集中在右尾弹性、近端催化和NTM收入兑现：OpenAI 750MW/RPO约25B、FY2026收入指引、AWS解耦推理和Cerebras Cloud/API把它放在项目内最强高增长新股之一。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。核心短板是估值和下行保护：刚上市、外部源市值口径冲突但均显示高估值，Q2毛利指引下滑、数据中心租赁/供电/验收和客户集中让下行风险很重。",
        "- A 最适合的投资者画像：愿意用高波动仓位押注专用低延迟推理、OpenAI容量兑现、AWS商业化和非OpenAI API/模型生态扩张的高风险成长投资者。",
        "- A 最不适合的投资者画像：需要稳定盈利、自由现金流、低估值、低回撤、完整交易历史和压力窗口验证的核心配置投资者。",
        f"- 多数思路下最强反方公司：{'、'.join([str(x['ticker']) for x in strong_b_rows[:12]])}。这些公司通常在现金流、盈利、估值消化、交易历史、下行保护或更成熟AI主链份额上强于CBRS。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：CBRS 是全项目右尾高档、近端催化顶档，但风险调整和下行保护偏弱的高beta AI推理平台；综合最终选择为 A 的对比 {final_a} 家、B 的对比 {final_b} 家。",
        "- 后续最重要跟踪数据：Q2/Q3 core revenue、cloud/services环比、OpenAI收入和RPO conversion、effective MW/数据中心上线、core GM是否从36-38%修复、pass-through占比、AWS商业收入、非OpenAI API付费客户、data center lease commitments、operating cash flow、客户集中度和锁定期/二级市场流动性。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "CBRS"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a["category"]]),
        base.row(["重要产品/业务线", "OpenAI Dedicated Capacity / Cerebras Cloud；WSE-3/CS-3硬件系统；AWS Trainium prefill+CS-3 decode；非OpenAI Cerebras Inference API、Kimi K2.6、Gemma 4、Cerebras Code；支持/管理服务与数据中心pass-through"]),
        base.row(["NTM 基准收入", a["base_rev"]]),
        base.row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        base.row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        base.row(["最大传导瓶颈", "OpenAI/AWS容量能否按MW、数据中心、上电、部署、验收和利用率转为可确认收入；租赁、电力、第三方数据中心和pass-through成本会决定毛利质量。"]),
        base.row(["最大反证", "Q2 core GM指引36-38%低于Q1；RPO初始24个月约16%确认；OpenAI客户集中；AWS金额/最低采购量未披露；非OpenAI API流量尚未转成可披露收入。"]),
        base.row(["近端催化剂", "Q2/Q3财报与指引、cloud/services连续增长、OpenAI capacity tranche、core GM修复、AWS Bedrock/Marketplace商业化、Kimi/Gemma/Cerebras Code企业付费和使用率。"]),
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
        base.row(["直接同业", "与CBRS在AI加速器、AI推理/训练芯片、定制ASIC、加速器平台或AI计算份额上直接竞争，优先比较收入兑现、客户、产品代际、生态、毛利和估值。", "NVDA、AMD、AVGO、MRVL、INTC、ARM、QCOM", "证据权重最高；若B有更成熟生态、利润和份额，不能只因CBRS右尾大就强判投A。"]),
        base.row(["相邻替代", "同属AI芯片、EDA/IP、连接芯片、数据中心电力/冷却/配电或AI基础设施资金篮子，但不直接销售同类加速器。", "ALAB、CRDO、CDNS、SNPS、VRT、ETN、CEG、GEV、POWL", "重点比较资金只能买一个时谁的增长质量、估值消化和催化更好。"]),
        base.row(["上下游", "B位于CBRS需求链、供应链或客户预算链，包括云厂、NeoCloud、服务器/网络/存储、代工、封测、设备和材料。", "AMZN、MSFT、GOOGL、META、ORCL、CRWV、DELL、SMCI、TSM、ASML、AMAT、MU", "不把下游CapEx直接等同于CBRS收入，核心看利润池位置、议价权、订单硬度和反证。"]),
        base.row(["跨赛道", "业务差异较大，但作为项目内资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "部分非AI工业、软件、材料和能源标的", "默认降低结论力度；只有档位和证据明显拉开时给建议或强烈建议。"]),
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
        out.append(base.row([strat] + [stats[strat][label] for label in TAG_ORDER] + [a_side[strat], b_side[strat]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, row_obj in enumerate(strong_b_rows, start=1):
        b = row_obj["b"]
        wins = [strat for strat in STRATS if (tag(row_obj[strat]) or "").endswith("投B")]
        need = "CBRS需要证明RPO按期转收入、core GM修复到40%+、AWS/非OpenAI客户商业化，并给出更稳定的估值和交易数据。"
        if row_obj["relationship"] == "直接同业":
            need = "CBRS需要在AI加速器同业中证明收入增速、客户多元化、毛利、生态和TCO足以对抗B的成熟平台优势。"
        elif row_obj["relationship"] == "上下游":
            need = "CBRS需要证明自己能从下游AI云/服务器/半导体CapEx中捕获足够利润，而不是只承担高成本容量扩张。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), row_obj["key_reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), base.row(["---:", "---", "---", "---", "---"])]
    for index, row_obj in enumerate(strong_a_rows, start=1):
        b = row_obj["b"]
        wins = [strat for strat in STRATS if (tag(row_obj[strat]) or "").endswith("投A")]
        need = "B需要拿出更硬的收入/订单/客户/产品代际证据，或显著改善增长、催化和短线关注度。"
        if b["scores"]["下行保护优先"] > a["scores"]["下行保护优先"]:  # type: ignore[index,operator]
            need = "B即使更稳，也需要证明上行或近端催化足以抵消CBRS的OpenAI/AWS高增长右尾。"
        out.append(base.row([index, base.short_name(b), "、".join(wins), row_obj["key_reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        "- 公司 A 公司调研文件：`公司调研/AI计算芯片_EDA_IP_custom_ASIC/CBRS_Cerebras Systems Inc_公司调研_2026-06-30.md`。",
        "- 关键行业资料：`行业调研/AI服务器_存储_芯片/行业调研_商用AI加速芯片_2026-06-10.md`；`行业调研/AI服务器_存储_芯片/行业调研_云厂自研AI ASIC_2026-06-10.md`；`行业调研/AI服务器_存储_芯片/行业调研_AI集群调度与推理运行时_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_片上SRAM、MRAM与近存计算_2026-06-11.md`；`行业调研/AI服务器_存储_芯片/行业调研_AI芯片先进封装_2026-06-11.md`；`行业调研/产业背景/行业调研_头部AI芯片全景与产能释放_2026-06-10.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 ticker 如有多份则取文件名日期最新；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`分析报告/公司排序/`、`分析报告/简单排序/`、项目根 `tmp/` 或 `特征量化/` 作为本报告输入。",
        "- 项目日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-29.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-23.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-23.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-23.md`。",
        f"- 项目日度金融数据覆盖：2026-06-29金融快照覆盖项目索引189家，本报告公司评估全集为{n}家；缺少标准价格/估值或本报告补充前无项目价格的公司为 {('、'.join(missing_daily) if missing_daily else '无')}。CBRS因未进入项目日度快照，使用外部公开报价补充，估值/动量结论降低置信度。",
        f"- 公司 A 日度数据摘录：{daily_snapshot}",
        "- 外部补充金融来源：Google Finance `CBRS:NASDAQ`（2026-06-30，日内区间、市值）；Robinhood `CBRS`（2026-06-30，价格/市值/PE口径）；TradingView `NASDAQ:CBRS`（2026-06-30，市值、历史高低点、波动率、beta、下一财报日期）；MarketWatch/IBD（2026-06-25前后，Q1财报后股价、毛利指引和投资者反应）。",
        "- 其他主要来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`，以及各正式公司评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "- 自动化脚本：`scripts/generate_cbrs_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对全项目强AI/电力/平台标的使用既有正式脚本的最低分校准，对CBRS的OpenAI 750MW、RPO、FY2026指引、AWS解耦推理、模型API、现金、毛利压力、数据中心租赁、估值源冲突和上市后价格波动做目标公司校准后建档；未读取下游量化目录、现成排序结论或既有公司对比结果。",
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
        raise SystemExit("缺少 CBRS 正式评估文件")
    score_companies(companies)
    comparisons = build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "cbrs_tiers": companies[TARGET]["tiers"],
        "cbrs_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
        "cbrs_ranks": companies[TARGET]["ranks"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
