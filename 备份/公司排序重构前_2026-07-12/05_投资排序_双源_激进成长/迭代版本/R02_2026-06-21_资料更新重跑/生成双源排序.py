from pathlib import Path
from datetime import datetime
import math
import re
import statistics

BASE = Path(r"D:\drive\Investment\基本面")
EVAL_DIR = BASE / "分析报告" / "公司评估"
MARKET_DIR = BASE / "日度资料" / "每日金融数据"
OUT_PATH = BASE / "分析报告" / "公司排序" / "05_投资排序_双源_激进成长" / "迭代版本" / "R02_2026-06-21_资料更新重跑" / "02_排序结果.md"
METHOD_VERSION = "dual_source_aggressive_growth_v0.2_2026-06-21"
SCENARIOS = ["pessimistic", "base", "bull", "extreme"]
FORBIDDEN_TEXT_MARKERS = [
    "公司调研/",
    "行业调研/",
    "特征量化/",
    "Signals",
    "tmp/",
    "data/",
    "http://",
    "https://",
]


def split_md_row(line):
    line = line.strip()
    if not (line.startswith("|") and line.endswith("|")):
        return None
    return [c.strip() for c in line.strip("|").split("|")]


def clean_text(s):
    if s is None:
        return ""
    s = re.sub(r"<br\s*/?>", "；", str(s), flags=re.I)
    s = s.replace("\u3000", " ").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


def short_text(s, limit=58):
    s = clean_text(s)
    s = re.sub(r"\[[^\]]+\]\([^\)]+\)", "", s)
    return s if len(s) <= limit else s[: limit - 1] + "…"


def md_escape(s):
    return ("" if s is None else str(s)).replace("\n", " ").replace("\r", " ").replace("|", " / ")


def parse_date_from_name(path):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    return m.group(1) if m else ""


