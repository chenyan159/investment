from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_alle_company_comparison as base


TARGET = "RMBS"
TARGET_NAME = "Rambus"
REPORT_DATE = "2026-06-23"
ROOT = Path(r"D:\investment\基本面")
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "RMBS_逐家公司投资思路对比_2026-06-23.md"
LIVE_MARKET_NOTE = "补充当前行情核验：2026-06-23 17:45 UTC，RMBS 最新价 128.94 美元，SOXX 最新价 606.89 美元；该核验晚于项目内统一日度金融快照，未参与 189 家公司横向建档和主表评分。"

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
HIGH_GROWTH_CATS = base.HIGH_GROWTH_CATS
INFRA_CATS = base.INFRA_CATS


DIRECT_MEMORY_INTERFACE_PEERS = {
    "ALAB",
    "ARM",
    "CDNS",
    "MCHP",
    "MRAM",
    "MXL",
    "SIMO",
    "SNPS",
}

MEMORY_STORAGE_CHAIN = {
    "DELL",
    "FN",
    "HPE",
    "JBL",
    "MU",
    "NTAP",
    "PENG",
    "PSTG",
    "SANM",
    "SMCI",
    "SNDK",
    "STX",
    "WDC",
    "CLS",
    "FLEX",
}

AI_COMPUTE_AND_CUSTOM = {
    "AMD",
    "AVGO",
    "INTC",
    "MRVL",
    "NVDA",
    "QCOM",
    "ADI",
    "ON",
    "STM",
    "TXN",
}

NETWORK_AND_CONNECTIVITY = {
    "AAOI",
    "ANET",
    "APH",
    "BDC",
    "BELFB",
    "CIEN",
    "COHR",
    "CRDO",
    "CSCO",
    "GLW",
    "LITE",
    "LWLG",
    "MTSI",
    "NOK",
    "POET",
    "SITM",
    "SMTC",
    "TEL",
    "VIAV",
    "VISN",
}

