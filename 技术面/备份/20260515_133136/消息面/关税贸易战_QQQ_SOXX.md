# 川普/中期选举与关税/贸易战事件研究：QQQ 与 SOXX 走向

研究日期：2026-05-11  
市场数据截至：2026-05-08 美股收盘，因 2026-05-10 为周末，没有新的美股收盘价。  
用途：研究和交易框架，不构成投资建议。

## 结论摘要

基准判断：QQQ 中期仍偏强，但当前位置已经贴近 52 周高位，未来 1-3 个月更像“高位震荡 + 事件驱动”的结构；SOXX 的趋势更强，但对关税、出口管制、半导体供应链扰动和获利了结更敏感，短线风险收益比弱于 QQQ。

最重要的历史规律是：2018-2019 年贸易战中，关税升级事件对 SOXX 的 5-20 个交易日冲击明显大于 QQQ。按调整后收盘价计算，9 个关税升级/公告事件后，QQQ 后 5 日平均收益约 -0.3%，SOXX 约 -2.0%；后 20 日 QQQ 约 -0.1%，SOXX 约 -3.1%。这说明半导体链条不是简单跟随大盘，而是会放大贸易政策冲击。

当前政策环境比 2018-2019 年更复杂：一方面，AI 算力、数据中心和本土化制造支撑半导体需求；另一方面，2026 年已经出现临时 10% 进口附加税、先进计算芯片 25% 关税、钢铝铜 Section 232 强化，以及对更广泛半导体和衍生品关税的潜在预期。政治上，2026 年 11 月中期选举前，政府有动力维持强硬贸易姿态，但如果股市、通胀或消费者成本反应过强，也有动力通过豁免、延后、谈判框架来降温。

我的情景判断：

| 情景 | 触发条件 | QQQ 6-12 个月倾向 | SOXX 6-12 个月倾向 |
| --- | --- | --- | --- |
| 基准：强硬但可控 | 关税保持选择性，关键消费电子/USMCA/本土建设相关豁免延续；AI 盈利继续兑现 | 震荡上行，回撤后更容易修复 | 高波动上行，但短期需要消化过热 |
| 上行：贸易缓和 + AI 加速 | Section 122 附加税提前终止或不延长；半导体关税有清晰豁免；中国反制有限 | 估值扩张，可能继续创新高 | 高 beta 反弹，可能显著跑赢 QQQ |
| 下行：广泛半导体/中国反制 | Section 232 半导体扩围、豁免收窄，或中国在稀土/市场准入/采购端反制 | 可能出现 8%-15% 级别回撤 | 可能出现 15%-25% 级别回撤，且弱于 QQQ |

操作含义：如果只看关税/贸易战因子，QQQ 比 SOXX 更适合作为核心持仓，SOXX 更适合作为在政策缓和或 AI 订单确认后的卫星仓位。若未来出现新的“半导体广泛关税公告日”，应默认 SOXX 的第一反应更脆弱；若出现“延后/豁免/框架协议”类缓和事件，SOXX 的反弹弹性也更大。

## 研究设计

研究问题：在特朗普第二任期和 2026 年中期选举背景下，关税/贸易战事件会如何影响 QQQ 与 SOXX？

核心假设：

- 关税升级首先压缩估值倍数，其次影响毛利率、供应链成本、海外收入折现和库存周期。
- 半导体链条因台湾、中国、韩国、荷兰、墨西哥等跨境环节更长，对政策冲击的 beta 高于 QQQ。
- QQQ 受影响但更分散，软件、互联网、零售、医疗等权重能缓冲一部分冲击。
- 中期选举前，政策噪音可能升高，但市场也可能提前交易“政策结果明朗化”。

事件分类：

- 公告/升级：新关税清单、税率上调、覆盖范围扩大、反制升级。
- 缓和：延后生效、豁免、谈判框架、第一阶段协议。
- 事件窗口：T+1、T+5、T+20 个交易日，使用调整后收盘价 close-to-close。

样本：

- ETF：QQQ、SOXX、SPY。
- 受影响公司样本：AAPL、TSLA、NVDA、AMD、MU、QCOM、AVGO、AMAT、LRCX、KLAC、TSM、ASML。
- 注意：公司样本是“当前核心暴露代表”，不是 2018 年成分股权重复原，因此更适合做敏感度参考，而不是严格组合回测。

