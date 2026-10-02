from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(r"D:\investment\基本面")
BASE_SCRIPT = ROOT / "scripts" / "generate_googl_company_comparison_20260623.py"

spec = importlib.util.spec_from_file_location("company_comparison_base", BASE_SCRIPT)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = base
spec.loader.exec_module(base)

base.TARGET = "MSI"
base.TARGET_NAME = "Motorola Solutions"
base.REPORT_DATE = "2026-06-23"
base.OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "MSI_逐家公司投资思路对比_2026-06-23.md"

SCHEME_PATH = ROOT.parent / "分析报告" / "公司对比" / "研究方案.md"
MSI_COMPANY_RESEARCH_PATH = ROOT / "公司调研" / "机电_冷却_工程_水处理_边缘工业AI" / "MSI_Motorola Solutions_公司调研_2026-06-11.md"
SUPPORTING_INDUSTRY_PATHS = [
    ROOT / "行业调研" / "AI园区电力_机电_冷却" / "行业调研_机柜、围护结构与物理安防_2026-06-11.md",
    ROOT / "行业调研" / "AI服务器_存储_芯片" / "行业调研_AI边缘推理芯片_2026-06-11.md",
    ROOT / "行业调研" / "产业背景" / "行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md",
    ROOT / "行业调研" / "产业背景" / "AI产业链全局图谱与口径字典_2026-06-11.md",
]


PUBLIC_SAFETY_SECURITY_DIRECT = {
    "ALLE",
    "CSCO",
    "FTV",
    "JCI",
    "NOK",
    "TDY",
    "VISN",
}

PHYSICAL_SECURITY_AND_FACILITY_ADJACENT = {
    "AAON",
    "ABBNY",
    "ALNT",
    "CARR",
    "DCI",
    "DOV",
    "ECL",
    "ETN",
    "FLEX",
    "GNRC",
    "HUBB",
    "NVT",
    "PH",
    "PNR",
    "TT",
    "VRT",
}

GOVERNMENT_DEFENSE_EDGE_ADJACENT = {
    "BWXT",
    "CAT",
    "CMI",
    "GEV",
    "PSIX",
    "RKLB",
    "RYCEY",
}

