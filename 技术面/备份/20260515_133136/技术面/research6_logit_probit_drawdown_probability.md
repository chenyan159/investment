# 研究 6：Logit / Probit 回撤概率模型

> 截至日期：2026-05-11；模型当前条件使用本地面板最新交易日 **2026-05-08**。  
> 数据来源：`data/common_daily/features/common_research_daily_panel_full.csv` 与 `data/common_daily/raw/yahoo_ohlcv_daily.csv`。  
> 重要说明：本研究是概率风控框架，不构成投资建议；5 日窗口有重叠，系数显著性只能当作方向性证据。

## 0. 结论摘要

1. **当前一周回撤风险排序：SOXX > QQQ > SPY。** Logit 当前估计显示，未来 5 个交易日路径内最大回撤超过 3% 的概率约为：SPY **9.9%**，QQQ **17.0%**，SOXX **39.1%**。
2. **SOXX 的尾部概率明显高。** 当前 SOXX 未来 5 日最大回撤超过 5% 的 Logit 概率约 **19.1%**，显著高于 QQQ 的 **5.5%**。
3. **高 PE + 高 1 月涨幅没有在“最大回撤 >3%”目标上形成显著正向证据。** `PE x r21` 对 DD<-3% 的 p 值为 SPY 0.642、QQQ 0.416、SOXX 0.821。短线回撤概率更主要由 VIX、利率、信用压力、估值水平和中期动量共同解释。
4. **预测能力是“可用于风险分层”，不是可单独交易。** 5 年滚动训练、下一年预测的 DD<-3% ROC AUC：SPY 0.651，QQQ 0.561，SOXX 0.582。QQQ/SOXX 只有中等偏弱的分类能力，但 Brier score 可用于概率校准和仓位风控。

## 1. 当前数据快照

| 变量 | 最新值 | 解释 |
| --- | --- | --- |
| 数据最新交易日 | 2026-05-08 | 价格与公开面板的最新可用日期 |
| S&P 500 trailing PE | 28.43 | 估值处在偏高区间 |
| S&P 500 P/S | 3.08 | 本模型中比 trailing PE 更稳定 |
| ERP proxy | -0.89% | 盈利收益率减 10Y，美股风险补偿偏薄 |
| 10Y / 10Y real yield | 4.41% / 1.96% | 贴现率仍是主要风险变量 |
| 10Y 5 日变化 | +0.02 pct pt | 近期变化不大 |
| VIX | 17.19 | 中性，不是恐慌状态 |
| % above 50dma | 51.1% | 当前成分股宽度约半数在 50 日线上 |
| SPY r21 / r63 / r252 | 8.5% / 7.1% / 33.0% | 动量输入 |
| QQQ r21 / r63 / r252 | 16.6% / 16.8% / 47.9% | 动量输入 |
| SOXX r21 / r63 / r252 | 37.4% / 49.4% / 175.5% | 动量输入 |

## 2. 目标变量与模型设定

定义从 t 日收盘后的未来 5 个交易日风险：

```text
ret[t,t+5] = AdjClose[t+5] / AdjClose[t] - 1
DD[t,t+5]  = min(AdjLow[t+1] ... AdjLow[t+5]) / AdjClose[t] - 1
Y = 1(事件发生)
Pr(Y=1) = Λ(α + Xβ)
```

| 变量组 | 本次实际使用字段 |
| --- | --- |
| 估值 | S&P 500 trailing PE、P/S、ERP proxy；forward PE 不在公开面板中 |
| 动量 | 各资产 r5、r21、r63、r252 |
| 利率 | 10Y、10Y real yield、10Y 过去 5 日变化 |
| 信用 | `HY_OAS` 只有 2023-05 后样本，因此核心模型改用 `-log(HYG/LQD)` 信用压力代理及其 5 日变化 |
| 波动率 | VIX、VIX 5 日变化 |
| 盈利 | EPS revision 不在公开面板中，未强行代理 |
| 宽度 | RSP/SPY、当前成分股 % above 50dma；注意有当前成分股幸存者偏差 |
| 交互项 | PE x r21、ERP x 10Y 5 日变化；EPS revision x PE 缺数据未纳入 |