## 2018-2019 年贸易战关键时间线与 ETF 回测

数据来源：Yahoo Finance chart API 调整后收盘价，下载于 2026-05-11。事件日期若发生在非交易时段，使用当日或下一交易日收盘作为 T0。

| 日期 | 类型 | 事件 | QQQ +1D | QQQ +5D | QQQ +20D | SOXX +1D | SOXX +5D | SOXX +20D |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2018-03-22 | 升级 | Trump 宣布 Section 301 对华关税计划 | -2.6% | -1.6% | -0.3% | -3.3% | -3.0% | -7.3% |
| 2018-04-03 | 升级 | USTR 公布约 500 亿美元中国商品拟征税清单 | +1.6% | +2.5% | +3.5% | +1.3% | +1.0% | -2.8% |
| 2018-06-15 | 升级 | USTR 确认约 500 亿美元中国商品 25% 关税，首批 7/6 生效 | -0.1% | -0.7% | +1.5% | -1.0% | -3.6% | -5.6% |
| 2018-07-10 | 升级 | USTR 拟对约 2000 亿美元中国商品加征 10% 关税 | -0.5% | +1.7% | +2.5% | -2.6% | -1.0% | +2.1% |
| 2018-09-18 | 升级 | USTR 敲定 2000 亿美元清单，9/24 起 10%，计划 2019/1/1 升至 25% | -0.1% | +0.9% | -2.9% | +0.2% | -0.2% | -6.3% |
| 2018-12-03 | 缓和 | G20 后首个交易日，90 天停火，暂缓升税 | -3.8% | -5.1% | -12.8% | -4.8% | -7.0% | -13.7% |
| 2019-05-06 | 升级 | 5/5 周日推文威胁 2000 亿美元清单从 10% 升到 25% | -1.9% | -6.0% | -7.9% | -2.5% | -8.7% | -12.1% |
| 2019-05-10 | 升级 | USTR 宣布 2000 亿美元清单正式从 10% 升至 25% | -3.5% | -1.1% | -1.0% | -4.7% | -5.2% | -4.3% |
| 2019-08-01 | 升级 | 对剩余约 3000 亿美元中国商品征税计划 | -1.5% | -1.0% | -1.2% | -1.5% | -1.3% | -0.8% |
| 2019-08-13 | 缓和 | USTR 推迟部分消费电子/节日购物相关清单至 12/15 | -3.0% | -0.8% | +2.1% | -3.1% | +0.8% | +8.0% |
| 2019-08-23 | 升级 | 中方反制后，USTR 宣布现有关税再上调 5 个百分点 | +1.5% | +3.0% | +4.8% | +0.8% | +4.0% | +9.4% |
| 2019-09-11 | 缓和 | 美方推迟 10/1 升税；中方部分豁免 | +0.4% | +0.0% | -2.5% | +0.2% | -0.2% | -4.0% |
| 2019-10-11 | 缓和 | 第一阶段协议框架，美方暂缓 10/15 升税 | -0.0% | +0.3% | +5.3% | -0.0% | -0.2% | +9.1% |
| 2019-12-13 | 缓和 | USTR 宣布达成第一阶段协议，取消/下调部分关税 | +1.0% | +2.2% | +6.5% | +1.0% | +3.1% | +5.4% |

统计摘要：

| 事件组 | QQQ +5D 平均 | QQQ +20D 平均 | SOXX +5D 平均 | SOXX +20D 平均 |
| --- | ---: | ---: | ---: | ---: |
| 升级/公告，9 次 | -0.3% | -0.1% | -2.0% | -3.1% |
| 缓和，5 次 | -0.7% | -0.3% | -0.7% | +1.0% |

解释：

- SOXX 在升级事件后的平均表现更差，尤其是 2019 年 5 月，从“威胁升税”到“正式升税”的窗口里，SOXX 连续跑输。
- 缓和事件并不总是立刻上涨。2018-12-03 的 G20 停火反而落在美股流动性和增长担忧较重的阶段，因此 20 日表现很差。结论不能简化成“缓和必涨”，而是“缓和给半导体估值修复机会，但宏观环境必须配合”。
- 2019-12-13 第一阶段协议是更典型的正向缓和：QQQ 和 SOXX 后 20 日分别上涨约 6.5% 和 5.4%。

