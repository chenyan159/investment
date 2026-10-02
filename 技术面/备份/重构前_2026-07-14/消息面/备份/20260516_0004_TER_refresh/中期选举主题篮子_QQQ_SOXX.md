# 川普/中期选举主题篮子回测与 QQQ、SOXX 展望


## 2026-05-15 全面更新：中期选举/政治主题

### 对原结论的修正

1. 5/15 市场主导因素不是中期选举概率本身，而是 CPI、利率和半导体拥挤交易。中期选举主题仍是二阶变量。
2. 但政治变量会放大半导体波动：出口管制、对华销售许可、关税、能源和国防采购都可能在行政层面继续影响 SOXX。
3. 当前应把“选举主题篮子”用于风险归因，而不是直接择时 QQQ/SOXX。

### 当前使用方式

- 若政策新闻偏向出口管制放松，SOXX 可能修复快于 QQQ。
- 若关税/对华科技限制重新升级，SOXX 应继续比 QQQ 承压。
- 中期选举概率只有在改变行政政策可信度时，才会成为主导变量。


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

截至：2026-05-10 美国西岸晚间  
市场价格数据截至：2026-05-08 收盘  
结论属性：研究备忘录，非投资建议

## 1. 一页结论

当前最重要的矛盾不是“川普交易是否存在”，而是三组力量互相抵消：

1. **政治环境对共和党不利，降低了完整川普政策包继续扩张的概率。** Polymarket 在 2026-05-10 9:20 PM ET 更新的页面显示，民主党拿下众议院概率约 **79%**，共和党保住参议院概率约 **54%**。这更接近“民主党众议院 + 共和党参议院”的分裂国会，而不是共和党继续全控。
2. **行政权仍足以影响关税、出口管制、国防、能源和半导体供应链。** 即使国会分裂，白宫仍可通过 Section 232、USTR、BIS、采购和行政命令改变行业相对收益。
3. **AI capex 周期压过了大部分传统政治因子。** 本地历史研究显示，2026-2027 美国 AI 数据中心建设和半导体上游仍处在强订单周期；这解释了为什么 SOXX 对“关税/中期选举”的常规负面解释并不充分。

对 QQQ 和 SOXX 的判断：

| 标的 | 未来 1-2 个月 | 6-12 个月基准判断 | 核心风险 |
| --- | --- | --- | --- |
| QQQ | 已明显超买，倾向震荡或回撤消化，回撤区间可用 -5% 到 -10% 作为压力测试 | 若 AI capex 不被下修、利率不再上行，仍有上行，但斜率大概率低于 4-5 月反弹 | CPI 再抬头、10Y 利率上行、Mag7 盈利兑现不及预期、关税推高成本 |
| SOXX | 比 QQQ 更强也更拥挤，短线回撤弹性可达 -10% 到 -20% | 基本面强于 QQQ，但赔率已经前置；更适合等待波动后的二次确认 | HBM/CoWoS/Rubin 交付摩擦、AI capex ROI 质疑、对中出口和半导体关税反复 |

基准路径：**QQQ 仍是“结构性多头、战术性过热”；SOXX 是“基本面更强、位置更危险”。** 如果 2026 夏季 CPI、Fed、关税和 hyperscaler capex 没有负面共振，回撤后仍应优先看多 SOXX 相对 QQQ；但如果出现利率上行 + AI capex 下修，SOXX 的下跌 beta 会显著大于 QQQ。

## 2. 当前市场与政治状态

### 2.1 选情与赔率

- Polymarket 2026 中期选举页在 2026-05-10 更新：共和党控制参议院约 **54%**，民主党控制众议院约 **79%**；页面同时给出 35 个参议院席位和全部 435 个众议院席位改选。
- Kalshi 在 2026-03-14 的市场解读中，曾显示民主党拿下众议院 **84%**、参议院民主党 **51%**，之后 Polymarket 的参议院价格回到共和党略占优。结论是：**众议院翻蓝是主线，参议院仍接近五五开。**
- Pew Research 2026-04-20 至 2026-04-26 调查显示，Trump job approval 为 **34%**，为其第二任期低点；USPollingData 2026-05-09 聚合页则显示 generic ballot 为 **D+5.7**、Trump approval 约 **39%**。不同口径绝对值不同，但方向一致：政治环境对共和党不利。

市场含义：如果“民主党众议院 + 共和党参议院”成为基准，传统川普交易中的能源、银行、国防、小盘价值会失去一部分立法层面的想象空间；但关税、出口管制、国防采购和能源行政政策仍会保留。

