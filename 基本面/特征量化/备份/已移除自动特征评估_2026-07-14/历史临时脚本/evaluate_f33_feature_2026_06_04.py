from __future__ import annotations

import importlib.util
import re
from pathlib import Path


ROOT = Path(r"D:\drive\Investment\基本面")
BASE_SCRIPT = ROOT / "tmp" / "evaluate_F30_feature_2026_06_04.py"
REPORT_DATE = "2026-06-04"
FEATURE_ID = "F33"
FEATURE_NAME = "市场供给紧张度"
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
        "- 解释：",
        "- 解释：F33 衡量真实供不应求、交期延长、订单积压、slot锁定、客户提前下单或抢供是否能转化为公司级收入可见度和定价权。高分端集中在 GEV、VRT、ETN、TSM、NVDA、TT、POWL、FIX、MU、PWR 等供需紧张证据强的电力设备、冷却/工程、先进制造和AI硬件链条；但本窗口涨幅头部同时包含 AXTI、AAOI、MXL、AEHR、ICHR、MRAM、FCEL、NVTS、WOLF 等中低分或低置信度高贝塔标的。2025-11至2026-05 的6个月收益更像低基数修复、存储/光互联/设备周期、题材扩散和小盘弹性共同驱动，而不是单纯由供给紧张度排序决定。",
    )
    report = replace_line(
        report,
        "结论：",
        "结论：高分组压力窗口均值和最差窗口表现是否优于低分组，需要结合下表具体数值判断；近ATM IV说明高分供给紧张公司仍可能是高波动资产。F33 高分公司往往处于电力设备、冷却、工程、HBM/存储、AI网络或先进制造的供给瓶颈位置，但供给紧张不天然等同于低回撤：若估值已充分反映、订单兑现周期过长或项目执行风险上升，高分组在SOXX压力窗口中仍会承受明显回撤。",
    )
    report = replace_line(
        report,
        "说明：分类中性 Top30/Bottom30",
        "说明：分类中性 Top/Bottom 用于检验 F33 是否只是押中电力、冷却或AI硬件等强势目录。若分类内百分位和去均值残差仍为正，说明同目录内供给紧张排序有额外信息；若转弱或转负，则原始结果更多来自分类暴露、极端公司或窗口风格。",
    )
    report = replace_line(
        report,
        "分类内结果用于检验是否只是押中某个行业。",
        "分类内结果用于检验是否只是押中某个行业。F33 的类内有效性应重点看 Spearman 是否在电力设备、机电冷却、存储、光互联和晶圆制造等供给瓶颈更明确的目录中持续为正；若只有少数目录为正，则不宜把全样本相关直接解释为通用单因子能力。",
    )
    report = replace_line(
        report,
        "稳健性结论：",
        "稳健性结论：低流动性、ADR/币种异常和极端涨跌剔除后，重点看 Spearman 和 Top30-Bottom30 是否同向保持。若三项合并剔除后仍能保持正向，说明 F33 至少有弱排序价值；若转负或接近0，则更适合作为供需景气/订单兑现约束，而不是独立收益排序因子。",
    )
    report = replace_line(
        report,
        "本次 F33 的高分多来自",
        "本次 F33 的高分多来自燃机/变压器/配电gear、数据中心冷却与工程、HBM与AI存储、先进节点/先进封装、AI服务器和光互联链条中的明确 backlog、book-to-bill、lead time、capacity reservation 或客户提前锁供。该信息能解释收入可见度和定价权，但股价窗口还会被估值起点、小盘弹性、融资事件、空头回补、周期修复和风险偏好显著扰动；因此应把 F33 作为供需景气与兑现确定性变量，而不是直接等同于6个月收益弹性。"
    )

    old_advice = re.compile(
        r"## 使用建议\n"
        r"- 不建议把 F33 单独作为未来6个月收益排序因子；.*?\n"
        r"- 建议把 F33 用作质量/兑现约束：.*?\n"
        r"- 与 F31订单刚性、F32订单下修风险、F43基本面兑现确定性联用时更有价值：.*?\n"
        r"- 对低分但涨幅极高公司，应重点追问.*?\n",
        flags=re.DOTALL,
    )
    new_advice = (
        "## 使用建议\n"
        "- 不建议只用 F33 做单因子买入排序；本轮需要同时观察 Spearman、Top/Bottom差和稳健性剔除后的方向。\n"
        "- 建议把 F33 作为供需景气和定价权约束：同等估值赔率、订单刚性和催化剂强度下，供给紧张证据更强的公司应有更高兑现权重。\n"
        "- 与 F31订单刚性与可确认性、F32订单下修风险可控性、F34价格传导能力、F36供给瓶颈受益度、F43基本面兑现确定性联用更有价值：F33 回答“市场是否抢供”，但不单独回答“估值是否便宜”“订单是否会取消”“股价是否已提前反映”。\n"
        "- 对低分但涨幅极高公司，应重点复核涨幅是否来自真实供给紧张改善，还是来自低基数、融资、题材、周期反弹或交易拥挤；对高分但收益弱的公司，应复核估值拥挤、交付周期和项目利润率。\n"
    )
    report = old_advice.sub(new_advice, report)
    report = report.replace(
        "- Top/Bottom能力：成立。Top10、Top20、Top30 平均收益分别为",
        "- Top/Bottom能力：表层成立但不稳健。Top10、Top20、Top30 平均收益分别为",
    )
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
