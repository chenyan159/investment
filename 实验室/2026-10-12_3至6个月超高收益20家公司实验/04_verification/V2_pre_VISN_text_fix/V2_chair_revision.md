# V2主席复议修订

原版保存于04_verification/V2_pre_chair_review；修訂保留条件模型，不提升事实认证。

## 实质纠错

主席复议纠错：原83–85%总GM没有收入组合支持，已撤回。Q2产品GM74.6%、总GM约76.88%；AMVUTTRA大于1.5B销售部分30%版税，nucresiran尚未上市不能提前抹掉。四档总GM72/73/74/75%；另把净利息由45–60提高200–230M，Q2净利息53.908M且含出售未来版税负债成本，不能漏掉。所有费用含SBC；此修订强成功不再2倍。

600M可转债本金现金结算，目标股数含溢价/奖励但非已认证。营运库存629.9M，增长不保证现金；未来毛利22%须自制及利用率证实。 主席复议后扣NCI研究公允值192/320/552/832M，对应年NCI利润12/16/24/32M乘16/20/23/26；Q2实际3.2、H1 6.2、账面77.3不能当未来公允值。全集团现金债与NCI价值保持同一口径，未再次扣NCI利润。 资金复议：6/26现金255.9、可转本金600（账面599.4），净金融债344.1M；H1 CFO−74.4、PPE25.8、FCF−100.2，库存增238.9、应付增104.4。 未来净债550–600相对当前344.1增205.9–255.9M是模型融资/现金消耗预算；当前cash若留100流动性仅155.9可消耗，不能保证无需追加融资。 未逐笔核对未提款银行额度；净债目标不是已承诺融资；盈利增长若库存继续吸钱会稀释。

## SMCI分支差异

{
  "B2_central": 53.28,
  "B2_strong": 81.6,
  "V2_central_inputs": {
    "revenue_m": 72000,
    "GM": 0.11,
    "economic_opex_m": 2500,
    "NOPAT_m": 4281.8,
    "EV_NOPAT": 16
  },
  "V2_strong_inputs": {
    "revenue_m": 85000,
    "GM": 0.125,
    "economic_opex_m": 2800,
    "NOPAT_m": 6181.75,
    "EV_NOPAT": 19
  },
  "explanation": "B2强是经济EPS5.1×16；V2工作中枢等价接近这一成功强度，不是更稳健的期望。V2强收入85B比FY27官方上限72B高18.1%，是FY28运行速率且GM12.5%，费用率3.29%，相对工作分支利润+44.4%、倍数+18.75%，并计更多债转换。股价抬高主要由更强经营及重估，不是换公式免费增值。",
  "window_evidence": "8/11原始：FY27销售65–72B、Q1 14.5–15.5B、FY26新增订单>60B与纪录backlog。Q4GM17.5%，全年10.8%，故不年化17.5%。仅当11月/2月估计财报连续兑现交付、11–12.5%正常化GM及现金回收，市场才有理由提前看85B；目前没有85B官方承诺。",
  "required_reclassification": "工作中枢=有条件经营恢复位置，不可作为概率最大分支；135.84是更强于B2的成功，不因算术核验而提高发生权重。"
}

## ENPH净金融现金压力

{
  "separate_from_PE": true,
  "current_net_financial_cash_m": 362.7,
  "future_cash_burn_stress_m": [
    0,
    150,
    300
  ],
  "future_shares_m": 136,
  "net_financial_cash_per_share": [
    2.6669117647058824,
    1.5639705882352941,
    0.4610294117647059
  ],
  "PE_disappointment_price": 1.5485294117647062,
  "interpretation": "PE失望1.55仅资本化11.7M年利润，低于当前2.67/股净金融现金。若到目标净现金仍约213–363M，独立净金融现金压力值1.56–2.67可提供缓冲；若亏损/回购烧钱300M则仅0.46。此非清算估值/硬地板，未计员工、保修、租约及营运结算，资产处置可高可低。不把这一金额再加到含利息的PE。"
}

## 七家公司资金缺口

### IREN

{
  "known_or_committed": "截至6/30非受限现金5895.6M；6/1 GPU债额度3650M已close，含2100M私募及1550M延迟提款，6%债成本。与客户预付合计5590M覆盖微软5810M GPU CapEx。",
  "numeric_gap": "此已指定GPU包差额220M=5810−5590，另有设施、非微软GPU、预付抵扣与利息；它不是全公司缺口。现有现金只能用一次，不把3650再次全加至6/30现金。",
  "research_bounds_m": {
    "Microsoft_GPU_package_uncovered": 220,
    "whole_company_unfunded_capex_lower_bound": 220,
    "whole_company_upper_bound": null
  },
  "uncommitted": "NVIDIA 30M股×70权利不是到账2100M；2倍69.60低于行权价。未来模型债区间是融资条件，不能写已获14B自由现金。",
  "verdict": "局部项目融资覆盖可算，全公司逐季资金缺口未闭合；违约/重谈和追加股融仍能改变股价。"
}

### AAOI

