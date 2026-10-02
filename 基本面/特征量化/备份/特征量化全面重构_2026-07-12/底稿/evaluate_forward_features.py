from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"D:\drive\Investment")
WORK = ROOT / "基本面" / "特征量化" / "_work" / "restructure_20260712"
SCORES_FILE = WORK / "feature_scores_long.csv"
RETURNS_FILE = WORK / "company_returns_2026-06-04_to_latest.csv"
BENCHMARK_FILE = WORK / "benchmark_returns_2026-06-04_to_latest.csv"
EFFECTIVE_FILE = ROOT / "基本面" / "特征量化" / "有效指标清单_latest.json"
ENTRY_SNAPSHOT = ROOT / "基本面" / "日度资料" / "每日金融数据" / "每日金融数据_2026-06-04.md"

PRIMARY = "primary_adj_open_to_adj_close_return"
AUXILIARY = "auxiliary_adj_close_to_adj_close_return"
RNG_SEED = 20260712
PERMUTATIONS = 20_000


V2_GROUPS = {
    "N01": ("AI可归因盈利暴露", ["F01", "F48"], "alpha"),
    "N02": ("系统瓶颈不可替代性", ["F02", "F21"], "alpha"),
    "N03": ("AI需求传导与价值量弹性", ["F24", "F25", "F26", "F27"], "alpha"),
    "N04": ("已披露基本面动量", ["F04"], "alpha"),
    "N05": ("风险调整估值赔率", ["F05", "F06", "F07"], "alpha"),
    "N06": ("财务质量与融资韧性", ["F08", "F09"], "alpha"),
    "N07": ("前瞻基本面修正期限结构", ["F10", "F11", "F12", "F13", "F14", "F15"], "alpha"),
    "N08": ("产能交付执行兑现", ["F16", "F17", "F18", "F45"], "alpha"),
    "N09": ("商业化与平台路线适配", ["F19", "F20", "F23"], "alpha"),
    "N10": ("持久护城河与替代风险", ["F22", "F29", "F35", "F46"], "alpha"),
    "N11": ("客户与订单质量", ["F28", "F30", "F31", "F32", "F47"], "alpha"),
    "N12": ("供需景气与定价捕获", ["F33", "F34", "F36"], "alpha"),
    "N13": ("催化剂事件期限结构", ["F37", "F38", "F39"], "alpha"),
    "N14": ("有符号预期差", ["F03", "F40", "F41"], "alpha"),
    "N15": ("情景收益不对称性", ["F42", "F44"], "alpha"),
    "N16": ("行业中性相对强度", ["F50"], "alpha"),
    "G01": ("PIT证据与数据质量门槛", ["F49", "F43"], "gate"),
    "G02": ("流动性与可投资性门槛", ["F51"], "gate"),
    "G03": ("监管地缘风险覆盖层", ["F52"], "risk_overlay"),
}


FEATURE_ACTIONS = {
    "F01": ("保留并重做", "N01"), "F02": ("合并", "N02"), "F03": ("合并", "N14"),
    "F04": ("保留并重做", "N04"), "F05": ("保留并重做", "N05"), "F06": ("合并", "N05"),
    "F07": ("合并", "N05"), "F08": ("合并", "N06"), "F09": ("合并", "N06"),
    "F10": ("合并重做", "N07"), "F11": ("合并", "N07"), "F12": ("合并", "N07"),
    "F13": ("合并", "N07"), "F14": ("合并", "N07"), "F15": ("合并", "N07"),
    "F16": ("合并", "N08"), "F17": ("合并", "N08"), "F18": ("合并", "N08"),
    "F19": ("合并重做", "N09"), "F20": ("合并", "N09"), "F21": ("保留并重做", "N02"),
    "F22": ("保留并重做", "N10"), "F23": ("合并", "N09"), "F24": ("合并重做", "N03"),
    "F25": ("合并", "N03"), "F26": ("删除独立分数", "N03"), "F27": ("合并", "N03"),
    "F28": ("合并重做", "N11"), "F29": ("合并", "N10"), "F30": ("保留并重做", "N11"),
    "F31": ("合并", "N11"), "F32": ("合并", "N11"), "F33": ("保留并重做", "N12"),
    "F34": ("合并", "N12"), "F35": ("合并", "N10"), "F36": ("合并", "N12"),
    "F37": ("保留并重做", "N13"), "F38": ("合并", "N13"), "F39": ("合并", "N13"),
    "F40": ("保留并重做", "N14"), "F41": ("合并", "N14"), "F42": ("保留并重做", "N15"),
    "F43": ("删除", "G01"), "F44": ("合并", "N15"), "F45": ("合并", "N08"),
    "F46": ("合并", "N10"), "F47": ("合并", "N11"), "F48": ("合并", "N01"),
    "F49": ("移出alpha", "G01"), "F50": ("保留并重做", "N16"),
    "F51": ("移出alpha", "G02"), "F52": ("移出alpha", "G03"),
}


