# 研究 8：EPS Revision vs Multiple Compression 分解模型

> 研究日期：2026-05-11（美国时间）  
> 数据截止：市场价格使用 2026-05-08 收盘，本报告的核心 forward P/E 使用 FactSet 2026-05-08 报告（基于 2026-05-07 收盘价）。  
> 结论属性：基本面与估值拆分研究，不构成投资建议。

## 0. 结论摘要

当前 S&P 500 的上涨不是纯粹的 multiple 扩张，也还不能称为完全由盈利驱动的健康上涨。用 FactSet 的 forward 12M P/E 和 SPX 收盘价反推 forward EPS：

- **2026-03-31 到 2026-05-07**：SPX +12.4%，forward EPS +5.4%，forward P/E 19.7x -> 21.0x。按 log 拆分，约 **45% 来自 EPS 上修，55% 来自 multiple 扩张**。
- **2026-04-09 到 2026-05-07 的近 1 个月**：SPX +7.5%，forward EPS +4.4%，forward P/E 20.4x -> 21.0x。按 log 拆分，约 **60% 来自 EPS 上修，40% 来自 multiple 扩张**。
- **2026-04-16 到 2026-05-07 的财报核心段**：SPX +4.2%，forward EPS +3.7%，forward P/E 20.9x -> 21.0x。按 log 拆分，约 **88% 来自 EPS 上修**。

因此，当前 rally 的质量正在从“早期 PE 修复”转向“财报驱动的 EPS 上修”。但估值仍然偏高：FactSet 2026-05-08 显示 S&P 500 forward P/E 为 **21.0x**，高于 5 年均值 19.9x 和 10 年均值 18.9x。未来 1 周 / 1 月的核心矛盾是：**EPS 上修还能否继续快于 PE 均值回归**。

我的基准判断：

- 未来 5 个交易日：EPS 仍可能小幅上修，但 CPI、利率和财报尾声风险可能使 PE 略压缩；价格中性偏震荡。
- 未来 21 个交易日：EPS 仍有上修惯性，但如果没有 NVIDIA 等后续大型公司继续强化 AI 盈利叙事，21.0x 的 PE 更容易向 20.5x-20.8x 消化；价格基准为小幅震荡，右尾来自 EPS 再加速，左尾来自 PE 压缩。
- 如果 EPS revision 转平或转负，当前 21x forward PE 的容错率会明显下降。历史上，高估值市场在 EPS 仍上修但利率/风险溢价转坏时也会先压 PE；若 EPS 同时转负，压缩通常更快、更集中。

## 1. 数据口径与限制

核心恒等式：

```text
Price = Forward EPS * Forward PE

Delta ln Price = Delta ln Forward EPS + Delta ln Forward PE
```

本报告使用公开可验证数据：

- S&P 500 价格：本地数据 `data/common_daily/raw/yahoo_ohlcv_daily.csv`，Yahoo Finance chart API 抓取。
- S&P 500 forward P/E：FactSet Earnings Insight 周度报告与 FactSet Insight 文章。
- Forward EPS：用同一时点 `SPX close / forward P/E` 反推。
- Sector forward P/E：FactSet 2026-05-08 Earnings Insight PDF 的 sector-level forward 12M P/E 图表。
- Sector 与 Mag 7 盈利趋势：FactSet、Schwab/LSEG I/B/E/S 公开文章。
- EPS revision breadth：公开版本无法取得逐家公司 point-in-time 上修/下修比例；用 FactSet 的季度 EPS estimate change、正负 guidance 和 beat rate 做 proxy。

重要限制：真正的日频 forward EPS、forward P/E、EPS revision breadth、Mag 7 point-in-time EPS revision 需要 FactSet、IBES、Bloomberg、LSEG 或 S&P Capital IQ 授权数据。这里给出的是可复核的周频公开版模型。

## 2. 当前数据快照

