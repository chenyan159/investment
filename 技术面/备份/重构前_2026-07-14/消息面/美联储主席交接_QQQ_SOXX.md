# 美联储主席交接事件研究：历史窗口与 QQQ/SOXX 展望


## 2026-05-15 全面更新：Fed 主席交接

### 对原结论的修正

1. 5/15 更新后，Fed 主席交接的重要性低于通胀和长端利率本身。4 月 CPI 环比 +0.6%、核心 +0.4% 使市场更关心反应函数是否偏鹰。
2. 4/29 FOMC 仍维持 3.50%-3.75%，但声明承认通胀偏高和能源/中东不确定性。新主席叙事会通过“是否容忍更高通胀”影响 long-duration 估值。
3. QQQ/SOXX 的主要风险不是换人当天，而是首次沟通、点阵图/SEP、以及市场是否上调长期实际利率中枢。

### 当前使用方式

- 若新主席沟通偏鹰，DGS10/DFII10 上行，SOXX 风险高于 QQQ。
- 若沟通强调数据依赖且通胀后续降温，换届本身可能成为不确定性解除。
- 观察 6 月 FOMC 前后 VIX、DFII10 和 SOXX/QQQ 相对表现。


> 更新日期：2026-05-15 美西时间；市场数据已刷新至 2026-05-15 美股收盘。
> 备份位置：备份/20260515_133136/。
> 数据刷新：已重新运行 scripts/01_build_common_daily_data.py、02_build_public_supplement_data.py、03_build_policy_geopolitical_risk_data.py、04_refresh_workspace_inventory.py，写入 data/common_daily/features/common_research_daily_panel_full.csv。
> 口径限制：本次使用公开数据源（Yahoo chart API、FRED、Multpl、iShares/Wikipedia、BLS、Federal Reserve、FactSet 2026-05-15 Earnings Insight PDF）。历史模型系数没有原始训练脚本可复现时，本更新不伪造“重新训练”结果，而是用最新面板数据更新状态判断、风险档位和触发条件。

### 最新市场快照

| 指标 | 2026-05-15 最新值 | 关键变化 |
|---|---:|---|
| SPX | 7408.50 | 距历史高点 -1.24%，较 2026-03-30 低点 +16.78% |
| SPY | 739.17 | 1 日 -1.20%，21 日 +5.35%，252 日 +27.24% |
| QQQ | 708.93 | 1 日 -1.51%，21 日 +10.69%，252 日 +37.34%，相对 50 日均线 +12.30% |
| SOXX | 508.52 | 1 日 -4.06%，5 日 -2.26%，21 日 +25.27%，252 日 +138.26%，相对 50 日均线 +26.81% |
| SMH | 556.34 | 1 日 -3.80%，21 日 +22.33%，252 日 +125.04%，相对 50 日均线 +23.22% |
| VIX | 18.43 | 较 5/8 的低波动环境抬升，但还不是恐慌区 |
| 10Y 名义利率 DGS10 | 4.47% | 高于 5/8 的 4.41%，仍压制长久期估值 |
| 10Y 实际利率 DFII10 | 2.00% | 接近但未突破 2.10%-2.25% 的高压区 |
| 10Y breakeven T10YIE | 2.47% | 通胀预期未失控，但较舒适区偏高 |
| HY OAS / IG OAS | 2.76 / 0.76 | 信用压力仍低，不像系统性风险阶段 |
| S&P 当前成分 20/50/200 日线上比例 | 35.2% / 43.9% / 50.9% | 宽度继续走弱，指数强于多数股票 |
| 成分股涨跌家数 | 141 涨 / 360 跌 | 当日宽度明显偏空 |
| Mag7 当前持仓权重代理 | 35.1% | 集中度仍高 |

### 最新宏观与盈利证据