def parse_market_cap(text: str) -> float:
    s = str(text).strip().replace("$", "").replace(",", "")
    if not s or s in {"缺失", "nan"}:
        return float("nan")
    mult = 1.0
    if s[-1:] in {"K", "M", "B", "T"}:
        mult = {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}[s[-1]]
        s = s[:-1]
    try:
        return float(s) * mult
    except ValueError:
        return float("nan")


def load_entry_market_caps() -> pd.Series:
    rows: dict[str, float] = {}
    pattern = re.compile(r"^\| ([A-Z][A-Z0-9.]{0,7}) \|")
    for line in ENTRY_SNAPSHOT.read_text(encoding="utf-8-sig").splitlines():
        if not pattern.match(line):
            continue
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(cells) >= 5:
            rows[cells[0]] = parse_market_cap(cells[4])
    return pd.Series(rows, name="market_cap_entry", dtype=float)


def standardize(values: np.ndarray) -> np.ndarray:
    v = np.asarray(values, dtype=float)
    m = np.isfinite(v)
    out = np.full(v.shape, np.nan, dtype=float)
    if m.sum() < 2:
        return out
    centered = v[m] - v[m].mean()
    denom = math.sqrt(float(np.dot(centered, centered)))
    if denom == 0:
        out[m] = 0.0
    else:
        out[m] = centered / denom
    return out


def rank_standardized(values: pd.Series) -> np.ndarray:
    return standardize(values.rank(method="average").to_numpy(float))