预测概率使用 L2 收缩 Logit/Probit；系数表使用未惩罚 Logit。所有连续变量先做 z-score，因此 odds ratio 约等于变量上升 1 个样本标准差后的赔率变化。

## 3. 当前条件概率表

表内格式为 **Logit / Probit**。历史基准为 2010-03-16 至可验证样本末尾的无条件发生率。

### 3.1 未来 5 日收盘跌幅概率

| 标的 | P(ret<0) | P(ret<-2%) | P(ret<-3%) | P(ret<-5%) | 历史 P(ret<0) |
| --- | --- | --- | --- | --- | --- |
| SPY | 35.9% / 35.0% | 10.1% / 9.0% | 4.8% / 4.0% | 1.3% / 1.1% | 38.7% |
| QQQ | 42.7% / 42.3% | 17.2% / 16.4% | 10.1% / 9.6% | 2.8% / 2.7% | 39.2% |
| SOXX | 42.4% / 41.8% | 28.6% / 28.2% | 16.6% / 16.1% | 8.5% / 8.3% | 41.9% |

### 3.2 未来 5 日路径最大回撤概率

| 标的 | P(DD<-2%) | P(DD<-3%) | P(DD<-5%) | 历史 P(DD<-3%) |
| --- | --- | --- | --- | --- |
| SPY | 21.5% / 21.1% | 9.9% / 9.3% | 2.5% / 2.1% | 13.8% |
| QQQ | 30.1% / 30.0% | 17.0% / 16.5% | 5.5% / 4.8% | 20.9% |
| SOXX | 54.0% / 54.0% | 39.1% / 39.3% | 19.1% / 19.2% | 34.5% |

解释：QQQ 当前“收跌概率”不低，但 DD<-3% 概率低于自己的历史基准；SOXX 则相反，DD<-3% 与 DD<-5% 均高于自身历史基准，说明半导体短线更需要按高 beta 资产处理。

## 4. 哪些变量提高回撤概率

下面是 `DD<-3%` 的 Logit 系数中，正向且统计证据较强的变量。`OR` 为标准化变量上升 1 个标准差后的 odds ratio。

| 标的 | 变量 | 系数 | OR | p 值 |
| --- | --- | ---: | ---: | ---: |
| SPY | VIX | 0.585 | 1.79 | <0.001 |
| SPY | P/S | 0.513 | 1.67 | <0.001 |
| SPY | 信用压力(HYG/LQD) | 0.441 | 1.55 | 0.004 |
| SPY | RSP/SPY | 0.236 | 1.27 | 0.044 |
| QQQ | VIX | 0.444 | 1.56 | <0.001 |
| QQQ | 10Y | 0.745 | 2.11 | <0.001 |
| QQQ | P/S | 0.435 | 1.55 | 0.001 |
| QQQ | 信用压力(HYG/LQD) | 0.377 | 1.46 | 0.004 |
| SOXX | VIX | 0.344 | 1.41 | <0.001 |
| SOXX | P/S | 0.517 | 1.68 | <0.001 |
| SOXX | 10Y | 0.860 | 2.36 | <0.001 |
| SOXX | 信用压力(HYG/LQD) | 0.424 | 1.53 | <0.001 |
| SOXX | r63 | 0.111 | 1.12 | 0.020 |

主要读法：

- **VIX 是最稳定的正向变量。** 三个标的中 VIX 上升都提高 DD<-3% 的概率。
- **利率变量对 QQQ/SOXX 更重要。** 10Y 在 QQQ 和 SOXX 中显著为正，符合成长/半导体久期更长的直觉。
- **信用压力为正。** `-log(HYG/LQD)` 越高，表示 HYG 相对 LQD 越弱，回撤概率越高。
- **P/S 比 trailing PE 更稳定。** 在多变量框架下，P/S 的正向解释力比 PE 更强；这可能是因为 PE 与 ERP、利率变量存在较强共线性。

### 4.1 高 PE + 高 1 月涨幅检验

| 标的 | PE x r21 系数 | OR | p 值 |
| --- | ---: | ---: | ---: |
| SPY | 0.023 | 1.02 | 0.642 |
| QQQ | 0.034 | 1.04 | 0.416 |
| SOXX | 0.009 | 1.01 | 0.821 |

