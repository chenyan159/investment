import json,re,pathlib,hashlib
B=pathlib.Path(r'D:\investment\实验室\2026-10-12_20家公司多角色实验')
def read(p):return json.loads((B/p).read_text(encoding='utf-8-sig'))
models=read('04_verification/V2_models.json'); M={c['ticker']:c for c in models['companies']}
v=read('04_verification/V1_primary_verification.json'); V={c['ticker']:c for c in v['companies']}
u={c['ticker']:c for c in read('01_inputs/universe.json')}
rows=read('05_chair/chair_card_inputs.json'); a={c['ticker']:c for c in read('05_chair/主席阶段A_竞争池.json')['candidates']}
s2=read('07_logs/S2_sources.json')['sources']; logs=read('07_logs/V1_sources.json')['sources']
L={s['source_url']:s for s in logs}
extras={
'PSIX':[('https://blogs.nvidia.com/blog/ocp-global-summit-vera-rubin-scale-ai-factories/','2026-10-12','供电/机架架构需求；不证明PSIX得到订单')],
'SNDK':[('https://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Fiscal-Fourth-Quarter-and-Full-Year-2026-Results/','2026-09-30','MU同业实际利润及合同路径，用于存储替代比较')],
'BDC':[('https://ir.microchip.com/news-events/press-releases/detail/1409/microchip-technology-announces-financial-results-for-first-quarter-of-fiscal-year-2027','2026-08-06','工业电子替代MCHP去库存及每股权益限制，不证明BDC协同')],
'CARR':[('https://investors.pentair.com/node/27181/pdf','2026-10-01','PNR收购完成，比较另一路工业恢复；不证明CARR需求')],
'KYTX':[('https://pubmed.ncbi.nlm.nih.gov/38885382/','2024','PNAS单病例摘要，巨大个体功能改善；含公司利益关联'),('https://index.mirasmart.com/AAN2026/PDFfiles/AAN2026-005919.html','2026','AAN原始26人会议摘要，疗效及低级CRS/ICANS，不是独立第二组患者')],
'VST':[('https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2028-2029/2028-2029-bra-results-report.pdf','2026-07','2028/29容量拍卖325美元/UCAP MW-day；交付期晚于观察日，只影响前瞻定价'),('https://rss.globenewswire.com/news-release/2026/08/05/3339712/0/en/talen-energy-reports-second-quarter-2026-results-raises-2026-guidance.html','2026-08-05','Talen实际参与容量市场及不同套保比例，独立行业经营链')]
}
chainlimits={
'NVDA':'AWS支持需求、Maia提供竞争反证；都不是NVDA600B收入的独立预测。OCP与Cisco联合生态属于一个根事件。',
'MU':'TrendForce支持当前供需，微软HBM路线不锁定MU份额；合同价格持续到FY28仍需假设。',
'ADBE':'Canva提供真实替代方案，专业媒体评价不等于客户流失队列；公司ARR不拆全部AI增量。',
'PNR':'渠道POOL、同行Hayward与PNR品类和客户结构不同，支持反问而不直接证明失份额或恢复。',
'CLS':'SMCI与Cisco提供竞争和需求环境，不能证明CLS全部新客户份额；HPS嵌于CCS不得重复计。',
'AVGO':'云客户多架构部署支持定制需求，却不能自动证明Broadcom获取每一项ASIC设计。',
'PSIX':'Cummins是真实同行需求与竞争链；NVDA供电架构只说明需求场景，不证明PSIX专属订单。',
'ARGX':'KYTX机制可形成远期竞争，不能否定当前FcRn付费；监管批准也不担保未来净价及治疗年。',
'BNTX':'BMS及Duality自方财报、原协议验证不同经济权利；合作临床稿不算独立重复试验。精确版税/美国分利被删节，地区销售权重与净价仍需假设。',
'SMCI':'最终10K与早期财报为同一财年根事件，不能重复计独立性；CLS是不同企业的资本效率对照。',
'AGCO':'USDA美国行业数据不能外推欧洲同幅变化；Deere订单是竞争参照，不是AGCO订单。',
'IREN':'客户宏观投入与Maia路线支持需求且形成竞争，SOW才说明验收条件；仍不等于逐项目股东资金已闭合。',
'SNDK':'同业MU和行业报价能佐证周期，不能确认SNDK每份NBM最低付款或FY28合同实现。',
'BDC':'Cisco支持WiFi7/工业网络市场及竞争，MCHP是周期替代；均不验证RUCKUS交叉销售成功。',
'ALNY':'BBIO真实一线增长是竞争证据，AZ失败是另一项目事件；都不能替代ALNY净价和患者持续性。',
'BABA':'保诚真实上线验证采用但没有披露阿里净合同利润；媒体报道同一财报不重复计经营核验。',
'CRM':'ADBE与保诚定制路径是不同实施替代，不直接证实CRM会赢或输；ARR口径扩张依然未消除。',
'VST':'Meta客户需求和PJM市场规则是两条根链；2030扩容及2028/29容量期不能冒作观察日前现金。',
'KYTX':'PNAS单病例作者含公司雇员/股东；AAN摘要未经Neurology编辑审阅，同KYSA8一年更新不是第二批患者。CRS92.3%为1/2级、ICANS11.5%为1级，3/4级中性粒减少15.4%；24周仅16人是达到时点人数，不能判其他人失败。',
'CARR':'MOD及PNR说明不同业务结构与竞争，不能直接证实CARR住宅售出或数据中心验收。'
}
closest={'NVDA':'AVGO','ADBE':'CRM','MU':'SNDK','PNR':'CARR','CLS':'SMCI','AVGO':'TSM','PSIX':'FLNC','ARGX':'ALNY','BNTX':'IONS','SMCI':'FLNC','AGCO':'MCHP','IREN':'NBIS','SNDK':'TSM','BDC':'MOD','ALNY':'IONS','BABA':'GOOGL','CRM':'MOD','VST':'PGR','KYTX':'POET','CARR':'TSM'}
extras['BNTX']=[
('https://www.sec.gov/Archives/edgar/data/1776985/000177698523000016/ex991230320proncoc4.htm','2023-03-20','gotistobart全球独家商业权与双位数阶梯销售版税，不能混成80%股权'),
('https://www.sec.gov/Archives/edgar/data/1776985/000177698524000027/exhibit450dualityher2agree.htm','2023-03-16','T-Pam授权排除大陆香港澳门但包含台湾，销售版税数字删节'),
('https://en.dualitybiologics.com/news/615.html','2026-08-28','合作方确认DB1311美国利润/成本分成期权五月已行使，旧未行使状态作废'),
('https://www.biontech.com/au/en/home/mediaroom/news/statements/2026/08/BioNTech-Provides-Update-on-Phase-2-Clinical-Trial-of-Autogene-Cevumeran-in-Resected-Colorectal-Cancer.html','2026-08-28','autogene CRC试验终止，胰腺项目保留，不重新计入停止项目销售')]
for rank,r in enumerate(rows,1):
 t=r['ticker']; c=M[t]; r['rank']=rank;r['company_name']=u[t]['name'];r['project_member']=True
 r['reference_price']=c['reference_price'];r['reference_price_date']=c['reference_price_date'];r['observation_date']=c['observation_date'];r['currency']=c['currency'];r['security']=c['security'];r['scenarios']=c['scenarios'];r['model_type']=c['model_type'];r['earnings_period']=c['earnings_period']
 r['closest_alternative']=closest[t];r['catalysts']=r.pop('catalysts_text').split('；');r['kill_conditions']=r.pop('kill_text').split('；')
 r['verified_facts']=[x['claim'] for x in v['checks'] if x['ticker']==t]
 r['external_chain_limitations']=chainlimits[t];r['material_unresolved']=r['forecast_caveat']+'；'+V[t]['strongest_counterevidence'];r['numerical_unresolved_original']=c['unresolved']
 links=a[t]['read_role_links'];links=[x for x in links if x!='控制器V1进展转述']
 if t=='VST':links=[x for x in links if x not in ['S1','S2']]+['Controller非AI专项']
 r['round_chain']=links+['V1原始核验','V2独立计算','主席A/B替代裁决']
 r['evidence_files']=[{'R1':'02_round1/R1_cashflows.md','R2':'02_round1/R2_valuation.md','R3':'02_round1/R3_external.md','R4':'02_round1/R4_upside.md','R5':'02_round1/R5_diversification.md'}[role] for role in links if role in ['R1','R2','R3','R4','R5']]+['03_round2/B1_business_rebuttal.md','03_round2/B2_valuation_rebuttal.md','04_verification/V1_primary_verification.md','04_verification/V2_numeric_verification.md','04_verification/V2_models.json']
 if t=='VST':r['evidence_files']+=['03_round2/Controller_非AI需求交叉核验.md']
 elif t in ['NVDA','MU','AVGO','CLS','PSIX','SMCI','IREN','SNDK']:r['evidence_files']+=['03_round2/S1_ai_upside.md']
 else:r['evidence_files']+=['03_round2/S2_nonai_upside.md']
 if t=='KYTX':r['evidence_files']+=['03_round2/Controller_KYTX临床外部交叉核验.md']
 ss=[];seen=set()
 def add(url,date,note,kind):
  if url and url not in seen: ss.append({'url':url,'published_date':date,'key_information':note,'role':kind,'access':'继承团队实读记录；主席未重复访问'});seen.add(url)
 for x in v['checks']:
  if x['ticker']==t:add(x['source_url'],x.get('published_date',''),x['claim'],'原始事实')
 for x in V[t]['independent_external_chain']:add(x['source_url'],x.get('published_date',''),x.get('interpretation',''),'公司之外根链')
 for url,date,note in extras.get(t,[]):add(url,date,note,'补充原始/外部链')
 for s in s2:
  if t in s.get('tickers',[]):add(s['url'],s.get('publication_date',''),s.get('short_findings',''),'专项来源')
 for url in c.get('independent_V2_sources',[]):
  l=L.get(url,{});add(url,l.get('published_date',''),l.get('reading_note','V2原始经营/证券核验'),'V2来源')
 r['sources']=ss
 if t=='BNTX':
  r['evidence_files']+=['04_verification/V1_BNTX权益追加核验.md','04_verification/V2_BNTX_rights_correction.md']
  r['round_chain']+=['V1/V2权益追加与主席再裁决']
  r['verified_facts']+=['gotistobart是全球独家授权加双位数销售版税；T-Pam排除大陆港澳而包含台湾；DB1311美国成本/利润期权2026年5月已行使；autogene CRC及尿路上皮试验终止。']
 assert len(ss)>=3,(t,len(ss))