- BLS 2026-05-12 发布的 4 月 CPI：CPI-U 环比 +0.6%、同比 +3.8%；核心 CPI 环比 +0.4%、同比 +2.8%。这比 5/8 文件中的“3 月核心仍温和”更偏鹰，短线解释了利率与半导体估值压力。
- Federal Reserve 2026-04-29 FOMC：维持联邦基金目标区间 3.50%-3.75%，声明承认通胀偏高、能源和中东不确定性，政策路径仍依赖数据。
- FactSet 2026-05-15 Earnings Insight：S&P 500 Q1 2026 blended EPS growth 27.7%、revenue growth 11.4%；Information Technology revenue growth 29.2%、earnings growth 51.0%；forward 12M P/E 21.4，高于 5 年均值 19.9 和 10 年均值 18.9；CY2026 EPS growth 预期 21.5%、revenue growth 10.3%。

### 更新后的总判断

5/15 的新信息把风险从“高位但未触发”推向“已有一次去杠杆确认”。SOXX/SMH 的单日 -4% 左右下跌验证了原文件反复提示的半导体拥挤交易与左尾风险；但信用利差仍低、VIX 未进入恐慌、FactSet 盈利修正仍强，暂时不能把它升级成 AI/科技基本面崩塌。当前更合适的框架是：核心趋势未破，但短线仓位和估值已经进入需要分批、等待确认、控制 beta 的阶段。

## 历史正文

撰写日：2026-05-11  
美股价格数据截至：2026-05-08 收盘；DXY/黄金期货数据截至 2026-05-10；FRED 利率数据截至 2026-05-07。  
结论仅用于研究，不构成投资建议。

## 结论摘要

1. 历史上，Fed 主席交接本身通常不是决定市场中期方向的核心变量。提名日往往体现“解除不确定性”的短线风险偏好，确认日大多已被定价；真正影响资产的是随后市场如何重新定价政策反应函数、通胀可信度和长端利率。
2. 1979 年 Volcker 的经验说明，市场大波动不是来自“换人”这个动作，而是来自 1979-10-06 的政策框架切换：T-1 到 T+1 窗口内，标普 500 -4.17%，纳指 -4.66%，10Y 美债收益率 +49bp。
3. 2014 Yellen 和 2018 Powell 的首次 FOMC/记者会对成长股更敏感：Yellen 首次记者会附近 10Y +11bp、QQQ -0.27%；Powell 首次记者会附近 QQQ -2.89%、SOXX -2.45%。这说明“首次沟通”比“任命流程”更容易触发成长股估值重估。
4. 2026 年当前情景是：Warsh 已获提名并通过参议院银行委员会，但截至本报告写作时尚未看到最终全院确认；Powell 主席任期即将到期，下一次 FOMC 是 2026-06-16 至 06-17。当前 Fed 仍处于高通胀、低但放缓的就业增长、政策利率 3.50%-3.75% 的环境。
5. 对 QQQ/SOXX：基本判断是趋势仍偏多，但短线过热明显。QQQ 更像“强势但可承受回撤”的资产；SOXX 是更高 beta 的同向杠杆，继续上行需要 AI/半导体盈利预期与长端利率稳定同时配合。若 10Y 快速上破 4.75%、DXY 重回 101 以上或新主席释放过度政治化/过度宽松信号导致通胀风险溢价上升，SOXX 的回撤风险会显著高于 QQQ。

## 研究方法

事件窗口采用交易日对齐：若事件日非交易日，使用事件日之后的第一个可交易日。主要窗口：

- T-1 -> T+1：事件日前一交易日收盘到后一交易日收盘，适合观察短线反应。
- T-5 -> T+5：两周左右窗口，适合过滤单日噪音。
- T -> T+20：约一个月窗口，适合观察是否有延续。

资产代理：

- 股指：S&P 500、NASDAQ Composite。
- 利率：FRED DGS10，变化单位为 bp。
- 美元：DXY；长历史也参考 FRED DTWEXM，但 DTWEXM 已在 2019 后停更。
- 黄金：2000 年后使用黄金期货；1979/1987 等早期窗口缺少可直接复现的日频黄金现货数据，因此只在长历史表中使用 Fama-French Gold 行业作为“黄金矿业股代理”，不等同于现货黄金。
- 银行/科技/芯片：Fama-French 49 行业日频组合中的 Banks、Chips、Softw；现代窗口另看 XLF、SMH、QQQ、SOXX。