def pearson(a: np.ndarray | pd.Series, b: np.ndarray | pd.Series) -> float:
    x = np.asarray(a, dtype=float)
    y = np.asarray(b, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 3:
        return float("nan")
    xs = standardize(x[m])
    ys = standardize(y[m])
    return float(np.dot(xs, ys))


def spearman(a: pd.Series, b: pd.Series) -> float:
    m = a.notna() & b.notna()
    if m.sum() < 3:
        return float("nan")
    return pearson(a[m].rank(method="average"), b[m].rank(method="average"))


def within_group_rank_corr(score: pd.Series, ret: pd.Series, category: pd.Series) -> float:
    frame = pd.DataFrame({"score": score, "ret": ret, "category": category}).dropna()
    if len(frame) < 3:
        return float("nan")
    frame["s_pct"] = frame.groupby("category")["score"].rank(pct=True, method="average")
    frame["r_pct"] = frame.groupby("category")["ret"].rank(pct=True, method="average")
    return pearson(frame["s_pct"], frame["r_pct"])


def partial_rank_corr(score: pd.Series, ret: pd.Series, category: pd.Series, log_cap: pd.Series) -> float:
    frame = pd.DataFrame({"score": score, "ret": ret, "category": category, "log_cap": log_cap}).dropna()
    if len(frame) < 15:
        return float("nan")
    frame["score_rank"] = frame["score"].rank(pct=True, method="average")
    frame["ret_rank"] = frame["ret"].rank(pct=True, method="average")
    dummies = pd.get_dummies(frame["category"], drop_first=True, dtype=float)
    x = np.column_stack([np.ones(len(frame)), frame["log_cap"].to_numpy(float), dummies.to_numpy(float)])
    s = frame["score_rank"].to_numpy(float)
    r = frame["ret_rank"].to_numpy(float)
    s_res = s - x @ np.linalg.lstsq(x, s, rcond=None)[0]
    r_res = r - x @ np.linalg.lstsq(x, r, rcond=None)[0]
    return pearson(s_res, r_res)


def bh_qvalues(pvalues: pd.Series) -> pd.Series:
    p = pvalues.astype(float).to_numpy()
    q = np.full(len(p), np.nan)
    valid = np.where(np.isfinite(p))[0]
    if not len(valid):
        return pd.Series(q, index=pvalues.index)
    order = valid[np.argsort(p[valid])]
    ranked = p[order] * len(valid) / np.arange(1, len(valid) + 1)
    ranked = np.minimum.accumulate(ranked[::-1])[::-1]
    q[order] = np.clip(ranked, 0, 1)
    return pd.Series(q, index=pvalues.index)


def maturity(feature_id: str) -> str:
    if feature_id in {"F10", "F13", "F16", "F37"}:
        return "1-3月目标：仅约1.2个月，部分成熟"
    if feature_id in {"F11", "F14", "F17", "F38"}:
        return "3-6月目标：未成熟"
    if feature_id in {"F12", "F15", "F18", "F39"}:
        return "6-12月目标：未成熟"
    return "仅单一25交易日截面，未验证稳定性"


def empirical_label(rho: float, q: float, tb: float, neutral: float) -> str:
    if all(np.isfinite(x) for x in [rho, q, tb, neutral]) and rho >= 0.12 and q <= 0.10 and tb > 0 and neutral > 0.08:
        return "短期样本外初步有效"
    if np.isfinite(rho) and np.isfinite(tb) and rho >= 0.08 and tb > 0:
        return "正向但未通过多重检验"
    if np.isfinite(rho) and np.isfinite(tb) and rho <= -0.08 and tb < 0:
        return "短期反向/失效"
    if np.isfinite(rho) and abs(rho) < 0.08:
        return "近零/无排序力"
    return "方向混合/不稳定"


def evaluate_signal(
    feature_id: str,
    feature_name: str,
    score: pd.Series,
    confidence: pd.Series,
    base: pd.DataFrame,
    benchmark_primary: dict[str, float],
) -> dict[str, object]:
    frame = base.copy()
    frame["score"] = score
    frame["confidence"] = confidence
    if feature_id == "F10":
        # F10's source table demonstrably substituted the wrong companies for these tickers.
        frame.loc[frame.index.isin(["ASGLY", "MICLF"]), "score"] = np.nan
    valid = frame.dropna(subset=["score", PRIMARY])
    ranked = valid.assign(_ticker_sort=valid.index).sort_values(["score", "_ticker_sort"], ascending=[False, True])
    top = ranked.head(30)
    bottom = ranked.tail(30)
    qcuts = pd.qcut(valid["score"].rank(method="first"), 5, labels=False) + 1
    qmeans = valid.groupby(qcuts)[PRIMARY].mean().sort_index()
    monotonicity = spearman(pd.Series(qmeans.index, index=qmeans.index), qmeans)
    us = valid[valid["listing_class"] == "US exchange listed"]
    high = valid[valid["confidence"] == "高"]
    log_cap = np.log(valid["market_cap_entry"].where(valid["market_cap_entry"] > 0))
    return {
        "FeatureId": feature_id,
        "FeatureName": feature_name,
        "N": len(valid),
        "Pearson": pearson(valid["score"], valid[PRIMARY]),
        "Spearman": spearman(valid["score"], valid[PRIMARY]),
        "AuxiliarySpearman": spearman(valid["score"], valid[AUXILIARY]),
        "IndustryNeutralSpearman": within_group_rank_corr(valid["score"], valid[PRIMARY], valid["Category"]),
        "IndustrySizeNeutralRankCorr": partial_rank_corr(valid["score"], valid[PRIMARY], valid["Category"], log_cap),
        "USListedSpearman": spearman(us["score"], us[PRIMARY]) if len(us) >= 3 else np.nan,
        "HighConfidenceN": len(high),
        "HighConfidenceSpearman": spearman(high["score"], high[PRIMARY]) if len(high) >= 3 else np.nan,
        "Top30Mean": top[PRIMARY].mean(),
        "Bottom30Mean": bottom[PRIMARY].mean(),
        "Top30Bottom30": top[PRIMARY].mean() - bottom[PRIMARY].mean(),
        "Top30Median": top[PRIMARY].median(),
        "Bottom30Median": bottom[PRIMARY].median(),
        "Top30PositiveRate": (top[PRIMARY] > 0).mean(),
        "Bottom30PositiveRate": (bottom[PRIMARY] > 0).mean(),
        "Top30BeatSPY": (top[PRIMARY] > benchmark_primary["SPY"]).mean(),
        "Top30BeatQQQ": (top[PRIMARY] > benchmark_primary["QQQ"]).mean(),
        "Top30BeatSOXX": (top[PRIMARY] > benchmark_primary["SOXX"]).mean(),
        "QuintileMonotonicity": monotonicity,
        "Q1LowMean": qmeans.get(1, np.nan),
        "Q2Mean": qmeans.get(2, np.nan),
        "Q3Mean": qmeans.get(3, np.nan),
        "Q4Mean": qmeans.get(4, np.nan),
        "Q5HighMean": qmeans.get(5, np.nan),
        "Top30Tickers": ";".join(top.index),
        "Bottom30Tickers": ";".join(bottom.index),
    }


def permutation_pvalues(signal_frame: pd.DataFrame, returns: pd.Series, permutations: int) -> pd.Series:
    common = signal_frame.index.intersection(returns.dropna().index)
    x = signal_frame.loc[common].rank(method="average")
    y = returns.loc[common].rank(method="average")
    x_arr = x.to_numpy(float).copy()
    y_arr = y.to_numpy(float).copy()
    x_arr -= np.nanmean(x_arr, axis=0, keepdims=True)
    x_norm = np.sqrt(np.nansum(x_arr * x_arr, axis=0))
    y_arr -= np.nanmean(y_arr)
    y_norm = math.sqrt(float(np.nansum(y_arr * y_arr)))
    observed = np.nansum(x_arr * y_arr[:, None], axis=0) / (x_norm * y_norm)
    rng = np.random.default_rng(RNG_SEED)
    exceed = np.zeros(x_arr.shape[1], dtype=np.int64)
    batch = 1_000
    for start in range(0, permutations, batch):
        count = min(batch, permutations - start)
        perms = np.column_stack([rng.permutation(y_arr) for _ in range(count)])
        corr = (x_arr.T @ perms) / (x_norm[:, None] * y_norm)
        exceed += np.sum(np.abs(corr) >= np.abs(observed)[:, None], axis=1)
    return pd.Series((exceed + 1) / (permutations + 1), index=signal_frame.columns, name="PermutationP")


def main() -> None:
    scores = pd.read_csv(SCORES_FILE, encoding="utf-8-sig")
    returns = pd.read_csv(RETURNS_FILE, encoding="utf-8-sig")
    benchmarks = pd.read_csv(BENCHMARK_FILE, encoding="utf-8-sig")
    caps = load_entry_market_caps()
    prior_effective = set(json.loads(EFFECTIVE_FILE.read_text(encoding="utf-8-sig"))["effectiveFeatureIds"])

    base = returns.set_index("feature_ticker")
    base.index.name = "Ticker"
    base["Ticker"] = base.index
    base["market_cap_entry"] = caps.reindex(base.index)
    for col in [PRIMARY, AUXILIARY]:
        base[col] = pd.to_numeric(base[col], errors="coerce")
    benchmark_primary = dict(zip(benchmarks["benchmark"], benchmarks[PRIMARY].astype(float)))

    feature_names = scores.drop_duplicates("FeatureId").set_index("FeatureId")["FeatureName"].to_dict()
    score_wide = scores.pivot(index="Ticker", columns="FeatureId", values="Score").reindex(base.index)
    confidence_wide = scores.pivot(index="Ticker", columns="FeatureId", values="Confidence").reindex(base.index)
    category = scores[scores["FeatureId"] == "F01"].set_index("Ticker")["Category"].reindex(base.index)
    base["Category"] = category

    feature_results = []
    for feature_id in score_wide.columns:
        feature_results.append(
            evaluate_signal(
                feature_id,
                feature_names[feature_id],
                score_wide[feature_id],
                confidence_wide[feature_id],
                base,
                benchmark_primary,
            )
        )
    feature_eval = pd.DataFrame(feature_results).set_index("FeatureId")
    # Use the same clean sample rules for the multiple-testing audit.
    perm_scores = score_wide.copy()
    perm_scores.loc[["ASGLY", "MICLF"], "F10"] = np.nan
    # The two F10 NAs are filled with the cross-sectional median only for the shared permutation matrix;
    # the reported correlations above still exclude them. This has negligible influence and keeps one common null.
    perm_scores = perm_scores.apply(lambda s: s.fillna(s.median()))
    pvalues = permutation_pvalues(perm_scores, base[PRIMARY], PERMUTATIONS)
    feature_eval["PermutationP"] = pvalues
    feature_eval["FDR_Q"] = bh_qvalues(feature_eval["PermutationP"])
    feature_eval["PriorRetrospectiveEffective"] = feature_eval.index.map(lambda x: x in prior_effective)
    feature_eval["Maturity"] = feature_eval.index.map(maturity)
    feature_eval["EmpiricalLabel"] = [
        empirical_label(row.Spearman, row.FDR_Q, row.Top30Bottom30, row.IndustryNeutralSpearman)
        for row in feature_eval.itertuples()
    ]
    feature_eval["RefactorAction"] = feature_eval.index.map(lambda x: FEATURE_ACTIONS[x][0])
    feature_eval["V2Group"] = feature_eval.index.map(lambda x: FEATURE_ACTIONS[x][1])
    feature_eval = feature_eval.sort_values(["Spearman", "Top30Bottom30"], ascending=False)
    feature_eval.to_csv(WORK / "feature_forward_evaluation.csv", encoding="utf-8-sig", float_format="%.10f")

    # Proposed V2 composites are equal-weighted averages of member percentile ranks only as a diagnostic.
    rank_pct = score_wide.rank(pct=True, method="average")
    v2_scores = pd.DataFrame(index=rank_pct.index)
    v2_meta: dict[str, tuple[str, str, list[str]]] = {}
    for group_id, (name, members, role) in V2_GROUPS.items():
        v2_scores[group_id] = rank_pct[members].mean(axis=1)
        v2_meta[group_id] = (name, role, members)
    v2_results = []
    neutral_conf = pd.Series("中", index=base.index)
    for group_id in v2_scores.columns:
        name, role, members = v2_meta[group_id]
        row = evaluate_signal(group_id, name, v2_scores[group_id], neutral_conf, base, benchmark_primary)
        row["Role"] = role
        row["Members"] = ";".join(members)
        row["MemberMeanPairwiseCorr"] = float(score_wide[members].corr().where(np.triu(np.ones((len(members), len(members))), 1).astype(bool)).stack().mean()) if len(members) > 1 else np.nan
        v2_results.append(row)
    v2_eval = pd.DataFrame(v2_results).set_index("FeatureId")
    v2_p = permutation_pvalues(v2_scores, base[PRIMARY], PERMUTATIONS)
    v2_eval["PermutationP"] = v2_p
    v2_eval["FDR_Q_AcrossV2"] = bh_qvalues(v2_eval["PermutationP"])
    v2_eval["EmpiricalLabel"] = [
        empirical_label(row.Spearman, row.FDR_Q_AcrossV2, row.Top30Bottom30, row.IndustryNeutralSpearman)
        for row in v2_eval.itertuples()
    ]
    v2_eval = v2_eval.sort_values(["Role", "Spearman"], ascending=[True, False])
    v2_eval.to_csv(WORK / "v2_group_forward_evaluation.csv", encoding="utf-8-sig", float_format="%.10f")

    # Company table, sorted by the primary actionable OOS return.
    company = base.copy()
    company["ReturnRank"] = company[PRIMARY].rank(method="min", ascending=False).astype(int)
    company = company.sort_values(PRIMARY, ascending=False)
    company.to_csv(WORK / "company_returns_ranked.csv", encoding="utf-8-sig", float_format="%.10f")

    comparison = feature_eval[
        ["FeatureName", "PriorRetrospectiveEffective", "Spearman", "IndustryNeutralSpearman", "Top30Bottom30", "PermutationP", "FDR_Q", "EmpiricalLabel", "Maturity", "RefactorAction", "V2Group"]
    ].copy()
    comparison.to_csv(WORK / "old_effective_vs_forward.csv", encoding="utf-8-sig", float_format="%.10f")

    summary = {
        "as_of": "2026-07-12",
        "latest_market_date": str(base["latest_available_date"].max()),
        "feature_count": int(len(feature_eval)),
        "company_count": int(len(base)),
        "permutations": PERMUTATIONS,
        "fdr_10pct_pass": feature_eval.index[feature_eval["FDR_Q"] <= 0.10].tolist(),
        "short_oos_initial_effective": feature_eval.index[feature_eval["EmpiricalLabel"] == "短期样本外初步有效"].tolist(),
        "short_oos_reverse": feature_eval.index[feature_eval["EmpiricalLabel"] == "短期反向/失效"].tolist(),
        "prior_effective_count": int(feature_eval["PriorRetrospectiveEffective"].sum()),
        "prior_effective_short_oos_initial_effective": feature_eval.index[
            feature_eval["PriorRetrospectiveEffective"] & (feature_eval["EmpiricalLabel"] == "短期样本外初步有效")
        ].tolist(),
        "primary_return_mean": float(base[PRIMARY].mean()),
        "primary_return_median": float(base[PRIMARY].median()),
        "primary_positive_rate": float((base[PRIMARY] > 0).mean()),
        "outputs": {
            "feature_evaluation": str(WORK / "feature_forward_evaluation.csv"),
            "v2_evaluation": str(WORK / "v2_group_forward_evaluation.csv"),
            "company_returns": str(WORK / "company_returns_ranked.csv"),
        },
    }
    (WORK / "forward_evaluation_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