当前标准化条件如下：

| 标的 | PE z | r21 z | PE x r21 | VIX z | 10Y z |
| --- | ---: | ---: | ---: | ---: | ---: |
| SPY | 1.24 | 1.71 | 2.11 | -0.18 | 1.75 |
| QQQ | 1.24 | 2.89 | 3.57 | -0.18 | 1.75 |
| SOXX | 1.24 | 4.62 | 5.72 | -0.18 | 1.75 |

结论：`PE x r21` 在 DD<-3% 上没有显著正向证据。它对 QQQ 的 5 日收盘负收益有弱正向证据，对 SOXX 的 5 日收盘跌超 3% 也有弱正向证据，但没有稳定传导到路径最大回撤目标。因此交易上不宜把“PE 高 + 1 月涨幅高”单独当成一周回调触发器，更适合作为估值/动量过热的辅助条件。

## 5. 概率校准、ROC/PR 与 Brier score

回测方式：从 2015 年开始，每年用过去 5 年训练，预测下一年；所有结果为严格时间顺序的 walk-forward。核心目标为 `DD<-3%`。

| 标的 | 样本 | 事件率 | ROC AUC | PR AUC | Brier |
| --- | ---: | ---: | ---: | ---: | ---: |
| SPY | 2853 | 14.1% | 0.651 | 0.261 | 0.118 |
| QQQ | 2853 | 22.3% | 0.561 | 0.260 | 0.192 |
| SOXX | 2853 | 36.8% | 0.582 | 0.435 | 0.240 |

![Calibration DD<-3%](outputs/research6_logit_probit_drawdown_probability/calibration_dd3.svg)

![ROC PR DD<-3%](outputs/research6_logit_probit_drawdown_probability/roc_pr_dd3.svg)

读法：

- **ROC AUC**：SPY 的分类能力最好，QQQ/SOXX 只有中等偏弱；这说明科技和半导体回撤更多受事件冲击与仓位拥挤影响，单纯日频宏观/估值变量难以充分捕捉。
- **PR AUC**：要和事件率一起看。SOXX 的 PR AUC 最高，部分来自其 DD<-3% 本身更常发生。
- **Brier score**：概率质量比方向分类更有用，适合做仓位折扣、保护性期权预算、或“是否需要防一周回调”的风险仪表。

## 6. 交易与风控含义

1. **QQQ：当前不是最高风险档，但不适合无保护追涨。** DD<-3% 的模型概率低于历史基准，说明当前 VIX 和信用环境没有进入恐慌状态；但收跌概率仍在 40% 左右，一周尺度更像震荡消化。
2. **SOXX：短线防回撤优先级更高。** DD<-3% 约四成、DD<-5% 约两成，且高于自身历史基准；如果 VIX 上行、10Y 上行或信用压力扩大，概率会继续抬升。
3. **模型适合做风险开关，不适合做机械卖出信号。** 当 Logit/Probit 同时抬升、校准图对应区间的 realized frequency 也上升时，才更适合降低 beta、买保护或延后新增仓位。
4. **缺失数据限制很重要。** forward PE、EPS revision、真实点位成分股宽度、历史持仓集中度都需要授权或点位数据；加入这些变量后，SOXX/QQQ 的回撤概率模型可能会明显改善。

## 7. 输出文件

| 文件 | 内容 |
| --- | --- |
| `outputs/research6_logit_probit_drawdown_probability/current_probability_table.csv` | 当前 Logit/Probit 条件概率与历史基准 |
| `outputs/research6_logit_probit_drawdown_probability/coefficient_table_dd3_logit.csv` | DD<-3% 未惩罚 Logit 系数表 |
| `outputs/research6_logit_probit_drawdown_probability/pe_r21_interaction_tests.csv` | PE x r21 显著性检验 |
| `outputs/research6_logit_probit_drawdown_probability/walk_forward_metrics_dd3.csv` | walk-forward ROC/PR/Brier |
| `outputs/research6_logit_probit_drawdown_probability/calibration_dd3.svg` | 概率校准图 |
| `outputs/research6_logit_probit_drawdown_probability/roc_pr_dd3.svg` | ROC / PR 曲线 |