{
  "known_or_committed": "S1已核10/5 ATM净款588M、5.694845M股；V2原始页面首次打开有元信息，定位正文反复Internal Error，因此金额仍标继承，不升级独核。",
  "numeric_gap": "588M为本批已融资，不是新增未知额度；92.8M会计稀释与ATM相加不能当法律股数。之后产线CapEx、库存与回款缺同日全桥，无法以诚实证据给总缺口上限。",
  "research_bounds_m": {
    "inherited_completed_ATM_net_cash": 588,
    "minimum_incremental_uncommitted_financing": 0,
    "maximum_incremental_uncommitted_financing": null
  },
  "uncommitted": "零是可能无需再融的下限，不是结论；模型102–115M分母与净债变化仍是新增奖励/融资压力。",
  "verdict": "融资已发生与产线兑现分开；最关键缺口是扩大收入所需营运现金。"
}

### CRWV

{
  "known_or_committed": "6/30金融债本金35551M已独开。2026 CapEx35–39B为S1继承指引，不能和债本金相减得到缺口，因为期限、应付设备与受限现金不同。",
  "numeric_gap": "模型目标净债45–58B相对当前毛本金差额9.449–22.449B，属于量纲提示而非真实资金缺口；实际需再加目标现金、既有现金及其可用限制。",
  "research_bounds_m": {
    "target_net_debt_low": 45000,
    "target_net_debt_high": 58000,
    "minimum_difference_vs_current_gross_principal": 9449,
    "maximum_difference_vs_current_gross_principal": 22449
  },
  "uncommitted": "逐项目未提款facility、设备租赁、应付GPU期限和扩张CFO未完整对齐，不能认证融资全部已承诺。",
  "verdict": "必须在4月前将capex付款日期与可提款日期配对；当前模型仅条件成立。"
}

### PSIX

{
  "known_or_committed": "新220M ABL法律额度；初借35M、偿旧15M，再扣费用不是净增220M现金。6/30现金70.1/债72.6继承S2。",
  "numeric_gap": "名义未用上限185M=220−35，实际还受借款基数、LC及契约限制，可用下限0；新增订单库存及应收可能占用此额度。",
  "research_bounds_m": {
    "nominal_undrawn_ABL_max": 185,
    "verified_immediately_drawable_min": 0
  },
  "uncommitted": "不得把未提款185M列为当前cash；超过借款基数的增长资本尚无闭合来源。",
  "verdict": "盈利不等自由现金；优先监测应收库存与借款基数，未发现等额必须股融的证据。"
}

### ADBE

{
  "known_or_committed": "当前389.2M法律股继承主席9/18原始核查。盈利/运营现金提供内生资金，暂无本模型必须新增股融项目；回购授权不等执行承诺。",
  "numeric_gap": "未来股388–395M相对389.2M差−1.2至+5.8M；仅净减少1.2M按238.14至少285.8M回购现金，若同时对冲SBC需更多；中枢390M没有净回购依赖。",
  "research_bounds_m": {
    "minimum_cash_for_strong_net_share_reduction_at_reference_price": 285.768,
    "required_new_external_financing_in_model": 0
  },
  "uncommitted": "SBC真实股份交付及实际回购价未知。模型GAAP式利润费用保SBC，未再加现金。",
  "verdict": "缺口在回购执行/股数精度，非AI基建那种必须大额再融资；不得因此称全现金桥审计通过。"
}

### UCTT

{
  "known_or_committed": "6/26现金255.9、可转本金600（账面599.4），净金融债344.1M；H1 CFO−74.4、PPE25.8、FCF−100.2，库存增238.9、应付增104.4。",
  "numeric_gap": "未来净债550–600相对当前344.1增205.9–255.9M是模型融资/现金消耗预算；当前cash若留100流动性仅155.9可消耗，不能保证无需追加融资。",
  "research_bounds_m": {
    "target_net_debt_increment_low": 205.9,
    "target_net_debt_increment_high": 255.9,
    "cash_available_above_research_minimum100": 155.9
  },
  "uncommitted": "未逐笔核对未提款银行额度；净债目标不是已承诺融资；盈利增长若库存继续吸钱会稀释。",
  "verdict": "追加扣NCI价值192–832M；能过2倍但不能因为收入弹性忽略资本占用。"
}

### VISN

{
  "known_or_committed": "出售后全年现金700–750M为公司指引，非10/12已实际闲置现金。此前15美元分配不属于本次买入收益。",
  "numeric_gap": "研究回购150后现金550–600M；采用中枢550。未来2027H2退税160M不进入4/12现金。实际回购价决定减股15.63M是否成立。",
  "research_bounds_m": {
    "guided_cash_before_assumed_buyback_low": 700,
    "guided_cash_before_assumed_buyback_high": 750,
    "assumed_buyback": 150,
    "cash_after_assumed_buyback_low": 550,
    "cash_after_assumed_buyback_high": 600
  },
  "uncommitted": "交割税/分拆费用及准确回购进度缺完整桥；不以现金指引加160作为下行地板。",
  "verdict": "无需大规模外部融资是条件假设；主要误差为费用和资本返还节奏，而非凭空新资金。"
}

日期纠错：AAOI ATM 公告日期由误写的 2026-10-08 更正为 2026-10-05；588M 净款、5.694845M 新股及全部模型数值保持不变。