样本只有 5 次现代主席交接，不能当作统计显著的模型；它更适合做情景参考。

## 关键事件日期

| 主席 | 提名/宣布 | 参议院确认 | 就任 | 首次 FOMC / 首次记者会 |
| --- | --- | --- | --- | --- |
| Paul Volcker | 1979-07-25 | 1979-08-02 | 1979-08-06 | 首次常规 FOMC：1979-08-14；政策框架切换：1979-10-06 |
| Alan Greenspan | 1987-06-02 | 1987-08-03 | 1987-08-11 | 首次 FOMC：1987-08-18 |
| Ben Bernanke | 2005-10-24 | 2006-01-31 | 2006-02-01 | 首次 FOMC：2006-03-28；制度化 FOMC 记者会首次：2011-04-27 |
| Janet Yellen | 2013-10-09 | 2014-01-06 | 2014-02-03 | 首次 FOMC/记者会：2014-03-19 |
| Jerome Powell | 2017-11-02 | 2018-01-23 | 2018-02-05 | 首次 FOMC/记者会：2018-03-21 |
| Kevin Warsh 2026 | 2026-01-30 宣布；2026-03-04 正式送交参议院 | 2026-04-29 委员会通过，待全院确认 | 若确认，接替 Powell 主席任期结束后的职位 | 下一次 FOMC：2026-06-16 至 06-17 |

## 历史短线反应：T-1 -> T+1

单位：股票、美元、行业组合为百分比收益；US10Y 为 bp。`FF_Gold` 是黄金矿业股代理，不是现货黄金。