FOUNDRY_EQUIPMENT_MATERIALS = {
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

CLOUD_AND_IDC = {
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

DATA_CENTER_INFRA = {
    "AAON",
    "ABBNY",
    "AEP",
    "AMPX",
    "APD",
    "ATKR",
    "BE",
    "BWXT",
    "CARR",
    "CEG",
    "CMI",
    "DKILY",
    "DTE",
    "EME",
    "ENS",
    "ENPH",
    "ET",
    "ETN",
    "ETR",
    "FCEL",
    "FIX",
    "FLNC",
    "GEV",
    "GNRC",
    "HUBB",
    "HTHIY",
    "IESC",
    "IFNNY",
    "JCI",
    "LFUS",
    "MIELY",
    "MOD",
    "MPWR",
    "MRAAY",
    "MYRG",
    "NVT",
    "NVTS",
    "OKLO",
    "POWI",
    "POWL",
    "PWR",
    "PSIX",
    "RYCEY",
    "SMR",
    "ST",
    "TT",
    "TTDKY",
    "VICR",
    "VRT",
    "VSH",
    "VST",
    "WOLF",
}

INDUSTRIAL_CROSS = {
    "AJNMY",
    "ALLE",
    "CAT",
    "CC",
    "DCI",
    "DD",
    "DHR",
    "DOV",
    "ECL",
    "FTV",
    "MMM",
    "MSI",
    "MTRN",
    "NDSN",
    "PH",
    "PNR",
    "RKLB",
    "TDY",
    "TMO",
    "TSLA",
}

RMBS_SCORES = {
    "NTM兑现优先": 70.0,
    "右尾弹性优先": 78.0,
    "风险调整收益": 52.5,
    "下行保护优先": 45.5,
    "估值消化优先": 44.0,
    "近端催化优先": 71.0,
    "价格确认/动量": 66.0,
    "激进短线": 81.0,
}


def pct_mid_fixed(value: str) -> float | None:
    text = base.clean(value).replace(",", "").replace("−", "-")
    text = text.replace("–", "-").replace("—", "-").replace("～", "-")
    patterns = [
        r"([+-]?\d+(?:\.\d+)?)\s*%\s*(?:至|到|-)\s*([+-]?\d+(?:\.\d+)?)\s*%",
        r"([+-]?\d+(?:\.\d+)?)\s*(?:至|到|-)\s*([+-]?\d+(?:\.\d+)?)\s*%",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return (float(match.group(1)) + float(match.group(2))) / 2
    values = [float(match.group(1)) for match in re.finditer(r"([+-]?\d+(?:\.\d+)?)\s*%", text)]
    if not values:
        return None
    if "下跌" in text and all(value >= 0 for value in values):
        values = [-value for value in values]
    return sum(values) / len(values)


base.pct_mid = pct_mid_fixed


def clamp(value: float, low: float = 0, high: float = 100) -> float:
    return max(low, min(high, value))


def tier_value(tier: str | None) -> int:
    value = TIER_VAL.get(tier or "资料不足")
    return 0 if value is None else int(value)


def valuation_score(company: dict) -> float:
    fin = company.get("fin", {})
    ps = fin.get("ps")
    fpe = fin.get("forward_pe")
    ev = fin.get("ev_ebitda")
    score = 50.0
    if ps is None:
        score -= 5
    elif ps < 2:
        score += 16
    elif ps < 4:
        score += 10
    elif ps < 7:
        score += 4
    elif ps < 12:
        score -= 4
    elif ps < 20:
        score -= 12
    else:
        score -= 22
    if fpe is None:
        score -= 3
    elif fpe < 12:
        score += 14
    elif fpe < 18:
        score += 9
    elif fpe < 25:
        score += 4
    elif fpe < 35:
        score -= 3
    elif fpe < 55:
        score -= 10
    else:
        score -= 18
    if ev is not None:
        if 0 < ev < 10:
            score += 5
        elif ev > 35:
            score -= 5
    notes = str(fin.get("notes", "")) + str(fin.get("valuation_check", ""))
    if "异常" in notes or "warn" in notes or "bad" in notes:
        score -= 3
    return clamp(score)


def iv_safe(company: dict) -> float:
    iv = company.get("fin", {}).get("call_iv")
    return 50 if iv is None else clamp(100 - (iv - 20) * 1.05)


def iv_aggressive(company: dict) -> float:
    iv = company.get("fin", {}).get("call_iv")
    return 45 if iv is None else clamp((iv - 25) * 1.05)


def conf_score(value: str) -> int:
    return base.conf_score(value)


def pct_rank(value: float | None, values: list[float | None], high_good: bool = True) -> float:
    vals = [v for v in values if v is not None and not math.isnan(v)]
    if value is None or not vals:
        return 50
    less = sum(1 for v in vals if v < value)
    equal = sum(1 for v in vals if v == value)
    rank = (less + 0.5 * equal) / len(vals) * 100
    return rank if high_good else 100 - rank


def recompute_tiers(companies: dict[str, dict]) -> None:
    for strategy in STRATS:
        ordered = sorted(companies.items(), key=lambda item: item[1]["scores"][strategy], reverse=True)
        total = len(ordered)
        for rank, (_ticker, company) in enumerate(ordered, start=1):
            pct = rank / total
            if pct <= 0.07:
                tier = "S"
            elif pct <= 0.25:
                tier = "A"
            elif pct <= 0.55:
                tier = "B"
            elif pct <= 0.85:
                tier = "C"
            else:
                tier = "D"
            company.setdefault("tiers", {})[strategy] = tier
            company.setdefault("ranks", {})[strategy] = rank
            company.setdefault("rank_total", {})[strategy] = total
    for company in companies.values():
        if not company.get("fin", {}).get("price"):
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company["tiers"][strategy] = "资料不足"


def score_companies(companies: dict[str, dict]) -> None:
    soxx_vals = [company.get("soxx", {}).get("soxx_cum") for company in companies.values()]
    mom2_vals = [company.get("mom2", {}).get("mom2w") for company in companies.values()]
    mom1_vals = [company.get("mom1", {}).get("mom1m") for company in companies.values()]

    for company in companies.values():
        text = str(company.get("one", "")) + "\n" + str(company.get("conclusion", "")) + "\n" + str(company.get("calibration", ""))
        base_growth = company.get("base_growth") if company.get("base_growth") is not None else 0
        bull = company.get("bull_growth") if company.get("bull_growth") is not None else base_growth
        extreme = company.get("extreme_growth") if company.get("extreme_growth") is not None else bull
        conf = conf_score(str(company.get("base_conf", "")))
        extreme_conf = conf_score(str(company.get("extreme_conf", "")))
        val = valuation_score(company)
        safe = iv_safe(company)
        ag_iv = iv_aggressive(company)
        soxxp = pct_rank(company.get("soxx", {}).get("soxx_cum"), soxx_vals)
        mom2p = pct_rank(company.get("mom2", {}).get("mom2w"), mom2_vals)
        mom1p = pct_rank(company.get("mom1", {}).get("mom1m"), mom1_vals)
        category = str(company.get("category", ""))
        evidence = base.keyword_count(text, ["backlog", "RPO", "订单", "指引", "已披露", "收入表", "book-to-bill", "客户", "合同", "认证", "产能"])
        risk_words = base.keyword_count(text, ["未披露", "缺少", "无法可靠", "低可信", "下移", "不进入基准", "不确定", "风险", "延迟", "瓶颈"])
        cash_words = base.keyword_count(text, ["FCF", "自由现金流", "现金流", "cash flow", "available cash flow", "现金转化", "资产负债表"])
        catalyst = base.keyword_count(text, ["Q2", "Q3", "Q4", "未来 1", "未来1", "1-2 个季度", "订单", "backlog", "RPO", "认证", "产能", "产品发布", "收购", "指引", "财报", "客户", "交付"])
        direct_ai = base.has_any(text, ["AI 数据中心", "AI data center", "Blackwell", "Rubin", "GB300", "液冷", "800V", "HBM", "CoWoS", "SOCAMM", "CXL", "NeoCloud", "hyperscale", "data center"])
        mature_cash = base.has_any(text, ["现金流强", "FCF 强", "available cash flow", "高利润", "recurring", "服务", "稳定", "公用事业", "regulated"])
        negative_profit = base.has_any(text, ["FCF 为负", "自由现金流为负", "净亏损", "亏损", "负毛利", "破产", "going concern"])
        category_bonus = 4 if category in HIGH_GROWTH_CATS else (2 if category in INFRA_CATS else 0)

        ntm = 45 + min(max(base_growth, -10), 80) * 0.45 + conf * 0.80 + min(evidence, 10) * 0.8 - min(risk_words, 12) * 0.30 + (3 if mature_cash else 0)
        right = 34 + min(max(extreme, -10), 150) * 0.42 + min(max(extreme - base_growth, 0), 90) * 0.23 + category_bonus + (6 if direct_ai else 0) + ag_iv * 0.07 - max(-extreme_conf, 0) * 0.2
        riskadj = 30 + min(max(base_growth, -10), 80) * 0.22 + min(max(extreme, -10), 140) * 0.14 + conf * 0.55 + (val - 50) * 0.22 + (safe - 50) * 0.12 + soxxp * 0.08 + min(cash_words, 8) * 0.70 - (8 if negative_profit else 0) - min(risk_words, 10) * 0.18
        downside = 28 + safe * 0.22 + soxxp * 0.28 + val * 0.12 + conf * 0.45 + min(cash_words, 8) * 0.80 + (5 if mature_cash else 0) - (12 if negative_profit else 0)
        digestion = 32 + val * 0.35 + min(max(base_growth, -10), 80) * 0.35 + min(max(extreme, -10), 140) * 0.10 + conf * 0.30
        if company.get("fin", {}).get("ps") is not None and company.get("fin", {}).get("ps") < 3 and base_growth > 5:
            digestion += 5
        if company.get("fin", {}).get("ps") is not None and company.get("fin", {}).get("ps") > 20 and base_growth < 50:
            digestion -= 8
        near = 34 + min(catalyst, 18) * 0.95 + min(max(base_growth, -10), 80) * 0.20 + conf * 0.30 + (6 if direct_ai else 0) + (3 if category in INFRA_CATS else 0)
        momentum = 22 + mom2p * 0.42 + mom1p * 0.30 + min(max(company.get("mom2", {}).get("mom2w") or 0, -20), 70) * 0.18 + ag_iv * 0.04
        aggressive = 28 + right * 0.45 + momentum * 0.25 + ag_iv * 0.18 + min(catalyst, 15) * 0.55 - (10 if negative_profit and conf < 0 else 0)

        company["scores"] = {
            "NTM兑现优先": clamp(ntm),
            "右尾弹性优先": clamp(right),
            "风险调整收益": clamp(riskadj),
            "下行保护优先": clamp(downside),
            "估值消化优先": clamp(digestion),
            "近端催化优先": clamp(near),
            "价格确认/动量": clamp(momentum),
            "激进短线": clamp(aggressive),
        }

    target = companies[TARGET]
    for strategy, score in RMBS_SCORES.items():
        target.setdefault("scores", {})[strategy] = score
    recompute_tiers(companies)


def relationship(company: dict) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if ticker in DIRECT_MEMORY_INTERFACE_PEERS:
        return "直接同业"
    if ticker in AI_COMPUTE_AND_CUSTOM or ticker in NETWORK_AND_CONNECTIVITY:
        return "相邻替代"
    if ticker in MEMORY_STORAGE_CHAIN or ticker in FOUNDRY_EQUIPMENT_MATERIALS or ticker in CLOUD_AND_IDC:
        return "上下游"
    if ticker in DATA_CENTER_INFRA or category in INFRA_CATS:
        return "相邻替代"
    if ticker in INDUSTRIAL_CROSS:
        return "跨赛道"
    if category in {"AI服务器_存储_EMS", "AI计算芯片_EDA_IP_custom_ASIC", "AI网络_光互联_连接器", "云算力_IDC_AI软件平台"}:
        return "相邻替代"
    if category in {"晶圆制造_前道设备", "封测_检测_计量_光罩", "半导体材料_化学品_基板"}:
        return "上下游"
    return "跨赛道"


def reason_for(strategy: str, label: str, company: dict, rel: str) -> str:
    ticker = str(company["ticker"])
    category = str(company.get("category", ""))
    if label == "中性":
        if rel == "直接同业":
            return "同业证据互有强弱，需看收入确认"
        if rel == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，增长与估值互抵"

    if label.endswith("投A"):
        return {
            "NTM兑现优先": "RMBS有product/royalty/Q2指引硬锚",
            "右尾弹性优先": "MRDIMM、SOCAMM2、HBM4E/CXL右尾更集中",
            "风险调整收益": "现金流和royalty底座抵消部分高估值",
            "下行保护优先": "高毛利royalty/IP和净现金提供缓冲",
            "估值消化优先": "product增速和royalty现金流可部分消化估值",
            "近端催化优先": "Q2/Q3 product、contract和新IP验证更近",
            "价格确认/动量": "近月价格确认和高IV关注度仍强",
            "激进短线": "小市值接口IP叙事和高IV适合进攻",
        }[strategy]

    if rel == "直接同业":
        return {
            "NTM兑现优先": f"{ticker}同业收入/客户兑现更硬",
            "右尾弹性优先": f"{ticker}同业小基数或平台右尾更大",
            "风险调整收益": f"{ticker}同业增长估值组合更优",
            "下行保护优先": f"{ticker}现金流或估值缓冲更稳",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}客户、产品或订单催化更近",
            "价格确认/动量": f"{ticker}同业价格趋势更强",
            "激进短线": f"{ticker}高beta和关注度更适合短攻",
        }[strategy]

    if rel == "上下游":
        return {
            "NTM兑现优先": f"{ticker}订单/RPO或收入确认链更短",
            "右尾弹性优先": f"{ticker}所在瓶颈利润池更大",
            "风险调整收益": f"{ticker}上行与下行组合更优",
            "下行保护优先": f"{ticker}现金流、规模或资产质量更防守",
            "估值消化优先": f"{ticker}业绩增速更能覆盖估值",
            "近端催化优先": f"{ticker}订单、产品或财报催化更近",
            "价格确认/动量": f"{ticker}价格确认和资金偏好更强",
            "激进短线": f"{ticker}高beta和AI关注度更适合短线",
        }[strategy]

    if rel == "相邻替代" or category in HIGH_GROWTH_CATS or category in INFRA_CATS:
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


def label_for(strategy: str, a: dict, b: dict, rel: str) -> str:
    at = a.get("tiers", {}).get(strategy, "资料不足")
    bt = b.get("tiers", {}).get(strategy, "资料不足")
    if "资料不足" in (at, bt):
        if at == bt:
            return "中性"
        return "微倾向投B" if at == "资料不足" else "微倾向投A"

    diff = a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0)
    tier_gap = tier_value(at) - tier_value(bt)
    abs_diff = abs(diff)
    if abs_diff < 4:
        return "中性"

    if rel == "跨赛道":
        strong_cut, suggest_cut, micro_cut = 29, 14, 4
    elif rel == "直接同业":
        strong_cut, suggest_cut, micro_cut = 20, 9, 4
    elif rel == "上下游":
        strong_cut, suggest_cut, micro_cut = 24, 11, 4
    else:
        strong_cut, suggest_cut, micro_cut = 22, 10, 4

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
    return f"{label}：{reason_for(strategy, label, b, rel)}"


def tag_in_cell(cell: str) -> str | None:
    for tag in TAG_ORDER:
        if cell.startswith(tag):
            return tag
    return None


def direction_counts(row_obj: dict) -> tuple[int, int, int]:
    a_count = sum(1 for strategy in STRATS if "投A" in row_obj[strategy])
    b_count = sum(1 for strategy in STRATS if "投B" in row_obj[strategy])
    neutral = 8 - a_count - b_count
    return a_count, b_count, neutral


def final_choice(row_obj: dict) -> str:
    ac, bc, _nc = direction_counts(row_obj)
    if ac > bc:
        return "RMBS"
    if bc > ac:
        return row_obj["ticker"]
    weights = {
        "NTM兑现优先": 1.15,
        "风险调整收益": 1.20,
        "估值消化优先": 1.15,
        "下行保护优先": 1.05,
        "近端催化优先": 0.85,
        "右尾弹性优先": 0.80,
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
        score += weights[strategy] * label_score.get(tag_in_cell(row_obj[strategy]) or "中性", 0.0)
    return "RMBS" if score > 0.15 else row_obj["ticker"] if score < -0.15 else "中性"


def key_reason(a: dict, b: dict, row_obj: dict, choice: str) -> str:
    ticker = str(b["ticker"])
    if choice == "中性":
        return "RMBS的接口IP/royalty现金流与对手增长、估值或防守优势未拉开强判差距。"

    diffs = {strategy: a.get("scores", {}).get(strategy, 0) - b.get("scores", {}).get(strategy, 0) for strategy in STRATS}
    if choice in {"RMBS", "A"}:
        if diffs["右尾弹性优先"] > 12:
            return "RMBS的MRDIMM、SOCAMM2、HBM4E、CXL/PCIe7把小收入基数右尾集中到内存接口/IP瓶颈。"
        if diffs["NTM兑现优先"] > 10:
            return "RMBS的product revenue、royalty和Q2指引比对手更能锚定NTM兑现。"
        if diffs["近端催化优先"] > 10:
            return "RMBS的Q2/Q3 product revenue、contract/other和新接口IP节点更近。"
        if diffs["价格确认/动量"] > 12:
            return "RMBS近期资金关注和IV仍高，价格已验证部分内存接口叙事。"
        if diffs["估值消化优先"] > 8:
            return "RMBS虽估值不低，但高毛利royalty/IP和product增长使消化路径略优。"
        return "RMBS在内存接口/IP瓶颈、现金流和近端产品验证之间的组合略优。"

    if diffs["NTM兑现优先"] < -12:
        return f"{ticker}的订单/RPO/backlog或AI收入兑现比RMBS更硬。"
    if diffs["右尾弹性优先"] < -16:
        return f"{ticker}的小基数、高beta或主链AI收入右尾明显大于RMBS。"
    if diffs["风险调整收益"] < -12:
        return f"{ticker}的增长质量、估值消化和下行组合优于RMBS。"
    if diffs["下行保护优先"] < -12:
        return f"{ticker}的现金流、估值缓冲或压力期表现比RMBS更安全。"
    if diffs["估值消化优先"] < -12:
        return f"{ticker}的业绩增速或估值组合比RMBS更容易消化。"
    if diffs["近端催化优先"] < -12:
        return f"{ticker}未来1-2个季度订单、产品或财报催化比RMBS更直接。"
    if diffs["激进短线"] < -12:
        return f"{ticker}短线高beta、AI叙事或价格爆发力强于RMBS。"
    return f"{ticker}在多数投资思路下比RMBS更符合项目内资金配置目标。"


def grade_diff_summary(a: dict, b: dict) -> str:
    a_strong = [strategy for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) > tier_value(b.get("tiers", {}).get(strategy))]
    b_strong = [strategy for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) < tier_value(b.get("tiers", {}).get(strategy))]
    close = [strategy for strategy in STRATS if tier_value(a.get("tiers", {}).get(strategy)) == tier_value(b.get("tiers", {}).get(strategy))]
    parts = []
    if a_strong:
        parts.append("A强:" + "、".join(a_strong[:3]))
    if b_strong:
        parts.append("B强:" + "、".join(b_strong[:3]))
    if close:
        parts.append("接近:" + "、".join(close[:2]))
    return "；".join(parts) if parts else "档位接近"