| 指标 | 最新读数 | 含义 |
|---|---:|---|
| SPX close | 7337.11（2026-05-07，FactSet 报告基准）；7398.93（2026-05-08 本地收盘） | 5/8 报告使用 5/7 收盘价；5/8 市场继续上涨 |
| S&P 500 forward P/E | 21.0x | 高于 5 年均值 19.9x、10 年均值 18.9x |
| 隐含 forward 12M EPS | 349.4（7337.11 / 21.0） | 3/31 隐含约 331.4，5/7 已上修约 5.4% |
| 2026 CY bottom-up EPS | 334.61（FactSet 2026-05-08 PDF 图表） | CY EPS 低于 forward 12M EPS，因 forward 12M 已包含部分 2027 权重 |
| Q1 2026 EPS beat rate | 84%（89% 公司已披露） | 高于 5 年均值 78% 与 10 年均值 76% |
| Q1 2026 aggregate surprise | +18.2% | 仍明显高于历史均值 |
| Q2 2026 EPS estimate | 2026 年 4 月 +2.1% | 通常季度第一个月会下修，这次反而上修 |
| CY 2026 EPS estimate | 2026 年 4 月 +3.4% | 全年 EPS 上修，Energy、Tech、Communication Services 支撑明显 |

## 3. 历史收益分解

下表使用相同口径：`forward EPS = SPX close / forward P/E`。FactSet 周五报告通常基于前一交易日收盘价，因此 4/17、4/24、5/8 报告分别匹配 4/16、4/23、5/7 收盘。

| 阶段 | 价格变化 | fwd EPS 变化 | fwd PE 变化 | ln 价格 | ln EPS 贡献 | ln PE 贡献 | EPS 贡献占比 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2025-10-29 -> 2026-03-31：高估值顶部到 Q1 压缩 | -5.3% | +11.1% | -14.7% | -5.4% | +10.5% | -15.9% | -195% |
| 2025-12-31 -> 2026-03-31：年末到 Q1 末 | -4.6% | +6.5% | -10.5% | -4.7% | +6.3% | -11.0% | -133% |
| 2026-03-31 -> 2026-05-07：Q1 末以来 | +12.4% | +5.4% | +6.6% | +11.7% | +5.3% | +6.4% | 45% |
| 2026-04-09 -> 2026-05-07：近 1 个月 | +7.5% | +4.4% | +2.9% | +7.2% | +4.3% | +2.9% | 60% |
| 2026-04-16 -> 2026-05-07：财报核心段 | +4.2% | +3.7% | +0.5% | +4.1% | +3.6% | +0.5% | 88% |
| 2026-04-23 -> 2026-05-07：最近两周 | +3.2% | +2.7% | +0.5% | +3.2% | +2.7% | +0.5% | 85% |

解释：

- 2025-10-29 的 forward P/E 为 23.1x，是 5 年多高位；到 2026-03-31 降到 19.7x，即使 EPS 继续上修，价格仍下跌。这说明 **EPS 上修只能部分缓冲 PE 压缩，不能保证价格上涨**。
- 2026-03-31 以后，早期上涨同时来自 EPS 和 PE；但越接近 5 月，EPS 贡献越高，说明财报季正在实质性接住估值。
- 当前更合理的表述是：**rally 的早期脆弱，后半段质量改善，但估值仍没有便宜**。

## 4. 当前 rally 的 EPS vs PE 结构

### 4.1 S&P 500 层面

FactSet 2026-05-08 显示，89% 的 S&P 500 公司已经披露 Q1，84% EPS 超预期，Q1 blended EPS growth 从 3/31 的 13.1% 上修到 27.7%。这是 forward EPS 上修的直接来源。

拆分后的含义：

- **3/31 到 5/7**：EPS 上修贡献 45%，PE 扩张贡献 55%。这不是纯盈利驱动。
- **近 1 个月**：EPS 上修贡献 60%，PE 扩张贡献 40%。质量改善。
- **4/16 后**：PE 基本横住，价格主要靠 EPS 上修。这是当前多头最强论据。

### 4.2 Sector 层面

FactSet 2026-05-08 sector forward P/E：

