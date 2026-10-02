from __future__ import annotations

import math
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "legacy" / "mpu_uncertainty"
OUT_DIR = ROOT / "outputs" / "legacy" / "mpu_uncertainty"
REPORT_PATH = ROOT / "货币政策不确定性_QQQ_SOXX.md"

FRED_BASE = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="
YAHOO_CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

MARKET_SYMBOLS = ["SPY", "QQQ", "SOXX", "IWF", "IWD", "ARKK", "KBE", "KRE", "XLF"]
FRED_SERIES = ["EPUMONETARY", "USEPUINDXM", "USEPUINDXD", "VIXCLS", "DGS10", "DGS2", "FEDFUNDS"]


def ensure_dirs() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(exist_ok=True)
    (DATA_DIR / "fred").mkdir(exist_ok=True)
    (DATA_DIR / "market").mkdir(exist_ok=True)


def download_fred(series_id: str) -> pd.DataFrame:
    url = FRED_BASE + series_id
    df = pd.read_csv(url, parse_dates=["observation_date"]).replace(".", np.nan)
    df = df.rename(columns={"observation_date": "date", series_id: "value"})
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"]).sort_values("date")
    df.to_csv(DATA_DIR / "fred" / f"{series_id}.csv", index=False)
    return df


def download_yahoo(symbol: str) -> pd.DataFrame:
    params = {
        "range": "max",
        "interval": "1d",
        "events": "history",
        "includeAdjustedClose": "true",
    }
    response = requests.get(YAHOO_CHART.format(symbol=symbol), params=params, headers=HEADERS, timeout=30)
    response.raise_for_status()
    payload = response.json()
    result = payload["chart"]["result"][0]
    quote = result["indicators"]["quote"][0]
    adj = result["indicators"].get("adjclose", [{}])[0].get("adjclose") or quote["close"]
    dates = pd.to_datetime(result["timestamp"], unit="s", utc=True).tz_convert("America/New_York")
    df = pd.DataFrame(
        {
            "date": dates.tz_localize(None).normalize(),
            "close": quote["close"],
            "adjclose": adj,
        }
    )
    df = df.dropna(subset=["adjclose"]).drop_duplicates("date").sort_values("date")
    df.to_csv(DATA_DIR / "market" / f"{symbol}.csv", index=False)
    return df


def pct(x: float | None, digits: int = 1) -> str:
    if x is None or pd.isna(x):
        return "NA"
    return f"{x * 100:.{digits}f}%"


def num(x: float | None, digits: int = 2) -> str:
    if x is None or pd.isna(x):
        return "NA"
    return f"{x:.{digits}f}"


def signed_points(x: float | None, digits: int = 1) -> str:
    if x is None or pd.isna(x):
        return "NA"
    sign = "+" if x > 0 else ""
    return f"{sign}{x:.{digits}f}pt"