### 2.2 宏观约束

- Fed 2026-03-18 FOMC 维持联邦基金目标区间在 **3.50%-3.75%**，并强调通胀仍偏高、会根据数据调整政策。
- BLS 2026-04-10 发布的 2026 年 3 月 CPI 显示：headline CPI **+0.9% MoM / +3.3% YoY**，core CPI **+0.2% MoM / +2.6% YoY**。能源是主要上行来源。
- 下一份 CPI 是 2026-05-12。对 QQQ/SOXX 来说，5 月中旬 CPI 比中期选举赔率更容易触发短期波动。

### 2.3 政策约束

白宫 2026-01 半导体相关 proclamation 的关键点是：对 covered semiconductor products 设置 **25% ad valorem duty**，但对美国数据中心、研发、维修替换、初创企业、非数据中心消费应用、公共部门等用途设置豁免；并要求 2026-07-01 前更新美国数据中心半导体市场情况，以决定是否调整关税。

这对 SOXX 是“双刃剑”：

- 正面：数据中心用途豁免降低了 AI 服务器/加速器进口成本冲击，强化美国 AI 建设优先级。
- 负面：对中国、全球供应链和非豁免半导体产品的政策不确定性仍会提高估值折价。

## 3. 当前价格、估值与技术状态

| 指标 | QQQ | SOXX |
| --- | ---: | ---: |
| 2026-05-08 收盘价 | 711.23 | 520.30 |
| 2026 YTD 回报（按日线复权价计算） | +15.9% | +72.9% |
| 近 1 个月 | +17.4% | +40.5% |
| 近 3 个月 | +16.8% | +49.4% |
| 相对 20 日均线 | +7.6% | +16.6% |
| 相对 50 日均线 | +14.6% | +35.8% |
| 相对 200 日均线 | +17.3% | +64.9% |
| RSI(14) | 82.8 | 78.0 |
| 20 日年化波动率 | 15.6% | 39.3% |

解释：

- QQQ 的强势已经进入超买区，但波动率还没有失控，说明更像趋势延伸后的估值消化，而不是恐慌性挤空。
- SOXX 的状态更极端：近 1 个月 +40% 以上、相对 200 日均线 +65% 左右。基本面强可以解释方向，但很难解释直线斜率。短线更容易被 CPI、关税、财报 guidance 或仓位止盈触发高 beta 回撤。

基金结构上：

- Invesco QQQ 2026-03-31 fact sheet 显示，QQQ 技术权重约 **59.8%**，前十大包括 NVIDIA、Apple、Microsoft、Amazon、Tesla、Meta、Alphabet、Broadcom 等。
- iShares SOXX 2026-03-31 fact sheet 显示，SOXX P/E 约 **42.29x**、3 年 beta **1.58**，前十大中 NVIDIA、Broadcom、Micron、AMD、Applied Materials、Marvell、Intel、KLA、MPWR、Teradyne 合计约 **57.42%**。

## 4. 主题篮子回测框架

### 4.1 篮子定义

受益篮子采用 5 个等权袖珍组合：

| 袖珍组合 | ETF 代理 |
| --- | --- |
| 国防 | ITA、XAR |
| 能源 | XLE |
| 银行 | XLF、KBE、KRE |
| 美国本土制造 | XLI |
| 小盘价值 | IWN、VBR |

受损篮子采用 4 个等权袖珍组合：

| 袖珍组合 | ETF 代理 |
| --- | --- |
| 高进口成本零售 | XRT |
| 全球供应链科技 | QQQ、XLK |
| 对中/全球周期敏感半导体 | SOXX、SMH |
| 长久期成长股 | VUG、ARKK |

价格数据：Yahoo Finance chart API 日线复权价格。  
窗口：事件日收盘后 5、20、60 个交易日表现。

### 4.2 核心事件结果

| 事件 | 20 日受益篮子 | 20 日受损篮子 | 受益-受损 | QQQ 20 日 | SOXX 20 日 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2016 Trump 胜选 | +14.1% | +5.5% | +8.6pct | +1.1% | +7.4% |
| 2018 中期选举 | -5.4% | -3.9% | -1.5pct | -2.0% | -2.9% |
| 2020 大选 | +17.6% | +14.9% | +2.7pct | +10.6% | +18.1% |
| 2024 Trump 胜选 | +6.5% | +8.2% | -1.6pct | +6.3% | +0.4% |
| 2018 Section 301 关税宣布 | +3.9% | -1.8% | +5.6pct | -0.3% | -7.3% |
| 2019 关税升级冲击 | -7.0% | -13.0% | +6.1pct | -11.0% | -17.1% |
| 2025 中国 100% 关税/软件出口冲击 | +2.2% | +2.0% | +0.2pct | +3.4% | +8.2% |
| 2026 半导体关税公告 | +3.3% | -3.5% | +6.7pct | -3.1% | +5.9% |

