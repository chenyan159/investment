from __future__ import annotations

import importlib.util
import json
from collections import Counter
from pathlib import Path


ROOT = Path(r"D:\drive\Investment\基本面")
BASE_SCRIPT = ROOT / "scripts" / "generate_alle_company_comparison.py"
OUT_PATH = ROOT.parent / "分析报告" / "公司对比" / "结果" / "CARR_逐家公司投资思路对比_2026-06-23.md"
TARGET = "CARR"
REPORT_DATE = "2026-06-23"

spec = importlib.util.spec_from_file_location("base_company_comparison", BASE_SCRIPT)
if spec is None or spec.loader is None:
    raise SystemExit(f"无法加载基础生成脚本：{BASE_SCRIPT}")
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

base.TARGET = TARGET
base.OUT_PATH = OUT_PATH

STRATS = base.STRATS
TAG_ORDER = base.TAG_ORDER
TIER_VAL = base.TIER_VAL
INFRA_CATS = base.INFRA_CATS
ORIG_SCORE_COMPANIES = base.score_companies


def row(cells: list[object]) -> str:
    return base.row(cells)


def short_name(company: dict[str, object]) -> str:
    return base.short_name(company)


def category_short(category: str) -> str:
    return base.category_short(category)


def tag_in_cell(cell: str) -> str | None:
    return base.tag_in_cell(cell)


def relationship(company: dict[str, object]) -> str:
    ticker = str(company["ticker"])
    category = str(company["category"])
    direct = {"AAON", "DKILY", "JCI", "MOD", "TT", "VRT"}
    upstream_downstream = {
        "AMZN",
        "MSFT",
        "GOOGL",
        "META",
        "ORCL",
        "BABA",
        "IBM",
        "EQIX",
        "DLR",
        "CRWV",
        "APLD",
        "IREN",
        "NBIS",
        "NTNX",
        "CRWD",
        "ADBE",
    }
    if ticker in direct:
        return "直接同业"
    if ticker in upstream_downstream or category in {"云算力_IDC_AI软件平台", "AI服务器_存储_EMS"}:
        return "上下游"
    if category in INFRA_CATS or category in {"配电_电源_功率器件", "电力_发电_能源_储能"}:
        return "相邻替代"
    return "跨赛道"


base.relationship = relationship


def score_companies(companies: dict[str, dict[str, object]]) -> None:
    ORIG_SCORE_COMPANIES(companies)

    # base.score_companies applies the target adjustment block from the ALLE run.
    # Convert that adjustment into a Carrier-specific calibration and rebuild tiers.
    alle_adjustments = {
        "NTM兑现优先": -3,
        "右尾弹性优先": -12,
        "风险调整收益": -8,
        "下行保护优先": 2,
        "估值消化优先": -2,
        "近端催化优先": -8,
        "价格确认/动量": -3,
        "激进短线": -10,
    }
    carr_adjustments = {
        "NTM兑现优先": 0,
        "右尾弹性优先": -6,
        "风险调整收益": 2,
        "下行保护优先": 0,
        "估值消化优先": 1,
        "近端催化优先": 2,
        "价格确认/动量": 0,
        "激进短线": -3,
    }
    target = companies[TARGET]
    for strategy in STRATS:
        delta = carr_adjustments[strategy] - alle_adjustments[strategy]
        target["scores"][strategy] = base.clamp(target["scores"][strategy] + delta)  # type: ignore[index,operator]

    for company in companies.values():
        company["tiers"] = {}
        company["ranks"] = {}

    for strategy in STRATS:
        ordered = sorted(companies.items(), key=lambda item: item[1]["scores"][strategy], reverse=True)  # type: ignore[index]
        total = len(ordered)
        for rank, (_, company) in enumerate(ordered, start=1):
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
            company["tiers"][strategy] = tier  # type: ignore[index]
            company["ranks"][strategy] = rank  # type: ignore[index]

    for company in companies.values():
        if not company["fin"].get("price"):  # type: ignore[union-attr]
            for strategy in ["价格确认/动量", "激进短线", "估值消化优先"]:
                company["tiers"][strategy] = "资料不足"  # type: ignore[index]


base.score_companies = score_companies