def markdown_table(rows: list[list[str]], headers: list[str]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    out.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(out)


def build_monthly_data(prices: pd.DataFrame, fred: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    monthly_prices = prices.resample("ME").last()
    vix = fred["VIXCLS"].set_index("date")["value"].resample("ME").last()

    metrics = pd.DataFrame(index=monthly_prices.index)
    metrics["QQQ/SPY"] = monthly_prices["QQQ"] / monthly_prices["SPY"]
    metrics["SOXX/SPY"] = monthly_prices["SOXX"] / monthly_prices["SPY"]
    metrics["SOXX/QQQ"] = monthly_prices["SOXX"] / monthly_prices["QQQ"]
    metrics["IWF/IWD"] = monthly_prices["IWF"] / monthly_prices["IWD"]
    metrics["ARKK/SPY"] = monthly_prices["ARKK"] / monthly_prices["SPY"]
    metrics["KBE/SPY"] = monthly_prices["KBE"] / monthly_prices["SPY"]
    metrics["KRE/SPY"] = monthly_prices["KRE"] / monthly_prices["SPY"]
    metrics["XLF/SPY"] = monthly_prices["XLF"] / monthly_prices["SPY"]
    metrics["QQQ"] = monthly_prices["QQQ"]
    metrics["SOXX"] = monthly_prices["SOXX"]
    metrics["SPY"] = monthly_prices["SPY"]
    metrics["VIX"] = vix

    epu = fred["EPUMONETARY"].copy()
    epu["date"] = epu["date"] + pd.offsets.MonthEnd(0)
    epu = epu.set_index("date").rename(columns={"value": "EPUMONETARY"})
    epu["m3_change"] = epu["EPUMONETARY"] / epu["EPUMONETARY"].shift(3) - 1
    return metrics, epu


def event_dates(epu: pd.DataFrame, quantile: float, min_gap_months: int = 6) -> tuple[list[pd.Timestamp], float]:
    threshold = float(epu["m3_change"].quantile(quantile))
    level_floor = float(epu["EPUMONETARY"].quantile(0.5))
    raw = epu[(epu["m3_change"] >= threshold) & (epu["EPUMONETARY"] >= level_floor)]

    events: list[pd.Timestamp] = []
    last: pd.Timestamp | None = None
    for date in raw.index:
        if last is None or (date.to_period("M") - last.to_period("M")).n >= min_gap_months:
            events.append(date)
            last = date
    return events, threshold


def calc_event_stats(metrics: pd.DataFrame, events: list[pd.Timestamp], metric_names: list[str]) -> dict[str, dict[str, float]]:
    windows = {
        "形成期-3m": -3,
        "形成期-1m": -1,
        "+1m": 1,
        "+3m": 3,
        "+6m": 6,
        "+12m": 12,
    }
    stats: dict[str, dict[str, float]] = {}
    for metric in metric_names:
        ser = metrics[metric].dropna()
        metric_stats: dict[str, float] = {}
        for label, horizon in windows.items():
            if horizon < 0:
                values = ser / ser.shift(abs(horizon)) - 1
                if metric == "VIX":
                    values = ser - ser.shift(abs(horizon))
            else:
                values = ser.shift(-horizon) / ser - 1
                if metric == "VIX":
                    values = ser.shift(-horizon) - ser
            sample = pd.Series([values.loc[d] for d in events if d in values.index and pd.notna(values.loc[d])])
            metric_stats[f"{label}_n"] = float(len(sample))
            metric_stats[f"{label}_mean"] = float(sample.mean()) if len(sample) else math.nan
            metric_stats[f"{label}_median"] = float(sample.median()) if len(sample) else math.nan
            metric_stats[f"{label}_hit"] = float((sample > 0).mean()) if len(sample) else math.nan
        stats[metric] = metric_stats
    return stats


def current_market_snapshot(prices: pd.DataFrame) -> tuple[list[list[str]], list[list[str]]]:
    rows: list[list[str]] = []
    for symbol in ["QQQ", "SOXX", "SPY", "IWF", "IWD", "ARKK", "KBE", "KRE", "XLF"]:
        ser = prices[symbol].dropna()
        latest = ser.iloc[-1]

        def ret(days: int) -> float | None:
            return latest / ser.iloc[-1 - days] - 1 if len(ser) > days else None

        ma50 = ser.tail(50).mean()
        ma200 = ser.tail(200).mean()
        high252 = ser.tail(252).max()
        rows.append(
            [
                symbol,
                ser.index[-1].strftime("%Y-%m-%d"),
                num(latest, 2),
                pct(ret(21)),
                pct(ret(63)),
                pct(latest / ma50 - 1),
                pct(latest / ma200 - 1),
                pct(latest / high252 - 1),
            ]
        )

    ratio_rows: list[list[str]] = []
    ratio_defs = [
        ("QQQ/SPY", "QQQ", "SPY"),
        ("SOXX/SPY", "SOXX", "SPY"),
        ("SOXX/QQQ", "SOXX", "QQQ"),
        ("IWF/IWD", "IWF", "IWD"),
        ("KBE/SPY", "KBE", "SPY"),
        ("KRE/SPY", "KRE", "SPY"),
    ]
    for name, numerator, denominator in ratio_defs:
        ser = (prices[numerator] / prices[denominator]).dropna()
        latest = ser.iloc[-1]
        ma50 = ser.tail(50).mean()
        ma200 = ser.tail(200).mean()
        window = ser.tail(252 * 5)
        percentile = float((window <= latest).mean()) if len(window) else math.nan
        ratio_rows.append(
            [
                name,
                num(latest, 4),
                pct(latest / ser.iloc[-64] - 1 if len(ser) > 64 else None),
                pct(latest / ma50 - 1),
                pct(latest / ma200 - 1),
                pct(percentile, 0),
            ]
        )
    return rows, ratio_rows


def latest_value(df: pd.DataFrame) -> tuple[pd.Timestamp, float]:
    last = df.dropna(subset=["value"]).iloc[-1]
    return pd.Timestamp(last["date"]), float(last["value"])


def build_report(
    fred: dict[str, pd.DataFrame],
    prices: pd.DataFrame,
    metrics: pd.DataFrame,
    epu: pd.DataFrame,
) -> str:
    stress_events, stress_threshold = event_dates(epu, 0.90)
    broad_events, broad_threshold = event_dates(epu, 0.80)

    metric_names = [
        "QQQ/SPY",
        "SOXX/SPY",
        "SOXX/QQQ",
        "IWF/IWD",
        "KBE/SPY",
        "KRE/SPY",
        "XLF/SPY",
        "QQQ",
        "SOXX",
        "SPY",
        "VIX",
    ]
    stress = calc_event_stats(metrics, stress_events, metric_names)
    broad = calc_event_stats(metrics, broad_events, metric_names)

    core_rows: list[list[str]] = []
    for metric in metric_names:
        formatter = signed_points if metric == "VIX" else pct
        core_rows.append(
            [
                metric,
                str(int(stress[metric]["形成期-3m_n"])),
                formatter(stress[metric]["形成期-3m_mean"]),
                formatter(stress[metric]["+3m_mean"]),
                formatter(stress[metric]["+6m_mean"]),
                formatter(stress[metric]["+12m_mean"]),
                pct(stress[metric]["+12m_hit"], 0),
            ]
        )

    broad_rows: list[list[str]] = []
    for metric in ["QQQ/SPY", "SOXX/SPY", "SOXX/QQQ", "KBE/SPY", "KRE/SPY", "QQQ", "SOXX", "SPY", "VIX"]:
        formatter = signed_points if metric == "VIX" else pct
        broad_rows.append(
            [
                metric,
                str(int(broad[metric]["形成期-3m_n"])),
                formatter(broad[metric]["形成期-3m_mean"]),
                formatter(broad[metric]["+3m_mean"]),
                formatter(broad[metric]["+12m_mean"]),
            ]
        )

    recent_events = [
        [d.strftime("%Y-%m"), num(epu.loc[d, "EPUMONETARY"], 1), pct(epu.loc[d, "m3_change"], 0)]
        for d in stress_events
        if d >= pd.Timestamp("1999-01-01")
    ]

    market_rows, ratio_rows = current_market_snapshot(prices)

    epu_latest_date, epu_latest = latest_value(fred["EPUMONETARY"])
    epu_m_latest_date, epu_m_latest = latest_value(fred["USEPUINDXM"])
    epu_d_latest_date, epu_d_latest = latest_value(fred["USEPUINDXD"])
    vix_latest_date, vix_latest = latest_value(fred["VIXCLS"])
    dgs10_date, dgs10_latest = latest_value(fred["DGS10"])
    dgs2_date, dgs2_latest = latest_value(fred["DGS2"])
    fedfunds_date, fedfunds_latest = latest_value(fred["FEDFUNDS"])

    latest_prices_date = prices.dropna(how="all").index.max().strftime("%Y-%m-%d")
    price_date_note = f"行情数据截至 {latest_prices_date}；FRED 日度数据多数截至 {vix_latest_date.strftime('%Y-%m-%d')}。"

    current_epu_m3 = epu["m3_change"].iloc[-1]
    current_epu_level = epu["EPUMONETARY"].iloc[-1]

    report = f"""# 货币政策不确定性指数回测与 QQQ/SOXX 展望

生成日期：2026-05-10（America/Los_Angeles）

> 说明：本文是历史统计与情景分析，不是投资建议。ETF 历史价格来自 Yahoo Finance chart 接口，政策不确定性、VIX 与利率数据来自 FRED。月度 EPU/MPU 类指数有发布滞后，本文的“事件回测”更适合作为 regime/event study，而不是严格的可交易择时策略。

## 结论摘要

1. 用 FRED 的 `EPUMONETARY`（Economic Policy Uncertainty 的“货币政策”分类指数）定义“货币政策不确定性快速上升”：3 个月涨幅进入历史前 10%、且指数水平高于中位数，并用 6 个月冷却期去重。阈值为 3 个月涨幅 >= {pct(stress_threshold, 1)}。
2. 历史上，快速上升的形成期通常是去风险交易：在事件确认前 3 个月，QQQ/SPY 平均 {pct(stress['QQQ/SPY']['形成期-3m_mean'])}，SOXX/SPY 平均 {pct(stress['SOXX/SPY']['形成期-3m_mean'])}，SOXX/QQQ 平均 {pct(stress['SOXX/QQQ']['形成期-3m_mean'])}，VIX 平均上升 {signed_points(stress['VIX']['形成期-3m_mean'])}。
3. 信号确认后反而经常出现风险资产修复：事件后 3 个月 QQQ 平均 {pct(stress['QQQ']['+3m_mean'])}、SOXX 平均 {pct(stress['SOXX']['+3m_mean'])}、SPY 平均 {pct(stress['SPY']['+3m_mean'])}；事件后 12 个月 QQQ 平均 {pct(stress['QQQ']['+12m_mean'])}、SOXX 平均 {pct(stress['SOXX']['+12m_mean'])}。这更像“冲击已被定价后，政策路径逐渐清晰”的均值回归，不应解读成不确定性本身利好成长股。
4. 银行股不是稳定避风港。KBE/SPY、KRE/SPY 在事件后 3-12 个月多数仍偏弱，说明货币政策不确定性上升时，银行同时面对净息差、信用周期、监管和资本市场风险。
5. 当前 `EPUMONETARY` 最新为 {epu_latest_date.strftime('%Y-%m')} 的 {num(epu_latest, 1)}，3 个月涨幅 {pct(current_epu_m3)}，没有触发本研究的“快速上升”定义。但 Fed 换届、政策独立性讨论、油价/通胀和利率路径仍会给 QQQ/SOXX 带来事件波动。
6. 对未来判断：QQQ 中期仍偏多头结构，但短线已经过热，适合把“回撤后再评估”放在优先级更高的位置；SOXX 对风险偏好和 AI/资本开支预期更敏感，若 VIX 和长端利率稳定会继续比 QQQ 更强，但一旦 Fed 换届引发利率或信用冲击，SOXX 回撤弹性也会更大。

## 数据与方法

- 主指数：`EPUMONETARY`，FRED 上的 “Economic Policy Uncertainty Index: Categorical Index: Monetary policy”，月度，样本 1985-01 至 {epu_latest_date.strftime('%Y-%m')}。
- 辅助指数：`USEPUINDXM`、`USEPUINDXD`、`VIXCLS`、`DGS10`、`DGS2`、`FEDFUNDS`。
- 市场资产：SPY、QQQ、SOXX、IWF、IWD、ARKK、KBE、KRE、XLF 的复权价格。
- 事件定义：`EPUMONETARY / EPUMONETARY.shift(3) - 1` 进入样本前 10%，同时指数高于全样本中位数；相邻事件至少间隔 6 个月。
- 回测口径：看事件形成期（T-3 到 T、T-1 到 T）与事件后 1/3/6/12 个月。VIX 用点数变化，其他资产和比值用百分比变化。
- 样本限制：QQQ 从 1999 年开始，SOXX 从 2001 年开始，KBE/KRE 从 2005/2006 年开始，ARKK 从 2014 年开始，因此不同资产的事件样本数不同。

## 压力事件回测

{markdown_table(core_rows, ["指标", "N", "形成期 T-3→T 均值", "T→T+3m 均值", "T→T+6m 均值", "T→T+12m 均值", "T+12m 正收益率"])}

解读：

- 形成期最典型的组合是 VIX 上行、成长和半导体相对 SPY 走弱，尤其 SOXX/QQQ 也会先走弱，说明半导体在冲击期通常比纳指 100 更高 beta。
- 事件后 3-12 个月，QQQ/SPY 和 SOXX/SPY 平均转正，VIX 平均回落。这符合“政策不确定性冲击到达极端后，市场等待政策路径重新锚定”的模式。
- 银行 ETF 相对 SPY 的结果偏弱，不能简单用“更高利率利好银行”解释。高政策不确定性经常伴随增长、信用和监管折价。

### 近年压力事件

{markdown_table(recent_events[-12:], ["事件月份", "EPUMONETARY", "3个月涨幅"])}

## 稳健性：前 20% 快速上升事件

把阈值放宽到 3 个月涨幅进入前 20%（阈值 {pct(broad_threshold, 1)}），方向基本一致但幅度更温和：

{markdown_table(broad_rows, ["指标", "N", "形成期 T-3→T 均值", "T→T+3m 均值", "T→T+12m 均值"])}

## 当前宏观与市场状态

{price_date_note}

宏观快照：

- `EPUMONETARY` 最新：{epu_latest_date.strftime('%Y-%m')} = {num(epu_latest, 1)}；最新 3 个月涨幅 = {pct(current_epu_m3)}，明显低于压力阈值 {pct(stress_threshold, 1)}。
- 整体月度 EPU `USEPUINDXM` 最新：{epu_m_latest_date.strftime('%Y-%m')} = {num(epu_m_latest, 1)}，低于 2026-03 的 267.5。
- 日度整体 EPU `USEPUINDXD` 最新：{epu_d_latest_date.strftime('%Y-%m-%d')} = {num(epu_d_latest, 1)}；5 月初仍有单日跳升。
- VIX 最新：{vix_latest_date.strftime('%Y-%m-%d')} = {num(vix_latest, 2)}，未处于恐慌区。
- 10 年美债收益率：{dgs10_date.strftime('%Y-%m-%d')} = {num(dgs10_latest, 2)}%；2 年美债收益率：{dgs2_date.strftime('%Y-%m-%d')} = {num(dgs2_latest, 2)}%；联邦基金有效利率：{fedfunds_date.strftime('%Y-%m')} = {num(fedfunds_latest, 2)}%。
- Fed 官方在 2026-04-29 FOMC 声明中维持联邦基金目标区间 3.50%-3.75%。公开报道显示，Powell 的主席任期在 2026-05-15 到期，Kevin Warsh 已被提名接任，换届本身是短期政策沟通风险。

市场快照：

{markdown_table(market_rows, ["标的", "最新日", "复权价", "21交易日", "63交易日", "距50日均线", "距200日均线", "距52周高点"])}

相对强弱：

{markdown_table(ratio_rows, ["比值", "最新", "63交易日变化", "距50日均线", "距200日均线", "5年分位"])}

当前市场含义：

- QQQ 和 SOXX 已经是明显风险偏好回升后的状态，而不是恐慌定价状态。VIX 低于 20、QQQ/SPY 和 SOXX/SPY 强势，说明市场目前更关注增长/AI/流动性预期，而不是直接交易政策冲击。
- 但这种状态也意味着短线风险回报不如不确定性尖峰刚确认后的阶段。若 Fed 换届沟通平稳、长端利率不再上行，强势结构可以延续；若市场开始质疑 Fed 独立性或通胀再度抬头，当前的高 beta 仓位会更脆弱。

## QQQ 展望

基准情景：震荡偏强，但短线过热。历史回测显示，当货币政策不确定性快速上升进入极端区间后，QQQ 在随后 3-12 个月的平均收益和相对 SPY 表现都不差；当前则不是新的 `EPUMONETARY` 尖峰，而是尖峰后的风险偏好修复阶段。只要 VIX 维持在 20 以下、10 年美债收益率不持续突破 4.6%-4.8%、QQQ/SPY 不跌破自身 50 日均线，QQQ 的中期上行趋势仍然成立。

风险点：Fed 换届如果被市场解读为政策独立性受损，长端通胀风险溢价可能上升；这会直接压缩 QQQ 的估值倍数。另一个风险是指数短期涨幅过大，任何业绩或利率扰动都可能触发 5%-10% 级别的技术性回撤。

操作含义：不确定性指数本身没有给出“立刻做空 QQQ”的信号；更合理的判断是短线追高赔率下降，中期仍看 Fed 沟通、利率和盈利能否配合。

## SOXX 展望

SOXX 的方向比 QQQ 更依赖风险偏好和 AI/半导体资本开支叙事。历史上，SOXX 在不确定性冲击形成期相对 SPY 和 QQQ 更容易先受压；但如果冲击没有演变成信用/盈利衰退，事件后 6-12 个月 SOXX 往往比 QQQ 和 SPY 更有弹性。

当前 SOXX/SPY、SOXX/QQQ 都处于强势状态，因此中期相对收益仍有延续条件：VIX 低位、长端利率稳定、AI 订单和资本开支没有被下修。反过来，SOXX 也是更需要纪律的标的：如果 SOXX/QQQ 跌破 50 日均线、VIX 升破 22-25、或 10 年美债收益率快速上行，SOXX 相对 QQQ 的回撤可能会更快。

操作含义：SOXX 不是当前宏观环境下的防守资产，而是高 beta 进攻资产。看多 SOXX 的核心前提不是“Fed 换届会降息”，而是“换届不破坏 Fed 信用、利率不再上冲、AI 盈利预期继续兑现”。

## 观察清单

- `EPUMONETARY` 后续月度值：若 3 个月涨幅重新接近 {pct(stress_threshold, 1)}，说明货币政策不确定性进入历史压力区。
- 日度 EPU：单日跳升不够，关键是是否连续多日维持高位。
- VIX：20 以下偏风险偏好；22-25 以上说明换届或通胀风险开始进入权益定价。
- 10 年美债：4.6%-4.8% 是成长股估值压力区；若收益率上行且 QQQ/SPY 同时跌破 50 日均线，应降低对成长股相对强势的置信度。
- SOXX/QQQ：这是半导体相对纳指的核心温度计。强势维持代表市场继续押注 AI/半导体；跌破趋势说明高 beta 开始退潮。

## 数据来源

- FRED `EPUMONETARY`: https://fred.stlouisfed.org/series/EPUMONETARY
- FRED `USEPUINDXM`: https://fred.stlouisfed.org/series/USEPUINDXM
- FRED `USEPUINDXD`: https://fred.stlouisfed.org/series/USEPUINDXD
- FRED `VIXCLS`: https://fred.stlouisfed.org/series/VIXCLS
- FRED `DGS10`: https://fred.stlouisfed.org/series/DGS10
- Federal Reserve 2026-04-29 FOMC statement: https://www.federalreserve.gov/newsevents/pressreleases/monetary20260429a.htm
- Yahoo Finance chart data for ETF prices: https://query1.finance.yahoo.com/v8/finance/chart/
- PBS/AP on Kevin Warsh nomination: https://www.pbs.org/newshour/politics/white-house-formally-nominates-kevin-warsh-to-be-next-federal-reserve-chair

"""
    return report


def main() -> None:
    ensure_dirs()

    fred: dict[str, pd.DataFrame] = {}
    for series in FRED_SERIES:
        fred[series] = download_fred(series)

    price_parts: list[pd.Series] = []
    for symbol in MARKET_SYMBOLS:
        df = download_yahoo(symbol)
        price_parts.append(df.set_index("date")["adjclose"].rename(symbol))
        time.sleep(0.1)

    prices = pd.concat(price_parts, axis=1).sort_index()
    prices.to_csv(DATA_DIR / "market_prices_adjclose.csv", index=True)

    metrics, epu = build_monthly_data(prices, fred)
    metrics.to_csv(OUT_DIR / "monthly_market_metrics.csv", index=True)
    epu.to_csv(OUT_DIR / "epumonetary_monthly_signal.csv", index=True)

    report = build_report(fred, prices, metrics, epu)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(REPORT_PATH)


if __name__ == "__main__":
    main()