| chair | event | date | SPX | NASDAQ | US10Y | DXY | FF_Banks | FF_Chips | FF_Softw | FF_Gold | QQQ | SOXX | XLF | SMH | GoldFut |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Volcker | nomination_announced | 1979-07-25 | 1.11 | 1.09 | -9 | 0.40 | 1.14 | 1.87 | 3.02 | -2.19 |  |  |  |  |  |
| Volcker | senate_confirmed | 1979-08-02 | -0.12 | 0.51 | -7 | 0.20 | 2.36 | 1.33 | 0.70 | -0.30 |  |  |  |  |  |
| Volcker | first_FOMC_regular | 1979-08-14 | 0.77 | 0.73 | 0 | 0.22 | 1.94 | 2.63 | 3.00 | -0.46 |  |  |  |  |  |
| Volcker | policy_regime_shift_not_transition | 1979-10-06 | -4.17 | -4.66 | 49 | 0.97 | -5.87 | -4.32 | -7.00 | -3.02 |  |  |  |  |  |
| Greenspan | nomination_announced | 1987-06-02 | 1.26 | 0.22 | 19 | -1.03 | 0.78 | -0.35 | -0.72 | 0.38 |  |  |  |  |  |
| Greenspan | senate_confirmed | 1987-08-03 | -0.76 | -0.48 | 15 | 1.24 | -1.21 | -1.08 | -1.03 | 4.56 |  |  |  |  |  |
| Greenspan | first_FOMC | 1987-08-18 | -1.28 | -0.82 | 21 | -2.06 | -1.78 | -1.33 | -1.52 | 2.44 |  |  |  |  |  |
| Bernanke | nomination_announced | 2005-10-24 | 1.44 | 1.31 | 15 | -1.18 | 1.77 | -0.10 | 2.32 | 5.75 | 1.19 | -0.39 | 1.40 | -1.58 | 1.24 |
| Bernanke | senate_confirmed | 2006-01-31 | -0.21 | 0.16 | 3 | 0.10 | -0.79 | 0.34 | -0.16 | 4.90 | -0.09 | -0.33 | -0.44 | -0.37 | 0.64 |
| Bernanke | first_FOMC | 2006-03-28 | 0.10 | 0.96 | 11 | 0.20 | -0.77 | 1.60 | 1.17 | 4.28 | 1.48 | 0.94 | -0.37 | 0.99 | 1.06 |
| Bernanke | first_regular_FOMC_press_conf | 2011-04-27 | 0.98 | 0.88 | 0 | -0.98 | 1.91 | 2.30 | 1.98 | 2.27 | 0.53 | -0.57 | 1.42 | 0.22 | 1.85 |
| Yellen | nomination_announced | 2013-10-09 | 2.24 | 1.78 | 5 | 0.45 | 1.96 | 0.33 | -0.22 | -3.62 | 1.80 | 1.86 | 3.22 | 1.94 | -2.08 |
| Yellen | senate_confirmed | 2014-01-06 | 0.36 | 0.51 | -5 | 0.05 | 1.01 | -0.89 | 1.23 | -0.03 | 0.55 | 0.20 | 0.14 | -0.31 | -0.73 |
| Yellen | first_FOMC_and_press_conf | 2014-03-19 | -0.01 | -0.32 | 11 | 1.01 | 2.68 | 1.47 | 1.15 | -4.55 | -0.27 | 1.75 | 1.54 | 1.57 | -2.10 |
| Powell | nomination_announced | 2017-11-02 | 0.33 | 0.71 | -3 | 0.13 | 0.75 | 2.14 | 0.22 | -0.86 | 0.77 | 2.27 | 0.53 | 1.58 | -0.60 |
| Powell | senate_confirmed | 2018-01-23 | 0.16 | 0.09 | -1 | -1.32 | 1.30 | -1.45 | 1.69 | 5.13 | 0.17 | -1.51 | 0.77 | -1.39 | 1.88 |
| Powell | first_FOMC_and_press_conf | 2018-03-21 | -2.70 | -2.68 | -6 | -0.56 | -3.86 | -2.53 | -3.62 | 0.83 | -2.89 | -2.45 | -3.72 | -2.49 | 1.18 |
| Warsh_2026 | nomination_announced | 2026-01-30 | 0.11 | -0.39 | 5 | 1.38 | 2.63 | 0.27 | -3.83 | -15.78 | -0.52 | -2.34 | 0.90 | -2.29 | -13.08 |
| Warsh_2026 | formal_nomination_to_senate | 2026-03-04 | 0.21 | 1.03 | 7 | 0.27 | -0.89 | -0.77 | 2.03 | -10.98 | 1.22 | 0.89 | 0.04 | 1.10 | -0.82 |
| Warsh_2026 | senate_hearing | 2026-04-21 | 0.40 | 1.04 | 4 | 0.55 |  |  |  |  | 1.29 | 3.41 | -0.80 | 2.77 | -1.54 |
| Warsh_2026 | committee_advanced | 2026-04-29 | 0.98 | 0.93 | 4 | -0.55 |  |  |  |  | 1.55 | 5.18 | 0.54 | 3.16 | 0.51 |

## 历史规律提炼

### 1. 提名日常见“解除不确定性”效应

Volcker、Greenspan、Bernanke、Yellen、Powell 五次提名日的 T-1 -> T+1 中位数：

| 指标 | 中位数反应 |
| --- | ---: |
| S&P 500 | +1.26% |
| NASDAQ | +1.09% |
| 10Y 美债 | +5bp |
| DXY | +0.13% |
| Fama-French Banks | +1.14% |
| Fama-French Chips | +0.33% |
| Fama-French Softw | +0.22% |

解释：市场通常先交易“人选明确”，而不是立即交易完整政策框架。若候选人被认为可信、可沟通，风险资产会短线受益；但 10Y 往往不一定下行，说明“风险偏好改善”和“通胀/增长预期上修”可能同时发生。

### 2. 确认日信息含量较低