def reason_for(strategy: str, tag: str, rel: str) -> str:
    if tag.endswith("投A"):
        return {
            "NTM兑现优先": "A订单/backlog和指引更清楚",
            "右尾弹性优先": "A数据中心热管理右尾更实",
            "风险调整收益": "A现金流和估值缓冲更均衡",
            "下行保护优先": "A多元业务和FCF底座更稳",
            "估值消化优先": "A低PS与FCF更易消化",
            "近端催化优先": "A H2数据中心出货验证更近",
            "价格确认/动量": "A短期价格确认更稳",
            "激进短线": "A有AI冷却和IV弹性",
        }[strategy]
    if tag.endswith("投B"):
        return {
            "NTM兑现优先": "B收入增速和订单锚更强",
            "右尾弹性优先": "B右尾收入弹性更大",
            "风险调整收益": "B上行赔率更好",
            "下行保护优先": "B资产质量或防御性更强",
            "估值消化优先": "B业绩增速更能覆盖估值",
            "近端催化优先": "B近端订单/产品催化更强",
            "价格确认/动量": "B价格确认更强",
            "激进短线": "B高弹性叙事更适合进攻",
        }[strategy]
    if rel == "跨赛道":
        return "业务差异大且证据互抵"
    if strategy in {"下行保护优先", "估值消化优先"}:
        return "安全性和估值接近"
    return "档位接近需再验证"


base.reason_for = reason_for


