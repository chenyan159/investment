# V1：BNTX 权益追加核验

信息截止 2026-10-12 19:40 LA；观察日 2028-04-12。原 V1 封存稿不改，本追加覆盖其 DB1311 春季期权状态。

**结论：四桶中只有 pumitamig 的 0.5 可以直接解释为已核实的全球利润分成。其余代理应拆成地区、销售版税或产品利润分成；这属于模型语义修正，不意味着全部资产都需向下砍估值。**

| 资产 | 已核实权利 | 可执行模型处理 |
|---|---|---|
| pumitamig | BMS 全球利润/亏损50/50，有协议例外 | 保留0.5，只作用于该药物利润 |
| gotistobart | BioNTech全球独家商业权；OncoC4双位数阶梯销售版税 | 取消“80%股权”；税前利润率减销售版税再计税，12/15/18%仅敏感假设 |
| T-Pam | BioNTech拥有除大陆、香港、澳门以外权利；明确含台湾；须付销售版税 | 用授权地区销售×扣版税后的利润；85%地区占比、10/15/20%版税皆非合同数字 |
| DB1311/elfe-D | 2026年5月已行使美国成本/利润期权；非美国授权区域仍付版税 | 美国利润分成比例未披露，50%中枢及40–60%范围仅假设；美国不叠同项销售版税 |
| BNT113/BNT116 | 全有FixVac | 自身药物权益可100%；联合用药不等于自动分成，也不能把整套联合售价归自身 |
| autogene/BNT122 | Genentech净利润/亏损50/50，退出则改版税 | 单独建模；CRC、尿路上皮癌已停试验不给旧销售，未停胰腺等保留可辩护右尾 |

最关键的新事实来自合作方 Duality 8月28日中报：五月已书面行使 DB1311 美国期权，并确认人民币2.907亿元历史开发费抵收入。春季“未行使”状态已经过时。原协议§8.8(f)明确行权后版税针对美国以外授权地区；美国比例被删节，不可将50/50写成披露事实。

销售版税与利润分成不能混用。若35%是版税前税后净利率，假设税率25%、销售版税10/15/20%，实际净利率为27.5/23.75/20%，并非35%×80%=28%。但若35%本就已扣版税，再乘80%反而重复扣减。若V2改用税前营业利润率，统一公式为 `地区销售 × (版税前营业利润率 − 销售版税率) × (1 − 税率)`。

T-Pam旧0.5是无法追溯的聚合代理，不能简单判为过高：相同全球销售下，授权地区占比、净销售版税及利润率组合能使实际归属利润高于或低于旧值。应保留双向敏感性。gotistobart全球授权也支持保留合理商业右尾，不能当成只有某一区域授权。

所有预计销售、地区份额、税率、成功概率仍属研究假设。里程碑、后续研发及商业化费用要在现金或管线估值中计算一次；联合方案中的两药销售必须各自分配，不能两桶都使用整套方案售价。最新20F PDF成功打开但后续全文定位出现Internal Error；没有把检索片段当作精确费率核准，决定性权益由协议正文和合作方最新中报验证。

## 逐URL审计

- **ONCO_PR / 2023-03-20**：[原始来源](https://www.sec.gov/Archives/edgar/data/1776985/000177698523000016/ex991230320proncoc4.htm)。全球独家商业权；双位数阶梯销售版税；特定联合开发成本平分，不等于利润平分。

- **ONCO_AGREEMENT / 2023-03-17**：[原始来源](https://www.sec.gov/Archives/edgar/data/1776985/000177698524000027/exhibit448oncoc4agreementr.htm)。原协议§7.5版税数字删节，不能确认20%或80%经济权益。

- **HER2_AGREEMENT / 2023-03-16**：[原始来源](https://www.sec.gov/Archives/edgar/data/1776985/000177698524000027/exhibit450dualityher2agree.htm)。§1.147/1.163排除大陆、香港、澳门，明确含台湾；§8.5销售版税率删节。

- **B7H3_AGREEMENT / 2023-03**：[原始来源](https://www.sec.gov/Archives/edgar/data/1776985/000177698524000027/exhibit451dualityb7h3agree.htm)。§1.54美国利润分成区域；§8.8(a)-(d)数字删节；§8.8(f)行权后美国以外授权区域仍付销售版税，美国不可再叠同一版税。

- **DUALITY_AR / 2026-04-26**：[原始来源](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0426/2026042600131.pdf)。p44当时DB1311期权尚未行使；属于被后来事件覆盖的状态。

- **DUALITY_INTERIM / 2026-08-28**：[原始来源](https://en.dualitybiologics.com/news/615.html)。5月已书面行使DB1311美国成本/利润分成期权；确认290.7M人民币历史开发费抵收入。

- **BNTX_20F / 2026-03-10**：[原始来源](https://investors.biontech.de/static-files/242c45fc-69f7-4abb-b1a5-f29ab19c590d)。FY2025报告PDF成功打开，但后续定位请求Internal Error；Duality single-digit至double-digit仅检索正文片段获得，精确率仍不得视为核准。

- **BNTX_FY25 / 2026-03-10**：[原始来源](https://www.biontech.com/us/en/home/mediaroom/news/press-releases/2026/03/biontech-announces-fourth-quarter-and-full-year-2025-financial.html)。BNT113基于完全自有FixVac；autogene与Genentech合作；肌层浸润尿路上皮癌试验停止。

- **GENENTECH_AGREEMENT / 2016-09-20**：[原始来源](https://www.sec.gov/Archives/edgar/data/1776985/000119312519241112/d635330dex1014.htm)。§8.2.2开发成本平分；§8.4净利润亏损50/50；§8.5退出后转版税，不能同时算二者。

- **AUTOGENE_CRC / 2026-08-28**：[原始来源](https://www.biontech.com/au/en/home/mediaroom/news/statements/2026/08/BioNTech-Provides-Update-on-Phase-2-Clinical-Trial-of-Autogene-Cevumeran-in-Resected-Colorectal-Cancer.html)。BNT122-01辅助CRC试验已决定终止，不能作为仍活跃商业机会计入。

- **BMS_Q2 / 2026-08**：[原始来源](https://www.sec.gov/Archives/edgar/data/14272/000001427226000020/bmy-20260630.htm)。原V1已独立实读：pumitamig全球利润/亏损50/50，存在合同例外；本追加继承该核验。

## 未解决项

- OncoC4精确阶梯费率/里程碑及更新商业参与条款未公开核准
- Duality具体ADC阶梯费率及DB1311美国分成比例被删节
- 所有地区销售权重、销售峰值、产品净利润率、税率及成功概率都是研究假设
- 四桶组合或联合疗法不能把同一患者完整联合方案售价重复归入不同药物
- V2应确保before/after royalty margin语义一致，避免既减净利率又乘权益代理
- 最新20F正文定位受工具限制，未声称完整逐页审读；合同正文与合作方最新中报封口核心权利