五次确认日的中位数：S&P 500 -0.12%、NASDAQ +0.16%、10Y -1bp。确认日往往只是流程落地，除非伴随政治冲突或政策承诺，否则不是主要交易信号。

### 3. 首次 FOMC/记者会更重要

主席第一次主持 FOMC 或第一次面对记者会时，市场开始测试三个问题：

- 是否改变前任政策路径；
- 是否维护 Fed 独立性；
- 是否改变对通胀、就业和金融条件的反应函数。

2014 年 Yellen 首次记者会，10Y +11bp、DXY +1.01%，成长股温和承压。2018 年 Powell 首次记者会，QQQ -2.89%、SOXX -2.45%，但该窗口同时受到贸易政策、科技股监管和广义风险偏好的扰动。

### 4. Volcker 是“政策 regime shift”，不是普通换届模板

1979 年提名、确认、首次常规 FOMC 反应并不极端；真正极端的是 1979-10-06 的政策框架切换。这对 2026 的启示是：市场更怕的是新主席引发“政策可信度重估”，而不是换届本身。

## 2026 当前情况

截至本报告写作时可核验的信息：

- 2026-01-30，白宫宣布 Trump 提名 Kevin Warsh 为 Fed 主席。
- 2026-03-04，白宫将 Warsh 相关提名送交参议院。
- 2026-04-21，参议院银行委员会举行 Warsh 提名听证。
- 2026-04-29，参议院银行委员会以 13-11 推进 Warsh 提名，后续交由全院处理。
- Powell 于 2018-02-05 就任主席，2022-05-23 宣誓第二个四年任期；其 Fed 理事任期到 2028-01-31。
- Fed 2026-04-29 决定维持联邦基金目标区间 3.50%-3.75%，同时声明通胀仍高企，并提到能源价格和中东局势带来的不确定性。
- 最新宏观读数：2026 年 3 月 PCE 同比 +3.5%、核心 PCE +3.2%；2026 年 3 月 CPI 同比 +3.3%、核心 CPI +2.6%；2026 年 4 月非农 +11.5 万、失业率 4.3%。
- 下一次 FOMC 是 2026-06-16 至 06-17，且带 SEP 点阵图。

当前市场状态：

| 资产 | 日期 | 收盘/水平 | 1个月 | YTD | 相对50日均线 | 相对200日均线 | 20日年化波动 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| QQQ | 2026-05-08 | 711.23 | +16.56% | +16.15% | +14.59% | +17.34% | 15.57% |
| SOXX | 2026-05-08 | 520.30 | +37.42% | +65.97% | +35.83% | +64.92% | 39.35% |
| S&P 500 | 2026-05-08 | 7398.93 | +8.41% | +7.88% | +7.80% | +9.56% | 10.76% |
| NASDAQ | 2026-05-08 | 26247.08 | +15.01% | +12.96% | +13.12% | +14.98% | 15.44% |
| DXY | 2026-05-10 | 98.09 | -0.57% | -0.33% | -0.90% | -0.46% | 4.95% |
| Gold futures | 2026-05-10 | 4693.00 | -1.45% | +8.78% | -1.61% | +9.34% | 21.59% |
| 10Y Treasury | 2026-05-07 | 4.41% | +8bp | +22bp |  |  |  |
| 2Y Treasury | 2026-05-07 | 3.92% | +11bp | +45bp |  |  |  |

这张表的重点不是“价格高所以必跌”，而是 SOXX 的短线拥挤度极高。SOXX 1 个月 +37%、YTD +66%、高于 200 日均线约 65%，这类结构在趋势市可以继续冲，但对利率、盈利、地缘和仓位冲击非常敏感。

## 对 QQQ 和 SOXX 的情景判断

### 基准情景：偏多但不适合忽视回撤

条件：

- 10Y 大致维持在 4.25%-4.60% 区间，没有出现持续上破；
- DXY 不重新站上 101；
- Warsh 若确认，在首次 FOMC 中强调数据依赖和 Fed 独立性，而不是迎合政治压力承诺快速降息；
- AI 资本开支、云厂商 capex、半导体订单和大盘科技盈利预期不被下修。