| Sector | 当前 fwd P/E | 5 年均值 | 10 年均值 | 估值状态 |
|---|---:|---:|---:|---|
| Information Technology | 24.6x | 25.8x | 22.8x | 低于 5 年均值，高于 10 年均值；需要 EPS 继续强 |
| Communication Services | 21.6x | 18.6x | 17.4x | 明显高于历史均值；对广告、AI capex 回报敏感 |
| S&P 500 | 21.0x | 19.9x | 18.9x | 整体偏贵 |
| 非科技近似：S&P 500 ex Info Tech & Comm | 无公开直接 forward EPS | 估值低于 mega-cap growth，但 EPS revision 分化 | 不能简单等同便宜 |

Schwab/LSEG I/B/E/S 的 2026-05-01 数据显示，2026 年全年 EPS 增长预期被明显上修：S&P 500 从年初 15.6% 升到 22.6%，Technology 从 30.8% 升到 46.2%，Communication Services 从 10.5% 升到 23.1%。这说明盈利上修主要集中在科技、通信服务和少数高动量行业，而不是完全均匀扩散。

半导体方面，公开 index-level forward EPS 不完整。可用 proxy 是：

- SOXX 2026-05-08 收盘 520.30，近 1 个月涨幅远高于 SPX。
- Schwab/LSEG 数据指出，Technology 2026 EPS 上修中，Micron、Intel、Broadcom 等是主要贡献者之一。
- 这意味着半导体的 EPS revision 方向仍偏正，但价格弹性和仓位拥挤度也最高；一旦 EPS 上修放缓，multiple 压缩会比 SPX 更剧烈。

### 4.3 Mag 7 层面

Mag 7 仍是 EPS 上修的核心来源。FactSet 2026-05-04 指出，NVIDIA、Meta、Microsoft 是推动 Q1 S&P 500 EPS 增长上修的关键公司；若排除这三家公司，Q1 S&P 500 EPS growth 会从 14.4% 降到 9.1%。Schwab/LSEG 也显示，Mag 7 2026 年 EPS 增速预期约 30%，其他 493 家约 20%。

当前结论：

- Mag 7 盈利仍足以支撑高估值，但支撑越来越集中。
- Apple、Tesla 不是当前 EPS 上修的主要来源；当前更关键的是 NVIDIA、Microsoft、Meta、Alphabet、Amazon。
- 后续若 NVIDIA 等 AI 链公司继续上修，21x forward PE 可以被消化；若只剩价格上涨而 EPS 不再跟进，市场会重新按 2025Q4/2026Q1 的模式压缩 PE。

## 5. EPS Revision Breadth

公开可得的真实 breadth 不完整，下面用三组 proxy 判断。

| Proxy | 最新状态 | 判断 |
|---|---:|---|
| Q1 EPS beat rate | 84% | 广义财报 surprise breadth 很强 |
| Q1 revenue beat rate | 80% | 收入端也强，但 surprise 幅度低于 EPS |
| Q2 bottom-up EPS estimate | 2026 年 4 月 +2.1% | 反季节性上修，强信号 |
| CY 2026 bottom-up EPS estimate | 2026 年 4 月 +3.4% | 全年上修，支持 forward EPS |
| Q2 sector revision breadth | 6/11 sectors 上修 | breadth 不差，但不是全市场均匀扩散 |
| Q1 sector EPS growth | 10/11 sectors 正增长 | 财报实际 breadth 好于 4 月中旬 |
| 风险点 | 上修集中在 Tech、Comm、少数 Discretionary 和 Energy | 如果主线公司失速，breadth 不足以完全保护指数估值 |

一句话：**EPS revision breadth 是正的，但质量偏集中；不是“所有板块一起上修”的低风险状态。**

## 6. 未来 5 / 21 日预测

模型形式：