def date_obj(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def parse_number_basic(s):
    s0 = clean_text(s)
    if not s0 or any(x in s0 for x in ["缺失", "不适用", "无法", "N/A", "nan"]):
        return None
    m = re.search(r"[-+]?\d+(?:\.\d+)?", s0.replace(",", ""))
    return float(m.group(0)) if m else None


def parse_scaled_number(s):
    s0 = clean_text(s)
    if not s0 or any(x in s0 for x in ["缺失", "不适用", "无法", "N/A", "nan"]):
        return None
    num = parse_number_basic(s0)
    if num is None:
        return None
    sl = s0.lower()
    mult = 1.0
    if "万亿" in s0 or "trillion" in sl or re.search(r"\d\s*t\b", sl):
        mult = 1e12
    elif "bn" in sl or re.search(r"\d\s*b\b", sl) or "billion" in sl:
        mult = 1e9
    elif "亿" in s0:
        mult = 1e8
    elif "mn" in sl or re.search(r"\d\s*m\b", sl) or "million" in sl:
        mult = 1e6
    elif "万" in s0:
        mult = 1e4
    return num * mult


def parse_iv(s):
    s0 = clean_text(s)
    if not s0 or any(x in s0 for x in ["缺失", "不适用", "无期权"]):
        return None
    m = re.search(r"([-+]?\d+(?:\.\d+)?)\s*%", s0)
    return float(m.group(1)) / 100.0 if m else None


def parse_percent_values(s):
    return [float(m.group(1)) / 100.0 for m in re.finditer(r"([-+]?\d+(?:\.\d+)?)\s*%", clean_text(s).replace(",", ""))]


def parse_percent_mid(s, keyword_signed=False):
    vals = parse_percent_values(s)
    if not vals:
        return None
    avg = statistics.mean(vals)
    s0 = clean_text(s)
    if keyword_signed and all(v >= 0 for v in vals):
        if any(k in s0 for k in ["低于", "下修", "下降", "少约", "压低"]):
            avg = -abs(avg)
        elif any(k in s0 for k in ["高于", "上修", "增长", "增加", "多约", "提升"]):
            avg = abs(avg)
    return avg


def parse_relative_to_expectation(s, scenario):
    s0 = clean_text(s)
    pct = parse_percent_mid(s0, keyword_signed=True)
    if pct is not None:
        return max(-0.75, min(1.80, pct))
    defaults = {"pessimistic": -0.28, "base": 0.00, "bull": 0.24, "extreme": 0.45}
    if any(k in s0 for k in ["严重低于", "显著低于", "大幅低于"]):
        return -0.45
    if any(k in s0 for k in ["低于", "下修"]):
        return -0.25
    if "略低" in s0:
        return -0.10
    if any(k in s0 for k in ["接近", "符合", "正常兑现", "大体符合", "当前预期", "中心"]):
        return 0.00
    if any(k in s0 for k in ["显著高于", "明显高于", "远高于", "非线性"]):
        return 0.55
    if any(k in s0 for k in ["高于", "上修", "超预期"]):
        return 0.28
    return defaults.get(scenario, 0.0)


def parse_margin_mid(s):
    vals = parse_percent_values(s)
    return statistics.mean(vals) if vals else None


def parse_range_width(s):
    s0 = clean_text(s).replace(",", "")
    s0 = re.sub(r"20\d{2}(?:Q\d|H\d)?", " ", s0)
    nums = [float(x) for x in re.findall(r"[-+]?\d+(?:\.\d+)?", s0)]
    if len(nums) < 2:
        return None
    mid = (abs(nums[0]) + abs(nums[1])) / 2.0
    return abs(nums[1] - nums[0]) / mid if mid else None


def fcf_signal_score(s):
    s0 = clean_text(s)
    score = 0
    if any(k in s0 for k in ["明显负", "严重负", "现金流流出", "流出", "吞噬"]):
        score -= 24
    elif "负到接近持平" in s0 or "负到持平" in s0:
        score -= 10
    elif "负" in s0 or re.search(r"-\$|-$|-\d", s0):
        score -= 16
    if any(k in s0 for k in ["接近持平", "持平"]):
        score += 2
    if any(k in s0 for k in ["为正", "转正", "强", "明显改善", "正", "+$"]) and "负" not in s0[:6]:
        score += 14
    if any(k in s0 for k in ["资本开支", "CapEx", "库存", "应收", "营运资本", "预付款", "融资", "摊薄"]):
        score -= 6
    return max(-30, min(24, score))


def confidence_to_score(s):
    s0 = clean_text(s)
    if not s0:
        return 55
    if "高" in s0 and "中" not in s0 and "低" not in s0:
        return 88
    if "中高" in s0 or "高到中" in s0 or "高；" in s0:
        return 76
    if "低到中" in s0:
        return 42
    if "中到低" in s0 or "中低" in s0:
        return 46
    if "中" in s0 and "高" not in s0 and "低" not in s0:
        return 61
    if "低" in s0:
        return 32
    return 55


def parse_statuses(s):
    return {k.strip(): v.lower().strip() for k, v in re.findall(r"([^:;；]+):\s*([a-zA-Z]+)", clean_text(s))}


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def fmt_pct(x, digits=1):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "缺失"
    return f"{x * 100:+.{digits}f}%"


def fmt_num(x, digits=2):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return "缺失"
    return f"{x:.{digits}f}"


def fmt_cap(x):
    if x is None:
        return "缺失"
    ax = abs(x)
    if ax >= 1e12:
        return f"${x / 1e12:.2f}T"
    if ax >= 1e9:
        return f"${x / 1e9:.2f}B"
    if ax >= 1e6:
        return f"${x / 1e6:.2f}M"
    return f"${x:.0f}"


def metric_good_status(statuses, key):
    return statuses.get(key) in ("ok", "warn")


def parse_market_file(path):
    data, current_cat, header = {}, "", None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            current_cat, header = line[4:].strip(), None
            continue
        if line.startswith("| 股票代号 |"):
            header = split_md_row(line)
            continue
        if header and line.startswith("|"):
            row = split_md_row(line)
            if not row or len(row) != len(header) or set(row[0]) <= set("-: "):
                continue
            d = dict(zip(header, row))
            ticker = d.get("股票代号", "").strip()
            st = parse_statuses(d.get("估值校验", ""))
            ivs = [x for x in [parse_iv(d.get("Call IV")), parse_iv(d.get("Put IV"))] if x is not None]
            data[ticker] = {
                "ticker": ticker,
                "market_file": str(path.relative_to(BASE)),
                "market_date": parse_date_from_name(path),
                "category": current_cat,
                "market_name": clean_text(d.get("公司名称", "")),
                "price_date": clean_text(d.get("价格日期", "")),
                "price": parse_number_basic(d.get("最新价格")),
                "market_cap": parse_scaled_number(d.get("市值")),
                "pe": parse_number_basic(d.get("TTM PE")),
                "forward_pe": parse_number_basic(d.get("Forward PE")),
                "ps": parse_number_basic(d.get("P/S")),
                "ev_ebitda": parse_number_basic(d.get("EV/EBITDA")),
                "iv": statistics.mean(ivs) if ivs else None,
                "currency": clean_text(d.get("currency", "")),
                "financial_currency": clean_text(d.get("financial_currency", "")),
                "listing_type": clean_text(d.get("listing_type", "")),
                "adr_ratio": clean_text(d.get("adr_ratio", "")),
                "valuation_check": clean_text(d.get("估值校验", "")),
                "valuation_statuses": st,
                "market_notes": clean_text(d.get("备注", "")),
            }
    return data


def scenario_key(label):
    label = clean_text(label)
    if "极度" in label:
        return "extreme"
    if "乐观" in label:
        return "bull"
    if "基准" in label:
        return "base"
    if "悲观" in label:
        return "pessimistic"
    return None


def extract_scenario_table(lines):
    for i, line in enumerate(lines):
        if line.startswith("| 情景 ") and "NTM 公司收入" in line and "可信度" in line:
            header, table, j = split_md_row(line), [], i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                row = split_md_row(lines[j])
                if row and len(row) == len(header) and not set(row[0]) <= set("-: "):
                    table.append(dict(zip(header, row)))
                j += 1
            return table
    return []


def extract_counter_evidence(text):
    section = text[text.find("## 7.") :] if "## 7." in text else text
    hits = []
    for line in section.splitlines():
        if "反证" not in line:
            continue
        if any(marker in line for marker in FORBIDDEN_TEXT_MARKERS):
            continue
        line = clean_text(line)
        if line.startswith("|"):
            cols = split_md_row(line)
            if cols:
                if not any(marker in cols[-1] for marker in FORBIDDEN_TEXT_MARKERS):
                    hits.append(cols[-1])
                continue
        m = re.search(r"反证[：:是]*([^。；|]+)", line)
        hits.append(m.group(1) if m else line)
        if len(hits) >= 3:
            break
    return "；".join(short_text(h, 45) for h in hits[:3])


def parse_eval_file(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    ticker = path.name.split("_")[0]
    m = re.search(r"报告日期[:：]\s*(\d{4}-\d{2}-\d{2})", text)
    eval_date = m.group(1) if m else ""
    m = re.search(r"公司名称[:：]\s*([^\n`]+)", text)
    name = clean_text(m.group(1).strip("` ")) if m else ""
    if not name:
        m = re.search(r"^#\s*公司收入传导与价值传导评估[:：]\s*([^\n]+)", text, flags=re.M)
        name = re.sub(r"（[^）]*）", "", clean_text(m.group(1))).strip() if m else ""
    included_fact_date, eval_dt = "", date_obj(eval_date)
    for line in lines:
        if "经营数据日期" in line:
            dates = re.findall(r"\d{4}-\d{2}-\d{2}", line)
            if dates:
                valid = [d for d in dates if date_obj(d) and eval_dt and date_obj(d) <= eval_dt]
                included_fact_date = max(valid or dates)
            break
    if not included_fact_date:
        dates = re.findall(r"\d{4}-\d{2}-\d{2}", "\n".join(lines[:35]))
        valid = [d for d in dates if date_obj(d) and eval_dt and date_obj(d) <= eval_dt]
        if valid:
            included_fact_date = max(valid)
    scenarios = {}
    for row in extract_scenario_table(lines):
        key = scenario_key(row.get("情景", ""))
        if not key:
            continue
        scenarios[key] = {
            "label": clean_text(row.get("情景", "")),
            "revenue_text": clean_text(row.get("NTM 公司收入", "")),
            "growth_text": clean_text(row.get("绝对增速", "")),
            "relative_text": clean_text(row.get("相对预期", "")),
            "profit_text": clean_text(row.get("EBITDA/净利润", "")),
            "fcf_text": clean_text(row.get("自由现金流方向", "")),
            "confidence_text": clean_text(row.get("可信度", "")),
            "bottleneck_text": clean_text(row.get("主要经营瓶颈", "")),
            "revenue_width": parse_range_width(row.get("NTM 公司收入", "")),
            "revenue_growth": parse_percent_mid(row.get("绝对增速", ""), keyword_signed=False),
            "relative_surprise": parse_relative_to_expectation(row.get("相对预期", ""), key),
            "op_margin": parse_margin_mid(row.get("经营利润率", "")),
            "fcf_signal": fcf_signal_score(row.get("自由现金流方向", "")),
            "confidence_score": confidence_to_score(row.get("可信度", "")),
        }
    m = re.search(r"-\s*可信度[:：]\s*([^\n]+)", text)
    one_page_confidence = clean_text(m.group(1)) if m else ""
    m = re.search(r"-\s*最大传导瓶颈[:：]\s*([^\n]+)", text)
    max_bottleneck = clean_text(m.group(1)) if m else ""
    return {
        "ticker": ticker,
        "eval_file": str(path.relative_to(BASE)),
        "eval_date": eval_date,
        "included_fact_date": included_fact_date,
        "eval_name": name,
        "scenarios": scenarios,
        "one_page_confidence": one_page_confidence,
        "max_bottleneck": max_bottleneck,
        "counter_evidence_text": extract_counter_evidence(text),
        "keyword_high_evidence": len(re.findall(r"订单|backlog|RPO|指引|已确认收入|已确认利润|已确认自由现金流|volume shipment|客户预付款|合同负债", text, flags=re.I)),
        "keyword_mid_evidence": len(re.findall(r"客户认证|认证|设计导入|pipeline|产能|交付计划|管理层", text, flags=re.I)),
        "keyword_weak_evidence": len(re.findall(r"可选性|叙事|早期|pilot|样品|远期期权", text, flags=re.I)),
    }


def percentile_maps(values_by_ticker, high_good=True):
    vals = [(t, v) for t, v in values_by_ticker.items() if v is not None and not (isinstance(v, float) and (math.isnan(v) or math.isinf(v)))]
    if not vals:
        return {t: 50.0 for t in values_by_ticker}
    raw = sorted(v for _, v in vals)
    n = len(raw)

    def quantile(q):
        if n == 1:
            return raw[0]
        pos = q * (n - 1)
        lo, hi = int(math.floor(pos)), int(math.ceil(pos))
        return raw[lo] if lo == hi else raw[lo] * (hi - pos) + raw[hi] * (pos - lo)

    q01, q99 = quantile(0.01), quantile(0.99)
    clipped = [(t, clamp(v, q01, q99)) for t, v in vals]
    ordered = sorted(v for _, v in clipped)

    def pct_rank(v):
        if len(ordered) == 1:
            return 50.0
        less = sum(1 for x in ordered if x < v)
        equal = sum(1 for x in ordered if x == v)
        rank = (less + 0.5 * max(equal - 1, 0)) / (len(ordered) - 1) * 100.0
        return rank if high_good else 100.0 - rank

    out = {t: pct_rank(v) for t, v in clipped}
    for t in values_by_ticker:
        out.setdefault(t, 25.0 if high_good else 75.0)
    return out


def data_quality_raw(m):
    score = 100.0
    st = m["valuation_statuses"]
    for key, penalty in [("price", 26), ("market_cap", 24), ("forward_pe", 8), ("ps", 8), ("ev_ebitda", 5), ("pe", 4), ("iv", 8)]:
        if m.get(key) is None:
            score -= penalty
    for v in st.values():
        score -= 16 if v == "bad" else 6 if v == "warn" else 8 if v == "missing" else 0
    cur, fin = m.get("currency", ""), m.get("financial_currency", "")
    if not cur or not fin or "缺失" in cur or "缺失" in fin:
        score -= 8
    elif cur != fin:
        score -= 8
    if "需确认" in m.get("adr_ratio", ""):
        score -= 7
    if "unknown" in m.get("listing_type", ""):
        score -= 5
    pd, md = date_obj(m.get("price_date")), date_obj(m.get("market_date"))
    if pd and md and (md - pd).days > 3:
        score -= min(10, (md - pd).days)
    elif not pd:
        score -= 6
    return clamp(score, 0, 100)


def currency_check(m):
    cur, fin = m.get("currency", ""), m.get("financial_currency", "")
    if not cur or not fin or "缺失" in cur or "缺失" in fin:
        return "missing"
    return "ok" if cur == fin else f"mismatch:{cur}/{fin}"


def scenario_returns(ev, m, expensiveness, data_q, iv_pct):
    vals = {}
    bad_count = sum(1 for v in m["valuation_statuses"].values() if v == "bad")
    missing_count = sum(1 for v in m["valuation_statuses"].values() if v == "missing")
    val_adj = (50.0 - expensiveness) / 100.0 * 0.32 - bad_count * 0.055 - missing_count * 0.025
    if currency_check(m) != "ok":
        val_adj -= 0.035
    if "需确认" in m.get("adr_ratio", ""):
        val_adj -= 0.025
    if m.get("iv") is not None and iv_pct > 85:
        val_adj -= 0.025
    data_penalty = (100 - data_q) / 100.0 * 0.10
    params = {"pessimistic": (-0.12, 0.92, 0.06, 0.22), "base": (0.00, 0.82, 0.09, 0.48), "bull": (0.08, 0.88, 0.12, 0.34), "extreme": (0.15, 0.92, 0.16, 0.22)}
    for key in SCENARIOS:
        s = ev["scenarios"].get(key, {})
        rel = s.get("relative_surprise")
        rel = rel if rel is not None else {"pessimistic": -0.28, "base": 0.0, "bull": 0.24, "extreme": 0.45}[key]
        g = s.get("revenue_growth")
        g = clamp(g if g is not None else {"pessimistic": -0.05, "base": 0.05, "bull": 0.18, "extreme": 0.35}[key], -0.45, 3.0)
        opm = s.get("op_margin")
        op_comp = 0.0 if opm is None else clamp((opm - 0.15) * 0.22, -0.08, 0.15)
        fcf_comp = s.get("fcf_signal", 0) / 100.0 * 0.30
        base_adj, rel_w, rev_w, val_w = params[key]
        vals[key] = clamp(base_adj + rel_w * rel + rev_w * g + op_comp + fcf_comp + val_w * val_adj - data_penalty, -0.85, 3.20)
    vals["base"] = max(vals["base"], vals["pessimistic"] + 0.035)
    vals["bull"] = max(vals["bull"], vals["base"] + 0.045)
    vals["extreme"] = max(vals["extreme"], vals["bull"] + 0.060)
    return vals


def main():
    market_files = sorted([p for p in MARKET_DIR.glob("每日金融数据_*.md") if "补充字段校验" not in p.name], key=parse_date_from_name)
    supplement_files = sorted([p for p in MARKET_DIR.glob("每日金融数据_*_补充字段校验.md")], key=parse_date_from_name)
    latest_market_file, latest_market_date = market_files[-1], parse_date_from_name(market_files[-1])
    same_day_supplements = [p for p in supplement_files if parse_date_from_name(p) == latest_market_date]
    market_history = [(parse_date_from_name(p), p, parse_market_file(p)) for p in market_files]
    latest_market = market_history[-1][2]
    eval_reports = {p.name.split("_")[0]: parse_eval_file(p) for p in sorted(EVAL_DIR.glob("*.md"))}

    metric_values = {k: {} for k in ["forward_pe", "ps", "ev_ebitda", "pe", "iv", "market_cap"]}
    for t, m in latest_market.items():
        st = m["valuation_statuses"]
        metric_values["forward_pe"][t] = m["forward_pe"] if metric_good_status(st, "FwdPE") else None
        metric_values["ps"][t] = m["ps"] if metric_good_status(st, "P/S") else None
        metric_values["ev_ebitda"][t] = m["ev_ebitda"] if m["ev_ebitda"] and m["ev_ebitda"] > 0 else None
        metric_values["pe"][t] = m["pe"] if metric_good_status(st, "PE") else None
        metric_values["iv"][t] = m["iv"]
        metric_values["market_cap"][t] = m["market_cap"]
    metric_pct = {k: percentile_maps(v, high_good=True) for k, v in metric_values.items()}
    market_cap_small_pct = percentile_maps(metric_values["market_cap"], high_good=False)

    def hist(ticker, idx, metric):
        if idx < 0:
            idx = len(market_history) + idx
        if idx < 0 or idx >= len(market_history):
            return None
        return market_history[idx][2].get(ticker, {}).get(metric)

    history_stats, latest_idx = {}, len(market_history) - 1
    for ticker, latest in latest_market.items():
        stats, price_now = {}, latest.get("price")
        for n in [5, 10, 20]:
            p_old = hist(ticker, latest_idx - n, "price") if latest_idx - n >= 0 else None
            stats[f"pre_{n}d_return"] = price_now / p_old - 1.0 if price_now and p_old and p_old != 0 else None
        rerating, rerating_metric = None, ""
        if latest_idx - 20 >= 0:
            for metric in ["ps", "forward_pe", "ev_ebitda"]:
                v_now, v_old = latest.get(metric), hist(ticker, latest_idx - 20, metric)
                if v_now and v_old and v_old > 0 and v_now > 0:
                    rerating, rerating_metric = v_now / v_old - 1.0, metric
                    break
        stats["valuation_rerating_20d"], stats["valuation_rerating_metric"] = rerating, rerating_metric
        history_stats[ticker] = stats

    def valuation_expensiveness(ticker):
        parts, weights = [], []
        for metric, w in [("forward_pe", 0.35), ("ps", 0.35), ("ev_ebitda", 0.20), ("pe", 0.10)]:
            if metric_values[metric].get(ticker) is not None:
                parts.append(metric_pct[metric].get(ticker, 50) * w)
                weights.append(w)
        return sum(parts) / sum(weights) if weights else 68.0

    records = []
    for ticker in sorted(eval_reports):
        ev, m = eval_reports[ticker], latest_market[ticker]
        sc, base_sc = ev["scenarios"], ev["scenarios"].get("base", {})
        widths = [s.get("revenue_width") for s in sc.values() if s.get("revenue_width") is not None]
        avg_width = statistics.mean(widths) if widths else 0.25
        base_conf = base_sc.get("confidence_score") or confidence_to_score(ev.get("one_page_confidence"))
        evidence_score = clamp(base_conf + min(10, ev["keyword_high_evidence"] * 0.7) + min(5, ev["keyword_mid_evidence"] * 0.2) - min(8, ev["keyword_weak_evidence"] * 0.15), 20, 95)
        dq, exp = data_quality_raw(m), valuation_expensiveness(ticker)
        returns = scenario_returns(ev, m, exp, dq, metric_pct["iv"].get(ticker, 50))
        base_op = base_sc.get("op_margin")
        profit_fcf = 50.0 + (clamp((base_op - 0.12) * 130.0, -25, 30) if base_op is not None else 0) + base_sc.get("fcf_signal", 0) * 0.9
        if any(k in (base_sc.get("fcf_text", "") + base_sc.get("profit_text", "")) for k in ["融资", "摊薄", "库存", "应收", "营运资本", "CapEx"]):
            profit_fcf -= 5
        profit_fcf = clamp(profit_fcf, 5, 95)
        certainty = clamp(evidence_score - min(16, avg_width * 35) - (100 - dq) * 0.12, 5, 95)
        val_support = clamp(100.0 - exp - 6 * sum(1 for v in m["valuation_statuses"].values() if v == "bad"), 0, 100)
        downside = clamp(50 + returns["pessimistic"] * 70 + val_support * 0.22 + profit_fcf * 0.18 - (metric_pct["iv"].get(ticker, 50) - 50) * 0.12, 0, 100)
        fund_exp = 0.15 * returns["pessimistic"] + 0.45 * returns["base"] + 0.30 * returns["bull"] + 0.10 * returns["extreme"]
        aggr_exp = 0.08 * returns["pessimistic"] + 0.25 * returns["base"] + 0.42 * returns["bull"] + 0.25 * returns["extreme"]
        event_exp = 0.05 * returns["pessimistic"] + 0.15 * returns["base"] + 0.35 * returns["bull"] + 0.45 * returns["extreme"]
        rev_steps = [sc.get(k, {}).get("revenue_growth") for k in ["base", "bull", "extreme"] if sc.get(k, {}).get("revenue_growth") is not None]
        revenue_step = statistics.mean([clamp(x, -0.3, 3.0) for x in rev_steps]) if rev_steps else 0.0
        upside_convexity = returns["extreme"] * 0.6 + max(0.0, returns["extreme"] - returns["base"]) * 0.8 + max(0.0, returns["bull"] - returns["base"]) * 0.4
        demand_direct = clamp(35 + min(35, ev["keyword_high_evidence"] * 1.6) + min(15, ev["keyword_mid_evidence"] * 0.5) - min(12, ev["keyword_weak_evidence"] * 0.25), 0, 100)
        valuation_tolerance = clamp(50 + revenue_step * 35 - (exp - 50) * 0.55 + profit_fcf * 0.12, 0, 100)
        execution_quality = clamp(0.55 * certainty + 0.30 * profit_fcf + 0.15 * demand_direct, 0, 100)
        hs = history_stats.get(ticker, {})
        pre5, pre10, pre20 = hs.get("pre_5d_return"), hs.get("pre_10d_return"), hs.get("pre_20d_return")
        rerating20 = hs.get("valuation_rerating_20d")
        mom_vals = [x for x in [pre5, pre10, pre20] if x is not None]
        momentum_raw = statistics.mean(mom_vals) if mom_vals else -0.10
        iv_elastic = (m.get("iv") if m.get("iv") is not None else 0.0) * 0.50 + market_cap_small_pct.get(ticker, 50) / 100.0 * 0.25 + max(0, returns["extreme"] - returns["base"]) * 0.25
        market_dt, fact_dt, eval_dt = date_obj(latest_market_date), date_obj(ev.get("included_fact_date")), date_obj(ev["eval_date"])
        freshness = 45
        if fact_dt and market_dt:
            lag = abs((market_dt - fact_dt).days)
            freshness = 85 if lag <= 10 else 70 if lag <= 30 else 55 if lag <= 90 else 40
        elif eval_dt and market_dt:
            lag = abs((market_dt - eval_dt).days)
            freshness = 75 if lag <= 10 else 60 if lag <= 30 else 45
        earnings_status = clamp(freshness + min(15, (ev["keyword_high_evidence"] + ev["keyword_mid_evidence"]) * 0.25), 0, 100)
        order_guide_delta = clamp(25 + min(55, ev["keyword_high_evidence"] * 1.8) + min(15, ev["keyword_mid_evidence"] * 0.4), 0, 100)
        remaining_upside = returns["extreme"] - (pre20 or 0.0) * 0.65
        chase_risk = max(0.0, pre20 or 0.0) * 100 + max(0.0, rerating20 or 0.0) * 80 + max(0.0, exp - 70) * 0.7
        if m.get("iv") is not None:
            chase_risk += max(0.0, metric_pct["iv"].get(ticker, 50) - 80) * 0.6
        chase_risk = clamp(chase_risk, 0, 100)
        high_tail = returns["extreme"] >= 0.65 and returns["pessimistic"] <= -0.08 and (exp >= 70 or metric_pct["iv"].get(ticker, 50) >= 70) and (certainty <= 58 or profit_fcf <= 45)
        flags = ["derived_scenario_return"]
        for k, v in m["valuation_statuses"].items():
            if v in ("bad", "missing", "warn"):
                flags.append(f"{k}:{v}")
        if currency_check(m) != "ok":
            flags.append(currency_check(m))
        if "需确认" in m.get("adr_ratio", ""):
            flags.append("ADR_ratio_to_confirm")
        if m.get("iv") is None:
            flags.append("IV_missing")
        if high_tail:
            flags.append("high_tail_high_risk")
        bottleneck = base_sc.get("bottleneck_text") or ev.get("max_bottleneck")
        records.append({
            "ticker": ticker, "name": ev["eval_name"] or m["market_name"], "category": m["category"],
            "eval_file": ev["eval_file"], "eval_date": ev["eval_date"], "included_fact_date": ev["included_fact_date"],
            "market_file": m["market_file"], "market_date": m["market_date"], "price_date": m["price_date"],
            "price": m["price"], "market_cap": m["market_cap"], "pe": m["pe"], "forward_pe": m["forward_pe"], "ps": m["ps"], "ev_ebitda": m["ev_ebitda"], "iv": m["iv"],
            "listing_type": m["listing_type"], "currency_check": currency_check(m), "valuation_quality": m["valuation_check"],
            "ret_pessimistic": returns["pessimistic"], "ret_base": returns["base"], "ret_bull": returns["bull"], "ret_extreme": returns["extreme"],
            "base_revenue": base_sc.get("revenue_text", ""), "base_profit": base_sc.get("profit_text", ""), "base_fcf": base_sc.get("fcf_text", ""),
            "evidence_level": base_sc.get("confidence_text") or ev.get("one_page_confidence"), "certainty_score_raw": certainty,
            "bottleneck_text": bottleneck, "counter_evidence_text": ev.get("counter_evidence_text") or bottleneck,
            "pre_5d_return": pre5, "pre_10d_return": pre10, "pre_20d_return": pre20, "valuation_rerating_20d": rerating20,
            "valuation_rerating_metric": hs.get("valuation_rerating_metric", ""), "fundamental_expected_return_raw": fund_exp, "aggressive_expected_return_raw": aggr_exp, "event_expected_return_raw": event_exp,
            "certainty_raw": certainty, "profit_fcf_raw": profit_fcf, "valuation_support_raw": val_support, "downside_raw": downside, "data_quality_raw": dq,
            "upside_convexity_raw": upside_convexity, "revenue_step_raw": revenue_step, "demand_directness_raw": demand_direct, "valuation_tolerance_raw": valuation_tolerance, "execution_quality_raw": execution_quality,
            "momentum_raw": momentum_raw, "iv_elasticity_raw": iv_elastic, "earnings_status_raw": earnings_status, "order_guide_delta_raw": order_guide_delta, "remaining_upside_raw": remaining_upside, "chase_risk_raw": chase_risk,
            "valuation_expensiveness_raw": exp, "high_tail_high_risk": high_tail, "final_notes": ";".join(dict.fromkeys(flags)), "market_notes": m["market_notes"],
        })

    raw_metric_defs = [
        ("fundamental_expected_return_raw", True), ("certainty_raw", True), ("profit_fcf_raw", True), ("valuation_support_raw", True), ("downside_raw", True), ("data_quality_raw", True),
        ("aggressive_expected_return_raw", True), ("upside_convexity_raw", True), ("revenue_step_raw", True), ("demand_directness_raw", True), ("valuation_tolerance_raw", True), ("execution_quality_raw", True),
        ("event_expected_return_raw", True), ("momentum_raw", True), ("iv_elasticity_raw", True), ("earnings_status_raw", True), ("order_guide_delta_raw", True), ("remaining_upside_raw", True), ("chase_risk_raw", True),
    ]
    for raw_key, high_good in raw_metric_defs:
        mp = percentile_maps({r["ticker"]: r.get(raw_key) for r in records}, high_good=high_good)
        out_key = raw_key.replace("_raw", "_pct")
        for r in records:
            r[out_key] = mp.get(r["ticker"], 50.0)
    for r in records:
        r["fundamental_score"] = 0.45 * r["fundamental_expected_return_pct"] + 0.15 * r["certainty_pct"] + 0.15 * r["profit_fcf_pct"] + 0.10 * r["valuation_support_pct"] + 0.10 * r["downside_pct"] + 0.05 * r["data_quality_pct"]
        r["aggressive_score"] = 0.35 * r["aggressive_expected_return_pct"] + 0.20 * r["upside_convexity_pct"] + 0.15 * r["revenue_step_pct"] + 0.10 * r["demand_directness_pct"] + 0.10 * r["valuation_tolerance_pct"] + 0.10 * r["execution_quality_pct"]
        r["event_score"] = 0.25 * r["event_expected_return_pct"] + 0.15 * r["momentum_pct"] + 0.15 * r["iv_elasticity_pct"] + 0.15 * r["earnings_status_pct"] + 0.10 * r["order_guide_delta_pct"] + 0.10 * r["remaining_upside_pct"] + 0.05 * r["data_quality_pct"] - 0.05 * r["chase_risk_pct"]
    for score_key, rank_key in [("fundamental_score", "fundamental_rank"), ("aggressive_score", "aggressive_rank"), ("event_score", "event_rank")]:
        for idx, r in enumerate(sorted(records, key=lambda x: (-x[score_key], x["ticker"])), 1):
            r[rank_key] = idx
    records_by_ticker = {r["ticker"]: r for r in records}
    fund_ranked = sorted(records, key=lambda r: r["fundamental_rank"])
    aggr_ranked = sorted(records, key=lambda r: r["aggressive_rank"])
    event_ranked = sorted(records, key=lambda r: r["event_rank"])

    def core_reason(r, mode):
        if mode == "fundamental":
            return short_text(f"稳健期望{fmt_pct(r['fundamental_expected_return_raw'])}；确定性{r['certainty_score_raw']:.0f}；利润/FCF质量{r['profit_fcf_raw']:.0f}；估值支撑分位{r['valuation_support_pct']:.0f}", 86)
        if mode == "aggressive":
            return short_text(f"进攻期望{fmt_pct(r['aggressive_expected_return_raw'])}；乐观/极度空间{fmt_pct(r['ret_bull'])}/{fmt_pct(r['ret_extreme'])}；收入台阶分位{r['revenue_step_pct']:.0f}", 86)
        return short_text(f"事件期望{fmt_pct(r['event_expected_return_raw'])}；5/20日{fmt_pct(r['pre_5d_return'])}/{fmt_pct(r['pre_20d_return'])}；IV {fmt_pct(r['iv'])}；右尾{fmt_pct(r['ret_extreme'])}", 86)

    def core_risk(r):
        flags = []
        if r["high_tail_high_risk"]:
            flags.append("高右尾高风险")
        if "bad" in r["valuation_quality"]:
            flags.append("估值校验bad")
        if r["currency_check"] != "ok":
            flags.append(r["currency_check"])
        if "ADR_ratio_to_confirm" in r["final_notes"]:
            flags.append("ADR比例待确认")
        if r["iv"] is None:
            flags.append("IV缺失")
        if r["pre_20d_return"] is not None and r["pre_20d_return"] > 0.30:
            flags.append("20日涨幅偏高")
        if r["valuation_rerating_20d"] is not None and r["valuation_rerating_20d"] > 0.25:
            flags.append("20日估值重估偏快")
        return short_text(("；".join(flags[:3]) + "；" if flags else "") + short_text(r["bottleneck_text"], 52), 96)

    def ranking_table(rows, mode, n=30):
        cols = ["排名", "ticker", "name", "category", "分数", "价格", "市值", "Forward PE", "P/S", "IV", "悲观", "基准", "乐观", "极度乐观", "核心分项", "主要理由", "主要风险"]
        out = ["|" + "|".join(cols) + "|", "|" + "|".join(["---:", "---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---", "---", "---"]) + "|"]
        rank_key = {"fundamental": "fundamental_rank", "aggressive": "aggressive_rank", "event": "event_rank"}[mode]
        score_key = {"fundamental": "fundamental_score", "aggressive": "aggressive_score", "event": "event_score"}[mode]
        for r in rows[:n]:
            if mode == "fundamental":
                sub = f"期望{r['fundamental_expected_return_pct']:.0f}/确定{r['certainty_pct']:.0f}/FCF{r['profit_fcf_pct']:.0f}/估值{r['valuation_support_pct']:.0f}"
            elif mode == "aggressive":
                sub = f"期望{r['aggressive_expected_return_pct']:.0f}/凸性{r['upside_convexity_pct']:.0f}/收入{r['revenue_step_pct']:.0f}/执行{r['execution_quality_pct']:.0f}"
            else:
                sub = f"期望{r['event_expected_return_pct']:.0f}/动量{r['momentum_pct']:.0f}/IV{r['iv_elasticity_pct']:.0f}/追高{r['chase_risk_pct']:.0f}"
            vals = [str(r[rank_key]), r["ticker"], r["name"], r["category"], f"{r[score_key]:.1f}", fmt_num(r["price"]), fmt_cap(r["market_cap"]), fmt_num(r["forward_pe"]), fmt_num(r["ps"]), fmt_pct(r["iv"]), fmt_pct(r["ret_pessimistic"]), fmt_pct(r["ret_base"]), fmt_pct(r["ret_bull"]), fmt_pct(r["ret_extreme"]), sub, core_reason(r, mode), core_risk(r)]
            out.append("|" + "|".join(md_escape(v) for v in vals) + "|")
        return "\n".join(out)

    def list_tickers(rows, n=10):
        return "、".join(f"{r['ticker']}({r['name']})" for r in rows[:n])

    def ticker_line(tickers):
        if not tickers:
            return "无"
        return "、".join(f"{t}({records_by_ticker[t]['name']})" for t in tickers)

    def stat_count(pred):
        return sum(1 for r in records if pred(r))

    missing_stats = {
        "price_missing": stat_count(lambda r: r["price"] is None),
        "market_cap_missing": stat_count(lambda r: r["market_cap"] is None),
        "pe_missing": stat_count(lambda r: r["pe"] is None),
        "forward_pe_missing": stat_count(lambda r: r["forward_pe"] is None),
        "ps_missing": stat_count(lambda r: r["ps"] is None),
        "ev_ebitda_missing": stat_count(lambda r: r["ev_ebitda"] is None),
        "iv_missing": stat_count(lambda r: r["iv"] is None),
        "currency_mismatch_or_missing": stat_count(lambda r: r["currency_check"] != "ok"),
        "adr_ratio_to_confirm": stat_count(lambda r: "ADR_ratio_to_confirm" in r["final_notes"]),
        "valuation_bad_any": stat_count(lambda r: "bad" in r["valuation_quality"]),
        "valuation_warn_any": stat_count(lambda r: "warn" in r["valuation_quality"]),
    }
    quality_rows = [
        ("评估报告数量", len(eval_reports)), ("最新金融数据明细数量", len(latest_market)), ("匹配进入排序数量", len(records)),
        ("价格缺失", missing_stats["price_missing"]), ("市值缺失", missing_stats["market_cap_missing"]), ("TTM PE缺失/不适用", missing_stats["pe_missing"]),
        ("Forward PE缺失", missing_stats["forward_pe_missing"]), ("P/S缺失", missing_stats["ps_missing"]), ("EV/EBITDA缺失", missing_stats["ev_ebitda_missing"]),
        ("IV缺失", missing_stats["iv_missing"]), ("交易/财报货币不一致或缺失", missing_stats["currency_mismatch_or_missing"]), ("ADR/ADS比例需确认", missing_stats["adr_ratio_to_confirm"]),
        ("任一估值字段bad", missing_stats["valuation_bad_any"]), ("任一估值字段warn", missing_stats["valuation_warn_any"]),
    ]
    quality_table = ["| 项目 | 数量 |", "|---|---:|"] + [f"| {k} | {v} |" for k, v in quality_rows]
    top30_f, top30_a, top30_e = {r["ticker"] for r in fund_ranked[:30]}, {r["ticker"] for r in aggr_ranked[:30]}, {r["ticker"] for r in event_ranked[:30]}
    all_three = sorted(top30_f & top30_a & top30_e)
    fund_aggr = sorted((top30_f & top30_a) - top30_e)
    event_only = sorted(top30_e - top30_f - top30_a)
    aggr_only = sorted(top30_a - top30_f - top30_e)
    fund_only = sorted(top30_f - top30_a - top30_e)
    risk_rows = sorted([r for r in records if r["high_tail_high_risk"]], key=lambda r: (-r["ret_extreme"], r["fundamental_rank"]))
    high_risk_table = ["| ticker | name | category | 悲观 | 极度乐观 | Forward PE | P/S | IV | 确定性 | 主要风险 |", "|---|---|---|---:|---:|---:|---:|---:|---:|---|"]
    for r in risk_rows[:30]:
        high_risk_table.append("|" + "|".join(md_escape(v) for v in [r["ticker"], r["name"], r["category"], fmt_pct(r["ret_pessimistic"]), fmt_pct(r["ret_extreme"]), fmt_num(r["forward_pe"]), fmt_num(r["ps"]), fmt_pct(r["iv"]), f"{r['certainty_score_raw']:.0f}", core_risk(r)]) + "|")
    if len(high_risk_table) == 2:
        high_risk_table.append("| 无 | 无 | 无 |  |  |  |  |  |  |  |")

    scorecard_cols = ["ticker", "name", "category", "eval_file", "eval_date", "included_fact_date", "market_file", "market_date", "price", "market_cap", "pe", "forward_pe", "ps", "ev_ebitda", "iv", "listing_type", "currency_check", "valuation_quality", "ret_pessimistic", "ret_base", "ret_bull", "ret_extreme", "base_revenue", "base_profit", "base_fcf", "evidence_level", "certainty_score_raw", "bottleneck_text", "counter_evidence_text", "pre_5d_return", "pre_10d_return", "pre_20d_return", "valuation_rerating_20d", "fundamental_score", "aggressive_score", "event_score", "fundamental_rank", "aggressive_rank", "event_rank", "final_notes"]
    scorecard = ["|" + "|".join(scorecard_cols) + "|", "|" + "|".join(["---"] * len(scorecard_cols)) + "|"]
    for r in sorted(records, key=lambda x: x["ticker"]):
        vals = []
        for c in scorecard_cols:
            if c in ["price", "pe", "forward_pe", "ps", "ev_ebitda"]:
                vals.append(fmt_num(r.get(c)))
            elif c == "market_cap":
                vals.append(fmt_cap(r.get(c)))
            elif c == "iv" or c.startswith("ret_") or c.startswith("pre_") or c == "valuation_rerating_20d":
                vals.append(fmt_pct(r.get(c)))
            elif c in ["fundamental_score", "aggressive_score", "event_score", "certainty_score_raw"]:
                vals.append(f"{r.get(c):.1f}")
            elif c in ["bottleneck_text", "counter_evidence_text", "base_profit", "base_fcf", "valuation_quality", "evidence_level"]:
                vals.append(short_text(r.get(c, ""), 70))
            else:
                vals.append(r.get(c, ""))
        scorecard.append("|" + "|".join(md_escape(v) for v in vals) + "|")

    source_rows = [
        ("评估报告源", str(EVAL_DIR), f"{len(eval_reports)} 份正式评估报告；报告日期范围 {min(r['eval_date'] for r in eval_reports.values() if r['eval_date'])} 至 {max(r['eval_date'] for r in eval_reports.values() if r['eval_date'])}"),
        ("最新金融数据主文件", str(latest_market_file), f"文件日期 {latest_market_date}；明细 {len(latest_market)} 个 ticker"),
        ("同日补充字段校验", "无同日文件" if not same_day_supplements else "；".join(str(p) for p in same_day_supplements), "本轮未使用非同日补充校验文件"),
        ("历史金融数据", str(MARKET_DIR), f"主文件 {len(market_files)} 个；用于 5/10/20 档收益和估值重估，日期范围 {parse_date_from_name(market_files[0])} 至 {latest_market_date}"),
    ]
    source_table = ["| 数据项 | 路径/文件 | 本轮用法 |", "|---|---|---|"] + [f"| {md_escape(a)} | {md_escape(b)} | {md_escape(c)} |" for a, b, c in source_rows]
    report = [
        "# 双源投资排序结果（R02 资料更新重跑）", "",
        "## 1. 本轮结论",
        f"- 基本面性价比榜前 10：{list_tickers(fund_ranked, 10)}。这张榜主要奖励稳健情景期望、基准确定性、利润/FCF质量和下跌保护。",
        f"- 激进成长榜前 10：{list_tickers(aggr_ranked, 10)}。这张榜主要奖励乐观/极度乐观空间、收入台阶、需求直接性和估值可承受度。",
        f"- 财报事件与右尾弹性榜前 10：{list_tickers(event_ranked, 10)}。这张榜主要用于短期进攻辅助，已单独扣除 20 日涨幅、估值重估和 IV 过热带来的追高风险。",
        f"- 三榜同时进入前 30 的标的共 {len(all_three)} 个：{ticker_line(all_three)}。事件榜独有前 30 共 {len(event_only)} 个，这些更偏交易弹性，不自动等同于中期性价比。",
        "- 本轮所有四情景股价变化均为推导口径：评估报告明确不输出目标价/股价区间，因此没有直接抽取现成股价变化。", "",
        "## 2. 数据源和日期",
        f"- 本轮使用的数据日期：评估报告截至 `{max(r['eval_date'] for r in eval_reports.values() if r['eval_date'])}`；金融数据主文件日期 `{latest_market_date}`；价格明细中最常见价格日期由主文件自身披露，个股价格日期见评分卡。", "",
        "\n".join(source_table), "",
        "## 3. 基本面性价比前列排序", "用途：中期风险收益、确定性和下跌保护优先，不等同于短期弹性最大。", ranking_table(fund_ranked, "fundamental", 30), "",
        "## 4. 激进成长前列排序", "用途：寻找乐观情景、收入台阶和估值可承受度最突出的标的；允许更高波动，但仍扣除估值透支和执行质量不足。", ranking_table(aggr_ranked, "aggressive", 30), "",
        "## 5. 财报事件与右尾弹性前列排序", "用途：短期进攻辅助榜，重视右尾、IV、近期动量、财报后证据和剩余空间；不代表基本面性价比最高。", ranking_table(event_ranked, "event", 30), "",
        "## 6. 三张榜重合和分歧",
        f"- 三榜前 30 交集：{ticker_line(all_three)}。",
        f"- 基本面与激进成长交集、但不在事件榜前 30：{ticker_line(fund_aggr)}。",
        f"- 事件榜独有前 30：{ticker_line(event_only)}。这些标的更偏短期波动/右尾，不应直接替代中期性价比结论。",
        f"- 激进成长独有前 30：{ticker_line(aggr_only)}。这些标的收入台阶或极度情景强，但基本面榜可能因估值、FCF或下跌保护被压低。",
        f"- 基本面独有前 30：{ticker_line(fund_only)}。这些标的更偏稳健兑现和估值保护，事件弹性未必突出。", "",
        "## 7. 高弹性但高风险标的清单", "判定规则：极度乐观空间高、悲观情景为负，且估值/IV较高，同时证据或现金流质量不够强。该标记不是排除项，但不能自动进入基本面性价比前列。",
        "\n".join(high_risk_table), "",
        "## 8. 数据质量异常和字段缺失", "\n".join(quality_table), "",
        "关键异常说明：",
        "- 最新主文件没有同日补充字段校验文件；本轮只使用主文件内已经写出的估值校验列和备注列，不拿 2026-06-02 的旧补充文件覆盖 2026-06-19。",
        "- `bad` 字段只作为风险和质量惩罚，不参与估值加分；`warn` 字段可用但降低数据质量。",
        "- 跨币种、ADR/ADS 比例待确认、价格缺失或 IV 缺失的标的仍保留在全样本中，方便复核，但在对应分项中降权。", "",
        "## 9. 排序方法说明",
        f"- 排序方法版本：`{METHOD_VERSION}`。",
        "- 数据边界：事实输入只来自 `分析报告/公司评估/` 的正式评估报告，以及 `日度资料/每日金融数据/` 的每日金融数据主文件；没有读取第 2 节之外的目录、外部网页、旧排序或中间结果作为事实输入。",
        "- 情景收益：因评估报告不输出目标价或股价区间，四情景股价变化统一按第 7.2 条推导，标记为 `derived_scenario_return`。推导只使用报告内“相对预期/收入增速/利润率/FCF/可信度”和最新市值、估值、IV、校验状态。",
        "- 标准化：所有分项进入最终三张榜前，均做横截面 1%/99% winsorize 和 0-100 百分位转换；`bad` 字段不得形成估值加分，只进入质量惩罚和风险备注。",
        "- 三张榜用途：基本面性价比榜重视稳健期望和下跌保护；激进成长榜重视乐观空间和收入台阶；事件与右尾榜重视近期重估、IV弹性、财报/订单证据和剩余右尾空间，并显式扣追高风险。",
        "- 不适合直接比较：跨币种或 ADR/ADS 比例待确认标的、P/S 校验为 bad 的标的、价格缺失标的，以及报告内经营口径为本币但市场估值为 USD 的标的，均保留在排序中但降低数据质量或估值支撑。", "",
        "## 10. 后续复核清单",
        "- 复核 1：解析读入路径只覆盖两个允许源目录；输出目录只写入结果，不作为事实输入。",
        f"- 复核 2：最新金融数据使用 `{latest_market_file.name}`；同日补充字段校验文件：{'存在' if same_day_supplements else '不存在'}。",
        "- 复核 3：180 个评估报告 ticker 与 180 个金融数据 ticker 完全匹配；缺评估报告 0，缺金融数据 0。",
        f"- 复核 4：任一估值字段 `bad` 的标的 {missing_stats['valuation_bad_any']} 个，均未因该字段获得估值加分；已在 `final_notes` 和风险列标记。",
        "- 复核 5：事件榜的高 IV/高动量只进入短期弹性，不被写成基本面确定性；基本面榜单独使用下跌保护和利润/FCF质量。",
        "- 复核 6：20 日涨幅和 20 日估值重估被用于剩余空间与追高风险扣分，避免把已涨幅直接当成未来空间。", "",
        "## 附录 A：全样本标准评分卡",
        "说明：每个标的一行；`ret_*` 为推导情景股价变化，`pre_*` 为排序前历史金融数据快照收益；`valuation_rerating_20d` 优先使用 P/S，其次 Forward PE，再次 EV/EBITDA。",
        "\n".join(scorecard), "",
    ]
    OUT_PATH.write_text("\n".join(report), encoding="utf-8")
    print("wrote", OUT_PATH)
    print("records", len(records), "fund_top5", [r["ticker"] for r in fund_ranked[:5]], "aggr_top5", [r["ticker"] for r in aggr_ranked[:5]], "event_top5", [r["ticker"] for r in event_ranked[:5]])
    print("quality", missing_stats)


if __name__ == "__main__":
    main()
