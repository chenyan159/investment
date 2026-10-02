# MF010 聚合卖空与 Short Interest 研究结果（2026-07-15）

> **报告日期：** 2026-07-15（America/Los_Angeles）  
> **研究对象：** NDX、SPX、美国全市场、Russell 2000、SOX  
> **预测窗口：** 10 / 21 / 63 / 126 / 252 个交易日  
> **核心因子：** 成分股聚合 short interest、days-to-cover（DTC）、证券借贷压力、卖空交易流量  
> **正式输出：** 本文件为本次运行唯一正式报告

## 一、执行结论

### 1.1 一句话结论

**长样本聚合 short interest 对未来 63—126 日收益存在负向条件关系，但该关系高度依赖 2008 年等危机期，2010 年后显著衰减，252 日结果甚至变号；截至 2026-07-15，公开且可审计的数据又不足以恢复五类指数的点时成分、free float、退市证券和证券借贷状态，因此五类市场在全部五个窗口的正式当前方向判断均为“无法可靠判断”。**

这不是“卖空因子没有信息”，而是三个不同结论必须同时成立：

1. **历史均值信息：** 在 1990—2021 的美国聚合代理中，short interest 较高时，SPX、NDX、SOX、全市场和 Russell 2000 的未来 63—126 日平均收益普遍较低；SOX 的负向幅度最大。
2. **尾部风险信息：** 高 short interest 状态同时对应更高的未来波动、更深的平均最大回撤，也保留很大的向上极端路径；它更像“负面信息与拥挤风险并存”的状态变量，而不是单向做空定时器。
3. **当前可交易信息：** 当前唯一能较完整重算的是 **NDX 当前成分回推代理**。该代理显示 2026-06-30 short interest 水平和 3 个报告期变化偏高，但聚合 DTC 仅处在过去 24 期的中位附近、上尾集中度反而较低，且缺少 fee、utilization、lendable supply 和 recall，不能确认“借贷拥挤”，更不能替代五指数正式点时结果。

### 1.2 结论分级

| 问题 | 本次结论 | 证据强度 |
|---|---|---:|
| 63—126 日聚合 short interest 是否有历史预测力 | 长样本中有负向关系；危机期贡献大，近年不稳定 | 中等（历史），低（当前外推） |
| 10—21 日能否由长期文献直接推出 | 不能；本次短窗口斜率较小，事件上涨率接近 50% | 低 |
| 252 日是否可靠 | 不可靠；剔除 2008 或缩短样本后大幅衰减，2010/2015 后多市场变号 | 低 |
| 高 short interest 是否必然看空 | 否；高状态同时提高下行回撤和向上尾部，存在拥挤/回补机制 | 中等 |
| short volume 能否替代 short interest | 不能；前者是交易流量，后者是某一结算日的存量 | 高 |
| ETF/期货空头能否与成分股 short interest 混合 | 不能；ETF 可用于对冲和相对价值，期货 COT 是另一套持仓口径 | 高 |
| 当前五指数是否可给出可靠方向 | 不能；除 NDX 当前成分代理外，点时成分、退市样本、float 和借贷数据均不完整 | 高（数据审计结论） |

## 二、资料边界与证据分层

### 2.1 本次实际使用的本地资料

本次只读取了方案允许范围内的 `技术面/data/` 和 `技术面/scripts/` 活动资料。允许数据提供了：

- SPX、NDX、SOX 等指数的日度 OHLCV/收盘价历史；
- 截至 2026-05-15 左右的公共日频面板；
- 2026-05-14 的 **SPX 当前成分**代理；
- 当前成分回推数据的明确生存偏差提示。

允许资料中**不存在**以下完成正式 MF010 所必需的数据：

- 五类指数逐历史日期的点时成分、权重和 free float；
- 全市场与 Russell 2000 的完整证券主表、退市收益、并购和换码链；
- 全市场逐证券的半月 short-interest 历史及其真实公开时间戳；
- securities-lending fee、utilization、on-loan quantity、lendable supply、recall；
- SOX 的完整历史成分和逐期权重。

因此，本报告将证据严格分成三层：

| 层级 | 定义 | 本报告中的用途 |
|---|---|---|
| A：直接证据 | 有真实结算日、实际公开日、当时证券集合和原始字段 | 最新 FINRA/Nasdaq 时间表、Nasdaq 单证券 short interest、FINRA 日度 off-exchange short volume |
| B：可审计代理 | 输入与计算透明，但存在当前成分回推、历史较短或市场映射偏差 | NDX 当前 103 证券代理、作者聚合 SII 对五指数收益的长样本映射、ETF 单独口径 |
| C：不可恢复 | 缺少关键输入，任何数值都会伪装精度 | SPX/全市场/Russell 2000/SOX 的 2026-06-30 成分股 SI/float、借贷拥挤和完整历史近邻 |

### 2.2 为什么不能“先拼一条长历史再说”