```text
Delta ln EPS_fwd(t,t+h) = alpha + beta1 * recent_revision_momentum
                         + beta2 * beat_rate
                         + beta3 * guidance_breadth
                         + beta4 * sector_concentration
                         + error

Delta ln FwdPE(t,t+h) = alpha + gamma1 * real_rate_change
                       + gamma2 * inflation_surprise
                       + gamma3 * risk_appetite
                       + gamma4 * valuation_gap_to_10y_avg
                       + error
```

由于公开数据不能做日频回归，本报告使用周频 nowcast。基准输入是：EPS 上修动能强、估值高于历史均值、5/12 CPI 与利率是主要 PE 风险。

| 情景 | 未来 5 日 fwd EPS | 未来 5 日 fwd PE | 未来 5 日 price | 未来 21 日 fwd EPS | 未来 21 日 fwd PE | 未来 21 日 price |
|---|---:|---:|---:|---:|---:|---:|
| Bull：AI 财报/指引继续上修，利率稳定 | +0.7% | +0.7% | +1.4% | +2.2% | +1.5% | +3.7% |
| Base：EPS 继续上修，但 PE 小幅消化 | +0.4% | -0.3% | +0.1% | +1.3% | -1.5% | -0.2% |
| Bear：CPI/利率冲击，EPS 动能转弱 | 0.0% | -2.0% | -2.0% | -1.0% | -6.0% | -7.0% |

基准判断的关键是：未来一周 EPS 端仍有惯性，但 PE 端要面对 CPI、利率和财报尾声后的买盘真空。未来一个月如果没有新的大盘盈利上修，21.0x 更容易被压到 20.5x-20.8x；EPS +1% 到 +2% 才能抵消这类温和压缩。

## 7. 情景表：EPS 与 PE 压缩

基准使用 FactSet 2026-05-08 报告匹配的 2026-05-07 SPX close 7337.11，forward P/E 21.0x，隐含 forward EPS 349.4。

| EPS 假设 | PE 压缩到 19x | PE 压缩到 18x | PE 压缩到 17x |
|---|---:|---:|---:|
| EPS 不变 | 6638（-9.5%） | 6289（-14.3%） | 5940（-19.0%） |
| EPS +2% | 6771（-7.7%） | 6415（-12.6%） | 6058（-17.4%） |
| EPS -2% | 6506（-11.3%） | 6163（-16.0%） | 5821（-20.7%） |

含义：

- 如果 PE 从 21x 回到 19x，即使 EPS 再上修 2%，SPX 仍有约 8% 下行空间。
- 如果 EPS 转负且 PE 回到 18x，跌幅约 16%。
- 17x 不是崩盘假设，而是 2022 年估值压缩中曾经接近的区间；在高利率 + EPS 失速组合下不能排除。

## 8. 当 EPS Revision 转平或转负时，市场通常怎么反应

历史经验不是“EPS 一转负就立刻崩”，而是三步：

1. **先压 multiple**：2022 年 1/3 到 5/12，FactSet 记录 S&P 500 价格下跌 17.5%，forward EPS 反而上修 6.1%，forward P/E 下降到 16.6x。说明利率和风险溢价冲击时，EPS 上修也挡不住 PE 压缩。
2. **再看 EPS 是否兑现**：如果 EPS 仍上修，市场会在更低 PE 附近寻找支撑；如果 EPS 开始下修，则价格需要同时消化 `EPS 下修 * PE 压缩`。
3. **高估值资产反应更非线性**：2025-10-29 到 2026-03-31，S&P 500 forward EPS 仍上修约 11.1%，但 PE 从 23.1x 压到 19.7x，指数仍跌 5.3%。这就是当前市场最重要的历史参照。

对当前市场的含义：

- 只要 forward EPS 继续以每月 1%-2% 的速度上修，21x 估值可以通过横盘或小幅上涨消化。
- 如果 EPS revision 转平，21x 会变成纯估值风险，19x-20x 是合理压缩区间。
- 如果 EPS revision 转负，同时 10Y 实际利率上行或 CPI 超预期，压缩会更接近 18x-19x，而不是温和回到 20x。

## 9. 监控阈值

未来 1-4 周重点看以下触发器：

