from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"D:\drive\Investment")
WORK = ROOT / "基本面" / "特征量化" / "_work" / "restructure_20260712"
OUTPUT_DIR = ROOT / "备份" / "特征量化全面重构_2026-07-12"
OUTPUT_FILE = OUTPUT_DIR / "特征量化全面重构审计_2026-07-12.md"
SCHEME_AUDIT = ROOT / "基本面" / "特征量化" / "_work" / "研究方案全面重构审计_2026-07-12.md"


def esc(value: object) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "—"
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def pct(value: object, digits: int = 1) -> str:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return "—"
    if not np.isfinite(x):
        return "—"
    return f"{x * 100:+.{digits}f}%"


def num(value: object, digits: int = 3) -> str:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return "—"
    if not np.isfinite(x):
        return "—"
    return f"{x:.{digits}f}"


def money(value: object) -> str:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return "—"
    if not np.isfinite(x):
        return "—"
    if abs(x) >= 100:
        return f"${x:,.2f}"
    return f"${x:,.3f}"


def table(headers: list[str], rows: list[list[object]], aligns: list[str] | None = None) -> str:
    aligns = aligns or ["---"] * len(headers)
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(aligns) + "|"]
    out.extend("| " + " | ".join(esc(v) for v in row) + " |" for row in rows)
    return "\n".join(out)


def load() -> dict[str, object]:
    scores = pd.read_csv(WORK / "feature_scores_long.csv", encoding="utf-8-sig")
    meta = pd.read_csv(WORK / "feature_files_metadata.csv", encoding="utf-8-sig")
    returns = pd.read_csv(WORK / "company_returns_2026-06-04_to_latest.csv", encoding="utf-8-sig")
    benchmarks = pd.read_csv(WORK / "benchmark_returns_2026-06-04_to_latest.csv", encoding="utf-8-sig")
    feature_eval = pd.read_csv(WORK / "feature_forward_evaluation.csv", encoding="utf-8-sig")
    v2_eval = pd.read_csv(WORK / "v2_group_forward_evaluation.csv", encoding="utf-8-sig")
    summary = json.loads((WORK / "forward_evaluation_summary.json").read_text(encoding="utf-8"))
    effective = json.loads((ROOT / "基本面" / "特征量化" / "有效指标清单_latest.json").read_text(encoding="utf-8-sig"))
    f01 = scores[scores["FeatureId"] == "F01"].set_index("Ticker")
    returns = returns.set_index("feature_ticker")
    returns["Ticker"] = returns.index
    returns["Company"] = f01["Company"].reindex(returns.index)
    returns["Category"] = f01["Category"].reindex(returns.index)
    returns["PriceReturnOpenClose"] = (
        returns["latest_close_split_adjusted_ex_distributions"].astype(float)
        / returns["entry_open_split_adjusted"].astype(float)
        - 1
    )
    return {
        "scores": scores,
        "meta": meta,
        "returns": returns,
        "benchmarks": benchmarks,
        "feature_eval": feature_eval,
        "v2_eval": v2_eval,
        "summary": summary,
        "effective": effective,
    }


def scheme_blueprint() -> str:
    text = SCHEME_AUDIT.read_text(encoding="utf-8-sig")
    start = text.index("## 五、16 个新核心特征的差异化研究方案骨架")
    end = text.index("## 八、正式研究方案文件应如何改")
    excerpt = text[start:end].strip()
    excerpt = excerpt.replace("## 五、", "## 十、").replace("## 六、", "## 十一、").replace("## 七、", "## 十二、")
    excerpt = excerpt.replace("### 7.", "### 12.")
    return excerpt