NYSE 的完整历史 short-interest 产品属于商业数据；Nasdaq 的公共逐证券查询只展示滚动约 12 个月/24 个报告期，完整报告通过付费 FTP 提供。NYSE Group 产品说明称其半月历史可追溯至 1988 年，但属于专有产品；Nasdaq 也明确完整 Short Interest Report 通过安全 FTP 提供，公共页面只支持逐证券查询（[NYSE Group Short Interest](https://beta.nyse.com/data-products/catalog/nyse-group-short-interest)，[Nasdaq Short Interest Report](https://www.nasdaq.com/solutions/data/equities/short-interest)，[Nasdaq Trader Short Interest](https://nasdaqtrader.com/trader.aspx?id=ShortInterest)）。

证券借贷数据同样不是一个稳定的免费公共长样本。商业产品可以提供逐日 supply、demand、fee、utilization 和 point-in-time 历史，但覆盖、供应商和字段定义会变化（[S&P Global Securities Finance](https://www.spglobal.com/market-intelligence/en/solutions/products/securities-finance)）。在没有供应商原始覆盖表的情况下，把近期 fee/utilization 与几十年 FINRA short interest 直接拼接，会制造一条从未真实存在的“伪长历史”。

## 三、结算日、申报日、公开日与模型可用日

### 3.1 四个日期必须分开

| 日期 | 含义 | 是否可作为模型信息日 |
|---|---|---:|
| 结算日（settlement date） | 券商账簿上 gross short position 的状态日 | 否，市场当时尚未看到汇总值 |
| 申报截止日（firm due date） | FINRA 会员提交数据的截止日，通常为结算日后第二个工作日 | 否，仍非公开 |
| 公开日（publication/dissemination date） | FINRA/交易所向市场发布汇总数据的日期 | 盘后发布时仍不可用于当日收盘交易 |
| 模型可用日 | 公开之后第一个可交易日 | 是；本报告所有事件收益从该日之后计算 |

FINRA Rule 4560 要求会员半月报告客户账户和自营账户中的 **gross short positions**；监管指引说明通常在指定结算日后第二个工作日申报，FINRA 在之后的公开日发布（[FINRA Rule 4560](https://www.finra.org/rules-guidance/rulebooks/finra-rules/4560)，[FINRA Short-Interest Reporting Instructions](https://www.finra.org/filing-reporting/short-interest/regulation-filing-applications-instructions)）。

### 3.2 截至本报告日的真正最新公开状态

| 项目 | 日期 | 处理 |
|---|---:|---|
| 最新已公开 short-interest 结算日 | **2026-06-30** | 可使用 |
| 会员申报截止日 | 2026-07-02 | 不作为信息日 |
| 实际公开日 | **2026-07-10** | 公开，但 Nasdaq 在 16:00 后发布 |
| 第一个模型可用交易日 | **2026-07-13** | 本报告的当前快照交易起点 |
| 下一结算日 | 2026-07-15 | **截至报告日尚未知** |
| 下一申报截止日 | 2026-07-17 | 尚未公开 |
| 下一预定公开日 | 2026-07-24 | 尚未公开，绝不估算为事实 |

以上日期来自 [FINRA 2026 Short Interest Reporting Schedule](https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest)。Nasdaq 于 2026-07-10 16:05 EDT 公布 2026-06-30 状态：全部 Nasdaq 证券 short interest 为 226.812 亿股，前一期为 219.492 亿股；全市场 DTC 则由 2.06 降至 1.64，已经直观说明“空头股数上升”和“回补所需天数上升”不是同一个命题（[Nasdaq 2026-06-30 Short Interest Release](https://www.nasdaq.com/press-release/nasdaq-announces-end-month-open-short-interest-positions-nasdaq-stocks-settlement-5)）。

### 3.3 未来监管数据也不能倒填当前历史

SEC 于 2025-12-03 再次延期：Rule 13f-2/Form SHO 的合规日延至 2028-01-02；Rule 10c-1a/SLATE 的证券借贷申报延至 2028-09-28，公共传播延至 2029-03-29。因此截至 2026-07-15，不存在可用于本研究的 Form SHO 公共长历史或 SLATE 公共贷款流（[SEC Order 34-104303](https://www.sec.gov/files/rules/exorders/2025/34-104303.pdf)，[FINRA SLATE](https://www.finra.org/filing-reporting/slate)）。

而且 Rule 10c-1a 最终规则删除了 available-to-loan 和 total-on-loan 等拟议字段；即使未来 SLATE 上线，单靠公共字段也未必能直接恢复供应商口径的 utilization（[SEC Rule 10c-1a Final Rule](https://www.sec.gov/files/rules/final/2023/34-98737.pdf)）。

## 四、四类“空头数据”不是同一个变量

### 4.1 Short interest：低频存量

Short interest 是指定结算日券商账簿中的 gross short shares。常用比率为：

\[
SIR^{float}_{i,t}=\frac{SI_{i,t}}{FreeFloat_{i,t}},\qquad
SIR^{SO}_{i,t}=\frac{SI_{i,t}}{SharesOutstanding_{i,t}}
\]

它只回答“结算日仍未回补的空头有多少”，不提供持有人身份、建仓价格、动机或实时变化。

### 4.2 Days-to-cover：仓位与流动性的联合量

\[
DTC_{i,t}=\frac{SI_{i,t}}{AverageDailyShareVolume_{i,t}}
\]

FINRA 也按 short interest 除以平均日成交量定义 DTC（[FINRA Short-Interest Glossary](https://www.finra.org/finra-data/browse-catalog/equity-short-interest/glossary)）。DTC 上升既可能因为 SI 上升，也可能因为成交量下降；它不是借贷成本，更不是预计实际回补天数。

### 4.3 Securities lending：供需与持仓成本

证券借贷提供另一个维度：

\[
Utilization_{i,t}=\frac{OnLoan_{i,t}}{LendableInventory_{i,t}}
\]

高 fee + 高 utilization + lendable supply 收缩 + recall 上升，才更接近“借券需求超过可借供给”的拥挤状态。只有 SI 高、但 fee 低且供给充足，可能只是可轻易维持的对冲或做市仓位。

### 4.4 Short volume：日度交易流量

FINRA daily short-sale volume 是 TRF/ADF 等场外报告设施中被标为 short/short-exempt 的**成交量流量**。它不是净空头变化：做市商可先 short sale 再于同日买回，客户便利交易和跨市场对冲也会形成大量 short volume。FINRA 明确警告不能把该流量直接等同于 short interest；文件也不是全交易所合并口径（[FINRA Understanding Short Sale Volume Data](https://www.finra.org/rules-guidance/notices/information-notice-051019)，[FINRA Daily Short Sale Volume](https://www.finra.org/finra-data/daily-short-sale-volume-transaction-data)）。

### 4.5 ETF 与期货必须另表记录

- ETF short interest 可能代表 long-stock/short-ETF、期权 delta hedge、指数套利或流动性提供，不能与 ETF 成分股的 SI 相加。
- CFTC COT 是每周二的期货/期权未平仓分类持仓，通常周五发布；它按 dealer、asset manager、leveraged funds 等类别汇总，且总 long open interest 与总 short open interest恒等，不是股票 short interest（[CFTC Commitments of Traders](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)）。
- 学术研究发现行业 ETF short interest 在某些情形反而正向预测 ETF 收益，原因正是多空对冲与相对价值交易，进一步支持分表处理（[ETF Short Interest and Returns, RFS](https://academic.oup.com/rfs/article-pdf/34/3/1280/36264603/hhaa077.pdf)）。

## 五、经济机制与原始研究证据

### 5.1 负面信息机制

知情卖空者愿意承担借券费、召回风险和无限上行损失，因此聚合 SI 上升可能代表负面私人信息扩散。Rapach、Ringgenberg 与 Zhou（RRZ）构造 1973—2014 的美国聚合 short-interest index（SII），报告一个标准差的 SII 上升对应未来一年年化超额收益约低 6—7 个百分点，月度和年度回归的 \(R^2\) 分别约 1.24% 和 12.89%（[RRZ working-paper PDF](https://down.aefweb.net/WorkingPapers/w716.pdf)）。

### 5.2 拥挤、借贷成本和 squeeze 机制

SI 极高也可能表示悲观已被价格吸收，剩余边际买家较少；一旦基本面没有继续恶化、借券被 recall 或风险限额收紧，回补会产生上行尾部。个股层面的 DTC、loan demand 和借贷费率研究支持这些机制：

- DTC 把空头仓位与成交能力结合，横截面上比单纯 short-interest ratio 更能刻画拥挤成本，但它是**个股横截面**证据，不能直接当作指数时序定律（[Days to Cover and Stock Returns, NBER](https://www.nber.org/system/files/working_papers/w21166/w21166.pdf)）。
- 同时观察借入数量与 fee，才能区分 demand shift 和 supply shift；单看 SI 无法完成识别（[Supply and Demand Shifts in the Shorting Market](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID2758846_code353319.pdf?abstractid=672381)）。
- 高借券费和 recall 风险会改变卖空者的持有成本与价格效率（[Short-Selling Risk](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2312625)）。
- 系统研究显示 squeeze 在股票—日层面稀少、持续较短；少数 meme 案例不能推广为指数规律（[How Prevalent Are Short Squeezes?](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4526147)）。

### 5.3 聚合预测证据的复核

| 研究 | 样本/结论 | 对 MF010 的含义 |
|---|---|---|
| RRZ（JFE 2016） | 1973—2014 美国月度聚合 SII，对未来市场收益负向预测 | 提供 63—252 日长样本原始假说 |
| Goyal、Welch、Zafirov（RFS 2024） | 扩展到 2021 后，原规格 t 值由约 -2.15 降至 -1.88；月度 OOS \(R^2\) 约 1.26%，但经济择时表现不优于全仓股票，收益集中于 2008—2011 和疫情牛市 | 统计信号不等于可交易择时；必须检查期限缩短与市场变化（[原文](https://academic.oup.com/rfs/article/37/11/3490/7749383)） |
| Priestley working paper | 排除 2008 后，RRZ 证据大幅削弱 | 危机敏感性是必做检验（[SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3384620)） |
| Gorbenko（RAPS 2023） | 32 国中 24 国的下月关系为负，平均约 -0.62%/1SD；短样本显著性较弱 | 跨国方向有一定支持，但仍不能替代五指数点时检验（[原文](https://academic.oup.com/raps/article/13/4/691/7127046)） |
| Lamont、Stein | 市场 short interest 可呈逆周期，Nasdaq 泡沫顶点前反而下降 | 低 SI 也不等于低估值或低风险（[NBER](https://www.nber.org/papers/w10218)） |

## 六、正式点时研究应如何重建

### 6.1 必需的数据表

| 表 | 必需主键/字段 | 时间要求 |
|---|---|---|
| security master | PERMNO/FIGI/CUSIP、ticker 历史、上市/退市、并购、换码、证券类型 | 每个自然日可追溯 |
| index membership | index、security id、effective-from/to、点时权重、行业 | 不得用当前成分回推 |
| shares/float | shares outstanding、free float、来源和生效日 | 只能使用当时已公开值 |
| short interest | security id、settlement、firm due、publication、SI shares、ADV、DTC | 模型从 publication 后第一交易日进入 |
| securities lending | provider、fee、utilization、on-loan、lendable、recall、coverage flag | 按供应商真实起点建独立表 |
| short volume | trade date、venue、short、short-exempt、total volume | 日度流量表，不回填存量 |
| ETF/futures | ETF SI；期货 COT/Open Interest | 与成分股表严格隔离 |

### 6.2 聚合定义

对每一公开日 \(t\) 和当时指数证券集合 \(I_t\)，至少同时计算：

\[
EW_t=\frac{1}{N_t}\sum_{i\in I_t}SIR_{i,t},\quad
Median_t=median(SIR_{i,t}),\quad
FloatAgg_t=\frac{\sum_i SI_{i,t}}{\sum_i FreeFloat_{i,t}}
\]

\[
MCW_t=\sum_i w^{PIT}_{i,t}SIR_{i,t},\quad
Breadth^{(k)}_t=\frac{1}{N_t}\sum_i \mathbf{1}(SI_{i,t}>SI_{i,t-k})
\]

还应同时保存：

- 1/2/3 个报告期总量变化和连续上升期；
- 横截面 P90/P95、超过自身历史 P90 的证券比例；
- top-decile SI 占比、极端拥挤股票的指数权重；
- 行业 SI 占比和行业 HHI；
- 聚合 DTC、fee 加权中位数、utilization P90、lendable supply 变化和 recall 广度；
- 每一期可用证券数、占当时成分数、占指数权重、退市覆盖率和供应商覆盖率。

### 6.3 预先定义的事件

正式重跑时建议在任何结果可见前固定以下状态：

1. **SI 极高：** 聚合指标高于只用此前 120 个月计算的 P80/P90；
2. **快速上升：** 1/2/3 期变化分别高于自身历史 P80；
3. **快速回补：** 1/2/3 期变化低于 P20；
4. **共同拥挤：** SI、DTC、fee、utilization 至少三项同时高于 P80，且 lendable supply 不扩张；
5. **广度扩张：** 上升证券比例高于 P80，不能只由少数 meme 股票驱动；
6. **squeeze 风险：** SI/DTC/fee 高、上尾集中高，同时 recall 上升或可借供给下降；
7. **去簇：** 连续高状态只保留首次可用日；另按每个持有期删除重叠事件；
8. **独立周期：** 事件入口至少相隔 504 个交易日，单独报告数量。

事件收益从公开后第一个交易日的收盘开始，计算 10/21/63/126/252 日总收益、上涨概率、P10/P50/P90、区间最大回撤、最大有利变动（MFE）和相对 SPX 收益。原始快照数、连续状态簇数、各期限非重叠事件数和独立周期数必须同时出现。

## 七、长样本可审计代理：聚合 SII 与五类市场价格路径

### 7.1 代理设计

由于无法取得五指数完整点时成分 SI，本节使用 RRZ 作者公开的更新 SII（1973-01 至 2021-12；OOS 序列自 1978-01）映射到五类指数价格。这是**美国市场共同卖空状态代理**，不是五指数各自的成分股 short interest。作者数据来自 [Matthew Ringgenberg Data Page](https://www.matthewringgenberg.com/data)。

方法：

- 月度 SII 只在月末后的第一个交易日进入，晚于论文所述的典型月中公开节奏，避免把结算日误当公开日；
- 收益为该可用日之后 10/21/63/126/252 个交易日 close-to-close 总收益；
- 基准回归：\(R_{t,t+h}=\alpha+\beta SII_t+\epsilon_{t+h}\)；t 值使用 Newey-West HAC，滞后阶数为 \(\lceil h/21\rceil\)；
- 稳健版只用此前 120 个月计算均值、标准差和 P20/P80，避免全样本阈值偷看未来；
- 美国全市场以 Wilshire 5000 价格指数代理；Russell 2000、SOX 的价格起点分别约为 1987-09、1994-05；其余从 1990-01 起；
- 价格面板对 2026-05-15 后需要验证的近邻收益，使用相同 Yahoo Chart 数据源补充；这不改变 SII 截止 2021-12 的事实。

### 7.2 基准连续回归

下表每格为“每 +1 个标准化 SII 单位的未来收益百分点斜率 / HAC t 值 / \(R^2\)%”。月度原始观察大量共享未来持有期，不能把行数当作独立事件数。

| 市场 | 10 日 | 21 日 | 63 日 | 126 日 | 252 日 |
|---|---:|---:|---:|---:|---:|
| SPX | -0.45 / -2.28 / 1.83 | -0.53 / -2.31 / 1.63 | -1.71 / -2.67 / 5.62 | -2.91 / -2.20 / 7.72 | -4.23 / -1.73 / 7.25 |
| NDX | -0.37 / -1.37 / 0.58 | -0.67 / -1.93 / 1.04 | -2.15 / -2.23 / 3.12 | -3.59 / -1.96 / 4.07 | -3.73 / -1.04 / 1.79 |
| 美国全市场 | -0.45 / -2.28 / 1.74 | -0.48 / -2.08 / 1.29 | -1.55 / -2.40 / 4.36 | -2.68 / -2.07 / 6.29 | -4.02 / -1.70 / 6.38 |
| Russell 2000 | -0.52 / -2.18 / 1.58 | -0.58 / -1.74 / 1.03 | -1.51 / -1.86 / 2.36 | -2.53 / -1.62 / 3.45 | -3.71 / -1.36 / 3.81 |
| SOX | -0.74 / -1.89 / 1.20 | -1.18 / -2.36 / 1.63 | -3.83 / -2.93 / 5.21 | -6.84 / -2.77 / 7.04 | -10.60 / -2.41 / 6.67 |

**读法：** 10—21 日效应小且多个市场 t 值不足；63—126 日方向最一致；252 日 t 值普遍回落，除 SOX 外均不稳健。不能把 252 日文献结论按比例缩成 10 日交易信号。

### 7.3 仅用过去 120 个月标准化后的连续回归

| 市场 | 10 日 | 21 日 | 63 日 | 126 日 | 252 日 |
|---|---:|---:|---:|---:|---:|
| SPX | -0.29 / -1.97 / 1.16 | -0.40 / -2.16 / 1.37 | -1.40 / -2.92 / 5.64 | -2.34 / -2.37 / 7.53 | -3.14 / -1.66 / 5.99 |
| NDX | -0.25 / -1.07 / 0.41 | -0.58 / -1.88 / 1.16 | -2.07 / -2.59 / 4.34 | -3.36 / -2.19 / 5.34 | -3.20 / -1.01 / 1.99 |
| 美国全市场 | -0.30 / -2.04 / 1.17 | -0.38 / -2.02 / 1.15 | -1.33 / -2.74 / 4.76 | -2.29 / -2.37 / 6.83 | -3.10 / -1.72 / 5.65 |
| Russell 2000 | -0.40 / -2.26 / 1.38 | -0.54 / -1.95 / 1.30 | -1.49 / -2.43 / 3.41 | -2.53 / -2.24 / 5.13 | -3.46 / -1.80 / 4.89 |
| SOX | -0.64 / -1.77 / 1.21 | -0.96 / -1.97 / 1.42 | -3.60 / -2.93 / 6.11 | -6.30 / -2.66 / 7.90 | -8.54 / -2.04 / 5.74 |

滚动标准化后 63—126 日仍为主要负向窗口，说明基准结论不是完全由全样本标准化造成；但下面的时期检验显示它仍高度依赖特定市场周期。

### 7.4 公开滞后、2008 年与市场变化敏感性

下表只列 63/126/252 日；每格为“收益百分点斜率（HAC t）”。“再滞后 21 日”模拟公开/执行进一步延迟；“剔除 2008”删除起点落在 2008 年的观察；“2010 后”只用 2010-01 之后的信号。

| 市场 | 窗口 | 基准 | 再滞后 21 日 | 剔除 2008 | 2010 后 |
|---|---:|---:|---:|---:|---:|
| SPX | 63 | -1.71 (-2.67) | -1.61 (-2.37) | -0.99 (-1.87) | -2.12 (-1.18) |
| SPX | 126 | -2.91 (-2.20) | -2.75 (-2.12) | -1.36 (-1.24) | -0.74 (-0.18) |
| SPX | 252 | -4.23 (-1.73) | -3.94 (-1.62) | -1.56 (-0.72) | +1.26 (+0.16) |
| NDX | 63 | -2.15 (-2.23) | -1.96 (-1.98) | -1.37 (-1.46) | -0.28 (-0.12) |
| NDX | 126 | -3.59 (-1.96) | -3.22 (-1.77) | -2.00 (-1.08) | +4.22 (+0.77) |
| NDX | 252 | -3.73 (-1.04) | -2.89 (-0.80) | -0.89 (-0.23) | +12.59 (+1.08) |
| 美国全市场 | 63 | -1.55 (-2.40) | -1.48 (-2.20) | -0.87 (-1.61) | -1.98 (-0.96) |
| 美国全市场 | 126 | -2.68 (-2.07) | -2.52 (-1.98) | -1.24 (-1.15) | -0.16 (-0.04) |
| 美国全市场 | 252 | -4.02 (-1.70) | -3.73 (-1.60) | -1.63 (-0.78) | +2.56 (+0.28) |
| Russell 2000 | 63 | -1.51 (-1.86) | -1.30 (-1.54) | -0.89 (-1.19) | -1.93 (-0.59) |
| Russell 2000 | 126 | -2.53 (-1.62) | -2.18 (-1.40) | -1.14 (-0.79) | +0.27 (+0.04) |
| Russell 2000 | 252 | -3.71 (-1.36) | -3.29 (-1.22) | -1.38 (-0.54) | +3.94 (+0.35) |
| SOX | 63 | -3.83 (-2.93) | -3.68 (-2.73) | -2.93 (-2.22) | +2.13 (+0.66) |
| SOX | 126 | -6.84 (-2.77) | -6.33 (-2.60) | -4.88 (-1.88) | +8.96 (+1.33) |
| SOX | 252 | -10.60 (-2.41) | -9.24 (-2.07) | -7.14 (-1.46) | +22.08 (+1.57) |

关键判断：

- 额外 21 日滞后没有消灭长样本负号，说明公开时点并非唯一解释；
- 剔除 2008 后，所有市场的幅度和显著性明显下降；
- 2010 后 126/252 日多数市场变为正号；
- 2015 后的 252 日斜率更进一步变成 SPX +8.89、NDX +24.31、全市场 +12.28、Russell 2000 +16.58、SOX +34.45 个百分点，样本虽短但足以否定“252 日稳定线性外推”。

### 7.5 高 SII 状态下的波动、回撤与双向尾部

“高状态”定义为 SII 高于只用此前 120 个月计算的 P80；连续高状态合并为一个事件簇。高状态相对低状态的未来实现波动率差（年化百分点）如下：

| 市场 | 10 日 | 21 日 | 63 日 | 126 日 | 252 日 |
|---|---:|---:|---:|---:|---:|
| SPX | +4.54 | +4.26 | +5.47 | +7.52 | +6.37 |
| NDX | +12.27 | +11.35 | +11.48 | +12.06 | +8.56 |
| 美国全市场 | +3.83 | +3.34 | +4.39 | +6.20 | +5.07 |
| Russell 2000 | +2.88 | +3.04 | +3.71 | +5.60 | +4.59 |
| SOX | +14.01 | +13.44 | +13.45 | +13.92 | +9.97 |

高状态相对低状态的平均最大回撤差，在 126/252 日分别为：SPX -8.87/-10.57、NDX -12.31/-11.65、全市场 -7.82/-9.17、Russell 2000 -7.66/-9.01、SOX -15.28/-14.72 个百分点。**负向均值主要来自更差的左尾，而不是“每次都会下跌”。**

### 7.6 相对强弱

下表为高 SII 与低 SII 状态之差的相对 SPX 收益（百分点，长样本递归标准化口径）。负数表示高 SII 时该市场相对 SPX 更弱。

| 市场相对 SPX | 10 日 | 21 日 | 63 日 | 126 日 | 252 日 |
|---|---:|---:|---:|---:|---:|
| NDX | +0.13 | -0.59 | -2.23 | -4.61 | -4.75 |
| SOX | -0.60 | -2.06 | -6.93 | -13.01 | -21.64 |
| 美国全市场 | 0.00 | +0.06 | +0.26 | +0.43 | +1.32 |
| Russell 2000 | +0.08 | +0.41 | +0.98 | +1.05 | +3.46 |

长样本中，聚合空头压力对半导体和高成长大盘的相对强弱更不利；全市场和小盘相对 SPX 没有同样方向。但该结论也受危机和科技周期影响，不能替代当前各指数自己的成分股 SI。

## 八、2026-07-15 当前公开卖空状态

### 8.1 五类市场的直接可用性审计

| 市场 | 2026-06-30 点时成分 SI/float | DTC | 行业/上尾 | fee/utilization/supply/recall | 当前结论 |
|---|---|---|---|---|---|
| NDX | **仅当前 103 证券回推代理**；无真实 free float | 可算 shares-weighted 代理 | 上尾可算；行业字段不足 | 不可得 | 有方向线索，无拥挤确认 |
| SPX | 不可得；本地仅 2026-05-14 当前 503 成分代理 | 不可得 | 不可得 | 不可得 | 无法建立当前存量状态 |
| 美国全市场 | 不可得；无点时全证券主表 | 不可得 | 不可得 | 不可得 | 无法建立当前存量状态 |
| Russell 2000 | 不可得；换届与退市链缺失 | 不可得 | 不可得 | 不可得 | 无法建立当前存量状态 |
| SOX | 不可得；公开方法说明有 30 个成分，但历史权重/成分不足 | 不可得 | 不可得 | 不可得 | 无法建立当前存量状态 |

NDX 官方方法说明其衡量 100 家最大 Nasdaq 非金融公司并采用 modified market-cap weighting；多证券类别均可入选，因此公共 API 在 2026-07-15 返回 103 个证券行并不矛盾（[NDX Methodology](https://indexes.nasdaqomx.com/docs/methodology_NDX.pdf)，[Nasdaq-100 Current List API](https://api.nasdaq.com/api/quote/list-type/nasdaq100)）。SOX 官方方法为 30 个证券的 modified market-cap 指数，但完整点时权重并未在本次可访问资料中提供（[SOX Overview](https://indexes.nasdaqomx.com/index/Overview/SOX)，[SOX Methodology](https://indexes.nasdaqomx.com/docs/methodology_SOX.pdf)）。

### 8.2 NDX 当前成分回推代理

计算口径：以 2026-07-15 Nasdaq API 返回的 103 个证券为集合，逐证券读取 2026-06-30 short interest；shares outstanding 以**当前市值/当前价格**近似，因此下表是 SI/shares outstanding 代理，绝不是 SI/free float。完整 24 期比较只使用每一期都有数据的固定 100 证券，专用于敏感性和近邻，存在明显生存偏差。

| 指标 | 当前 103 证券 | 24 期固定 100 证券 | 解释 |
|---|---:|---:|---|
| 有 SI 的证券数/集合数 | 103/103 | 100/100 | 公共逐证券查询覆盖当前集合 |
| 总 short interest | 35.595 亿股 | — | 当前证券总和 |
| 聚合 SI/shares outstanding | 1.91% | 2.03% | **非 float**；固定集合不同导致差异 |
| 个股 SIR 等权均值 | 3.78% | — | 易受小市值高 SIR 证券影响 |
| 个股 SIR 中位数 | 2.94% | — | 横截面中枢 |
| 聚合 DTC | 1.90 | 1.97 | 总 SI / 总 ADV |
| 个股 DTC 中位数 | 2.46 | — | 低于聚合尾部 |
| 总 SI：1/2/3 期变化 | +3.25% / +5.74% / +7.83% | +0.71% / — / +7.97% | 固定集合削弱最近一期增幅 |
| SI 上升广度：1/2/3 期 | 53.92% / 61.39% / 71.29% | 53% / — / 71% | 3 期上升较广 |
| SI 最高 10% 证券占总 SI | 37.57% | 36.55% | 并非少数单股独占 |

以当前 103 证券回推过去 24 个半月报告期（2025-07 至 2026-06）的历史分位：

| 指标 | 24 期历史分位 | 读法 |
|---|---:|---|
| 总 SI | 100% | 当前集合的一年高点 |
| 聚合 SI/shares outstanding | 100% | 当前集合的一年高点 |
| 个股 SIR 等权均值 | 100% | 横截面均值高 |
| 个股 SIR 中位数 | 95.83% | 广泛偏高 |
| 聚合 DTC | 45.83% | 约在中位，不支持流动性极端拥挤 |
| 个股 DTC 中位数 | 12.50% | 多数证券相对容易由成交量吸收 |
| top-decile SI 集中度 | 8.33% | 当前高 SI 不是由最集中尾部驱动 |

**当前 NDX 解释：** “空头股数高且三期广度扩张”与“DTC 不高、上尾集中不高”同时存在。它更像广泛的看空/对冲需求增加，而不是已经由借贷稀缺确认的 squeeze 状态。由于没有 free float、fee、utilization、supply 和 recall，不能把该代理升级为正式拥挤判断。

### 8.3 ETF short interest：单独记录

| ETF | 对应关系 | 2026-06-30 SI | DTC | 1/2/3 期 SI 变化 | 24 期 SI 分位 | 解释 |
|---|---|---:|---:|---:|---:|---|
| QQQ | NDX ETF | 64,030,392 | 1.28 | -7.85% / -3.64% / -5.35% | 83.33% | 水平仍偏高，但近期回补；不能与成分股 SI 相加 |
| SOXQ | SOX 跟踪 ETF | 1,246,892 | API=1.00；原始 SI/ADV=0.38 | -28.79% / +23.18% / +499.23% | 95.83% | 基数小且 DTC 展示值有取整/下限差异，稳定性差 |
| SOXX | 半导体 ETF 对照 | 12,688,479 | 1.24 | -0.06% / +26.48% / +45.06% | 95.83% | 不是 SOX 成分聚合 |
| SMH | 半导体 ETF 对照 | 17,216,964 | 1.47 | +23.60% / +34.48% / +32.58% | 100% | ETF 对冲需求可能很强，仍不是成分股 SI |

公共逐证券数据入口见 [Nasdaq Short Interest](https://www.nasdaq.com/market-activity/quotes/short-interest)；QQQ 和 SOXQ 的查询分别为 [QQQ API](https://api.nasdaq.com/api/quote/QQQ/short-interest?assetclass=etf) 和 [SOXQ API](https://api.nasdaq.com/api/quote/SOXQ/short-interest?assetclass=etf)。

### 8.4 FINRA off-exchange short-volume 流量代理

下表使用截至报告日前最后完整交易日 2026-07-14 的 FINRA CNMS 日文件，比例为 short volume / total volume，不含 short-exempt；**只代表 FINRA 场外报告流量，不是净仓位，也不是全市场合并成交。**

| 市场/载体 | 聚合对象 | 1 日 | 5 日 | 21 日 | 可说与不可说 |
|---|---|---:|---:|---:|---|
| NDX | 当前 103 成分，103/103 有记录 | 42.71% | 44.20% | 43.12% | 可描述场外 short-marked 流量；不能推出净空头 |
| SPX | 2026-05-14 当前 503 成分，501 有记录 | 46.00% | 46.23% | 44.53% | 当前成分代理且有生存偏差 |
| QQQ | ETF | 62.94% | 67.33% | 61.80% | ETF 做市/对冲影响很大 |
| SPY | ETF | 60.28% | 59.36% | 54.96% | 不代表 SPX 成分股存量 |
| VTI | 全市场 ETF | 51.34% | 60.47% | 63.27% | 不代表全市场成分 SI |
| IWM | Russell 2000 ETF | 64.77% | 63.02% | 63.94% | 不代表 Russell 成分 SI |
| SOXQ | SOX ETF | 39.19% | 35.24% | 42.60% | 小基数、ETF 交易结构影响大 |

存量与流量目前有明显“冲突”：NDX 成分 short interest 的一年分位很高，但 DTC 中性；QQQ ETF SI 近期回落，QQQ off-exchange short volume 却很高。按照预设纪律，这种冲突必须降低置信度，而不是挑选最符合叙事的一列。

### 8.5 证券借贷的当前边界

本次没有五指数逐成分、逐日的 fee/utilization/on-loan/lendable/recall 数据。S&P Global 的 2026 年上半年市场总结显示全球证券借贷收入创纪录，但同时指出美洲股票 fee 较低、收入较软；这是全球/地区聚合背景，不能映射成 NDX、SPX、Russell 或 SOX 的当前借贷压力（[Global Securities Finance Snapshot, June/Q2/H1 2026](https://www.spglobal.com/market-intelligence/en/news-insights/research/2026/07/global-securities-finance-snapshot-june-q2-and-h1-2026)）。

因此五类市场的 fee、utilization、可借供给和 recall 历史分位在本报告中均正式记为：**不可得，不估算。**

## 九、仅以卖空变量寻找的历史近邻

### 9.1 NDX 当前成分代理近邻

距离使用固定 100 个当前证券的 7 个卖空变量做等权标准化欧氏距离：SI/shares outstanding、1 期变化、3 期变化、1 期广度、3 期广度、DTC、top-decile SI 集中度。收益从公开日后的第一个交易日起计算。

当前目标（结算 2026-06-30、公开 2026-07-10）：SIR 2.03%、1 期 +0.71%、3 期 +7.97%、1/3 期广度 53%/71%、DTC 1.97、top-decile 36.55%。

| 近邻结算日 | 公开日 | 距离 | SIR | 1期/3期变化 | 1期/3期广度 | DTC | Top10占比 | 后10日 | 后21日 | 后63日 | 126/252日 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2026-05-29 | 2026-06-09 | 0.966 | 1.92% | +2.08% / +8.05% | 61% / 77% | 2.35 | 37.53% | +3.27% | +2.65% | — | — |
| 2026-01-15 | 2026-01-27 | 1.126 | 1.65% | -0.50% / +3.25% | 47% / 56% | 2.18 | 37.07% | -3.16% | -4.08% | +4.47% | — |
| 2025-12-31 | 2026-01-12 | 1.134 | 1.66% | -0.48% / +11.52% | 59% / 72% | 2.41 | 36.47% | +1.09% | -4.10% | +1.80% | — |
| 2026-06-15 | 2026-06-25 | 1.179 | 2.01% | +5.02% / +11.79% | 71% / 85% | 2.30 | 36.94% | +0.50% | — | — | — |
| 2026-04-30 | 2026-05-11 | 1.213 | 1.80% | +1.51% / +12.56% | 56% / 68% | 2.24 | 38.23% | +3.13% | +1.31% | — | — |
| 2026-05-15 | 2026-05-27 | 1.291 | 1.88% | +4.27% / +9.77% | 69% / 69% | 2.25 | 38.10% | -2.57% | -1.49% | — | — |

近邻结论：

- 只有 24 个原始快照，六个近邻集中在同一个市场周期且未来窗口大量重叠；
- 10 日为 4 涨 2 跌，21 日为 2 涨 3 跌，方向混合；
- 只有两个近邻拥有完整 63 日收益，均为正；126/252 日为零；
- 当前证券回推会遗漏已退市和历史成分，且 shares outstanding 不是 free float。

所以这些近邻只能说明“近期相似卖空状态没有稳定的 10/21 日方向”，不能成为统计预测。

### 9.2 其余市场

| 市场 | 历史近邻状态 | 原因 |
|---|---|---|
| SPX | 无法恢复 | 缺少逐期公开日的点时成分、退市证券、float 和逐证券 SI |
| 美国全市场 | 无法恢复 | 缺少完整证券主表、退市收益和跨交易所 SI 历史 |
| Russell 2000 | 无法恢复 | 年度重构造成成员与借贷供给机械变化，缺少点时成员链 |
| SOX | 无法恢复 | 缺少点时 30 成分、权重、float 和逐证券 SI/loan 历史 |

QQQ、SPY、VTI、IWM、SOXQ 的 ETF 数据不是这些市场的成分股历史近邻；不得把 SPX 的长样本 SII 近邻伪装成 QQQ 或 SOX 的直接证据。

## 十、五类市场、五窗口的历史条件路径与当前正式预测

### 10.1 表格读法

- “样本起点”是可用价格起点；SII 本身有更早的 120 个月历史用于滚动阈值。
- “高态快照/去簇/周期”依次为：原始高 SII 月数、连续状态合并后的事件入口数、相隔至少 504 个交易日的独立市场周期数。
- “非重叠 n”针对每个持有期重新删除重叠事件。
- 条件区间是历史高 SII 快照之后收益的 P10—P90；不是参数置信区间。
- MDD 是区间内平均最大回撤；MFE90 是最大有利变动的 P90，作为**上行挤仓尾部代理**，不是被确认的 squeeze 次数。
- 由于当前五指数的完整因子状态无法建立，历史统计只作为风险基线；正式方向不会由代理强行定向。

### 10.2 逐市场逐期限结果

| 市场 | 窗口 | 样本起点 | 高态快照/去簇/周期 | 非重叠 n | 高态平均收益 | 上涨率 | P10—P90 | 平均 MDD | MFE90 | 当前方向与置信度 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| SPX | 10 | 1990-01 | 62/8/5 | 8 | -0.41% | 53.23% | -4.01%—+3.92% | -3.44% | +4.00% | **无法可靠判断**；极低 |
| SPX | 21 | 1990-01 | 62/8/5 | 8 | -0.44% | 50.00% | -6.70%—+5.01% | -5.28% | +6.05% | **无法可靠判断**；极低 |
| SPX | 63 | 1990-01 | 62/8/5 | 8 | -1.85% | 50.00% | -13.64%—+7.68% | -10.69% | +10.29% | **无法可靠判断；历史风险偏空**；低 |
| SPX | 126 | 1990-01 | 62/8/5 | 8 | -4.90% | 43.55% | -27.35%—+11.02% | -17.18% | +13.25% | **无法可靠判断；历史左尾偏大**；低 |
| SPX | 252 | 1990-01 | 62/8/5 | 6 | -2.98% | 53.23% | -25.88%—+17.48% | -21.74% | +18.09% | **无法可靠判断；时期不稳健**；极低 |
| NDX | 10 | 1990-01 | 62/8/5 | 8 | +0.15% | 54.84% | -7.51%—+7.07% | -5.67% | +8.42% | **无法可靠判断**；当前存量与流量冲突，极低 |
| NDX | 21 | 1990-01 | 62/8/5 | 8 | -0.10% | 51.61% | -13.52%—+8.77% | -8.37% | +10.52% | **无法可靠判断**；极低 |
| NDX | 63 | 1990-01 | 62/8/5 | 8 | -1.94% | 50.00% | -23.93%—+15.07% | -16.23% | +20.84% | **无法可靠判断；历史两侧尾部扩大**；低 |
| NDX | 126 | 1990-01 | 62/8/5 | 8 | -5.40% | 41.94% | -34.51%—+20.14% | -24.47% | +27.87% | **无法可靠判断；历史风险偏空**；低 |
| NDX | 252 | 1990-01 | 62/8/5 | 6 | -0.62% | 56.45% | -35.21%—+40.17% | -29.47% | +48.84% | **无法可靠判断；双向尾部极大**；极低 |
| 美国全市场 | 10 | 1989-01 | 69/9/5 | 9 | -0.36% | 50.72% | -3.80%—+3.77% | -3.33% | +3.87% | **无法可靠判断**；极低 |
| 美国全市场 | 21 | 1989-01 | 69/9/5 | 9 | -0.14% | 53.62% | -6.88%—+5.00% | -5.00% | +6.46% | **无法可靠判断**；极低 |
| 美国全市场 | 63 | 1989-01 | 69/9/5 | 9 | -1.10% | 50.72% | -13.09%—+9.23% | -10.22% | +10.33% | **无法可靠判断；历史风险偏空**；低 |
| 美国全市场 | 126 | 1989-01 | 69/9/5 | 9 | -3.93% | 44.93% | -22.94%—+12.02% | -16.57% | +14.83% | **无法可靠判断；历史左尾偏大**；低 |
| 美国全市场 | 252 | 1989-01 | 69/9/5 | 6 | -1.52% | 55.07% | -24.00%—+19.75% | -21.11% | +20.55% | **无法可靠判断；时期不稳健**；极低 |
| Russell 2000 | 10 | 1987-09 | 72/10/6 | 10 | -0.37% | 48.61% | -4.61%—+5.18% | -3.84% | +5.33% | **无法可靠判断**；极低 |
| Russell 2000 | 21 | 1987-09 | 72/10/6 | 10 | -0.23% | 59.72% | -7.48%—+8.01% | -6.04% | +8.40% | **无法可靠判断**；极低 |
| Russell 2000 | 63 | 1987-09 | 72/10/6 | 10 | -0.28% | 50.00% | -16.34%—+12.28% | -11.70% | +14.69% | **无法可靠判断**；低 |
| Russell 2000 | 126 | 1987-09 | 72/10/6 | 10 | -2.42% | 44.44% | -27.50%—+23.21% | -19.15% | +23.21% | **无法可靠判断；双向尾部大**；低 |
| Russell 2000 | 252 | 1987-09 | 72/10/6 | 7 | +2.02% | 54.17% | -24.84%—+34.20% | -24.82% | +36.05% | **无法可靠判断；历史均值不再偏空**；极低 |
| SOX | 10 | 1994-05 | 60/7/4 | 7 | +0.13% | 51.67% | -9.74%—+10.45% | -8.08% | +12.90% | **无法可靠判断**；极低 |
| SOX | 21 | 1994-05 | 60/7/4 | 7 | -0.34% | 46.67% | -13.49%—+15.62% | -11.81% | +16.15% | **无法可靠判断**；极低 |
| SOX | 63 | 1994-05 | 60/7/4 | 7 | -3.49% | 43.33% | -30.79%—+22.39% | -21.82% | +28.46% | **无法可靠判断；历史风险偏空、挤仓尾部高**；低 |
| SOX | 126 | 1994-05 | 60/7/4 | 7 | -6.85% | 33.33% | -42.91%—+29.59% | -32.07% | +43.00% | **无法可靠判断；历史左尾最大**；低 |
| SOX | 252 | 1994-05 | 60/7/4 | 5 | -4.87% | 36.67% | -43.04%—+56.37% | -40.19% | +65.12% | **无法可靠判断；双向尾部极端且近年变号**；极低 |

### 10.3 当前方向矩阵

| 市场 | 10 日 | 21 日 | 63 日 | 126 日 | 252 日 |
|---|---|---|---|---|---|
| NDX | 无法可靠判断 | 无法可靠判断 | 无法可靠判断；历史风险偏空 | 无法可靠判断；历史风险偏空 | 无法可靠判断 |
| SPX | 无法可靠判断 | 无法可靠判断 | 无法可靠判断；历史风险偏空 | 无法可靠判断；历史风险偏空 | 无法可靠判断 |
| 美国全市场 | 无法可靠判断 | 无法可靠判断 | 无法可靠判断；历史风险偏空 | 无法可靠判断；历史风险偏空 | 无法可靠判断 |
| Russell 2000 | 无法可靠判断 | 无法可靠判断 | 无法可靠判断 | 无法可靠判断；历史左尾偏大 | 无法可靠判断 |
| SOX | 无法可靠判断 | 无法可靠判断 | 无法可靠判断；历史双向尾部高 | 无法可靠判断；历史风险偏空 | 无法可靠判断 |

**不得误读：** “历史风险偏空”只描述高聚合 SII 条件下的长样本分布，不代表本报告已经证明 2026-07-15 的相应指数处于可比高状态。只有 NDX 有当前成分回推线索，而且该线索缺少借贷确认、DTC 不极端、近邻方向混合。

## 十一、要把 MF010 升级为可交易研究，仍需什么

### 11.1 数据采购/接入顺序

1. **逐证券 short-interest 完整历史：** NYSE Group、Nasdaq 及其他上市市场的历史文件，保留原始 settlement、due、publication 字段；
2. **点时指数数据：** S&P DJI、Nasdaq、FTSE Russell 的成分、权重、生效日和行业分类；
3. **证券主表与退市：** CRSP/Compustat 或同等 point-in-time security master，保留 delisting return、并购换股和 ticker/CUSIP 变更；
4. **点时 float/shares：** 逐证券生效日字段，不能以今日 shares 回填；
5. **证券借贷：** S&P Global/EquiLend/DataLend 等至少一个稳定供应商，原样保留 coverage flag、fee、utilization、inventory、on-loan 和 recall；
6. **交易流量：** 合并 FINRA 与各交易所 short-volume 文件，但仍作为独立流量表；
7. **ETF/期货：** ETF SI、CFTC TFF/COT 和 CME open interest 独立建表，只做交互，不与成分股 SI 加总。

### 11.2 正式重跑的验收门槛

在给出“可交易方向”前，至少应满足：

- 每个事件的当时成分覆盖率 ≥90%，指数权重覆盖率 ≥95%；
- 退市/并购/换码证券覆盖率单列，不得静默删除；
- publication timestamp 可验证，且收益从下一可交易日开始；
- 每个市场、每个窗口至少报告原始快照、去簇事件、非重叠事件和独立周期；
- 当前值与历史分位必须使用同一供应商、同一 float/fee 定义；
- 等权、中位数、float-aggregate、点时市值权重、行业中性五种聚合方向一致性单列；
- short interest、loan pressure、short volume 若冲突，预测置信度自动降级；
- 10/21 日、63/126 日和 252 日分别建模，不共享一个外推系数。

## 十二、边界、偏差与最终判断

### 12.1 主要偏差

- **报告滞后：** 2026-07-15 的结算期在报告日仍未公开；当前真正可知的是 2026-06-30。
- **存量/流量混淆：** 高 short volume 不等于净空头增加；低 DTC 也不等于 short interest 低。
- **生存偏差：** NDX 24 期历史和 SPX 日度流量使用当前成分代理，会遗漏已退出、退市、并购和换码证券。
- **float 偏差：** NDX 当前只可近似 shares outstanding，不能声称已算 SI/free float。
- **供应商偏差：** fee/utilization/lendable/recall 的覆盖和定义随供应商变化，不能跨供应商直接排序。
- **指数构成偏差：** Russell 年度重构本身会机械改变 short interest；Nasdaq 也观察到指数加入/剔除会显著改变个股 SI（[Nasdaq Short-Selling Education](https://www.nasdaq.com/articles/what-you-should-know-about-short-selling)）。
- **事件稀少与重叠：** 126/252 日月度窗口高度重叠，去簇后五市场只有 7—10 个入口，独立周期只有 4—6 个。
- **机制不可唯一识别：** 聚合 SI 同时混合负面信息、做市、可转债/期权/ETF 对冲、指数套利和拥挤回补。
- **个股外推错误：** 少数 meme/squeeze 案例不能当作大盘或行业指数的事件样本。

### 12.2 最终研究判断

1. **历史上最值得保留的是 63—126 日风险信号，而不是 10 日或 252 日方向信号。** 连续回归在五市场方向一致，高状态的未来波动与回撤也系统性扩大。
2. **该信号不具备稳定的现代样本外推资格。** 剔除 2008 后明显衰减，2010 后 126/252 日多市场变号；学术复核也发现经济择时收益集中在少数时期。
3. **当前 NDX 只有“仓位高、广度扩张”的代理证据，没有“借贷稀缺、回补困难”的确认。** DTC 中性、top-decile 集中度低、QQQ SI 回落、short volume 高，构成冲突而非单向结论。
4. **SPX、美国全市场、Russell 2000 和 SOX 的当前成分股卖空状态不可恢复。** 使用 SPY/VTI/IWM/SOXQ 或 SPX 长样本替代，会违反存量/流量和直接证据/代理边界。
5. **因此本次所有 25 个当前方向输出均为“无法可靠判断”。** 可保留的行动信息只有：若后续拿到点时 SI + fee/utilization/supply，并确认 63—126 日共同拥挤状态，则应把下行回撤预算上调，同时为 NDX/SOX 的大幅上行回补尾部保留风险限额，不能只做单边空头配置。

## 十三、主要来源

### 监管与原始数据

- [FINRA Short Interest Reporting Schedule](https://www.finra.org/filing-reporting/regulatory-filing-systems/short-interest)
- [FINRA Rule 4560](https://www.finra.org/rules-guidance/rulebooks/finra-rules/4560)
- [FINRA Equity Short Interest](https://www.finra.org/finra-data/browse-catalog/equity-short-interest)
- [FINRA Short-Interest Glossary](https://www.finra.org/finra-data/browse-catalog/equity-short-interest/glossary)
- [FINRA Daily Short Sale Volume](https://www.finra.org/finra-data/daily-short-sale-volume-transaction-data)
- [FINRA Understanding Short Sale Volume Data](https://www.finra.org/rules-guidance/notices/information-notice-051019)
- [Nasdaq 2026-06-30 Short Interest Release](https://www.nasdaq.com/press-release/nasdaq-announces-end-month-open-short-interest-positions-nasdaq-stocks-settlement-5)
- [Nasdaq Short Interest Report](https://www.nasdaq.com/solutions/data/equities/short-interest)
- [NYSE Group Short Interest](https://beta.nyse.com/data-products/catalog/nyse-group-short-interest)
- [SEC Rule 13f-2 / Rule 10c-1a Extension Order](https://www.sec.gov/files/rules/exorders/2025/34-104303.pdf)
- [SEC Rule 10c-1a Final Rule](https://www.sec.gov/files/rules/final/2023/34-98737.pdf)
- [SEC Rule 13f-2 / Form SHO Final Rule](https://www.sec.gov/files/rules/final/2023/34-98738.pdf)
- [CFTC Commitments of Traders](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)

### 指数、借贷与方法

- [Nasdaq-100 Methodology](https://indexes.nasdaqomx.com/docs/methodology_NDX.pdf)
- [SOX Methodology](https://indexes.nasdaqomx.com/docs/methodology_SOX.pdf)
- [S&P 500 Index Overview](https://www.spglobal.com/spdji/en/indices/equity/sp-500/)
- [S&P Global Securities Finance](https://www.spglobal.com/market-intelligence/en/solutions/products/securities-finance)

### 原始论文

- [Rapach, Ringgenberg and Zhou — Short Interest and Aggregate Stock Returns](https://down.aefweb.net/WorkingPapers/w716.pdf)
- [Goyal, Welch and Zafirov — A Comprehensive Look at The Empirical Performance of Equity Premium Prediction II](https://academic.oup.com/rfs/article/37/11/3490/7749383)
- [Gorbenko — The Predictive Power of Global Short Interest](https://academic.oup.com/raps/article/13/4/691/7127046)
- [Priestley — Short Interest, Macroeconomic Variables and Aggregate Stock Returns](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3384620)
- [Hong et al. — Days to Cover and Stock Returns](https://www.nber.org/system/files/working_papers/w21166/w21166.pdf)
- [Cohen, Diether and Malloy — Supply and Demand Shifts in the Shorting Market](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID2758846_code353319.pdf?abstractid=672381)
- [Engelberg, Reed and Ringgenberg — Short-Selling Risk](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2312625)
- [How Prevalent Are Short Squeezes?](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4526147)
- [ETF Short Interest and Returns](https://academic.oup.com/rfs/article-pdf/34/3/1280/36264603/hhaa077.pdf)

---

**报告纪律：** 本报告没有把 2026-07-15 尚未公开的结算期估算成已知事实，没有把 FINRA short volume 当作净空头，没有把 ETF/期货仓位与成分股 SI 混合，也没有用价格趋势、期权、新闻或盈利给当前方向定向。