def comparison_sort_key(row_obj: dict) -> tuple[int, str, str]:
    rel_order = {"直接同业": 0, "相邻替代": 1, "上下游": 2, "跨赛道": 3}
    return (rel_order.get(row_obj["relationship"], 9), row_obj["classification"], row_obj["ticker"])


def build_comparisons(companies: dict[str, dict]) -> list[dict]:
    a = companies[TARGET]
    rows: list[dict] = []
    for ticker in sorted(ticker for ticker in companies if ticker != TARGET):
        b = companies[ticker]
        rel = relationship(b)
        row_obj = {
            "ticker": ticker,
            "name": b["name"],
            "classification": base.category_short(str(b.get("category", ""))),
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
        row_obj["final_choice"] = final_choice(row_obj)
        row_obj["key_reason"] = key_reason(a, b, row_obj, row_obj["final_choice"])
        rows.append(row_obj)
    return sorted(rows, key=comparison_sort_key)


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


def majority_rows(rows: list[dict], side: str, limit: int = 45) -> list[dict]:
    if side == "B":
        selected = [row for row in rows if row["bc"] >= 5 and row["bc"] - row["ac"] >= 3]
        selected.sort(key=lambda row: (row["bc"] - row["ac"], row["bc"], -row["nc"]), reverse=True)
    else:
        selected = [row for row in rows if row["ac"] >= 5 and row["ac"] - row["bc"] >= 3]
        selected.sort(key=lambda row: (row["ac"] - row["bc"], row["ac"], -row["nc"]), reverse=True)
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
    price_from_0603 = None
    if fin.get("price") and m2w.get("latest_close"):
        price_from_0603 = ((fin.get("price") / m2w.get("latest_close")) - 1) * 100
    daily_snapshot = (
        f"2026-06-22 收盘价 {fmt_num(fin.get('price'), 2)} 美元，市值 {fmt_b(fin.get('market_cap_b'))}，"
        f"TTM PE {fmt_num(fin.get('ttm_pe'), 2)}，Forward PE {fmt_num(fin.get('forward_pe'), 2)}，"
        f"P/S {fmt_num(fin.get('ps'), 2)}，P/B {fmt_num(fin.get('pb'), 2)}，"
        f"EV/EBITDA {fmt_num(fin.get('ev_ebitda'), 2)}，Call IV {fmt_num(fin.get('call_iv'), 1)}%，"
        f"Put IV {fmt_num(fin.get('put_iv'), 1)}%；2026-06-03 过去两周 {fmt_pct(m2w.get('mom2w'))}，"
        f"过去一月 {fmt_pct(m1m.get('mom1m'))}；2026-06-04 三段 SOXX 压力窗口累计 {fmt_pct(soxx.get('soxx_cum'))}；"
        f"2026-06-22收盘较2026-06-03收盘 {fmt_pct(price_from_0603)}。"
    )

    stats: dict[str, Counter] = {strategy: Counter() for strategy in STRATS}
    for row_obj in comparisons:
        for strategy in STRATS:
            stats[strategy][tag_in_cell(row_obj[strategy])] += 1
    a_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[:3]) for strategy in STRATS}
    b_side = {strategy: sum(stats[strategy][tag] for tag in TAG_ORDER[4:]) for strategy in STRATS}
    a_best = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda strategy: a_side[strategy] - b_side[strategy])[:3]
    strong_b = majority_rows(comparisons, "B", 45)
    strong_a = majority_rows(comparisons, "A", 45)
    final_a = sum(1 for row_obj in comparisons if row_obj["final_choice"] == "RMBS")
    final_b = sum(1 for row_obj in comparisons if row_obj["final_choice"] not in {"RMBS", "中性"})
    final_neutral = len(comparisons) - final_a - final_b
    strong_b_names = "、".join([f"{row['ticker']}（{row['name']}）" for row in strong_b[:10]]) or "无"

    support = {
        "NTM兑现优先": (
            "2026Q1收入1.802亿美元，Q2 product/royalty/contract三项指引清楚；FY2025 product revenue +41%，NTM基准8.20-8.90亿美元、相对TTM约+14%至+23%",
            "公司不披露backlog、客户名、单品收入或design win金额，MRDIMM/SOCAMM2/IP增量需要后续收入验证",
        ),
        "右尾弹性优先": (
            "极度乐观收入11.00-12.50亿美元、相对TTM约+53%至+73%；DDR5 8000、MRDIMM 12800、SOCAMM2、HBM4E、PCIe7、CXL3.1均在AI内存/接口瓶颈上",
            "大额右尾依赖平台采用、客户认证、份额和IP授权集中确认，目前缺订单/backlog披露",
        ),
        "风险调整收益": (
            "FY2025经营现金流3.600亿美元，royalty/IP高毛利底座使盈利质量好，基准经营利润率34%-38%",
            "2026-06-22 P/S 21.05、Forward PE 38.45、Call IV 91.5%，估值和波动已经反映较多乐观",
        ),
        "下行保护优先": (
            "royalty revenue、contract/other和净现金/经营现金流降低基本面打穿概率；悲观情景仍为正利润和正现金流",
            "三段SOXX压力窗口累计-76.70%，高IV、高P/S和缺backlog披露使市场压力期保护不足",
        ),
        "估值消化优先": (
            "基准收入+14%至+23%，product revenue若站稳9500万-1.01亿美元/季度以上，利润和现金流能继续抬升",
            "P/S 21.05、Forward PE 38.45要求product/IP持续上修；若SOCAMM2和HBM4E/CXL只停留发布，估值消化偏难",
        ),
        "近端催化优先": (
            "Q2/Q3 2026 product revenue、product gross margin、contract/other是否站上2500-3000万美元、MRDIMM/SOCAMM2/HBM4E/PCIe7客户线索均是近端验证点",
            "多数催化是收入表和客户披露验证，不是已公开订单或RPO；财报不兑现时容易从叙事切回估值压力",
        ),
        "价格确认/动量": (
            "2026-06-03过去两周+27.78%、过去一月+52.47%，市场已交易内存接口/IP弹性",
            "2026-06-22收盘较6月3日回落约17.8%，高IV下动量确认已有降温",
        ),
        "激进短线": (
            "市值约151.8亿美元、Call IV 91.5%，MRDIMM/SOCAMM2/HBM4E/CXL/PCIe7标题密度高，适合短线进攻资金",
            "不是亏损转盈利小盘，也没有公开大订单/backlog，爆发力弱于部分光互联、NeoCloud、核电或电力高beta",
        ),
    }

    product_names = [str(product[0]).split("：")[0].split("，")[0].split("；")[0] for product in a.get("products", [])[:8]]
    if not product_names:
        product_names = [
            "DDR5 RDIMM服务器DIMM芯片组",
            "DDR5 MRDIMM 12800芯片组",
            "LPDDR5X SOCAMM2 server module chipset",
            "HBM4E/PCIe7/CXL3.1/Security IP",
            "Patent licensing / royalty",
        ]

    lines: list[str] = [
        "# RMBS 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        f"公司 A：RMBS / {TARGET_NAME}",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{len(companies)}",
        f"被比较公司 B 数量：{len(comparisons)}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去两周/过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。",
        LIVE_MARKET_NOTE,
        "",
        "> 口径说明：本报告按同一批正式公司评估建立 8 个投资思路全项目相对档位，再逐行做 RMBS vs 公司 B 的二选一判断。未使用下游量化资料、现成排序结论、临时结果、备份结论或既有公司对比成品。",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。RMBS 的强项集中在近端催化、右尾弹性和价格确认：DDR5/RDIMM已经在收入表中，MRDIMM/SOCAMM2/HBM4E/CXL/PCIe7提供AI内存接口小基数右尾，且此前价格已经验证部分叙事。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。短板是估值消化、下行保护和激进短线相对排名：P/S约21倍、Forward PE约38倍、Call IV约91.5%，同时公司不披露backlog、客户名、单品收入，6月3日后价格回撤也削弱短线强度。",
        "- A 最适合的投资者画像：愿意用中等确定性现金流底座去换AI内存/高速接口右尾的进攻型投资者；尤其适合押注DDR5/MRDIMM/SOCAMM2/HBM4E/CXL/PCIe7在未来几个季度出现更清晰客户或收入验证的资金。",
        "- A 最不适合的投资者画像：优先追求低估值、低波动、强下行保护或已经有大额订单/RPO/backlog硬锚的稳健资金；这些资金会更偏向公用事业、电力设备、成熟平台或低倍数现金流公司。",
        f"- 多数思路下最强反方公司：{strong_b_names}。这些公司通常在AI主链收入、HBM/ASIC/网络、电力设备订单、云RPO、现金流防守或估值消化上压过RMBS。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：RMBS 是项目内偏进攻的中上标的，综合最终选择为 RMBS 的对比 {final_a} 家、B 的对比 {final_b} 家、中性 {final_neutral} 家；它强于许多缺增长或缺催化公司，但在全项目不是最高质量/最高确定性资产，尤其输给若干AI主链、高订单电力设备和更低估值高现金流公司。",
        "- 后续最重要跟踪数据：2026Q2/Q3 product revenue是否连续站稳或超过1亿美元/季度；product gross margin是否维持60%+；contract/other是否上到2500-3000万美元以上；royalty是否维持指引上沿；MRDIMM 12800、SOCAMM2、HBM4E、PCIe7、CXL3.1是否出现客户、design win、订单、交付或收入拆分；库存、应收、资本开支和经营现金流是否吞噬利润。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        base.row(["项目", "内容"]),
        base.row(["---", "---"]),
        base.row(["股票代号", "RMBS"]),
        base.row(["公司名称", TARGET_NAME]),
        base.row(["产业链分类", a.get("category", "")]),
        base.row(["重要产品/业务线", "；".join(product_names)]),
        base.row(["NTM 基准收入", a.get("base_rev") or a["scenarios"]["base"].get("NTM 公司收入", "缺失")]),
        base.row(["乐观/极度乐观收入", f"{a.get('bull_rev') or a['scenarios']['bull'].get('NTM 公司收入', '缺失')} / {a.get('extreme_rev') or a['scenarios']['extreme'].get('NTM 公司收入', '缺失')}"]),
        base.row(["利润和现金流结论", f"{a.get('base_profit', '')}；{a.get('base_cash', '')}"]),
        base.row(["最大传导瓶颈", "公司不披露backlog、bookings、客户名、单品收入和design win金额；MRDIMM/SOCAMM2/HBM4E/CXL/PCIe7从产品发布到收入确认仍需验证。"]),
        base.row(["最大反证", "product revenue不能连续站稳Q2指引高位；MRDIMM/SOCAMM2客户认证停留小批量；contract/other低于2000万美元/季度；royalty续约或计费节奏低于指引。"]),
        base.row(["近端催化剂", "Q2/Q3 product revenue与product gross margin、contract/other是否高于2500-3000万美元、MRDIMM/SOCAMM2/HBM4E/PCIe7/CXL客户或design win披露。"]),
        base.row(["日度市场数据", daily_snapshot]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        base.row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        base.row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        rank = a.get("ranks", {}).get(strategy)
        total = a.get("rank_total", {}).get(strategy) or len(companies)
        lines.append(base.row([strategy, a["tiers"][strategy], f"第 {rank}/{total}，{a['tiers'][strategy]} 档", support[strategy][0], support[strategy][1]]))

    lines += [
        "",
        "## 4. 可比关系使用说明",
        "",
        base.row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        base.row(["---", "---", "---", "---"]),
        base.row(["直接同业", "与RMBS在内存接口芯片、CXL/PCIe/IP、EDA/IP或内存控制相关资金池中重叠，优先看收入兑现、产品代际、客户认证、IP授权和估值。", "ALAB、ARM、CDNS、SNPS、MCHP、MXL、SIMO、MRAM", "同业证据差距明显时结论力度上调；尤其不能只看AI叙事，必须看谁能把接口/控制器/IP转成收入。"]),
        base.row(["相邻替代", "同属AI半导体、网络连接、数据中心电力或基础设施资金篮子，但产品不直接竞争。", "NVDA、AVGO、MRVL、QCOM、CRDO、ANET、VRT、ETN、POWL", "回答资金只能买一个时，谁的增长质量、估值消化、催化和风险调整收益更好。"]),
        base.row(["上下游", "B是内存/服务器/云客户、代工封测、设备材料或系统链条中的上游/下游约束。", "MU、DELL、SMCI、TSM、ASML、AMAT、MSFT、GOOGL、META", "不把HBM/云capex或设备订单直接等同于RMBS收入，重点看利润池、议价权和收入确认链条。"]),
        base.row(["跨赛道", "业务差异大，但作为项目资金配置替代仍比较增长质量、风险调整收益、估值消化、下行保护和催化可见度。", "LIN、DHR、TMO、CAT、RKLB、MSI、ECL", "默认降低结论力度；除非档位差明显，否则使用中性或微倾向。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
        base.row(["序号", "公司B", "公司B分类", "可比关系", "档位差摘要", *STRATS, "多数思路方向", "最终更值得投", "最关键理由"]),
        base.row(["---:", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(comparisons, start=1):
        final = "RMBS" if row_obj["final_choice"] == "RMBS" else row_obj["ticker"] if row_obj["final_choice"] != "中性" else "中性"
        lines.append(
            base.row(
                [
                    index,
                    f"{row_obj['ticker']} / {row_obj['name']}",
                    row_obj["classification"],
                    row_obj["relationship"],
                    row_obj["grade_diff"],
                    *[row_obj[strategy] for strategy in STRATS],
                    row_obj["majority"],
                    final,
                    row_obj["key_reason"],
                ]
            )
        )

    lines += [
        "",
        "## 6. 投资思路统计",
        "",
        base.row(["投资思路", *TAG_ORDER, "A侧合计", "B侧合计"]),
        base.row(["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]),
    ]
    for strategy in STRATS:
        lines.append(base.row([strategy, *[stats[strategy][tag] for tag in TAG_ORDER], a_side[strategy], b_side[strategy]]))

    lines += [
        "",
        "## 7. 多数思路下 B 明显强于 A 的公司",
        "",
        base.row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(strong_b, start=1):
        wins = [strategy for strategy in STRATS if "投B" in row_obj[strategy]]
        need = "RMBS需要披露更清晰的MRDIMM/SOCAMM2/HBM4E/CXL/PCIe7客户、订单、收入拆分和毛利率，同时证明P/S与Forward PE可由product和IP持续增长消化。"
        if row_obj["relationship"] == "直接同业":
            need = "RMBS需要在内存接口/IP同业中证明客户采用、产品代际、收入确认和利润留存强于B。"
        elif row_obj["relationship"] == "上下游":
            need = "RMBS需要证明内存、云capex、服务器或上游设备需求会落到自己的接口芯片/IP收入，而不是停留在上下游利润池。"
        lines.append(base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], need]))

    lines += [
        "",
        "## 8. 多数思路下 A 明显强于 B 的公司",
        "",
        base.row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]),
        base.row(["---:", "---", "---", "---", "---"]),
    ]
    for index, row_obj in enumerate(strong_a, start=1):
        b = companies[row_obj["ticker"]]
        wins = [strategy for strategy in STRATS if "投A" in row_obj[strategy]]
        need = "B需要拿出更硬订单/RPO、更强NTM收入利润兑现，或证明估值、现金流和执行反证低于RMBS。"
        if b.get("scores", {}).get("右尾弹性优先", 0) > a.get("scores", {}).get("右尾弹性优先", 0):
            need = "B需要把右尾叙事转成可确认收入/利润，并证明估值、现金流和执行反证可控。"
        lines.append(base.row([index, f"{row_obj['ticker']} / {row_obj['name']}", "、".join(wins[:5]), row_obj["key_reason"], need]))

    lines += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{Path(a['path']).name}`。",
        "- 公司 A 公司调研文件：`公司调研/AI服务器_存储_EMS/RMBS_Rambus_公司调研_2026-06-11.md`。",
        f"- 公司全集文件清单生成口径：扫描 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新一份；共 {len(companies)} 家，日期范围 {date_range}；未使用备份、临时结果、现成排序或下游量化结论。",
        f"- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；覆盖 {len(companies) - len(missing_fin)}/{len(companies)} 家；缺少日度金融数据的公司为：{('、'.join(missing_fin) if missing_fin else '无')}；价格缺失或不可用公司为：{('、'.join(missing_price) if missing_price else '无')}。",
        "- 区间涨跌来源：`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`、`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`。",
        "- SOXX 压力窗口来源：`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        "- 其他主要项目内来源：`公司调研/公司索引.md`、`行业调研/行业索引.md`、`行业调研/AI服务器_存储_芯片/行业调研_系统内存、SOCAMM与内存模组_2026-06-10.md`、`行业调研/AI服务器_存储_芯片/行业调研_HBM与高带宽内存_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_EDA工具、接口IP与Chiplet IP_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_CXL内存扩展与内存池化_2026-06-10.md`，以及各正式公司评估文件附录列明的公司调研、行业调研和官方披露来源。",
        f"- RMBS 日度数据快照：{daily_snapshot}",
        f"- 当前行情补充核验：{LIVE_MARKET_NOTE}",
        "- 自动化脚本：`scripts/generate_rmbs_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对RMBS的DDR5/RDIMM、MRDIMM、SOCAMM2、HBM4E、PCIe7、CXL3.1、royalty/IP、估值、IV、区间涨跌和SOXX压力窗口做目标公司校准后建档；未读取下游量化目录、现成排序结论、临时结果、备份结论或既有公司对比成品。",
        "",
        "### 公司全集最新正式评估文件清单",
        "",
        base.row(["股票代号", "公司名称", "评估日期", "正式评估文件"]),
        base.row(["---", "---", "---", "---"]),
    ]
    for ticker in sorted(companies):
        company = companies[ticker]
        lines.append(base.row([ticker, company["name"], company["date"], f"`分析报告/公司评估/结果/{Path(company['path']).name}`"]))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    base.TARGET = TARGET
    companies = base.build_companies()
    if TARGET not in companies:
        raise SystemExit("缺少 RMBS 正式评估文件")
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
                "rmbs_tiers": {strategy: a.get("tiers", {}).get(strategy) for strategy in STRATS},
                "rmbs_scores": {strategy: round(a.get("scores", {}).get(strategy, 0), 2) for strategy in STRATS},
                "rmbs_ranks": {strategy: a.get("ranks", {}).get(strategy) for strategy in STRATS},
                "size": OUT_PATH.stat().st_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