### 4.3 回测读法

1. **2016 的“川普胜选交易”最清晰。** 国防、能源、银行、小盘价值显著跑赢成长科技，20 个交易日受益篮子跑赢受损篮子约 8.6pct。
2. **2018 中期选举不是单纯政治事件。** 当时处在贸易战、Fed 收紧和成长股估值压力中，事件窗口里两边都弱，主题篮子方向不稳定。
3. **2024 川普胜选后，传统受益篮子没有持续跑赢成长。** 这说明 2024-2026 的主导变量已经不是简单“共和党胜选 = 价值/能源/银行赢”，而是 AI capex、利率和半导体供应链。
4. **关税冲击对半导体和成长的负面在 2018-2019 很明显。** 但 2025-2026 的半导体表现不同，因为 AI 数据中心需求、半导体豁免、国产化补贴和供应链锁单抵消了传统关税负面。

## 5. 对 QQQ 的推演

### 基准情景：震荡消化后继续上行

条件：

- 2026-05-12 CPI 没有明显超预期；
- Fed 保持 2026 下半年降息或至少不再转鹰的可能性；
- Microsoft、Amazon、Alphabet、Meta、Oracle 的 2026/2027 capex 没有下修；
- Polymarket 维持“民主党众议院 + 共和党参议院”附近，市场把它理解为政策约束和财政冲动降温。

对应判断：

- QQQ 可能先围绕 20 日均线回归，短线 -5% 至 -10% 都属于健康消化；
- 6-12 个月仍可看正收益，但不应外推 4-5 月的单边斜率；
- 如果民主党拿下众议院概率继续上升，QQQ 未必受损，反而可能因为“完整关税/财政刺激政策受限”而获得估值支撑。

### 熊市情景：利率 + capex 双杀

触发器：

- CPI 连续高于预期，10Y 利率上行；
- hyperscaler 明确下修 capex 或强调 AI ROI/折旧压力；
- 对中出口管制或半导体关税升级，且豁免范围收窄；
- QQQ 前十大权重股 earnings revision 下修。

对应判断：QQQ 的合理压力测试为 -12% 至 -20%。如果只是 CPI 单点扰动但 capex 不下修，更像买点；如果 capex 同时下修，就不是普通回调。

## 6. 对 SOXX 的推演

### 基准情景：强基本面，先等波动释放

本地 AI 产业链研究对 SOXX 仍偏正面：

- 2026 全球 AI 计算芯片/模块产能释放金额的务实区间约 **$300B-$360B**，2027 务实区间约 **$430B-$520B**。
- 美国 AI 数据中心建设规模 2026 务实区间约 **$400B-$490B**，2027 务实区间约 **$520B-$650B**。
- 半导体上游 2026 订单务实区间 **$280B-$430B**，2027 为 **$400B-$650B**，增速约 **40%-55%**。

这说明 SOXX 的上涨不是纯赔率或政策叙事，而有订单支撑。但位置已经很高：

- SOXX 2026 YTD 约 +72.9%；
- 近 1 个月约 +40.5%；
- 相对 50 日均线 +35.8%，相对 200 日均线 +64.9%。

结论：**中期仍强，短线不追。** 更合理的策略是等以下至少一个信号确认：

- 回撤到 20 日/50 日均线附近但没有破坏高阶趋势；
- NVIDIA/AMD/Broadcom/Micron/AMAT/KLA/TER 的订单和毛利率继续上修；
- 2026-07-01 半导体关税更新没有收窄数据中心豁免；
- SOXX 内部涨幅从少数 memory/AI beta 扩散到设备、测试、模拟/电源、封装。

### 熊市情景：SOXX 跌幅会显著大于 QQQ

SOXX 的风险不是“AI 没需求”，而是：

- 市场开始质疑 2027 capex ROI；
- HBM/CoWoS/Rubin 交付节奏让收入确认后移；
- 关税或出口管制把中国收入和全球供应链折价放大；
- 高估值 + 高仓位导致任何坏消息被放大。

在这些条件下，SOXX 的压力测试应大于 QQQ，短中期 -25% 至 -40% 并不极端。