## 受影响公司样本敏感度

下表为 2018-2019 事件窗口内，当前代表性公司样本的平均 +5D 表现。它反映“如果今天的主流持仓暴露在类似贸易战新闻流中，哪些类型更敏感”。

| 标的 | 暴露类型 | 升级 +5D 平均 | 升级相对 SPY | 缓和 +5D 平均 | 缓和相对 SPY |
| --- | --- | ---: | ---: | ---: | ---: |
| QQQ | Nasdaq-100 ETF | -0.3% | -0.1% | -0.7% | +0.1% |
| SOXX | 半导体 ETF | -2.0% | -1.9% | -0.7% | +0.1% |
| AAPL | 中国组装/消费硬件 | -1.3% | -1.2% | -1.4% | -0.6% |
| TSLA | 中国/墨西哥/汽车链 | -1.7% | -1.6% | +2.8% | +3.5% |
| NVDA | AI 芯片/海外收入高 | -3.3% | -3.1% | +0.3% | +1.1% |
| AMD | AI 芯片/海外收入高 | +1.3% | +1.4% | -1.3% | -0.5% |
| MU | 存储/周期半导体 | -3.4% | -3.3% | -1.6% | -0.8% |
| QCOM | 手机链/中国收入敏感 | -0.9% | -0.8% | +0.9% | +1.7% |
| AVGO | 半导体/网络芯片 | -3.3% | -3.2% | +0.3% | +1.1% |
| AMAT | 半导体设备 | -0.8% | -0.6% | -2.0% | -1.2% |
| LRCX | 半导体设备 | -1.6% | -1.5% | -1.5% | -0.7% |
| KLAC | 半导体设备 | -2.2% | -2.1% | +0.8% | +1.6% |
| TSM | 台湾晶圆代工 ADR | -0.8% | -0.7% | -0.7% | +0.1% |
| ASML | 荷兰光刻设备 ADR | -0.0% | +0.1% | -2.0% | -1.3% |

读法：

- NVDA、MU、AVGO、KLAC 对升级事件的负面 beta 较高；这与半导体链条跨境依赖、海外收入、估值弹性有关。
- AAPL 的负面反应更稳定，符合中国组装和消费硬件进口风险。
- AMD 在 2018-2019 样本中没有表现出负 beta，主要因为当时 AMD 自身产品周期和份额提升强，说明个股 alpha 可以覆盖宏观政策 beta。
- 设备股不完全同向：AMAT、LRCX、KLAC 都受半导体资本开支预期影响，但不同公司在事件窗口里的表现差异较大。

## 当前政策背景，截至 2026-05-11

1. 临时 10% 进口附加税仍是总量风险。白宫 2026-02-20 公告依据 Trade Act Section 122，对进口商品征收 10% ad valorem surcharge，生效时间为 2026-02-24 至 2026-07-24，除非提前暂停、修改、终止，或由国会延长。该政策包含豁免，并且不与 Section 232 关税重复叠加。

2. 半导体进入 Section 232 政策主线。白宫 2026-01-14 公告称，特朗普签署 Section 232 Proclamation，针对半导体、半导体制造设备及衍生品的进口国家安全风险，并对部分先进计算芯片，如 NVIDIA H200、AMD MI325X，征收 25% 关税；同时保留未来扩大到更广泛半导体和衍生品关税的可能。

3. 中国 Section 301 框架没有消失。USTR 2024 年四年复审认为，中国相关技术转让、网络窃取和产业政策问题仍然存在，并表示关税有助于降低对中国进口的依赖、推动供应链多元化。这说明 2018-2019 的政策工具箱仍在，只是从“消费品/工业品清单”扩展到“关键技术/供应链安全”。

4. 钢、铝、铜关税会通过数据中心和制造资本开支传导。白宫 2026-04-02 公告强化 Section 232 金属关税，钢铝铜主体产品可达 50%，衍生品 25%，部分工业/电网设备 15% 至 2027 年。这对数据中心、电网、制造厂房建设成本构成压力，但也可能利好美国本土产能建设相关订单。

5. 中期选举使政策节奏更不稳定。BlackRock 的 2026 春季展望指出，中期选举年历史上收益更低、波动更高，但临近投票和结果明朗后，市场往往有修复倾向。对 2026 年而言，关税是政治叙事工具，也是通胀和股市风险源，因此政策可能呈现“强硬表态 + 定向豁免/交易”的组合。

