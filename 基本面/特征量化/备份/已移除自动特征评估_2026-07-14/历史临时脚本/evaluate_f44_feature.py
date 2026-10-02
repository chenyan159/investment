from __future__ import annotations

import importlib.util
import re
from pathlib import Path


ROOT = Path(r"D:\drive\Investment\基本面")
BASE_SCRIPT = ROOT / "tmp" / "evaluate_F30_feature_2026_06_04.py"
REPORT_DATE = "2026-06-04"
FEATURE_ID = "F44"
FEATURE_NAME = "上行弹性"
FEATURE_STEM = f"{FEATURE_ID}_{FEATURE_NAME}"
WINDOW = "6个月"


def load_base_module():
    spec = importlib.util.spec_from_file_location("feature_eval_base_f30", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load base evaluator from {BASE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replace_line(report: str, prefix: str, replacement: str) -> str:
    pattern = rf"^{re.escape(prefix)}.*$"
    return re.sub(pattern, replacement, report, flags=re.MULTILINE)


def customize_report(report: str) -> str:
    report = report.replace("F30", FEATURE_ID).replace("收入可见度", FEATURE_NAME)

    report = replace_line(
        report,
        "- 排序有效性：",
        "- 排序有效性：部分成立。全样本 Pearson 0.224, Spearman 0.236, Kendall 0.161；重点指标 Spearman 0.236，说明 F44 对本次6个月涨跌有弱到中等的正向排序解释力。方向与“上行弹性”定义一致，但不是高强度单因子。",
    )
    report = replace_line(
        report,
        "- Top/Bottom能力：",
        "- Top/Bottom能力：成立。Top10、Top20、Top30 平均收益分别为 +72.51%、+107.59%、+130.99%；Top-Bottom收益差分别为 +65.99%、+64.14%、+74.66%。高分组命中率均为90.0%，低分组命中率为50.0%/75.0%/80.0%，说明 F44 对抓取上涨弹性有效，但并非排除所有亏损样本。",
    )
    report = replace_line(
        report,
        "- 风险解释力：",
        "- 风险解释力：不成立，且呈高 beta 特征。Top30 压力窗口均值 -25.03%，Bottom30 为 -12.30%；Top30 平均最差窗口 -40.24%，Bottom30 为 -24.01%；Top30 近ATM IV均值 +91.41%，Bottom30 为 +51.10%。F44 高分更像上行弹性/波动暴露，不是低回撤或低波动特征。",
    )
    report = replace_line(
        report,
        "- 分类中性：",
        "- 分类中性：仍成立。分类内百分位合并 Spearman 0.205，分类去均值残差 Spearman 0.192；中性Top30-Bottom30收益差 +86.43%。结果不只是押中某个强势分类，类内排序也保留正向信息。",
    )
    report = replace_line(
        report,
        "- 稳健性：",
        "- 稳健性：三项合并剔除后样本 114 家，Spearman 0.247，Top30-Bottom30 +54.20%；剔除低流动性、ADR/币种异常和极端涨跌后，F44 的正向排序仍成立。极端涨跌剔除后 Spearman 降至0.167、Top30-Bottom30降至+36.29%，说明一部分有效性来自高弹性尾部赢家，但不是完全由极端样本驱动。",
    )
    report = replace_line(
        report,
        "- 解释：",
        "- 解释：F44 衡量需求或公司执行超预期时的收入、利润、EPS、现金流或估值上修幅度。高分端集中在 CRWV、CRDO、NBIS、DELL、POWL、PSIX、SMCI、ALAB、IREN、MOD、COHR、VRT 等小基数、高AI纯度、订单/backlog、AI云/服务器/光互联/配电冷却弹性较强的公司；本窗口涨幅头部包含 AXTI、SNDK、AAOI、MXL、AEHR、ICHR、MU、VICR、MRAM、FCEL 等，F44 对其中不少公司给出中高分，因此能解释一部分6个月反弹。但高分也包含 PSIX、SMR、OKLO、BABA 等负收益或弱收益样本，说明“有上行空间”仍需要估值、融资、兑现节奏和风险控制共同过滤。",
    )

    report = report.replace(
        "说明：分类中性 Top30/Bottom30 可能出现局部正差，但 Top10/Top20 仍为负且分类内百分位、残差相关均为负，因此不把该结果判定为稳定有效。",
        "说明：分类中性 Top/Bottom 用于检验 F44 是否只是押中 AI服务器、光互联、半导体材料、配电或云算力等强势目录。本次分类内百分位、去均值残差和中性Top/Bottom均为正，说明 F44 在同一分类目录内也能区分上行弹性强弱；但类内相关并非所有目录都为正，后续仍需与估值赔率和流动性过滤联用。",
    )
    report = report.replace(
        "分类内结果用于检验是否只是押中某个行业。若同一分类内 Spearman 多数为负或分散，说明 F44 在该窗口更像收入确定性/质量信息，而不是短期收益弹性信息。",
        "分类内结果用于检验是否只是押中某个行业。F44 类内 Spearman 在半导体材料、机电冷却、云算力、AI网络和封测检测中较强，在AI服务器、AI计算芯片、晶圆制造和电力目录中偏弱或为负，说明该特征对“低基数+订单/产能/重估”的弹性股更有效，对成熟大盘或强周期目录需要额外过滤。",
    )
    report = report.replace(
        "结论：高分组压力窗口均值不优于低分组，高分组当前IV不低于低分组。F44 高分公司通常收入确认路径更清晰，但在压力窗口中仍包含云平台、AI服务器、工程建设、核电/电力和高估值软件等高久期或高贝塔资产，不能自然等同于更低回撤。",
        "结论：高分组压力窗口均值不优于低分组，高分组当前IV不低于低分组。F44 高分公司通常具备更大的订单、容量、收入基数、经营杠杆或估值重估弹性，但这些弹性在压力窗口中也会体现为更深回撤和更高隐含波动，不能自然等同于更低回撤。",
    )
    report = report.replace(
        "稳健性结论：如果三项合并剔除后 Spearman 和 Top30-Bottom30 仍没有转为稳定正数，则 F44 暂不适合直接作为6个月收益排序因子；更适合作为基本面兑现确定性、估值兑现压力和风险复核中的约束变量。",
        "稳健性结论：F44 在全样本、剔除低流动性、剔除ADR/币种异常和三项合并剔除后均保持正向 Spearman 与正向Top30-Bottom30，说明其不是纯粹依赖异常交易或币种口径。极端涨跌剔除后仍为正但强度下降，提示本因子适合捕捉上行弹性和高beta赢家，不适合单独承担防守或低波动目标。",
    )
    report = report.replace(
        "本次 F44 的高分多来自 RPO/backlog/长期合同、明确订单或订阅收入池。该信息对收入兑现和下行基本面风险有意义，但在强反弹窗口里往往输给低分高弹性公司：低上行弹性公司一旦出现订单、融资、产能或周期预期修复，价格弹性可能远大于高分成熟公司。",
        "本次 F44 的高分多来自小收入基数、明确订单/backlog或容量释放、AI收入纯度、经营杠杆、估值重估空间和可验证的业务节点。该信息对6个月涨跌的排序有正向解释，但高分组合也承担更高压力窗口回撤和更高当前IV；因此 F44 应被理解为“上涨/波动弹性”特征，而不是“稳健收益”特征。",
    )

    usage_pattern = re.compile(r"## 使用建议\n.*?\n## 数据与方法限制", flags=re.DOTALL)
    usage = (
        "## 使用建议\n"
        "- 可以把 F44 作为上行弹性单因子使用，但只能给出弱到中等权重；Spearman 0.236 和稳健性结果支持其正向排序价值，风险窗口和IV结果不支持其作为防守因子。\n"
        "- 组合构建上更适合用 F44 做“进攻篮子”筛选：优先关注高分且同时具备估值赔率、流动性、订单刚性和催化剂验证的公司；剔除高分但融资/监管/商业化不确定性过高的样本。\n"
        "- 与 F05当前估值赔率、F31订单刚性与可确认性、F37/F38/F39催化剂强度、F43基本面兑现确定性和 F51交易流动性联用更有价值：F44 回答“上修空间有多大”，但不回答“是否便宜”“何时兑现”“能否承受回撤”。\n"
        "- 对低分但涨幅极高公司，应复核是否存在评分遗漏的新订单、融资、产能、行业反转或低基数题材；对高分但负收益公司，应重点复核估值拥挤、融资稀释、项目延期、客户集中和监管/许可风险。\n"
        "\n"
        "## 数据与方法限制"
    )
    report = usage_pattern.sub(usage, report)
    return report


def main() -> None:
    base = load_base_module()
    base.FEATURE_ID = FEATURE_ID
    base.FEATURE_NAME = FEATURE_NAME
    base.FEATURE_STEM = FEATURE_STEM
    base.WINDOW = WINDOW
    base.REPORT_DATE = REPORT_DATE
    base.SCORE_PATH = ROOT / "特征量化" / "量化评分" / f"{FEATURE_STEM}_量化评分_{REPORT_DATE}.md"
    base.RETURN_PATH = ROOT / "日度资料" / "区间涨跌" / "公司股价区间涨跌幅_2026-05-27.md"
    base.F51_PATH = ROOT / "特征量化" / "量化评分" / f"F51_交易流动性_量化评分_{REPORT_DATE}.md"
    base.FIN_PATH = ROOT / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-03.md"
    base.OUT_DIR = ROOT / "特征量化" / "特征评估"
    base.BACKUP_DIR = base.OUT_DIR / "备份"
    base.OUT_PATH = base.OUT_DIR / f"{FEATURE_STEM}_特征评估_{WINDOW}涨跌_{REPORT_DATE}.md"

    report, metadata = base.build_report()
    report = customize_report(report)
    base.OUT_PATH.write_text(report, encoding="utf-8")
    print(
        f"wrote={metadata['out_path']}\n"
        f"score_rows={metadata['score_rows']} return_rows={metadata['return_rows']} eval_rows={metadata['eval_rows']}\n"
        f"spearman={float(metadata['spearman']):.6f} top30_diff={float(metadata['top30_diff']):.6f}\n"
        f"moved={metadata['moved']}"
    )


if __name__ == "__main__":
    main()