DATA_CENTER_SECURITY_CUSTOMERS = {
    "ADBE",
    "AMZN",
    "APLD",
    "BABA",
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

AI_HIGH_GROWTH_ADJACENT_CATEGORIES = {
    "AI服务器_存储_EMS",
    "AI计算芯片_EDA_IP_custom_ASIC",
    "AI网络_光互联_连接器",
    "云算力_IDC_AI软件平台",
    "晶圆制造_前道设备",
    "封测_检测_计量_光罩",
    "半导体材料_化学品_基板",
}

INFRA_AND_INDUSTRIAL_CATEGORIES = {
    "电力_发电_能源_储能",
    "配电_电源_功率器件",
    "机电_冷却_工程_水处理_边缘工业AI",
}


MSI_SCORE_OVERRIDES = {
    # MSI's formula score underweights its formal FY2026 guide and $15.7B
    # backlog for the NTM path, but it should not be promoted into the AI
    # main-chain right-tail bucket. Keep the profile defensive and cash-flow
    # led: strong downside/valuation digestion, middling NTM and catalyst,
    # weak right-tail/momentum/short-term aggression.
    "NTM兑现优先": 0.600,
    "右尾弹性优先": 0.455,
    "风险调整收益": 0.555,
    "下行保护优先": 0.670,
    "估值消化优先": 0.565,
    "近端催化优先": 0.745,
    "价格确认/动量": 0.420,
    "激进短线": 0.405,
}


def calibrate_msi(companies: dict[str, object]) -> None:
    c = companies[base.TARGET]
    for strategy, score in MSI_SCORE_OVERRIDES.items():
        c.scores[strategy] = score


def validate_supporting_sources() -> None:
    for path in [SCHEME_PATH, MSI_COMPANY_RESEARCH_PATH, *SUPPORTING_INDUSTRY_PATHS]:
        if not path.exists():
            raise SystemExit(f"required supporting source missing: {path}")
        base.read_text(path)


def relation_for(b) -> str:
    ticker = b.ticker
    category = b.category
    if ticker in PUBLIC_SAFETY_SECURITY_DIRECT:
        return "直接同业"
    if ticker in DATA_CENTER_SECURITY_CUSTOMERS:
        return "上下游"
    if ticker in PHYSICAL_SECURITY_AND_FACILITY_ADJACENT or ticker in GOVERNMENT_DEFENSE_EDGE_ADJACENT:
        return "相邻替代"
    if category in AI_HIGH_GROWTH_ADJACENT_CATEGORIES:
        return "相邻替代"
    if category in INFRA_AND_INDUSTRIAL_CATEGORIES:
        return "相邻替代"
    return "跨赛道"


def reason_for(strat: str, label: str, b, relation: str) -> str:
    if label == "中性":
        if relation == "跨赛道":
            return "业务差异大且档位接近"
        return "档位接近，证据互有强弱"
    side = "A" if label.endswith("投A") else "B"
    if side == "A":
        return {
            "NTM兑现优先": "MSI指引、15.7B backlog和利润路径更稳",
            "右尾弹性优先": "MSI有Silvus、Command AI和Video上行",
            "风险调整收益": "MSI现金流、backlog和利润质量更均衡",
            "下行保护优先": "MSI公共安全客户粘性和FCF更抗压",
            "估值消化优先": "MSI用NTM利润和FCF更能消化估值",
            "近端催化优先": "MSI订单/backlog、Silvus和Command验证更近",
            "价格确认/动量": "MSI短期反弹有基本面支撑",
            "激进短线": "MSI有Silvus/AI安防事件弹性",
        }[strat]
    return {
        "NTM兑现优先": f"{b.ticker}收入增速或订单兑现更硬",
        "右尾弹性优先": f"{b.ticker}AI主链、小基数或右尾更大",
        "风险调整收益": f"{b.ticker}上行和下行组合更优",
        "下行保护优先": f"{b.ticker}现金流、估值或压力期更稳",
        "估值消化优先": f"{b.ticker}增长或低倍数更能消化估值",
        "近端催化优先": f"{b.ticker}近端订单/产品催化更强",
        "价格确认/动量": f"{b.ticker}价格趋势确认更强",
        "激进短线": f"{b.ticker}高beta和资金关注更适合进攻",
    }[strat]


def final_choice(decisions: dict[str, str], b) -> tuple[str, str, str]:
    counts = Counter(base.label_side(v) for v in decisions.values())
    a_count, b_count, n_count = counts["A"], counts["B"], counts["N"]
    if a_count > b_count:
        final = base.TARGET
        reason = "MSI在多数思路下胜在backlog、FCF、公共安全粘性和估值消化。"
    elif b_count > a_count:
        final = b.ticker
        reason = f"{b.ticker}在多数思路下胜出，MSI需要更高增速、订单或价格确认才能反超。"
    else:
        risk_label = decisions["风险调整收益"].split("：", 1)[0]
        if risk_label.endswith("投A"):
            final = base.TARGET
            reason = "多数思路打平时，风险调整收益更支持MSI。"
        elif risk_label.endswith("投B"):
            final = b.ticker
            reason = f"多数思路打平时，风险调整收益更支持{b.ticker}。"
        else:
            ntm_label = decisions["NTM兑现优先"].split("：", 1)[0]
            if ntm_label.endswith("投A"):
                final = base.TARGET
                reason = "多数思路打平，MSI的NTM兑现略更清楚。"
            elif ntm_label.endswith("投B"):
                final = b.ticker
                reason = f"多数思路打平，NTM兑现略偏{b.ticker}。"
            else:
                final = base.TARGET
                reason = "多数思路打平且证据互有强弱，MSI防守质量略占优。"
    return f"A {a_count} / B {b_count} / 中性 {n_count}", final, reason


def grade_support_limit(strat: str, c) -> tuple[str, str]:
    support = {
        "NTM兑现优先": "FY2026收入指引约12.8B、non-GAAP EPS 16.87-16.99，Q1 2026 backlog 15.7B同比+11%，NTM基准12.9-13.2B",
        "右尾弹性优先": "Silvus MANET/FASST、Command Center云与agentic AI、Video/Avigilon/Blue Eye和SVX提供中期上行",
        "风险调整收益": "2025 FCF 2.6B，基准non-GAAP OPM 29.2%-30.2%，公共安全/关键通信客户粘性高",
        "下行保护优先": "公共安全和关键基础设施需求刚性，Software and Services backlog高，FCF和服务续约构成底盘",
        "估值消化优先": "Forward PE 21.18、P/S 5.49，若FY2026指引和NTM FCF 2.6-2.9B兑现，可用利润和现金流消化估值",
        "近端催化优先": "Q2/Q3收入、backlog、Silvus订单/扩产、Command/Video订单、Bell Canada LMR交易是未来1-2季验证点",
        "价格确认/动量": "2026-06-03过去两周+3.15%，基本面未破坏且估值从6月初回落",
        "激进短线": "Silvus国防无人系统、公共安全AI、Video AI和数据中心物理安防叙事有事件交易弹性",
    }[strat]
    limit = {
        "NTM兑现优先": "总收入增速约10%-13%不属于项目内高增速，PSI Q1仅+1%，政府/国防合同收入确认存在时点风险",
        "右尾弹性优先": "MSI不是GPU/HBM/光互联/电力冷却主链，AI数据中心直接收入未披露且估算占比低",
        "风险调整收益": "Silvus收购后债务约9.0B，GAAP利润受earnout和摊销压制，估值仍要求持续执行",
        "下行保护优先": "SOXX三段压力窗口累计-33.68%，股价仍会受高估值工业/科技资金风格影响",
        "估值消化优先": "EV/EBITDA 21.27、P/S 5.49并不便宜，若Silvus/Command/Video低于预期，估值消化会变慢",
        "近端催化优先": "催化多是合同、财报和收购整合验证，不是AI主链订单爆发；Hyper/AI ARR和AI DC订单未单列",
        "价格确认/动量": "2026-06-03过去1个月-6.31%，2026-05-27过去3个月-15.25%，趋势确认并不连续",
        "激进短线": "市值约65B、IV约29%，低于小市值AI/光互联/电力链高beta标的，短线爆发力不是核心优势",
    }[strat]
    return support, limit


def finance_snapshot(c) -> str:
    f = c.finance
    return (
        f"2026-06-22金融快照：价格日期{f.get('价格日期', '缺失')}，"
        f"最新价格{f.get('最新价格', '缺失')}美元，市值{f.get('市值', '缺失')}，"
        f"TTM PE {f.get('TTM PE', '缺失')}，Forward PE {f.get('Forward PE', '缺失')}，"
        f"P/S {f.get('P/S', '缺失')}，EV/EBITDA {f.get('EV/EBITDA', '缺失')}，"
        f"Call/Put IV {f.get('Call IV', '缺失')}/{f.get('Put IV', '缺失')}；"
        "2026-06-03过去两周+3.15%、过去一月-6.31%；"
        "2026-06-04三段SOXX压力窗口累计-33.68%。"
    )


def make_report(companies: dict[str, object]) -> str:
    a = companies[base.TARGET]
    rows = []
    stats = {s: Counter() for s in base.STRATEGIES}
    b_rank_rows = []
    a_rank_rows = []
    decisions_by_b = {}

    sorted_bs = [c for t, c in companies.items() if t != base.TARGET]
    sorted_bs.sort(key=lambda c: (c.category, c.ticker))

    for idx, b in enumerate(sorted_bs, start=1):
        relation = relation_for(b)
        decisions = {s: base.decision_for(a, b, s, relation) for s in base.STRATEGIES}
        decisions_by_b[b.ticker] = decisions
        for s, cell in decisions.items():
            stats[s][cell.split("：", 1)[0]] += 1
        majority, final, final_reason = final_choice(decisions, b)
        counts = Counter(base.label_side(v) for v in decisions.values())
        rows.append(
            [
                str(idx),
                f"{b.ticker} / {b.name}",
                b.category,
                relation,
                base.grade_summary(a, b),
                *[decisions[s] for s in base.STRATEGIES],
                majority,
                final,
                final_reason,
            ]
        )
        diff = counts["B"] - counts["A"]
        if diff >= 3:
            b_rank_rows.append((diff, counts["B"], b, decisions))
        if -diff >= 3:
            a_rank_rows.append((-diff, counts["A"], b, decisions))

    a_majority_wins = sum(1 for b, ds in decisions_by_b.items() if final_choice(ds, companies[b])[1] == base.TARGET)
    b_majority_wins = len(sorted_bs) - a_majority_wins
    by_strategy_a = {s: stats[s]["强烈建议投A"] + stats[s]["建议投A"] + stats[s]["微倾向投A"] for s in base.STRATEGIES}
    by_strategy_b = {s: stats[s]["强烈建议投B"] + stats[s]["建议投B"] + stats[s]["微倾向投B"] for s in base.STRATEGIES}
    a_best = sorted(base.STRATEGIES, key=lambda s: by_strategy_a[s] - by_strategy_b[s], reverse=True)[:3]
    a_worst = sorted(base.STRATEGIES, key=lambda s: by_strategy_a[s] - by_strategy_b[s])[:3]
    strongest_b = sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker))[:12]
    strongest_b_names = "、".join(f"{b.ticker}" for _, _, b, _ in strongest_b) or "无明显集中反方"

    eval_dates = [c.eval_date for c in companies.values()]
    finance_meta = base.load_finance()[1]
    missing_finance = sorted([t for t, c in companies.items() if not c.finance])
    missing_price = sorted([t for t, c in companies.items() if (not c.finance) or c.metrics.get("price") is None])

    a_intro = base.section_between(a.text, "1. 一页结论")
    conclusion = base.section_between(a.text, "8. 结论")
    products = base.bullet_after(a_intro, "重要产品/业务线")
    ntm = a.scenarios.get("基准", {}).get("NTM 公司收入", "")
    optimistic = " / ".join(
        filter(
            None,
            [
                a.scenarios.get("乐观", {}).get("NTM 公司收入", ""),
                a.scenarios.get("极度乐观", {}).get("NTM 公司收入", ""),
            ],
        )
    )
    profit_cash = base.bullet_after(conclusion, "利润/现金流结论") or a.scenarios.get("基准", {}).get("EBITDA/净利润", "")
    bottleneck = base.bullet_after(conclusion, "主要传导瓶颈") or base.bullet_after(a_intro, "最大传导瓶颈")
    bear = base.bullet_after(conclusion, "悲观情景触发条件") or "Q2/Q3 backlog或订单放缓、Silvus订单/扩产低于预期、Command AI商业化慢、Video竞争压价、FCF走弱。"
    catalysts = base.bullet_after(conclusion, "后续跟踪数据") or base.bullet_after(conclusion, "乐观情景成立条件")

    lines = []
    lines.append("# MSI 逐家公司投资思路对比")
    lines.append("")
    lines.append(f"生成日期：{base.REPORT_DATE}")
    lines.append("公司 A：MSI / Motorola Solutions")
    lines.append("公司全集来源：分析报告/公司评估/结果/")
    lines.append(f"项目内公司总数：{len(companies)}")
    lines.append(f"被比较公司 B 数量：{len(companies) - 1}")
    lines.append(f"公司评估文件日期范围：{min(eval_dates)} 至 {max(eval_dates)}")
    lines.append("日度数据日期：价格/估值/IV 为 2026-06-22 金融快照；过去两周和过去1个月区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04。")
    lines.append("")
    lines.append("> 口径说明：本报告读取 `分析报告/公司评估/结果/` 根层最新正式评估、`公司调研/公司索引.md`、MSI 正式公司调研、相关行业调研、`金融资料/每日金融数据/每日金融数据_2026-06-22.md` 和 `金融资料/区间涨跌/` 三个正式行情文件。未读取、引用或继承 `特征量化/`、Signals、回归、模型比较、`公司排序/`、`简单排序/`、`分析报告/tmp/` 或 `分析报告/备份/` 的结论。")
    if missing_finance:
        lines.append(f"> 金融资料覆盖差异：正式评估公司 {len(companies)} 家，最新金融快照覆盖 {len(companies) - len(missing_finance)} 家；缺少日度金融明细的公司为 {', '.join(missing_finance)}，价格/估值/IV/动量相关档位按资料不足或低置信处理。")
    if missing_price:
        lines.append(f"> 价格字段缺失或不可用公司：{', '.join(missing_price)}；这些公司在价格确认、估值消化、下行保护和激进短线中自动降权。")
    lines.append("")
    lines.append("## 1. 一页结论")
    lines.append("")
    lines.extend(
        [
            f"- A 最占优的投资思路：{'、'.join(a_best)}。MSI 的优势集中在公共安全/关键通信客户粘性、15.7B backlog、强 FCF、相对温和 Forward PE 和压力期防守质量。",
            f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是收入增速不是项目内最高、AI 数据中心直接收入占比低、不是 GPU/HBM/光互联/电力冷却主链，且近月价格确认不连续。",
            "- A 最适合的投资者画像：偏中期质量、防守、现金流和可兑现订单，愿意接受中个位数到低双位数收入增长、用 Silvus/Command/Video 作为附加右尾的资金。",
            "- A 最不适合的投资者画像：只追求极端高增长、小市值爆发、高 IV 短线、AI 主链订单或强动量确认的资金。",
            f"- 多数思路下最强反方公司：{strongest_b_names}。",
            f"- 如果只追求更高增长、更好公司，A 的总体位置：MSI 对 {a_majority_wins}/{len(sorted_bs)} 家公司多数思路占优，对 {b_majority_wins}/{len(sorted_bs)} 家公司多数思路落后；它是全项目里下行保护和估值消化强、NTM兑现中上、但右尾/动量/激进短线偏弱的高质量防守成长股。",
            "- 后续最重要跟踪数据：Q2/Q3 2026 MCN/Video/Command revenue growth、PSI与S&S backlog、Silvus单笔订单和扩产进度、FASST 6000客户、SVX联邦/州地采用、Hyper/Exacom/RapidDeploy客户和ARR、Avigilon/Blue Eye数据中心或关键基础设施客户、non-GAAP operating margin、FCF、库存、应收、净债务。",
        ]
    )
    lines.append("")
    lines.append("## 2. 公司 A 基准画像")
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 股票代号 | MSI |")
    lines.append("| 公司名称 | Motorola Solutions |")
    lines.append(f"| 产业链分类 | {a.category} |")
    lines.append(f"| 重要产品/业务线 | {base.md_escape(base.short_phrase(products, 340))} |")
    lines.append(f"| NTM 基准收入 | {base.md_escape(ntm)} |")
    lines.append(f"| 乐观/极度乐观收入 | {base.md_escape(optimistic)} |")
    lines.append(f"| 利润和现金流结论 | {base.md_escape(base.short_phrase(profit_cash, 300))} |")
    lines.append(f"| 最大传导瓶颈 | {base.md_escape(base.short_phrase(bottleneck, 300))} |")
    lines.append(f"| 最大反证 | {base.md_escape(base.short_phrase(bear, 300))} |")
    lines.append(f"| 近端催化剂 | {base.md_escape(base.short_phrase(catalysts, 300))} |")
    lines.append(f"| 日度市场数据 | {base.md_escape(finance_snapshot(a))} |")
    lines.append("")

    lines.append("## 3. 公司 A 全项目相对档位")
    lines.append("")
    lines.append("建档口径：对同一批正式评估公司，抽取基准/乐观/极度乐观 NTM 收入增速、经营利润率、毛利率、FCF/现金流、可信度、反证、估值、IV、区间涨跌和 SOXX 压力窗口表现。每个投资思路独立排序，`S` 约为前 8%，`A` 约为 8%-25%，`B` 约为 25%-50%，`C` 约为 50%-80%，`D` 为后 20%；日度价格或估值缺失时按资料不足/低置信处理。MSI 的人工校准只补入 FY2026 指引、15.7B backlog 和 FCF 对 NTM/防守/估值的支撑，同时保留其不是 AI 主链高右尾公司的限制。")
    lines.append("")
    lines.append("| 投资思路 | 公司 A 档位 | A 所处位置 | 关键支撑 | 主要限制 |")
    lines.append("| --- | --- | --- | --- | --- |")
    for strat in base.STRATEGIES:
        sup, lim = grade_support_limit(strat, a)
        lines.append(f"| {strat} | {a.grades[strat]} | {base.format_grade_position(a, strat)} | {base.md_escape(sup)} | {base.md_escape(lim)} |")
    lines.append("")

    lines.append("## 4. 可比关系使用说明")
    lines.append("")
    lines.append("| 可比关系 | 本报告使用口径 | 典型公司B | 对判断力度的影响 |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| 直接同业 | 与 MSI 在公共安全、关键通信、视频安防、门禁、工业/关键基础设施安全或任务关键网络上有较高客户和需求池重叠，优先比较订单/backlog、服务续约、客户锁定、收入兑现和同业估值 | ALLE、JCI、CSCO、NOK、VISN、FTV、TDY | 同档时必须复核谁真正吃到公共安全、企业安防、任务关键网络或物理安防预算；两档以上才给强烈建议 |")
    lines.append("| 相邻替代 | 不直接竞争但同属 AI 基础设施、工业自动化、物理安防、电力冷却或国防/边缘 AI 资金篮子，重点回答资金只能买一个时谁增长质量和赔率更好 | VRT、ETN、NVT、CARR、RKLB、BWXT、NVDA、AVGO、CRDO、ALAB | 默认按档位判断，避免把 AI 主链热度直接当胜负；若增长、估值或催化显著拉开，可给建议级别 |")
    lines.append("| 上下游 | 数据中心、云平台、软件/企业客户或运营商可能采购 MSI facility security、视频、无线电、Command/SOC 工作流，但也会把资金吸向更大 AI 下游平台 | AMZN、GOOGL、MSFT、META、ORCL、DLR、EQIX、APLD、NBIS、CRWV | 强调利润捕获，不把云厂商收入规模或数据中心建设金额自动转为 MSI 收入；AI DC 安防缺客户披露时只小比例计入 |")
    lines.append("| 跨赛道 | 医疗工具、材料、化学品、半导体设备之外的非相关公司，业务差异大但仍作为项目资金配置替代 | DHR、TMO、LIN、ECL、MMM、APD | 默认降低结论力度；证据互有强弱时优先中性或微倾向 |")
    lines.append("")

    lines.append("## 5. 全项目逐行投资思路决策表")
    lines.append("")
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要", *base.STRATEGIES, "多数思路方向", "最终更值得投", "最关键理由"]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---:" if h == "序号" else "---" for h in headers]) + " |")
    for row in rows:
        lines.append("| " + " | ".join(base.md_escape(x) for x in row) + " |")
    lines.append("")

    lines.append("## 6. 投资思路统计")
    lines.append("")
    stat_headers = ["投资思路", *base.LABEL_ORDER, "A侧合计", "B侧合计"]
    lines.append("| " + " | ".join(stat_headers) + " |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for strat in base.STRATEGIES:
        counter = stats[strat]
        a_total = counter["强烈建议投A"] + counter["建议投A"] + counter["微倾向投A"]
        b_total = counter["强烈建议投B"] + counter["建议投B"] + counter["微倾向投B"]
        vals = [str(counter[label]) for label in base.LABEL_ORDER]
        lines.append(f"| {strat} | " + " | ".join(vals) + f" | {a_total} | {b_total} |")
    lines.append("")

    def winning_strats(decisions: dict[str, str], side: str) -> str:
        out = [s for s, cell in decisions.items() if base.label_side(cell) == side]
        return "、".join(out) if out else "无"

    lines.append("## 7. 多数思路下 B 明显强于 A 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | B 胜出的主要投资思路 | 为什么 B 更值得投 | A 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(b_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'B')} | {b.ticker}在对应档位中高于MSI，且多数思路下增长、右尾、近端催化、价格确认或AI主链收入化证据更强。 | MSI需要Silvus/Command/Video连续超预期、AI安防或公共安全AI披露客户/ARR、收入增速上修、FCF维持且价格趋势重新确认。 |")
    if not b_rank_rows:
        lines.append("| 1 | 无 | 无 | 没有公司在多数思路下显著压过MSI | 继续跟踪backlog、Silvus、Command/Video和价格确认 |")
    lines.append("")

    lines.append("## 8. 多数思路下 A 明显强于 B 的公司")
    lines.append("")
    lines.append("| 排名 | 公司B | A 胜出的主要投资思路 | 为什么 A 更值得投 | B 需要什么证据才能反超 |")
    lines.append("| ---: | --- | --- | --- | --- |")
    for rank, (_, _, b, decisions) in enumerate(sorted(a_rank_rows, key=lambda x: (-x[0], -x[1], x[2].ticker)), start=1):
        lines.append(f"| {rank} | {b.ticker} / {base.md_escape(b.name)} | {winning_strats(decisions, 'A')} | MSI相对{b.ticker}的backlog、FCF、公共安全客户粘性、下行保护或估值消化更清楚。 | {b.ticker}需要更硬的NTM订单/利润兑现、现金流改善、估值消化证据和价格确认。 |")
    if not a_rank_rows:
        lines.append("| 1 | 无 | 无 | MSI没有在多数思路下明显压过其他公司 | 需等待backlog、利润和价格进一步确认 |")
    lines.append("")

    lines.append("## 9. 来源")
    lines.append("")
    lines.append(f"- 公司 A 评估文件：`{a.eval_path.relative_to(ROOT).as_posix()}`。")
    lines.append("- 公司 A 公司调研文件：`公司调研/机电_冷却_工程_水处理_边缘工业AI/MSI_Motorola Solutions_公司调研_2026-06-11.md`。")
    lines.append("- 公司全集文件清单生成口径：读取 `分析报告/公司评估/结果/` 根层所有 `*_收入传导估值评估_*.md` 正式报告；同一 Ticker 取文件名日期最新版本；目录、备份和临时文件不计入。")
    lines.append(f"- 公司全集数量和日期：正式评估 {len(companies)} 家；日期范围 {min(eval_dates)} 至 {max(eval_dates)}。")
    lines.append(f"- 日度数据来源：`{base.FINANCE_PATH.relative_to(ROOT).as_posix()}`（生成时间 {finance_meta.get('generated') or '见文件'}，价格/估值/IV 主日期 2026-06-22）；`{base.RET_2W_PATH.relative_to(ROOT).as_posix()}`、`{base.RET_1M_PATH.relative_to(ROOT).as_posix()}`（区间口径至 2026-06-03）；`{base.SOXX_PATH.relative_to(ROOT).as_posix()}`（SOXX 三段压力窗口生成于 2026-06-04）。")
    lines.append("- 关键行业资料：`行业调研/AI园区电力_机电_冷却/行业调研_机柜、围护结构与物理安防_2026-06-11.md`、`行业调研/AI服务器_存储_芯片/行业调研_AI边缘推理芯片_2026-06-11.md`、`行业调研/产业背景/行业调研_AI数据中心建设规模与产业链订单映射_2026-06-11.md`、`行业调研/产业背景/AI产业链全局图谱与口径字典_2026-06-11.md`。")
    lines.append(f"- 日度金融数据覆盖：2026-06-22 金融快照覆盖 {len(companies) - len(missing_finance)}/{len(companies)} 家；缺少当日金融明细的公司为 {('、'.join(missing_finance) if missing_finance else '无')}；价格字段缺失或不可用公司为 {('、'.join(missing_price) if missing_price else '无')}。")
    lines.append(f"- 公司 A 日度数据摘录：{finance_snapshot(a)}")
    lines.append("- 自动化脚本：`scripts/generate_msi_company_comparison.py`。脚本复用项目内正式评估与金融资料解析函数，对 MSI 的 FY2026 指引、15.7B backlog、Silvus、Command/Video、FCF、估值、IV、压力窗口和动量做人工校准后建档；未读取下游量化目录或现成排序结论。")
    lines.append("- 排除来源：未使用 `特征量化/`、`分析报告/公司排序/`、`分析报告/简单排序/`、`分析报告/备份/`、`分析报告/tmp/` 或项目根 `tmp/` 中的结论作为本次决策依据。")
    lines.append("")
    return "\n".join(lines)


base.relation_for = relation_for
base.reason_for = reason_for
base.final_choice = final_choice
base.grade_support_limit = grade_support_limit


def main() -> None:
    validate_supporting_sources()

    companies = base.load_latest_reports()
    if base.TARGET not in companies:
        raise SystemExit("MSI not found in formal company evaluation universe")

    index = base.load_index_categories()
    finance, _ = base.load_finance()
    ret_1m = base.load_return_table(base.RET_1M_PATH, "过去1个月涨跌幅")
    ret_2w = base.load_return_table(base.RET_2W_PATH, "过去两周涨跌幅")
    soxx = base.load_return_table(base.SOXX_PATH, "三段累计涨跌幅")

    for ticker, c in companies.items():
        if ticker in index:
            idx_name, cat = index[ticker]
            c.category = cat
            if c.name.replace(" ", "") == ticker:
                c.name = idx_name
        c.finance = finance.get(ticker, {})
        c.returns = {"1m": ret_1m.get(ticker), "2w": ret_2w.get(ticker), "soxx": soxx.get(ticker)}

    base.build_metrics(companies)
    base.assign_scores(companies)
    calibrate_msi(companies)
    base.assign_grades(companies)

    base.OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = make_report(companies)
    base.OUT_PATH.write_text(report, encoding="utf-8", newline="\n")
    print(base.OUT_PATH)
    print(f"companies={len(companies)} b={len(companies)-1} bytes={base.OUT_PATH.stat().st_size}")
    print("MSI grades:", {s: companies[base.TARGET].grades[s] for s in base.STRATEGIES})
    print("MSI ranks:", {s: companies[base.TARGET].ranks[s] for s in base.STRATEGIES})


if __name__ == "__main__":
    main()