def key_reason(a: dict[str, object], b: dict[str, object], final: str) -> str:
    if final == "A":
        if a["scores"]["NTM兑现优先"] - b["scores"]["NTM兑现优先"] > 10:  # type: ignore[index,operator]
            return "CARR 的数据中心订单/backlog、2026指引和H2出货路径更清楚。"
        if a["scores"]["下行保护优先"] - b["scores"]["下行保护优先"] > 10:  # type: ignore[index,operator]
            return "CARR 的多元HVAC/冷链、约20亿美元FCF和中等估值提供更好缓冲。"
        if a["scores"]["估值消化优先"] - b["scores"]["估值消化优先"] > 10:  # type: ignore[index,operator]
            return "CARR 的P/S、Forward PE和FCF质量让当前估值更容易消化。"
        return "CARR 的AI冷却订单证据和现金流质量略好，B 的上行不足以抵消反证。"
    if b["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"] > 18:  # type: ignore[index,operator]
        return f"{b['ticker']} 的增长右尾和重定价弹性明显强于 CARR。"
    if b["scores"]["NTM兑现优先"] - a["scores"]["NTM兑现优先"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的 NTM 收入/订单兑现证据更强。"
    if b["scores"]["价格确认/动量"] - a["scores"]["价格确认/动量"] > 14:  # type: ignore[index,operator]
        return f"{b['ticker']} 的价格确认和短线资金偏好更强。"
    return f"{b['ticker']} 在多数投资思路下比 CARR 更符合项目内资金配置目标。"


base.key_reason = key_reason


def rank_position(a: dict[str, object], strategy: str, n: int) -> str:
    return f"第 {a['ranks'][strategy]}/{n}，{a['tiers'][strategy]} 档"  # type: ignore[index]


def render_report(companies: dict[str, dict[str, object]], comparisons: list[dict[str, object]]) -> str:
    a = companies[TARGET]
    n = len(companies)
    company_dates = [str(company["date"]) for company in companies.values()]
    date_range = f"{min(company_dates)} 至 {max(company_dates)}"
    stats = {strategy: Counter() for strategy in STRATS}
    for comparison in comparisons:
        for strategy, cell in zip(STRATS, comparison["cells"]):  # type: ignore[arg-type]
            stats[strategy][tag_in_cell(cell)] += 1
    a_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[:3]) for s in STRATS}
    b_side = {s: sum(stats[s][tag] for tag in TAG_ORDER[4:]) for s in STRATS}
    a_best = sorted(STRATS, key=lambda s: a_side[s] - b_side[s], reverse=True)[:3]
    a_worst = sorted(STRATS, key=lambda s: a_side[s] - b_side[s])[:3]
    strong_b = sorted(comparisons, key=lambda x: (x["bc"] - x["ac"], x["b"]["scores"]["右尾弹性优先"] - a["scores"]["右尾弹性优先"]), reverse=True)  # type: ignore[index,operator]
    strong_a = sorted(comparisons, key=lambda x: (x["ac"] - x["bc"], a["scores"]["NTM兑现优先"] - x["b"]["scores"]["NTM兑现优先"]), reverse=True)  # type: ignore[index,operator]
    strong_b_rows = [x for x in strong_b if x["bc"] >= 5 and x["bc"] - x["ac"] >= 3]  # type: ignore[operator]
    strong_a_rows = [x for x in strong_a if x["ac"] >= 5 and x["ac"] - x["bc"] >= 3]  # type: ignore[operator]
    missing_fin = [ticker for ticker in sorted(companies) if not companies[ticker]["fin"]]

    product_names = [str(product[0]).split("：")[0] for product in a["products"][:7]]  # type: ignore[index]
    file_list = "；".join([f"{ticker}:{companies[ticker]['path'].name}" for ticker in sorted(companies)])  # type: ignore[union-attr]
    rank_text = {s: rank_position(a, s, n) for s in STRATS}
    final_a = sum(1 for c in comparisons if c["final"] == "A")
    final_b = sum(1 for c in comparisons if c["final"] == "B")

    support = {
        "NTM兑现优先": ("2026指引约220亿美元、DC订单+500%+、backlog覆盖2026 DC sales，基准NTM收入223-228亿美元", "公司层收入增速仅+3%至+5%，住宅/RLC和Q1 OM拖累"),
        "右尾弹性优先": ("DC central plant/chiller、CDU、controls/DCIM/service有AI热管理上限，极度乐观收入248-260亿美元", "体量大导致弹性不如小基数液冷/光互联/NeoCloud，CDU客户和拆分仍少"),
        "风险调整收益": ("Forward PE 22.42、P/S 2.73、FCF约20-23亿美元，AI订单不是纯叙事", "若住宅弱和项目成本延续，DC增量会被利润率稀释"),
        "下行保护优先": ("多元HVAC、冷链、aftermarket/service和FCF底盘较稳", "SOXX压力三段累计-45.94%，防御性弱于公用事业/优质现金流平台"),
        "估值消化优先": ("P/S 2.73、Forward PE 22.42，若OM回到15.5%-16.2%且FCF恢复可消化", "增速不高，估值消化依赖利润率修复而非收入爆发"),
        "近端催化优先": ("2026H2 DC shipments、Commercial HVAC backlog转收入、data center sales是否超过15亿美元会被快速验证", "若Q2-Q3未见加速，订单证据会转为递延反证"),
        "价格确认/动量": ("截至2026-06-03过去两周+6.27%，2026-06-22价格已高于6月初收盘", "过去一月-0.06%，项目内AI高beta标的价格确认更强"),
        "激进短线": ("Call IV 46.1%，AI冷却/H2出货/订单披露具备事件弹性", "短线爆发力不如VRT、AAON、MOD、CRDO、NBIS等高关注标的"),
    }

    out: list[str] = [
        "# CARR 逐家公司投资思路对比",
        "",
        f"生成日期：{REPORT_DATE}",
        "公司 A：CARR / Carrier Global",
        "公司全集来源：分析报告/公司评估/结果/",
        f"项目内公司总数：{n}",
        f"被比较公司 B 数量：{n - 1}",
        f"公司评估文件日期范围：{date_range}",
        "日度数据日期：价格/估值/IV 为 2026-06-22；过去1个月/过去两周区间涨跌为 2026-06-03；SOXX三段压力窗口为 2026-06-04",
        "",
        "## 1. 一页结论",
        "",
        f"- A 最占优的投资思路：{'、'.join(a_best)}。CARR 的优势不在最高右尾，而在数据中心热管理订单已经进入公司收入表，同时仍有 HVAC、aftermarket、冷链和约20亿美元FCF底盘。",
        f"- A 最吃亏的投资思路：{'、'.join(a_worst)}。主要短板是公司总收入基数大、NTM增速只有中个位数、住宅/RLC和Q1利润率拖累，使右尾和激进短线弱于小基数AI主线。",
        "- A 最适合的投资者画像：希望配置AI数据中心冷却链条，但不愿只押高估值小基数液冷或纯主题公司的稳健成长型资金。",
        "- A 最不适合的投资者画像：只追求非线性收入上修、强价格爆发、极高IV或单季订单超预期的短线进攻型资金。",
        f"- 多数思路下最强反方公司：{'、'.join([x['ticker'] for x in strong_b_rows[:10]])}。这些公司通常有更高AI主链收入增速、更强订单/RPO/backlog透明度或更强动量。",
        f"- 如果只追求更高增长、更好公司，A 的总体位置：CARR 在 {n} 家正式评估公司中是中上游的AI冷却稳健型标的，不是全项目右尾冠军；本报告最终更值得投 CARR 的对比为 {final_a} 家，更值得投 B 的对比为 {final_b} 家。",
        "- 后续最重要跟踪数据：季度data center orders、Commercial HVAC book-to-bill/backlog、data center sales是否单列或超过15亿美元、chiller/CDU产能与客户认证、controls/DCIM attach、CSA/CSE/CSAME margin、Residential sell-through/channel inventory、中国RLC、FCF和net debt。",
        "",
        "## 2. 公司 A 基准画像",
        "",
        row(["项目", "内容"]),
        row(["---", "---"]),
        row(["股票代号", "CARR"]),
        row(["公司名称", "Carrier Global"]),
        row(["产业链分类", a["category"]]),
        row(["重要产品/业务线", "；".join(product_names)]),
        row(["NTM 基准收入", a["base_rev"] or "$22.3-22.8B"]),
        row(["乐观/极度乐观收入", f"乐观：{a['bull_rev']}；极度乐观：{a['extreme_rev']}"]),
        row(["利润和现金流结论", f"基准经营利润率：{a['base_margin']}；利润/现金流：{a['base_profit']}；{a['base_cash']}"]),
        row(["最大传导瓶颈", "订单到收入确认：大型数据中心冷却系统受制造、MEP同步、FAT/SAT、现场commissioning、客户上电窗口和验收节奏约束。"]),
        row(["最大反证", "2026Q1调整后OM下滑、FCF为负，Residential/China RLC拖累仍可能抵消数据中心订单增量。"]),
        row(["近端催化剂", "2026H2 data center shipments、Commercial HVAC backlog转收入、data center sales超过15亿美元、CDU/controls客户认证和FCF恢复。"]),
        "",
        "## 3. 公司 A 全项目相对档位",
        "",
        row(["投资思路", "公司 A 档位", "A 所处位置", "关键支撑", "主要限制"]),
        row(["---", "---", "---", "---", "---"]),
    ]
    for strategy in STRATS:
        out.append(row([strategy, a["tiers"][strategy], rank_text[strategy], support[strategy][0], support[strategy][1]]))  # type: ignore[index]

    out += [
        "",
        "说明：本节档位基于同一批正式评估公司建立，先用每家公司最新收入传导估值评估抽取 NTM/乐观/极度乐观、利润、现金流、证据和反证，再叠加日度价格、估值、IV、区间涨跌和 SOXX 压力窗口。未读取 `特征量化/`，也未用公司排序结果作为原始依据。",
        "",
        "## 4. 可比关系使用说明",
        "",
        row(["可比关系", "本报告使用口径", "典型公司B", "对判断力度的影响"]),
        row(["---", "---", "---", "---"]),
        row(["直接同业", "HVAC、数据中心冷却、液冷/CDU、热管理和楼宇控制需求池直接重叠，优先看订单/backlog、产品代际、毛利率、客户验收和同业估值。", "TT、JCI、AAON、MOD、DKILY、VRT", "同档或相邻档时要复核订单和收入拆分；直接同业证据强时允许更明确建议。"]),
        row(["相邻替代", "同属AI数据中心物理基础设施、配电、电力、工程或工业基础设施篮子，但产品不直接替代。", "ETN、NVT、PWR、GEV、FIX、EME、IESC、MYRG、DOV", "以增长质量、兑现确定性、估值消化和近端催化为主，不硬比产品细节。"]),
        row(["上下游", "B是云/IDC/服务器/存储等需求端或资本开支端，CARR是设施侧热管理供应商。", "MSFT、AMZN、GOOGL、EQIX、DLR、DELL、SMCI", "重点比较利润池、议价权、资本开支压力和客户集中度；下游收入规模不自动胜出。"]),
        row(["跨赛道", "半导体、材料、光互联、软件等与CARR业务差异大，但资金配置上仍可替代。", "NVDA、AVGO、TSM、ASML、CRDO、ALAB", "默认降低结论力度；只有增长质量、估值消化或风险收益明显拉开时才给建议/强烈建议。"]),
        "",
        "## 5. 全项目逐行投资思路决策表",
        "",
    ]
    headers = ["序号", "公司B", "公司B分类", "可比关系", "档位差摘要"] + STRATS + ["多数思路方向", "最终更值得投", "最关键理由"]
    out.append(row(headers))
    out.append(row(["---:", "---", "---", "---", "---"] + ["---"] * 8 + ["---", "---", "---"]))
    for index, comparison in enumerate(comparisons, start=1):
        b = comparison["b"]
        out.append(
            row(
                [
                    index,
                    short_name(b),  # type: ignore[arg-type]
                    category_short(str(b["category"])),  # type: ignore[index]
                    comparison["rel"],
                    comparison["summary"],
                    *comparison["cells"],  # type: ignore[list-item]
                    base.majority(comparison["ac"], comparison["bc"], comparison["nc"]),  # type: ignore[arg-type]
                    comparison["final"],
                    comparison["reason"],
                ]
            )
        )

    out += ["", "## 6. 投资思路统计", "", row(["投资思路"] + TAG_ORDER + ["A侧合计", "B侧合计"]), row(["---"] + ["---:"] * 9)]
    for strategy in STRATS:
        out.append(row([strategy] + [stats[strategy][tag] for tag in TAG_ORDER] + [a_side[strategy], b_side[strategy]]))

    out += ["", "## 7. 多数思路下 B 明显强于 A 的公司", "", row(["排名", "公司B", "B 胜出的主要投资思路", "为什么 B 更值得投", "A 需要什么证据才能反超"]), row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_b_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投B")]  # type: ignore[arg-type]
        need = "需要CARR披露更细的data center sales、CDU/controls客户认证和backlog，并把H2出货转成利润率与FCF恢复。"
        if comparison["rel"] == "跨赛道":
            need = "需要CARR证明其AI冷却增长和利润扩张能接近该跨赛道标的，或用更强FCF/估值缓冲抵消右尾差距。"
        out.append(row([index, short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += ["", "## 8. 多数思路下 A 明显强于 B 的公司", "", row(["排名", "公司B", "A 胜出的主要投资思路", "为什么 A 更值得投", "B 需要什么证据才能反超"]), row(["---:", "---", "---", "---", "---"])]
    for index, comparison in enumerate(strong_a_rows, start=1):
        b = comparison["b"]
        wins = [strategy for strategy, cell in zip(STRATS, comparison["cells"]) if (tag_in_cell(cell) or "").endswith("投A")]  # type: ignore[arg-type]
        need = "需要B提高收入确认可信度、现金流质量和估值消化能力，或出现明确订单/指引上修。"
        if b["scores"]["右尾弹性优先"] > a["scores"]["右尾弹性优先"]:  # type: ignore[index,operator]
            need = "需要B把右尾叙事转成可确认收入/利润，并降低估值、波动或现金流反证。"
        out.append(row([index, short_name(b), "、".join(wins), comparison["reason"], need]))  # type: ignore[arg-type]

    out += [
        "",
        "## 9. 来源",
        "",
        f"- 公司 A 评估文件：`分析报告/公司评估/结果/{a['path'].name}`。",  # type: ignore[union-attr]
        f"- 公司全集文件清单生成口径：从 `分析报告/公司评估/结果/` 根层读取 `*_收入传导估值评估_*.md`，同一 Ticker 取文件名日期最新版本；本次共 {n} 家，日期范围 {date_range}；未读取 `分析报告/备份/`、`分析报告/tmp/`、`公司排序/`、`简单排序/` 或 `特征量化/`。",
        f"- 公司全集最新正式评估文件清单：{file_list}",
        "- 日度数据来源：`金融资料/每日金融数据/每日金融数据_2026-06-22.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去两周_2026-06-03.md`；`金融资料/区间涨跌/公司股价区间涨跌幅_过去1个月_2026-06-03.md`；`金融资料/区间涨跌/公司股价三段SOXX下跌区间累计涨跌幅_2026-06-04.md`。",
        f"- 日度金融数据覆盖：2026-06-22 文件覆盖 {n - len(missing_fin)}/{n} 家；缺少当日价格/估值/IV 的公司为 {('、'.join(missing_fin) if missing_fin else '无')}，涉及估值、价格确认和激进短线列时按资料不足或保守口径处理。",
        "- 公司 A 日度数据摘录：2026-06-22 收盘价 `71.85`，市值 `$59.68B`，TTM PE `47.90`，Forward PE `22.42`，P/S `2.73`，Call IV `46.1%`，Put IV `51.3%`；2026-06-03 过去两周 `+6.27%`、过去一月 `-0.06%`；2026-06-04 三段 SOXX 压力窗口累计 `-45.94%`。",
        "- 其他主要来源：`公司调研/公司索引.md`、`公司调研/机电_冷却_工程_水处理_边缘工业AI/CARR_Carrier_Global_公司调研_2026-06-11.md`、`行业调研/行业索引.md`，以及 CARR 和各公司正式评估文件附录中列明的公司调研、行业调研和官方披露来源。",
        "",
    ]
    return "\n".join(out)


base.render_report = render_report


def main() -> None:
    companies = base.build_companies()
    score_companies(companies)
    comparisons = base.build_comparisons(companies)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(render_report(companies, comparisons), encoding="utf-8")
    summary = {
        "out": str(OUT_PATH),
        "companies": len(companies),
        "comparisons": len(comparisons),
        "size": OUT_PATH.stat().st_size,
        "carr_tiers": companies[TARGET]["tiers"],
        "carr_scores": {k: round(v, 2) for k, v in companies[TARGET]["scores"].items()},
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