## 与前序历史研究的合并判断

这份关税/贸易战研究与当前目录里的前序研究结论基本一致，但补充了“半导体链条对贸易政策事件更高 beta”的证据。

| 前序研究 | 核心结论 | 与本报告的合并含义 |
| --- | --- | --- |
| `tmp/midterm_cycle_qqq_soxx_research.md` | 2002 年以来 QQQ、SOXX 在中期选举日至后 12 个月样本中全部为正，但当前 2026 年不是低位修复，而是高位动量 | 中期选举本身不是看空理由；真正问题是选前政策不确定性与当前位置过热 |
| `政策不确定性冲击_QQQ_SOXX.md` | 政策不确定性冲击当月 SOXX 明显弱于 QQQ/SPY；若 VIX 没有同步上升，冲击后常出现修复 | 关税新闻若只停留在标题风险，可能被 AI 盈利吸收；若 VIX 上穿 22-25，应优先降低 SOXX beta |
| `通胀事件回测_QQQ_SOXX.md` 与 `tmp/inflation_regime_backtest_QQQ_SOXX_2026-05-10.md` | hot core CPI/PCE 会压低 1-5 日收益、加深回撤；持续通胀上行会显著降低 QQQ/SOXX 的 3-6 个月赔率 | 关税最危险的传导不是关税本身，而是“关税 -> 核心通胀/长端利率 -> 成长估值压缩” |
| `美联储政策意外_QQQ_SOXX.md` | 市场突然转鹰时 SOXX 比 QQQ 更敏感；转鸽且可信时成长和半导体修复更强 | 关税若推高通胀并导致 Fed 路径转鹰，SOXX 会承受贸易和利率双重压力 |
| `中期选举主题篮子_QQQ_SOXX.md` | 2024-2026 的主导变量已从传统川普交易转向 AI capex、半导体供应链和行政政策 | 关税负面不能单独决定 SOXX 方向；AI 数据中心、芯片订单和半导体豁免是抵消关税风险的关键 |

合并后的主线：

- QQQ 是“AI/平台科技盈利 + 利率路径 + 政策风险溢价”的组合，当前更适合核心持有和回撤承接。
- SOXX 是“AI 半导体订单 + 高 beta + 关税/出口管制敏感度”的组合，长期弹性更高，但需要更严格的仓位和触发器管理。
- 关税事件如果没有伴随 VIX 上行、核心通胀超预期、长端利率上行或 AI capex 下修，历史上容易被市场消化；如果这些变量共振，SOXX 的回撤应按 QQQ 的 1.5-2 倍压力测试。

## QQQ 当前暴露

QQQ 跟踪 Nasdaq-100，核心特征是大盘成长、AI、云、消费互联网、硬件和半导体混合暴露。Invesco 2026-03-31 数据显示，QQQ 前十大持仓为：

| 持仓 | 权重 |
| --- | ---: |
| NVIDIA | 8.67% |
| Apple | 7.62% |
| Microsoft | 5.62% |
| Amazon | 4.58% |
| Tesla | 3.80% |
| Meta Platforms A | 3.45% |
| Walmart | 3.43% |
| Alphabet A | 3.43% |
| Alphabet C | 3.19% |
| Broadcom | 3.00% |

行业权重大致为：科技 59.8%、可选消费 21.2%、医疗 5.1%、电信 3.8%、工业 3.7%。这意味着 QQQ 并不是纯半导体 ETF，但前十大里 NVDA、AAPL、AVGO、TSLA 的关税/供应链敏感度都不低。

市场位置：按 Yahoo Finance chart API 计算，QQQ 2026-05-08 价格约 711 美元，接近 52 周高位；2026 年初至 2026-05-08 约 +15.9%，过去一年约 +46.4%。这不是低位修复阶段，而是动量强、估值容错较低的阶段。

对 QQQ 的判断：

- 正面因素：AI 盈利兑现、大盘成长盈利质量、可能的降息预期、龙头流动性。
- 负面因素：关税推升成本和通胀预期、硬件供应链扰动、监管/出口限制、持仓集中度高。
- 结论：QQQ 对关税冲击有缓冲，但若半导体/中国供应链冲击扩散，QQQ 很难独立上涨。更合理的路径是高位震荡，等盈利和政策明朗化后再选择方向。