## 7. 未来跟踪指标

| 指标 | 偏多信号 | 偏空信号 |
| --- | --- | --- |
| 中期选举赔率 | 民主党众议院高概率、参议院仍分裂，政策极端化受限 | 共和党保住两院概率快速上升，市场重估关税/财政/通胀风险 |
| Trump approval/generic ballot | approval 稳住、D+ 收敛，政策不确定性下降 | approval 继续下探，政策讲话更激进以动员基本盘 |
| CPI/Fed | core CPI 温和，Fed 维持降息选项 | headline/core 同时超预期，10Y 上行，成长股估值承压 |
| 半导体政策 | 数据中心豁免维持，关税 offset 支持美国制造 | 豁免收窄，对中出口限制升级 |
| AI capex | MSFT/AMZN/GOOGL/META/ORCL 上修 2026/2027 capex | 管理层强调折旧、ROI、租金压力或延迟项目 |
| SOXX 内部结构 | 设备、测试、封装、内存、ASIC 共同上涨 | 只剩少数动量股拉指数，广度恶化 |

## 8. 最终判断

中期选举赔率本身不是 QQQ/SOXX 的决定性变量。它更像一个**政策风险调节器**：

- 民主党拿下众议院概率高，会削弱完整川普交易中的能源、银行、小盘价值和再通胀因子；
- 但它未必伤害 QQQ，反而可能降低财政和关税失控预期；
- SOXX 的决定变量仍是 AI capex、HBM/CoWoS、Blackwell/Rubin、ASIC 和数据中心半导体豁免。

因此，未来更可能出现的是：

1. **QQQ：高位震荡后缓慢上行。** 除非 CPI 和 AI capex 同时转坏，否则不轻易判断顶部。
2. **SOXX：长期更强，短期更危险。** 位置过热，不适合用线性外推；但若回撤不破坏订单逻辑，仍是比 QQQ 更高 beta 的 AI 主线资产。
3. **主题篮子：2026 不能照搬 2016。** 2016 的受益篮子跑赢很清晰；2024-2026 的主导变量已经转向 AI 资本开支和供应链瓶颈。川普政策会改变相对收益，但不再单独决定科技和半导体方向。

## 9. 资料来源

外部资料：

- Polymarket 2026 Midterms odds, updated 2026-05-10: https://polymarket.com/predictions/midterms
- Polymarket Midterms live markets: https://polymarket.com/midterms
- Kalshi 2026 Senate/House odds commentary: https://news.kalshi.com/p/2026-senate-odds-democrats-now-favored
- Pew Research Center, Trump approval survey, 2026-05-01: https://www.pewresearch.org/wp-content/uploads/sites/20/2026/05/PP_2026.5.1_Trump-approval_report.pdf
- USPollingData 2026 polls dashboard: https://uspollingdata.com/polls/
- Federal Reserve FOMC statement, 2026-03-18: https://www.federalreserve.gov/newsevents/pressreleases/monetary20260318a.htm
- BLS CPI release, March 2026: https://www.bls.gov/news.release/cpi.htm
- White House semiconductor tariff proclamation, 2026-01: https://www.whitehouse.gov/presidential-actions/2026/01/adjusting-imports-of-semiconductors-semiconductor-manufacturing-equipment-and-their-derivative-products-into-the-united-states/
- USTR 2026 Trade Policy Agenda: https://ustr.gov/sites/default/files/files/Press/Releases/2026/2026%20Trade%20Policy%20Agenda.pdf
- Invesco QQQ fact sheet: https://www.invesco.com/us-rest/contentdetail?contentId=841e411c-a1eb-4541-8cb8-0fa603abea81&dnsName=us
- iShares SOXX fund page: https://www.ishares.com/us/products/239705/fund
- iShares SOXX fact sheet: https://www.ishares.com/us/literature/fact-sheet/soxx-ishares-semiconductor-etf-fund-fact-sheet-en-us.pdf
- QQQ 2026-05-08 close cross-check: https://www.financecharts.com/etfs/QQQ/summary/price

本地历史研究底稿：

- `D:\drive\Investment\工作台v5\AI产业和股票研究结果\AI数据中心建设规模与产业链订单映射_2026-2027_美国.md`
- `D:\drive\Investment\工作台v5\AI产业和股票研究结果\AI头部芯片市场占比和规模.md`
- `D:\drive\Investment\工作台v5\AI产业和股票研究结果\conference_update\nvidia_gtc_2026_research.md`