| 变量 | 多头健康状态 | 风险状态 |
|---|---|---|
| S&P 500 forward EPS | 每周继续上修，或至少不下修 | 连续 2 周转平/转负 |
| S&P 500 forward P/E | 20.5x-21.0x 横盘消化 | 跌破 20.5x 且 EPS 没上修 |
| Q2 EPS estimate | 继续上修或保持 80.47 附近 | 回吐 4 月上修幅度 |
| Mag 7 EPS revision | NVIDIA/MSFT/META/GOOGL/AMZN 继续正修 | AI capex 回报或毛利率被质疑 |
| Sector breadth | Tech/Comm 外的 Financials、Industrials、Materials 接力 | 上修重新集中到少数 mega-cap |
| 10Y real yield | 低于 2.10% | 2.10%-2.25% 以上会压高估值 |
| CPI / PCE | 核心通胀继续温和 | CPI 超预期导致降息预期被挤出 |

## 10. 最终判断

当前更接近 **“EPS 上修正在接住部分估值，但指数仍站在高 PE 上”**，而不是单纯的泡沫扩张或完全健康的盈利驱动牛市。

- 对 SPX：近一个月上涨中 EPS 贡献已经超过 PE，质量改善；但 21x forward PE 已经要求 EPS 继续上修。
- 对 QQQ / Mag 7：盈利驱动更强，但集中度更高；后续 NVIDIA、Microsoft、Meta、Alphabet、Amazon 的 revision 是关键。
- 对 SOXX / 半导体：EPS revision 方向仍偏正，但价格已经更激进。若 EPS 转平，PE 压缩和仓位消化会放大波动。
- 对非科技：估值相对低，但 EPS revision breadth 还不足以证明全面接力。市场若要健康上行，需要非科技盈利也继续上修。

一句话：**未来 1 个月能否继续上涨，不取决于 21x 本身能不能被接受，而取决于 forward EPS 能否继续每周上修；如果 EPS 动能停下来，21x 会迅速变成需要被压缩的估值。**

## 资料来源

- FactSet, [S&P 500 Earnings Season Update: May 8, 2026](https://insight.factset.com/sp-500-earnings-season-update-may-8-2026)
- FactSet, [S&P 500 Earnings Season Update: May 1, 2026](https://insight.factset.com/sp-500-earnings-season-update-may-1-2026)
- FactSet, [S&P 500 Earnings Season Update: April 24, 2026](https://insight.factset.com/sp-500-earnings-season-update-april-24-2026)
- FactSet, [S&P 500 Earnings Season Update: April 17, 2026](https://insight.factset.com/sp-500-earnings-season-update-april-17-2026)
- FactSet, [S&P 500 Earnings Season Preview: Q1 2026](https://insight.factset.com/sp-500-earnings-season-preview-q1-2026)
- FactSet, [Analysts Making Largest Increases in Quarterly EPS Estimates for S&P 500 in 5 Years](https://insight.factset.com/analysts-making-largest-increases-in-quarterly-eps-estimates-for-sp-500-in-5-years)
- FactSet, [Three “Magnificent 7” Companies Push S&P 500 Earnings Growth to Highest Level Since 2021](https://insight.factset.com/three-magnificent-7-companies-push-sp-500-earnings-growth-to-highest-level-since-2021)
- FactSet, [Highest Forward 12-Month P/E Ratio For the S&P 500 in More Than 5 Years](https://insight.factset.com/highest-forward-12-month-p/e-ratio-for-the-sp-500-in-more-than-5-years)
- FactSet, [S&P 500 Forward P/E Ratio Falls Below 10-Year Average for the First Time Since Q2 2020](https://insight.factset.com/sp-500-forward-p/e-ratio-falls-below-10-year-average-for-the-first-time-since-q2-2020)
- Charles Schwab, [First Quarter 2026 Earnings: Feelin' Alright](https://www.schwab.com/learn/story/earnings-season-update)
- Local workspace data: `data/common_daily/raw/yahoo_ohlcv_daily.csv`