## SOXX 当前暴露

iShares 2026-05-07 持仓数据显示，SOXX 是 30 只股票的集中半导体组合。前十大约为：

| 持仓 | 权重 |
| --- | ---: |
| Micron | 8.94% |
| AMD | 8.67% |
| Broadcom | 7.36% |
| Intel | 6.85% |
| NVIDIA | 6.80% |
| Marvell | 5.58% |
| Applied Materials | 4.69% |
| Qualcomm | 4.06% |
| Monolithic Power | 3.93% |
| Texas Instruments | 3.83% |

SOXX 还持有 TSM、ASML、ASE、UMC 等美国以外或台湾相关半导体链条暴露。BlackRock 页面显示，SOXX 2026-05-08 NAV 为 520.31 美元，52 周区间 191.92-520.31，费用率 0.34%，3 年 beta 1.58，持仓数 30。

市场位置：SOXX 2026-05-08 收于约 520 美元，贴近 52 周高位。按 Yahoo Finance chart API 计算，2026 年初至 2026-05-08 约 +72.9%，过去一年约 +173.1%。BlackRock 官方页面也显示，2026-05-07 的 NAV total return YTD 为 +63.68%，且 2026-05-08 单日 NAV +5.64%。这说明 SOXX 已经高度定价 AI 和半导体周期复苏。

对 SOXX 的判断：

- 正面因素：AI 训练/推理需求、HBM/存储周期、网络芯片、半导体设备订单、本土制造投资。
- 负面因素：高 beta、高集中度、对半导体关税和出口管制更敏感、台湾和中国供应链风险、涨幅过大后的估值风险。
- 结论：如果没有新的半导体广泛关税，SOXX 仍可能在 AI 主线中继续跑赢；但从风险调整角度，当前位置更适合等待回撤或政策缓和信号，而不是无条件追高。

## 未来走势框架

### 1-3 个月

QQQ：偏震荡上行，但追高胜率下降。若没有新的关税升级，技术面仍强；若出现新的中国/半导体/消费电子关税公告，第一反应大概率是估值压缩，5%-8% 回撤并不意外。

SOXX：动量最强，但短期最脆弱。过去一年和年初以来涨幅太大，任何“半导体关税扩围”“中国反制”“先进芯片出口限制升级”都可能触发 10% 以上快速调整。

### 3-6 个月

重点看 2026-07-24 临时 10% surcharge 到期节点：

- 若不延长或提前终止，市场会把它解读为贸易摩擦降温，QQQ 和 SOXX 都受益，SOXX 弹性更大。
- 若延长或扩大范围，市场会重新定价通胀和毛利率压力，SOXX 大概率弱于 QQQ。
- 若维持附加税但扩大豁免，影响可能被市场吸收，指数回到盈利和 AI capex 主线。

### 6-12 个月

中期选举后，政策不确定性通常下降。若届时没有严重通胀反弹或盈利下修，QQQ 更可能延续大盘成长优势；SOXX 则取决于 AI 资本开支是否继续上修，以及半导体关税是否从“选择性”变成“广泛性”。

我的优先级排序：

1. 政策风险调整后，QQQ 更适合做核心。
2. SOXX 更适合做交易型或卫星型高 beta 仓位。
3. 若出现关税缓和或豁免延长，SOXX 的反弹弹性高于 QQQ。
4. 若出现关税升级或中国反制，SOXX 应先降风险，QQQ 次之。

## 需要跟踪的触发器

| 触发器 | 对 QQQ | 对 SOXX |
| --- | --- | --- |
| Section 232 半导体扩围，覆盖更多芯片/设备/衍生品 | 负面，尤其 NVDA/AAPL/AVGO/TSLA | 强负面 |
| Advanced chip 25% tariff 豁免扩大 | 正面 | 强正面 |
| 2026-07-24 临时 10% surcharge 到期不延长 | 正面 | 正面，弹性更高 |
| 中国稀土/关键材料/市场准入反制 | 负面 | 强负面 |
| USMCA/墨西哥组装豁免稳定 | 对硬件和汽车链有利 | 中性偏正面 |
| Fed 转向降息且盈利不下修 | 正面 | 强正面 |
| AI capex 指引下修 | 负面 | 强负面 |
| 中期选举民调和结果明朗 | 波动下降后偏正面 | 波动下降后偏正面 |