def main() -> None:
    d = load()
    meta: pd.DataFrame = d["meta"]
    returns: pd.DataFrame = d["returns"]
    benchmarks: pd.DataFrame = d["benchmarks"]
    fe: pd.DataFrame = d["feature_eval"]
    v2: pd.DataFrame = d["v2_eval"]
    effective: dict = d["effective"]

    bench = benchmarks.set_index("benchmark")
    prior_ids = set(effective["effectiveFeatureIds"])
    short_pass = set(fe.loc[fe["EmpiricalLabel"] == "短期样本外初步有效", "FeatureId"])
    prior_replicated = sorted(prior_ids & short_pass)
    prior_failed = sorted(prior_ids - short_pass)
    newly_positive = sorted(short_pass - prior_ids)
    fdr_negative = fe[(fe["FDR_Q"] <= 0.10) & (fe["Spearman"] < 0)]["FeatureId"].tolist()

    generation_rows = []
    for row in meta.sort_values("FeatureNumber").itertuples():
        generation_rows.append([
            row.FeatureId,
            row.FeatureNameFromFile,
            row.FileDate,
            str(row.CreationTimeLocal).replace(".000", ""),
            str(row.LastWriteTimeLocal).replace(".000", ""),
            row.DataSnapshotFileDate,
        ])

    performance_rows = []
    by_id = fe.set_index("FeatureId")
    for fid in sorted(by_id.index):
        r = by_id.loc[fid]
        performance_rows.append([
            fid,
            r["FeatureName"],
            num(r["Spearman"]),
            num(r["IndustryNeutralSpearman"]),
            num(r["IndustrySizeNeutralRankCorr"]),
            pct(r["Top30Bottom30"]),
            num(r["FDR_Q"], 4),
            r["EmpiricalLabel"],
            "是" if bool(r["PriorRetrospectiveEffective"]) else "否",
            r["Maturity"],
            r["RefactorAction"],
            r["V2Group"],
        ])

    company_rows = []
    ranked_returns = returns.sort_values("primary_adj_open_to_adj_close_return", ascending=False)
    for rank, (_, r) in enumerate(ranked_returns.iterrows(), start=1):
        action = ""
        if str(r.get("split_details", "")).strip() and str(r.get("split_details")) != "nan":
            action = str(r["split_details"])
        if r["Ticker"] == "PSTG":
            action = "官方已于2026-04-17改码为P；按P连续行情计算"
        company_rows.append([
            rank,
            r["Ticker"],
            r["Company"],
            r["Category"],
            money(r["entry_open_split_adjusted"]),
            money(r["latest_close_split_adjusted_ex_distributions"]),
            pct(r["PriceReturnOpenClose"]),
            pct(r["primary_adj_open_to_adj_close_return"]),
            pct(r["primary_excess_spy"]),
            pct(r["primary_excess_qqq"]),
            pct(r["primary_excess_soxx"]),
            action or "—",
        ])

    v2_rows = []
    order = [f"N{i:02d}" for i in range(1, 17)] + ["G01", "G02", "G03"]
    v2i = v2.set_index("FeatureId")
    for gid in order:
        r = v2i.loc[gid]
        v2_rows.append([
            gid,
            r["FeatureName"],
            r["Role"],
            r["Members"],
            num(r["MemberMeanPairwiseCorr"]),
            num(r["Spearman"]),
            num(r["IndustryNeutralSpearman"]),
            num(r["IndustrySizeNeutralRankCorr"]),
            pct(r["Top30Bottom30"]),
            num(r["FDR_Q_AcrossV2"], 4),
            r["EmpiricalLabel"],
        ])

    top = ranked_returns.head(10)
    bottom = ranked_returns.tail(10).sort_values("primary_adj_open_to_adj_close_return")
    top_text = "、".join(f"{r.Ticker} {pct(r.primary_adj_open_to_adj_close_return)}" for r in top.itertuples())
    bottom_text = "、".join(f"{r.Ticker} {pct(r.primary_adj_open_to_adj_close_return)}" for r in bottom.itertuples())

    feature_top = fe.sort_values("Spearman", ascending=False).head(10)
    feature_weak = fe.sort_values("Spearman").head(12)
    feature_top_text = "、".join(f"{r.FeatureId}({num(r.Spearman)})" for r in feature_top.itertuples())
    feature_weak_text = "、".join(f"{r.FeatureId}({num(r.Spearman)})" for r in feature_weak.itertuples())

    lines: list[str] = []
    add = lines.append
    add("# 特征量化全面重构审计：从 52 个模板化评分压缩为 16 个 Alpha 特征与 3 个门槛层")
    add("")
    add("审计日期：2026-07-12（America/Los_Angeles）  ")
    add("最新行情日期：2026-07-10（2026-07-12 为周日）  ")
    add("审计范围：`基本面/特征量化/量化评分/` 根目录 52 个正式结果、`研究方案/` 52 个方案；所有备份目录均排除。")
    add("")
    add("## 一、结论先行")
    add("")
    add("1. **全部 52 个正式结果都属于同一个信号截面。** 文件名、标题和正文评分日期均为 2026-06-04；文件系统时间代理为当日 00:47:51–04:07:37 PDT，全部早于 06:30 PDT 美股开盘；输入金融快照统一为 2026-06-03。正文没有精确运行时刻，因此不能把 CreationTime/LastWriteTime 伪装成业务运行日志。")
    add("2. **旧的“有效指标清单”不是预测有效性证明。** 它把 2026-06-04 的评分与截至 2026-05-27 的过去 6 个月收益、以及更早的 SOXX 压力窗口做相关，目标发生在信号之前；它最多是描述性相关，不能作为样本外选因子依据。")
    add(f"3. **本次样本外期只有 25 个交易日。** 180 家公司从 6 月 4 日复权开盘到 7 月 10 日复权收盘，等权均值 {pct(returns['primary_adj_open_to_adj_close_return'].mean())}、中位数 {pct(returns['primary_adj_open_to_adj_close_return'].median())}、上涨率 {pct((returns['primary_adj_open_to_adj_close_return'] > 0).mean())}；SPY/QQQ/SOXX 分别为 {pct(bench.loc['SPY','primary_adj_open_to_adj_close_return'])}/{pct(bench.loc['QQQ','primary_adj_open_to_adj_close_return'])}/{pct(bench.loc['SOXX','primary_adj_open_to_adj_close_return'])}。这是明显的样本池风险收缩期，不等于完整市场周期。")
    add("4. **短期真正有效的是一个共同的‘质量/防守’潜在因子，而不是 24 个独立因子。** F41、F47、F49、F45、F08、F05、F09 等排序最强；但 52 个分数的第一主成分已解释 55.2%，五个主成分解释 80.6%，有效维数约 3.0。把高度相关的 24 个显著结果分别加权，会把同一风险因子重复下注。")
    add("5. **研究方案的模板化问题非常严重。** 每份方案平均 81 个非空行，其中 72 行逐字相同，占 88.9%；归一化字符相同占 86.2%，词 3-gram 两两 Jaccard 均值 85.9%。这解释了为什么概念不同、实评分却大量共振。")
    add("6. **重构结论是 52→19，而不是在 52 个旧分上重新调权。** 新体系包含 16 个 Alpha 特征 N01–N16、证据质量门槛 G01、流动性门槛 G02、监管地缘风险覆盖层 G03；旧 F43 删除，F26 删除独立分数，F49/F51/F52 移出 Alpha。旧研究方案应整体归档，不能在原模板上小修。")
    add("")
    add("## 二、结果文件是什么时候生成的")
    add("")
    add("下面的“创建/写入时间”来自文件系统，只是时刻代理；可审计的业务日期仍是文件名、标题和正文共同确认的 2026-06-04。所有文件都使用 2026-06-03 金融快照，覆盖相同 180 个 ticker、每个特征 180 行，共 9,360 行。")
    add("")
    add(table(
        ["特征", "名称", "评分日期", "CreationTime 代理", "LastWriteTime 代理", "输入快照日期"],
        generation_rows,
        ["---", "---", "---", "---", "---", "---"],
    ))
    add("")
    add("### 2.1 文件内部质量异常")
    add("")
    add("- 52 个 ticker 集合完全一致，无缺排名、重复排名、非法分数或非法置信度。")
    add("- F10 是公司名称不一致的唯一来源，影响 71 个 ticker；其中 ASGLY 被写成 Asahi Group Holdings（正确为 AGC Inc），MICLF 被实际评价成 Micronics Japan（正确为 Mycronic AB），这两条 F10 观测已从本次 F10 清洁评估中剔除。")
    add("- F11 用反引号包裹分类目录，F27 在分类末尾多写斜杠，导致 180 家公司的分类字符串各出现 3 个版本；本次统一使用 F01 的干净分类。")
    add("")
    add("## 三、行情口径与全样本概况")
    add("")
    add("主评估口径为 **2026-06-04 拆股和分红复权开盘 → 2026-07-10 复权收盘**，因为 52 个结果均在 6 月 4 日开盘前生成；附表同时给出拆股校正但不含分红的纯价格收益。行情来自 Yahoo Finance chart JSON，每行保留 source URL；复权定义参考 [Yahoo Finance Adjusted Close 说明](https://uk.help.yahoo.com/kb/finance/adjusted-close-sln28256.html)。")
    add("")
    add("- 180/180 公司均取得有效行情；15 个 OTC 报价均为 USD。")
    add("- CRWD 期间 4:1 拆股、KLAC 期间 10:1 拆股；若直接用两个日度快照原价相除，会被误判为约 -74% 和 -89%，复权后主收益分别为 +11.1% 和 +12.7%。公司行动分别由 [CrowdStrike SEC 8-K](https://www.sec.gov/Archives/edgar/data/1535527/000153552726000022/crwd-20260603.htm) 和 [KLA 官方公告](https://ir.kla.com/news-events/press-releases/detail/515/kla-corporation-announces-ten-to-one-stock-split-and)确认。")
    add("- 旧代码 PSTG 已于 2026-04-17 正式改为 P；本次按 P 的连续行情计算，依据 [Everpure 官方公告](https://www.everpuredata.com/company/newsroom/press-releases/everpure-to-change-ticker-symbol.html)。")
    add(f"- 最强 10 家：{top_text}。")
    add(f"- 最弱 10 家：{bottom_text}。")
    add("")
    add("## 四、旧 52 个特征的样本外有效性")
    add("")
    add("指标口径：Spearman 是分数与主收益的横截面排序相关；行业中性是在 10 个分类内分别做百分位后合并；行业+规模中性是对分类哑变量和期初市值对数做残差相关；Top30-Bottom30 是高分 30 家减低分 30 家平均收益；q 值来自 20,000 次置换检验后对 52 次检验做 Benjamini-Hochberg 校正。")
    add("")
    add(f"- 排序最强 10 项：{feature_top_text}。")
    add(f"- 排序最弱 12 项：{feature_weak_text}。")
    add(f"- 旧清单 22 项中，短期样本外初步复现 14 项：{'、'.join(prior_replicated)}。")
    add(f"- 旧清单未复现 8 项：{'、'.join(prior_failed)}；其中 F44 上行弹性显著反向。")
    add(f"- 旧清单漏掉但本次短期正向的 10 项：{'、'.join(newly_positive)}。")
    add(f"- 经多重检验仍显著反向的特征：{'、'.join(fdr_negative) if fdr_negative else '无'}。")
    add("")
    add(table(
        ["特征", "名称", "ρ", "行业中性ρ", "行业+规模中性ρ", "T30-B30", "FDR q", "短期判定", "旧清单", "期限成熟度", "重构动作", "V2"],
        performance_rows,
        ["---", "---", "---:", "---:", "---:", "---:", "---:", "---", "---", "---", "---", "---"],
    ))
    add("")
    add("### 4.1 如何读这些短期结果")
    add("")
    add("- **不能把显著数量当成独立特征数量。** 1326 个分数对的平均 Pearson 为 0.487、中位 0.567；110 对绝对相关不低于 0.80，行业去均值后反而有 144 对不低于 0.80，重复不是单纯行业构成。")
    add("- **当前窗口奖励的是防守质量。** F41 负向预期差风险、F47 客户集中风险、F45 执行风险、F08/F09 财务质量、F05-F07 估值共同领先；这与样本池平均跌幅远大于 SPY/QQQ/SOXX 的风险收缩背景一致。")
    add("- **F49/F51 不应因为短期有效就留在 Alpha。** F49 反映信号可信度，F51 在加入规模后相关从 0.207 降到 0.076；两者分别应作为可靠度收缩和可投资性门槛。")
    add("- **期限未成熟的结果不能用于定罪。** F11/F14/F17/F38 的 3-6 月目标和 F12/F15/F18/F39 的 6-12 月目标都尚未成熟；短期结果只用于发现设计错误和重复，不能证明长期经济假设无效。")
    add("- **但设计层面的失败已经足够明确。** F24-F27 内部平均相关约 0.81，四项样本外几乎都为零；这说明把同一 AI capex 叙事拆成四个主观分数既重复又没有公司级传导力，必须重建为一条可核算的收入/毛利桥。")
    add("")
    add("## 五、哪些特征大量重复，哪些效果不好")
    add("")
    add("### 5.1 必须强制合并的实评分重复簇")
    add("")
    add("- F02+F21：关键节点与功能瓶颈实质相同；合并为 N02，保留系统重要性、替代供应商、认证时间、切换损失四个可观察子项。")
    add("- F05-F07：当前估值、同业/历史分位、隐含增长门槛是同一个估值模型的输入；合并为 N05。")
    add("- F08+F09：资产负债表与现金转换属于同一财务质量模型；合并为 N06，但保留两个子量。")
    add("- F10-F15：收入/利润×三个期限是一个期限结构，不应形成 6 个可重复加权分数；合并为 N07 的六个底层字段。")
    add("- F16-F18+F45：交付、产能、执行是同一兑现概率树；合并为 N08。")
    add("- F19/F20/F23：商业化阶段、平台适配、路线主流概率是同一采用树；合并为 N09。")
    add("- F22/F29/F35/F46：复制难度、切换成本、持续优势、替代风险是护城河的正反两面；合并为 N10。")
    add("- F24-F27：单位价值量、传导链、行业空间、capex 弹性是同一桥接公式；合并为 N03，F26 删除独立公司分。")
    add("- F28/F30-F32/F47：客户、可见度、订单刚性/下修和集中度应统一为逐订单期望毛利模型 N11。")
    add("- F33/F34/F36：行业供需 regime 与公司定价/产能 capture 是同一乘法链，合并为 N12，但行业共同值不可直接当公司 Alpha。")
    add("- F37-F39：同一事件按三个时间桶重复；合并为带日期、概率、surprise、影响和时间衰减的事件表 N13。")
    add("- F03/F40/F41：重估空间、正向预期差、负向风险是一个有符号 Gap；合并为 N14。")
    add("- F42/F44：上行弹性是情景收益分布右尾；合并为 N15。F44 当前显著反向，禁止把旧分简单平均进新模型。")
    add("")
    add("### 5.2 当前效果差、必须重做而不是简单保留的项目")
    add("")
    add("- **F44 上行弹性：** Spearman -0.225、行业中性 -0.217、T30-B30 -13.1%，q=0.0094；旧清单曾把它列为有效，现在是最明确的反例。")
    add("- **F50 价格相对强度：** Spearman 0.004、行业中性 -0.017；旧方案的短窗口主观代理没有产生真正的残差动量，必须改成复权 21/63/126/252 日行业、规模、beta 中性信号。")
    add("- **F10-F12 收入期限：** F10/F12 近零、F11 微负；F10 还存在两处评价对象替换。新方案必须保存预测 vintage，计算修正而非从叙事判断“会兑现”。")
    add("- **F24-F27 AI capex 传导组：** 四项几乎无排序力且内部高相关；停止分开打分，改用 `capex→单位量→内容量→份额→收入→毛利/EV` 的逐跳公式。")
    add("- **F31 订单刚性：** Spearman 0.003；框架协议、pipeline、供应承诺和可取消订单混在一起，必须改为逐订单转化概率、时间折现和毛利。")
    add("- **F37-F39 催化剂：** 三项短期均弱；F37 的 1-3 月已部分成熟仍接近零，说明“催化剂强弱”缺少事件日期、概率、surprise 和未计价程度。")
    add("- **F43 基本面兑现确定性：** 与 F39 分数相关 0.941，是对底层信号的元汇总；规模中性相关为负，应删除独立分数，确定性改成每个底层概率和 G01 可靠度。")
    add("")
    add("## 六、V2 的 16 个 Alpha 与 3 个门槛层")
    add("")
    add("下表的 V2 分数是把旧成员分位等权平均得到的**诊断值**，不是建议直接上线的公式。它用于判断重构方向是否会把有效信息完全抵消；真正上线必须按第十至十二节的专有公式重算。")
    add("")
    add(table(
        ["V2", "名称", "角色", "旧成员", "成员均相关", "ρ", "行业中性ρ", "行业+规模中性ρ", "T30-B30", "V2-FDR q", "当前诊断"],
        v2_rows,
        ["---", "---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"],
    ))
    add("")
    add("V2 读数最重要的不是谁当前最高，而是哪些组合需要改公式：N05/N06/N08/N10/N11 有清晰短期信号；N03、N15、N16 用旧分合成后近零，说明它们必须从原始变量重建，不能把旧分取平均；N07/N13 期限尚未成熟，但方案结构必须立即改成期限字段和事件表。")
    add("")
    add("## 七、旧研究方案文件的具体处理")
    add("")
    add("### 7.1 文件级迁移")
    add("")
    add("1. 把当前 `研究方案/F01...F52` 52 份全部移动到 `备份/特征量化研究方案重构前_2026-07-12/研究方案/`，保留原字节与时间信息。")
    add("2. 在正式 `研究方案/` 新建 `00_通用PIT与验证规范.md`，只放公共数据契约、PIT、防前视、输出字段和验证规则。")
    add("3. 新建 N01-N16 与 G01-G03 共 19 份专有方案；每份只保留该特征独有的经济机制、原始变量、公式、适用业务模式、失败条件、缺失先验和验证目标，不再复制 72 行公共模板。")
    add("4. 更新 `特征量化索引.md`：删除“52 个必做核心特征”，改为 16 Alpha+3 门槛；旧 F 编号只保留迁移映射，不能继续运行。")
    add("5. 旧 `量化评分/` 结果保留为 2026-06-04 历史截面，但在索引中标记 `legacy_schema_v1`，禁止覆盖后继续与 V2 混排。")
    add("")
    add("### 7.2 还必须修改的相邻文件和脚本")
    add("")
    add("- `特征评估/研究方案/特征评估.md`：删除“当前分数 vs 过去 6 个月收益”；改成信号公开后下一可交易时点进入、按预注册持有期做 walk-forward，使用 embargo 防重叠泄漏，并报告 IC 均值、ICIR、单调性、换手、成本、最大回撤、行业/规模/beta 中性和 FDR。")
    add("- `基本面/scripts/build_effective_feature_registry.mjs`：只读取完成目标期限的前向 cohort；至少要求多个截面、方向一致、FDR 合格和交易成本后 spread 为正。`generatedAt` 不能让旧回溯结果看起来是新验证。")
    add("- `有效指标清单_latest.json`：schema 升级，加入 `status=experimental/validated/retired`、`nCohorts`、`oosStart/oosEnd`、`holdingPeriod`、`qValue`、`ICIR`、`turnover`、`dataQualityGate`；现有 22 项应重命名为“历史描述性相关清单”，不再称有效。")
    add("- `量化评分` 输出契约：每条观测保存 `feature_version,ticker,as_of_date,public_timestamp,tradable_timestamp,raw_value,unit,transform,peer_group,z_raw,z_neutral,reliability,interval_low/high,missing_reason,source_ids`；1-10 只作为展示分，NA 必须保持 NA。")
    add("- `基本面/scripts/generate_daily_financial_snapshot.py`：增加 split-adjusted open/close、total-return adjusted close、dividend/split/capital-gain events、ticker/CUSIP 映射、stale quote 与 delisting 状态；禁止只存 raw currentPrice 后跨日直接相除。")
    add("- `基本面/特征量化/AGENTS.md`：新增硬规则——财报按首次公开时间、盘后信息下一交易日生效、后来披露不得回填旧截面、无 vintage 不得声称“修正”、门槛层不得与 Alpha 机械加分。")
    add("")
    add("## 八、验证与淘汰制度")
    add("")
    add("- 以月度或财报日为信号截面，至少积累 12 个非重叠 cohort；1-3 月特征最早在 3 个月后作第一次正式判定，3-6 月和 6-12 月按自身期限等待。")
    add("- 每个特征必须先预测自己的经营目标（surprise、订单转化、毛利、里程碑、概率校准），再验证股价；只看股价会把 beta 和市场 regime 当能力。")
    add("- Alpha 保留门槛：方向预注册；行业+规模中性 IC 均值为正；至少 60% cohort 同向；FDR q≤0.10；成本后 Top-Bottom 为正；滚动窗口不依赖单一行业或极端股。")
    add("- 删除门槛：连续两个完整验证周期方向反向，或与另一个特征相关>0.80且增量回归/消融无贡献，或关键 raw 字段无法 PIT 保存。")
    add("- 权重按跨期 ICIR、稳定性和独立性决定；禁止因为单一截面 ρ 高就高权重。")
    add("")
    add("## 九、完整 180 家公司股价/总回报明细")
    add("")
    add("纯价格收益已做拆股校正、不含分红；复权总回报包含分红并用于特征评估。起点是 2026-06-04 开盘，终点是 2026-07-10 收盘。超额收益以复权总回报计算。")
    add("")
    add(table(
        ["排名", "Ticker", "公司", "分类", "起点拆股校正开盘", "终点拆股校正收盘", "纯价格收益", "复权总回报", "超SPY", "超QQQ", "超SOXX", "公司行动/备注"],
        company_rows,
        ["---:", "---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:", "---"],
    ))
    add("")
    add(scheme_blueprint())
    add("")
    add("## 十三、最终重构顺序")
    add("")
    add("1. 立即停止用旧 `有效指标清单_latest.json` 驱动权重或排序。")
    add("2. 先落地公共 PIT 数据契约、复权/公司行动管线和 walk-forward 评估器。")
    add("3. 第一批重做 N04/N05/N06/N08/N10/N11、G01/G02/G03；这些项目当前有较清楚经济机制和短期实证。")
    add("4. 第二批重做 N01/N02/N09/N12/N14；保留子字段，先验证经营目标。")
    add("5. 第三批从零重建 N03/N07/N13/N15/N16；它们不能沿用旧分平均。")
    add("6. 旧 52 方案归档后运行 V2 第一个新截面；未完成目标持有期前只标 `experimental`，不发布“有效”结论。")
    add("")
    add("## 十四、限制")
    add("")
    add("本次只有一个 25 交易日样本外截面，且恰逢样本池风险收缩；它足以识别拆股/代码/对象错误、模板重复、同质分数和明显反向特征，但不足以估计长期 ICIR 或证明 3-12 月特征失效。正式删除基于概念重复和测量污染；长期效果判定必须等待各自目标期限成熟并积累多个 PIT cohort。")
    add("")
    add("## 十五、数据与可复现底稿")
    add("")
    add("- 结果解析：`基本面/特征量化/_work/restructure_20260712/audit_feature_results.ps1`")
    add("- 行情下载与公司行动：`基本面/特征量化/_work/restructure_20260712/download_feature_returns.ps1`")
    add("- 特征样本外评估：`基本面/特征量化/_work/restructure_20260712/evaluate_forward_features.py`")
    add("- 结构化分数：`feature_scores_long.csv`、`feature_scores_wide.csv`")
    add("- 行情底稿：`company_returns_2026-06-04_to_latest.csv`、`price_history_daily.csv`")
    add("- 评估底稿：`feature_forward_evaluation.csv`、`v2_group_forward_evaluation.csv`")
    add("- 方案模板重复审计：`基本面/特征量化/_work/研究方案全面重构审计_2026-07-12.md`")
    add("- 实评分重复审计：`基本面/特征量化/_work/实评分重复性审计_2026-07-12.md`")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(OUTPUT_FILE)
    print(f"bytes={OUTPUT_FILE.stat().st_size}; lines={len(lines)}")


if __name__ == "__main__":
    main()