res=[('TSM','制造瓶颈和跨架构需求实证很强；当前基准22.4%上行，地缘和再投资尾部仍在，未优先于CARR双恢复路径。','海外成本和资本效率改善使同口径每股空间上修；或CARR交付/住宅失败，直接替换。'),('MOD','增长真实且无旧THRM分派错误；但基准需21%经济率，较大悲观尾部未换来更强当前收益。','持续业务正式指引与客户交付支持21%率、剔预付款后现金改善，可替CARR/BDC/CRM。'),('POET','真钱和光学客户融资支持大右尾；基准经营仍亏，量产净收入与权益稀释使中枢仅温和上行。','不可取消净采购、量产良率及第二客户验证；可替KYTX或边际工业席，不必等盈利后才回归。'),('IONS','两失败已逐项剔除，GSK批准/Roche阳性保留；基准留存收入1.813B但经济EBIT仅83.85M，6倍销售仍押远期。','付费治疗年和净价超过桥、版税/2028债务可控；可替ALNY/KYTX而非永久淘汰。'),('FLNC','重大指引下修和非递延赔偿/质量损失，使现有订单不能直接证明现金反转；高右尾仍在。','产线恢复、异常成本停止、担保及融资桥明确；可替SMCI/PSIX较弱者。'),('PGR','正常化承保具质量，基准上行约20%；高收益目标下不为保险标签自动占席。','事故年承保率和保单增长支持更高持续EPS，或资本密集候选普遍失效时回归。'),('MCHP','去库存真实，但扣优先股息和债息后基准空间约7%。','FY28经济EPS显著超过4或价格更低，且不靠忽略优先股，可替AGCO/BDC。'),('CRDO','已有AEC利润但持续SBC后基准低于当前价格；不否定光学第二引擎。','新光产品实际利润和客户分散超桥，或更好买价，可替CLS边际席。'),('AAOI','产能和1.6T资格具有右尾，但销量、SBC和融资股数后基准不足。','合格量产、正税前利润和现金兑现显著上修，可挑战PSIX/POET。')]
reserves=[{'rank':21+i,'ticker':t,'reason':reason,'reentry_conditions':reentry,'scenarios':M[t]['scenarios'],'reference_price':M[t]['reference_price']} for i,(t,reason,reentry) in enumerate(res)]
changes=['相较B1条件20：SMCI、CRM、BDC入选，MOD、FLNC、PGR移为候补；依据现金/资本和替代机会而非票数。','相较主席A：20个名称保留，但SMCI/PSIX及现金修复的排序重新调整，CARR置第20且以TSM作第21对照；保留不是免复核。','SMCI旧未审计淘汰理由撤销；FY26巨额负CFO和ITGC问题保留为等待条件。','NVDA费用含SBC不再扣；AVGO扣一次；MU90%OP旧错误修复而不强制回周期谷底；CLS剔TRS。','MOD新买家无旧THRM分派；PNR Taco已交割；VST采用94%/72%套保并将机会区间与正式指导分开。','KYTX一年数据已发生，100M左右融资后股数替代70M；BNTX以V2末审权益版模型为唯一数字来源。']
obj={'status':'final_chair_decision_subject_to_future_operating_conditions','information_cutoff':models['information_cutoff'],'observation_date':models['observation_date'],'ranked_companies':rows,'reserves':reserves,'decision_changes':changes,'selection_count':20,'all_project_members':all(r['ticker'] in u for r in rows),'model_sha256':hashlib.sha256((B/'04_verification/V2_models.json').read_bytes()).hexdigest(),'return_basis':'美元价格回报，不含未来股息、税费、交易成本；不是总收益，非统计概率区间','source_method':'继承各角色已实读原始/外部证据；主席全文阅读核验结论并作替代裁决，不冒称本人重复访问全部网页','portfolio_note':'研究优先级和行动条件，不是20等权马上买入；未提供无校准依据的组合期望回报/最大回撤'}
(B/'05_chair/主席最终裁决.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
head='''# 最终20家公司：18个月投资研究与条件裁决

本轮选择的重点是**有经营或事件证据支撑的高上行，同时诚实计入融资、稀释和失败尾部**。NVDA、ADBE、MU、PNR、CLS、AVGO提供主要经营/估值修复线索；PSIX、SMCI、IREN、KYTX提供更强但更有条件的进攻弹性。最终20是研究优先级，包含明确等待席，并非20等权立即买入。

信息截止为2026-10-12 19:40洛杉矶，价格统一用10月12日正常收盘；共同观察日2028-04-12。主表全部引用V2重建的18月模型，没有把S1的12月价格平移。表中回报是美元价格变化，未计未来股息、税费或交易成本；SPY、QQQ及全245家等权价格仅作未来比较基准，本报告不声称已经证明超额收益。

悲观、基准、乐观均为研究条件，不是统计置信区间，也不是最低/最高可能损益。没有按票数、单一PE、牛市涨幅或主观加权均值排序。股数、债务与SBC错误必须修复，未来盈利争议则保留不同路径，不能把所有悲观参数叠成基准。未来事件或价格变化允许候补回来。

## 统一总表

|序|公司|冻结价|悲观 / 基准 / 乐观价|对应价格收益|当前行动|
|---:|---|---:|---|---|---|
'''
for r in rows:
 sc=r['scenarios'];head+=f"|{r['rank']}|{r['ticker']}|{r['reference_price']:.2f}|"+' / '.join(f"{x['price']:.2f}" for x in sc)+'|'+' / '.join(f"{x['return_pct']:+.1f}%" for x in sc)+f"|{r['action_status']}|\n"
head+='''
## 名额选择：第20与第21不是机械分数之差

**CARR第20、TSM第21是边际决定，置信度低于前列。** CARR已经披露强数据中心订单，却只实现集团有机收入+3%、调整经营利润-6%，因此并非低风险现成利润；它的可审议预期差是住宅去库、欧洲经营和商业冷却有不完全同步的恢复路径。TSM的先进制造和封装稀缺性更扎实，9月收入+54.6%、Maia使用N2P也支持跨GPU/ASIC获得需求。但跨架构不能消除全球AI客户预算、海外厂成本、资本密度或地缘尾部。本20已经持有GPU、ASIC、存储、制造与算力，新增TSM的边际风险分散较小。

两模型基准约29.7%与22.4%、牛约97.7%与84.4%的差异仅说明假设下的价格空间，**不是CARR客观优越的证明**。CARR胜出还要求集团正常化利润与订单验收能在窗口内出现；若只是订单热而住宅/欧洲与现金无改善，应由TSM直接替换。反过来，不能仅为了不同行业强留CARR。

**KYTX保留第19事件席，POET/IONS/FLNC仍可越级。** KYTX融资后基准仅约35%并不突出，但患者功能改善和BLA/CMC为较具体的近期价值转折，成功分支有很大幅度，符合高风险偏好。POET有实际现金和客户融资、但量产净收入与权益尚需更多验证；IONS两失败并不毁掉平台，但扣版税权益后基准现金仍近盈亏平衡；FLNC订单不能自动修复1.25亿美元非递延损失。这里没有把不确定当否决，也没有把高成功价当基准。

**SMCI回归具有可逆条件。** 财报无保留与三项内控弱点修复使旧排除理由失效，而FY26经营现金-6.81B使当前等待理由仍强。目标较高只代表若毛利/现金修复的条件价值，不能让高目标价掩盖回款问题。其与CLS都入选是盈利质量与修复弹性的不同表达，仍共享AI交付因子。

## 20家公司详细卡
'''
def basebridge(c):
 s=c['scenarios'][1];x=s['inputs'];typ=c['model_type']
 if c['ticker']=='BNTX':
  buckets='；'.join(z['name']+' PV '+format(z['rNPV_B'],'.3f')+'B' for z in x['branches'])
  return '现金16.6342B欧元×1.10−3.6B观察日前烧损=14.69762B美元；六桶'+buckets+'；相加后扣观察日后开发/里程碑PV2.5B，除258M ADS。goti成功利润=3×(45%−15%销售版税)×80%；T-Pam=3.5×85%地区×(40%−15%)×80%；DB1311=1.5×[60%美国×40%利润率×50%分利+25%其他地区×(40%−15%)]×80%，美国不再扣同项版税。版税10–20%和美国分利40–60%的其他条件不变敏感价为124.72–138.65美元，不是概率区间。'

 if 'economic EPS' in typ:
  return f"收入{x['revenue_B']:g}B × 经济毛利/已含费用经营率{x['economic_gross_margin']:.2%}，减其他费用{x['opex_ex_SBC_B']:g}B、单列SBC{x['SBC_expense_B']:g}B、净利息{x['net_interest_expense_B']:g}B，正常税{x['tax_rate']:.1%}，再加税后其他{x.get('other_after_tax_B',0):g}B并减优先股息{x.get('preferred_dividend_B',0):g}B；除FD{x['FD_shares_B']:g}B股、乘{x['PE']:g}倍。SBC栏为0的经营率模型已经包含员工成本，并不免除SBC。"
 if 'revenue_B' in x:
  return f"收入{x['revenue_B']:g}B × 经济利润率{x['economic_margin']:.1%} × 倍数{x['multiple']:g}，减净债{x['net_debt_B']:g}B及其他优先权益{x['other_senior_claims_B']:g}B，除FD{x['FD_shares_B']:g}B股。EV模型债务扣一次。"
 return {'VST':'传统EBITDA8B + Cogentrix0.7B + Meta增量0.15B − SBC0.18B − 维护资本1.2B − 利息1.3B − 现金税0.8B − 优先股0.23B − 增长资本0.55B − 关闭/其他0.2B，除339M股、乘15倍FCFE。','CRM':'(15.5B经营现金减资本支出−4.7B持续SBC)/840M股×23倍；前项已含现金利息。','BABA':'[(160−16−7)B人民币×80%+10B归属其他收益]/(20.8B普通股/8)/7人民币每美元×21倍。','BNTX':'金融资产按汇率滚动并扣观察日前烧损，加逐资产地区/合作权益后的风险调整经营现值，减观察日后未含研发现值，再除ADS。具体末审分支列于模型文件及本卡机器记录；不把合作现金和同一管线重复相加。','KYTX':'SPS成熟年1000人×30万美元净价对应成功净利60M，22倍并以15%折现2年、乘70%主观成功率；另加其他净管线rNPV240M与剩余现金110M，扣债务60M和后续开发PV150M，再除约100.16M融资后股。'}[c['ticker']]
text=head
for r in rows:
 t=r['ticker'];c=M[t];sc=r['scenarios'];text+=f"\n### {r['rank']}. {t} — {r['thesis']}\n\n**裁决与行动：** {r['action_status']}。\n\n**已核披露（事实/指引按原文区分）：** "+'；'.join(r['verified_facts'])+f"\n\n**最强入选论据：** {r['strongest_bull']}。\n\n**最强反方：** {r['strongest_bear']}。\n\n**为何胜最接近替代 {r['closest_alternative']}：** {r['why_preferred']}。\n\n**18个月条件估值：** 悲观/基准/乐观 "+' / '.join(f"${x['price']:.2f}" for x in sc)+'；相对冻结价的收益 '+ ' / '.join(f"{x['return_pct']:+.1f}%" for x in sc)+f"。\n\n**基准桥（B为十亿美元，B股为十亿股）：** {basebridge(c)}\n\n**预测而非事实：** {r['forecast_caveat']}。估值盈利期：{c['earnings_period']}。\n\n**催化：** "+'；'.join(r['catalysts'])+"。\n\n**撤销/下修条件：** "+'；'.join(r['kill_conditions'])+f"。\n\n**保留异议与重大未决：** {r['minority_view']}。{V[t]['strongest_counterevidence']}。\n\n**外部链能证明什么：** {r['external_chain_limitations']}\n\n**多轮路径：** "+' → '.join(r['round_chain'])+"。各轮是不同问题复核，不以网页访问次数当证据强度。\n\n**可点来源：**\n\n"
 for k,s in enumerate(r['sources'],1):text+=f"- [{s['role']} {k}｜{s['published_date']}]({s['url']})：{s['key_information']}\n"
text+='''
## 候补与回归条件

|顺序|公司|本轮未选原因|回归条件|
|---:|---|---|---|
'''
for r in reserves:text+=f"|{r['rank']}|{r['ticker']}|{r['reason']}|{r['reentry_conditions']}|\n"
text+='''
## 共同风险与执行含义

这20家公司不是20个独立风险。NVDA、AVGO、MU、SNDK、CLS、SMCI、IREN以及PSIX/VST部分业务，共同受AI客户预算、融资与电力/建设交付影响；GPU与ASIC竞争可能改变份额，却未必改善整个组合总需求。MU与SNDK同受存储价格与扩产影响。SMCI/CLS收现、IREN融资、BDC并购和BABA资本开支又共同暴露于资本成本。

生物医药需要分开看已商业化的ARGX/ALNY、多管线BNTX和单事件KYTX；临床/监管不等经营周期，但同受风险偏好、支付和融资环境。ADBE/CRM共享代理软件替代与席位定价，不能把两只软件视作相互对冲。AGCO和CARR降低部分AI预算集中，却增加农户/住宅周期与利率风险。所谓缓冲是条件经营和资本资源，不是本金底线。

因此本报告不指定20等权或声称最大回撤可控。等待席所对应资金可以保持等待；SMCI/IREN/BDC/KYTX等门槛未出现时，名额代表跟踪优先级。任何一家新事实改变每股价值，都应与表中具体替代重做比较，不能为维护终榜而永久封锁回归。

## 模型、证据与审阅边界

20家均由冻结245公司索引核对；没有引入项目外证券。CLS为S1专项新增，经B1/B2、V1/V2和主席复核，不伪造首轮盲评票。VST用控制器PJM/Talen专项补查，不冒称S1/S2覆盖。各家已完成多角色、多轮的事实和计算审阅，**不表示未来预测或所有项目融资已经证实**；未解决问题在卡片内直接保留。

本稿数字来自04_verification/V2_models.json，三情景完整输入、公式、证券和币种信息保存在05_chair/主席最终裁决.json及V2文件。数学通过只说明给定参数可复算；利润率、净价、倍数、事件成功率和融资仍是研究判断。BNTX/KYTX内部已作临床概率调整，不再额外乘一个全公司成功概率；临床极端失败可比悲观价更低。

主席读入各轮及核验产物并重新裁决，外部网页实读归属保留为各研究者/控制器/V1/V2，不冒称主席重复访问。公司公告、SEC附件与转载可能同根，链接数量不是独立证据数量；每卡明确客户、竞争者、行业或合作方链能支持与不能支持的结论。完整证据日志在07_logs，冻结输入在01_inputs。
'''
(B/'06_final').mkdir(exist_ok=True)
text=re.sub('。{2,}','。',text)
(B/'06_final/最终20家公司投资研究.md').write_text(text,encoding='utf-8')
summary='# 主席最终裁决\n\n'+ '\n\n'.join(changes)+'\n\n最终20：'+', '.join(r['ticker'] for r in rows)+'。\n\n完整用户报告：[最终20家公司投资研究](../06_final/最终20家公司投资研究.md)。逐家结构化论证、三情景和来源：[主席最终裁决.json](主席最终裁决.json)。\n\n第20 CARR、第21 TSM的实质取舍及各候补回归，详见完整报告。没有按票数、单一模型均值或行业配额定榜；等待条件不因入选而消失。\n\n模型SHA256：'+obj['model_sha256']+'\n'
(B/'05_chair/主席最终裁决.md').write_text(summary,encoding='utf-8')
print(json.dumps({'count':len(rows),'project_members':obj['all_project_members'],'source_counts':{r['ticker']:len(r['sources']) for r in rows},'report_chars':len(text),'model_sha256':obj['model_sha256']},ensure_ascii=False))