## 后续可扩展回测

如果要把这个方案做成可重复研究脚本，建议下一步：

1. 建立事件库：2018-2019、2024 Section 301 复审、2025-2026 Section 122/232/301 事件。
2. 建立暴露因子：海外收入占比、中国收入占比、台湾制造依赖、墨西哥/USMCA 组装依赖、进口 COGS 敏感度、毛利率。
3. 建立公司池：QQQ 前 30、SOXX 全持仓、消费电子/汽车/零售进口依赖公司。
4. 计算事件窗口：T-1 至 T+1、T+5、T+20；同时计算相对 SPY 和相对行业 ETF。
5. 区分“公告日”和“生效日”：2018-2019 证明市场往往先交易公告，生效日只是二次确认。

## 主要来源

- USTR，2018-06-15，[USTR Issues Tariffs on Chinese Products in Response to Unfair Trade Practices](https://ustr.gov/about-us/policy-offices/press-office/press-releases/2018/june/ustr-issues-tariffs-chinese-products)。
- USTR，2018-09-18，[USTR Finalizes Tariffs on $200 Billion of Chinese Imports](https://ustr.gov/about-us/policy-offices/press-office/press-releases/2018/september/ustr-finalizes-tariffs-200)。
- USTR，2019-05-10，[Statement on Section 301 Action](https://ustr.gov/about-us/policy-offices/press-office/press-releases/2019/may/statement-us-trade-representative)。
- USTR，2019-08-23，[USTR Statement on Section 301 Tariff Action Regarding China](https://ustr.gov/about-us/policy-offices/press-office/press-releases/2019/august/ustr-statement-section-301-tariff)。
- USTR，2019-12-13，[United States and China Reach Phase One Trade Agreement](https://ustr.gov/about-us/policy-offices/press-office/press-releases/2019/december/united-states-and-china-reach)。
- USTR，2024-09-13，[USTR Finalizes Action on China Tariffs Following Statutory Four-Year Review](https://ustr.gov/about-us/policy-offices/press-office/press-releases/2024/september/ustr-finalizes-action-china-tariffs-following-statutory-four-year-review)。
- White House，2026-01-14，[Advanced Computing Chips Section 232 Fact Sheet](https://www.whitehouse.gov/fact-sheets/2026/01/fact-sheet-president-donald-j-trump-takes-action-on-certain-advanced-computing-chips-to-protect-americas-economic-and-national-security/)。
- White House，2026-02-20，[Temporary Import Surcharge Proclamation](https://www.whitehouse.gov/presidential-actions/2026/02/imposing-a-temporary-import-surcharge-to-address-fundamental-international-payments-problems/)。
- White House，2026-04-02，[Steel, Aluminum, and Copper Tariffs Fact Sheet](https://www.whitehouse.gov/fact-sheets/2026/04/fact-sheet-president-donald-j-trump-strengthens-tariffs-on-steel-aluminum-and-copper-imports/)。
- Invesco，2026-03-31，[Invesco QQQ fact sheet](https://www.invesco.com/us-rest/contentdetail?contentId=841e411c-a1eb-4541-8cb8-0fa603abea81&dnsName=us)。
- iShares/BlackRock，2026-05-08，[iShares Semiconductor ETF SOXX](https://www.ishares.com/us/products/239705/SOXX)；持仓 CSV：[SOXX holdings](https://www.ishares.com/us/products/239705/fund/1467271812596.ajax?dataType=fund&fileName=SOXX_holdings&fileType=csv)。
- BlackRock，2026 春季，[Investment Directions: Inflation, AI and portfolio diversification](https://www.blackrock.com/us/financial-professionals/insights/inside-the-market/investment-directions)。
- 市场价格和事件窗口：Yahoo Finance chart API，QQQ/SOXX/SPY 及样本公司调整后收盘价，下载于 2026-05-11。
- 前序本地研究：`tmp/midterm_cycle_qqq_soxx_research.md`、`政策不确定性冲击_QQQ_SOXX.md`、`通胀事件回测_QQQ_SOXX.md`、`tmp/inflation_regime_backtest_QQQ_SOXX_2026-05-10.md`、`美联储政策意外_QQQ_SOXX.md`、`中期选举主题篮子_QQQ_SOXX.md`。