推论：

- QQQ：中期趋势仍偏上，回撤更可能是上升趋势中的技术性消化。若 10Y 稳定且盈利继续上修，QQQ 有望继续跑赢 SPX，但短线已经离 50/200 日均线较远，追涨的风险回报下降。
- SOXX：相对 QQQ 仍有超额收益潜力，但路径会更剧烈。若 AI/先进制程/存储周期继续共振，SOXX 可以继续强于 QQQ；但任何 10%-20% 的回撤都不奇怪。

### 利多情景：长端利率下行但通胀预期不失控

条件：

- 4 月/5 月通胀数据确认能源冲击没有扩散；
- 市场相信 Warsh 会推动“更透明、更规则化”的政策沟通；
- 10Y 下行到 4.10%-4.25%，实际利率回落；
- 科技盈利继续上修。

推论：

- QQQ 将更像“广义成长股 beta”，有机会继续新高；
- SOXX 弹性更大，继续跑赢 QQQ；
- 黄金未必同步上涨，因为若是“软着陆式利率下行”，风险资产会吸收更多资金。

### 利空情景：政策独立性折价或通胀风险溢价上升

触发因素：

- 新主席或白宫沟通让市场相信 Fed 会在通胀仍高时被迫快速降息；
- 10Y 上破 4.75%，且 2Y/10Y 同时上行，说明不是单纯增长改善，而是通胀和期限溢价上升；
- DXY 走强、黄金也走强，出现“政策可信度下降”的组合；
- AI/半导体盈利预期下修，或出口管制/地缘风险冲击供应链。

推论：

- QQQ：有 8%-12% 的估值压缩风险，尤其是高估值软件、AI 平台和长久期成长股。
- SOXX：有 15%-25% 的回撤风险，因为半导体同时暴露于利率、周期、地缘、库存和 capex 预期。
- 这种情景下，“降息预期”本身不一定利多科技股；如果降息来自政治压力或通胀可信度受损，长端利率上行会抵消短端降息利好。

## 未来几个观察点

1. 参议院全院确认日：确认本身通常信息含量不高，但若票数、反对理由或候选人表态强化“独立性争议”，市场会交易风险溢价。
2. 2026-06-16 至 06-17 FOMC：这是真正的第一大事件。关注声明是否保留 easing bias、SEP 点阵图是否下调利率路径、记者会是否强调 2% 通胀目标。
3. 10Y 美债：4.60% 是第一压力区，4.75% 以上需要降低对 QQQ/SOXX 的中短期风险承受假设。
4. DXY：美元重新上 101 通常不利于海外收入占比高的大型科技和半导体链。
5. SOXX 相对 QQQ：若 SOXX/QQQ 比值继续上行，说明市场交易半导体盈利弹性；若 QQQ 新高但 SOXX 跑输，说明 AI/芯片链开始退潮。
6. CPI/PCE 的能源向核心传导：当前通胀压力有能源冲击成分，若核心服务和工资重新上行，Fed 转鸽空间会被压缩。

## 操作层面的研究结论

不做个股建议，仅给组合方向判断：

- QQQ：中期偏多，短线过热。更合理的风险管理是等待回踩或震荡消化，而不是把 Fed 换届简单理解成单向利多。只要 10Y 不持续上破 4.75%，QQQ 的主趋势尚未被破坏。
- SOXX：趋势强于 QQQ，但风险也显著高于 QQQ。当前更适合被视为“高 beta 进攻仓位”，而不是低波动核心仓位。SOXX 的核心风险不是主席换届，而是长端利率上行、AI capex 下修和半导体周期过热后的均值回归。
- 换届事件本身：提名、听证、确认不是主要决定变量；真正要交易的是首次 FOMC/记者会后的政策可信度。若新主席以规则化、反通胀、维护独立性的方式沟通，市场大概率会把换届当成可消化事件；若沟通呈现政治化降息，短线可能先涨，但中期对 QQQ/SOXX 反而更危险。

## 来源

- Fed 主席任期与 Powell 任期：[Federal Reserve Board Members, 1914-Present](https://www.federalreserve.gov/aboutthefed/bios/board/boardmembership.htm)，[Jerome H. Powell biography](https://www.federalreserve.gov/aboutthefed/bios/board/powell.htm)
- Volcker 提名：[American Presidency Project, 1979-07-25](https://www.presidency.ucsb.edu/documents/federal-reserve-system-nomination-paul-volcker-be-chairman-the-board-governors)
- Greenspan 提名与确认：[American Presidency Project, 1987-06-02](https://www.presidency.ucsb.edu/documents/remarks-announcing-the-nomination-alan-greenspan-be-chairman-the-board-governors-the)，[Congress.gov PN510](https://www.congress.gov/nomination/100th-congress/510)
- Bernanke 提名、确认、就任：[American Presidency Project, 2005-10-24](https://www.presidency.ucsb.edu/documents/remarks-announcing-the-nomination-ben-s-bernanke-be-chairman-the-federal-reserve)，[Fed 2006-02-01 swearing-in](https://www.federalreserve.gov/newsevents/pressreleases/other20060201a.htm)
- Yellen 提名、确认、首次记者会：[American Presidency Project, 2013-10-09](https://www.presidency.ucsb.edu/documents/remarks-the-nomination-janet-l-yellen-be-chair-the-federal-reserve)，[Fed 2014-02-03 swearing-in](https://www.federalreserve.gov/newsevents/pressreleases/other20140203a.htm)，[Fed 2014-03-19 press conference transcript](https://www.federalreserve.gov/files/FOMCpresconf20140319.pdf)
- Powell 提名、确认、首次记者会：[Trump White House Archive, 2017-11-02](https://trumpwhitehouse.archives.gov/presidential-actions/president-donald-j-trump-announces-nomination-jerome-powell-chairman-board-governors-federal-reserve-system/)，[Fed 2018-02-05 swearing-in](https://www.federalreserve.gov/newsevents/pressreleases/other20180205a.htm)，[Fed 2018-03-21 FOMC meeting](https://www.federalreserve.gov/monetarypolicy/fomcpresconf20180321.htm)
- Bernanke 2011 FOMC 记者会：[Fed 2011-04-27 press conference](https://www.federalreserve.gov/monetarypolicy/fomcpresconf20110427.htm)
- Warsh 2026 提名与听证：[White House 2026-01-30](https://www.whitehouse.gov/releases/2026/01/wide-acclaim-for-president-trumps-nomination-of-kevin-warsh-as-fed-chair/)，[White House nominations sent to Senate 2026-03-04](https://www.whitehouse.gov/presidential-actions/2026/03/nominations-sent-to-the-senate-b376/)，[Senate Banking hearing 2026-04-21](https://www.banking.senate.gov/hearings/04/14/2026/nomination-hearing)，[ABA Banking Journal committee vote 2026-04-29](https://bankingjournal.aba.com/2026/04/senate-banking-committee-advances-warsh-nomination/)
- 当前 Fed 政策与 FOMC 日程：[Fed FOMC statement 2026-04-29](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260429a.htm)，[Fed 2026 FOMC calendar](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)
- 当前宏观数据：[BEA Personal Income and Outlays, March 2026](https://www.bea.gov/news/2026/personal-income-and-outlays-march-2026)，[BLS CPI March 2026](https://www.bls.gov/news.release/cpi.htm)，[BLS Employment Situation April 2026](https://www.bls.gov/news.release/archives/empsit_05082026.htm)
- 市场数据：Yahoo Finance via `yfinance`；FRED `DGS10`, `DGS2`, `DTWEXM`；Kenneth R. French Data Library `49_Industry_Portfolios_daily_CSV.zip`。
