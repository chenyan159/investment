import json, hashlib, sys
from pathlib import Path

ROOT = Path(r'D:\investment\实验室\2026-10-12_3至6个月超高收益20家公司实验')
SEAL = '--seal' in sys.argv
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
notes = read('05_chair/主席条件卡工作稿.json')['candidates']
v1 = {c['ticker']: c for c in read('04_verification/V1_evidence.json')['companies']}
v2 = {c['ticker']: c for c in read('04_verification/V2_models.json')['companies']}
notes['MOD'] = dict(mechanism='存续冷却业务的实际数据中心订单、产能释放和低谷毛利恢复，让分拆后的经济利润持续期得到重估。',check3='预计11月首份拆分后财报核14.8%低谷DC EBITDA率是否恢复、留存费用和真实出货。10/1交割已发生，不列未来惊喜。',check6='预计2月后续结果核存续业务收入、经济利润、现金与4B长协转收入；前瞻FY28/29不是4月已实现利润。',touch='中低条件机会；两季增长/利润修复可触发，但需要超越普通恢复才能2倍。',hold='较低；5.1B收入和19.5%经济EBIT的强条件仍需订单与成本证明，不能只靠纯冷却标签。',left_tail='温水架构减少机械冷却内容、零件/扩产执行差或预付款逆转，令盈利与倍数一起回落。',opponents=['ICHR','CRDO','VRT'],dissent='19.5%经济EBIT已接近冻结FY28约20.3%调整EBITDA，折旧/SBC空间紧；收入扩大、利润率和27倍同时成立是强成功。',change='10/1分拆与156M偿债确认；新买入不含历史THRM分配。V2降低原18%NOPAT但仍需强假设；对ICHR复议后暂升最后席。')
notes['ACMR']['change']='9/30 backlog及10/28确定日支持上调；V2核8/4 A64.657388M+B4.991808M=69.649196M，纠正旧B5.021811M，剔投资收益并扣沪子NCI。'
notes['BNTX']['dissent']='2倍需约31.014B净归属管线/药物价值；现金不自动产生该增值，单一旧HR不能代Stage2，资产分成桥尚未逐项闭合。'
notes['RDW']['dissent']='V2强收入850M下2倍仍需5.604倍销售；7倍销售强价22.68隐含约73倍EV/NOPAT，融资现金不等盈利。'
notes['ADBE']['change']='X5/B2反向估值与控制器真实专项补齐复活；保留SBC。V2失望193.83只是条件，另看16EPS×11=176及14×10=140的竞争恶化压力，均非价格底。'
notes['SMCI']['dissent']='V2工作79.44已接近旧B2强81.6，不是更稳的期望。强135.84要求FY28运行速率85B、GM12.5%、19倍，超过FY27上限72B18.1%。CEO明确80B以上可能另需资金；模型净现金改善4.5B含4.725B债经济转换，不是4.5B经营现金创造。'
notes['SMCI']['change']+=' 末轮B2独开电话会补80B以上资金警示；保留右尾但进一步明确融资桥未闭合。'
notes['SMCI']['check6']+=' 若提前资本化85B收入，必须证明80B以上营运资金和可能增发的现金/股数对称，不将经济转换当法律已转。'
notes['ENPH']['dissent']='强核心EPS2.08×27=56.16，达2倍62.98另需941.16M净增量期权；2.3B是更强价格72.83的假设，不是最低门槛。失望1.55仅低盈利PE压力，非完整资产估值；当前净金融现金362.7M亦非地板，不能把旧937.7口径全额再加。'
notes['ENPH']['change']+=' 末轮B2区分核心56.16、2倍最低期权941.16M与强期权2.3B；研发留核心费用，新增商业化资金从期权净值扣。'
notes['UCTT']['dissent']='4B产能不是订单，当前GAAP经营率4.6%；V2强R4.5B/22%GM/10.5%费/20%税/23倍仍是大幅改善。扣未来NCI公允值552M后161.92；H1 FCF−100.2M、库存增加238.9M显示营运资金风险。'
notes['UCTT']['change']+=' 主席追问NCI后V2改扣192–832M研究公允值且不二次扣同一利润；强161.92仍过2倍。未来净债较现增加205.9–255.9M不是已获融资。'
notes['CLS']['dissent']='V2强44B/9.5%经济EBIT/28倍给700.98，仅过695约0.86%；44B较2027>65%增长对应33.825B起点高30.1%，须说明FY28提前定价。Q2 9.8%GAAP EBIT含TRS正收益，不能当9.5%经济率已达。'
notes['CLS']['change']+=' B2末轮独开10/26盘后与10/27 8ET官方日历及同期署名多头；排除与原始Q2数值冲突的转载，保留条件后段。'
notes['MOD']['dissent']+=' B2末轮17.5%经济EBIT只321.86、25倍只332.33；分拆后组合也可能优于旧集团，不能用旧20.3%跨口径直接判不可能。'
notes['MOD']['change']+=' B2末轮原始Q1与10/2 Oppenheimer署名短正文补审，260目标不背书345，但同时支持需求与供给执行风险。'
notes['VISN']['change']+=' V2未来回购150M对应15.63M股（研究均价9.5969），不能同时用20–25M股；失望231M股/550M现金是费用或烧钱压力，并不假设完成同样回购。'
notes['CRWV']['dissent']='旧A100续约只证明某批设备有残值，不证明所有新卡同价6年。45B净债/800M股是旧诊断假设；最终V2强成功用52B净债、850M股、37B收入、20.4%税后经济率及27倍，资本桥仍未闭合，不能混旧分母。'
order = ['MU','KYTX','SNDK','IREN','SMCI','AAOI','AMPX','PSIX','UCTT','VISN','BNTX','ENPH','ACMR','CRWV','LEU','ADBE','AOSL','CLS','RDW','MOD']
why = {
'MU':'较NVDA所需前瞻收入/持续期跃迁更接近当季经营；与SNDK相近机会下产品范围和金融现金更厚。',
'KYTX':'较ALNY小权益基数与Q4申报/PMS组合可由有限增量信息显著重估；保留小样本和融资二元风险。',
'SNDK':'10/29已定事件与NAND/SSD利润弹性胜过高估值AI质量替代；不是因股价低，亦不拿证券收益年化。',
'IREN':'Horizon2–4集中交付/验收比APLD普通股资本瀑布更容易在窗口检验，较NBIS起点更易给出2倍路径。',
'SMCI':'较CLS起点折价大，65–72B官方收入计划可与回款修复共同作用；必须接受优先股/转债经济摊薄，不能凭新模型高价自动升第一。',
'AAOI':'比POET真实批量收入更近、比COHR从更小盈利基数跃迁更陡，适合短期高右尾目标；资本/生产失败左尾极深。',
'AMPX':'CAMINUS Q1/27资格至量产有原始合作方计划，较TE/WOLF庞大建设融资和NVTS远期导入更贴近六个月。',
'PSIX':'比GNRC/PNR已有利润基础上的生产修复弹性更大，4–5经济EPS可检验；不是把Q2改善直接乘四。',
'UCTT':'现实Q3收入/EPS上台阶胜过ICHR尚需很大GM跃迁、AEHR与MRAM更远量产；薄利润和NCI仍需折价。',
'VISN':'较CC法律/债务尾部和FLNC新预警后的现金修复，存续业务与已出售资产现金更可检验，允许相近机会时较少融资风险胜出。',
'BNTX':'与ALNY相较有多个后期数据窗口而非单一期早期靶点，较KYTX融资续航长；仍需大额净归属管线重估，不是现金套利。',
'ENPH':'比NVTS既有业务/渠道与11月整机计划更具体，核心恢复加SST增量价值可成立；触及型重估强于期末站稳，不能当低风险。',
'ACMR':'有2.5B backlog和10/28已定更新，较AMBA/MRAM的远期产品量产更近；出口和NCI约束不因高订单而消失。',
'CRWV':'实际云交付运营和软件比APLD/部分新建者成熟，2倍可由执行和融资折价解除；保留其高债务左尾而非按现金负就一票否决。',
'LEU':'较OKLO/SMR已有浓缩业务及签约DOE项目，可由新增承购/资金去风险发生远期价值重估；没有确定新大单日，故条件层。',
'ADBE':'较CRDO/COHR需较小经济盈利跃迁，真实现金续航更强；如果市场对AI替代叙事逆转的机会接近，优先此较小融资风险路径。',
'AOSL':'较MRAM/NVTS有接近本季的AI/server组合转移与恢复产量，可先定价经济扭亏；相对ICHR较低权益和转型销售倍数提供不同路径。',
'CLS':'10/26与10/27近已定窗口及2027增长展望较COHR/TTMI更容易检验；执行质量较SMCI强但估值门槛更高，仅最后席。',
'RDW':'较AVAV更小权益基数及融资后续航有更陡触及右尾，较ASTS少跨几步发射/商业收费链；承认期末盈利支撑更弱。',
'MOD':'较ICHR从13.9%至20.5%GM还需证明定价权，MOD已有DC高增长与低谷毛利恢复线索更近；不靠压力情景绝对价格决定优先。'
}
invalid = {
'MU':'下一季量价/毛利或剔预付后现金明显回落，且无法由季度周数解释，NVDA或较低周期暴露替代上升。',
'KYTX':'完整BLA/CMC重大延误、PMS疗效不可复制或安全性恶化，BNTX/IONS替代；单纯受理不足以锁住2倍估值。',
'SNDK':'NBM定价被重谈、正常化经济利润/回款明显不及指引，MU优先且本席可退出。',
'IREN':'交付后仍不能验收收费或融资成本/摊薄显著上升，CRWV在同批设备现金回报清楚时上位。',
'SMCI':'两季经营现金/账龄不改善且低毛利无法正常化，CLS替换；治理/出口新证据可立即下调。',
'AAOI':'资格验收、量产良率或客户价格导致增长不形成毛利现金，COHR/CRDO替换。',
'AMPX':'CAMINUS资格/客户验收推迟且AR继续吞现金，PSIX或成熟盈利候选替换。',
'PSIX':'H2交付修复落空或SAR/正常税后归母现金仍差，PNR/GNRC替换。',
'UCTT':'收入虽增长但正常税/NCI后利润及现金不抬升，ICHR若自制件GM证据更强可替换。',
'VISN':'实际期末现金显著低于计划、总部成本不降、回购未兑现且主业弱，PLAB/PNR替换。',
'BNTX':'关键数据延期/效应竞争性弱或伙伴归属值大幅缩水，IONS或ALNY新实证胜出可替换。',
'ENPH':'整机演示无客户验证且核心去拉货后继续降，或2027试点完全后移，PSIX或MOD等实绩替代上升。',
'ACMR':'订单未转验收且应收恶化、管制切断关键需求，UCTT/PLAB更优。',
'CRWV':'经济GPU折耗后普通股回报不可成立、开票延迟或融资条件吞净值，IREN或资金更稳者替代。',
'LEU':'半年内无新绑定承购/资金、只重播已签奖项；或权证融资不能闭合工程，退候补。',
'ADBE':'两季有机ARR/创意残差和净付费没有改善，或推理成本/席位流失加速，CRDO/COHR若出现更强现金增长可替换。',
'AOSL':'AI局部增长未能推动集团GM/经济扭亏且工厂现金消耗继续，ICHR/PLAB替换。',
'CLS':'投资者日仅重述收入增速且经济增值/现金率不上修，MOD/ICHR或COHR可替换。',
'RDW':'旧Space有机增长停滞、已拨款订单弱或烧钱不降，AVAV优先。',
'MOD':'温水设计削减内容、DC利润不恢复、独立留存费用高，ICHR出现持续GM/现金证据时替换。'
}
final20=[]
for rank,t in enumerate(order,1):
 n=notes[t]; model=v2[t]; tier='A 重点翻倍机制' if rank<=6 else ('B 强条件机会' if rank<=13 else 'C 条件入选/竞争席')
 item=dict(rank=rank,ticker=t,tier=tier,selection_status='conditional_included_not_calibrated_probability',mechanism=n['mechanism'],why_selected=why[t],alternative=n['opponents'][0],alternatives=n['opponents'],condition=n['hold'],invalidator=invalid[t],major_dissent=n['dissent'],ruling='保留但接受反证约束；'+why[t],new_evidence=n['change'],three_month_vs_six_month={'three_month':n['check3'],'six_month':n['check6']},touch_2x=n['touch'],hold_2x_april12=n['hold'],relative_likelihood='相对等级只比较本池机制与窗口，不是统计概率；'+n['touch'],left_tail=n['left_tail'],price=model['price'],two_x_price=model['price']*2,scenario_summary=[{'branch':s['branch'],'price':s['result']['price'],'return_pct':s['return_pct'],'inputs':s['inputs'],'forward_operating_period':s['forward_operating_period']} for s in model['scenario_inputs']],two_x_inverse=model['two_x_inverse'],capital_bridge_status=model['target_cash_bridge']['status'],unresolved=model['unresolved'],v1_fact=v1[t]['independent_finding'],v1_event_3m=v1[t]['event_3m'],v1_event_6m=v1[t]['event_6m'],v1_counterevidence=v1[t]['counterevidence_unclosed'],source_urls=list(dict.fromkeys(v1[t]['source_urls']+model['source_urls'])),chair_external_access='none; citations inherited from actual role/controller accesses; chairman synthesized local evidence')
 item['displaced_candidate']=next((x for x in n['opponents'] if x not in order), n['opponents'][0])
 item['capital_bridge_residual']=model['target_cash_bridge'].get('chair_funding_review',model['target_cash_bridge'])
 item['model_assumption_boundary']=model['baseline_source_notes']
 if t in ['CLS','MOD','SMCI','ENPH']:
  item['late_rebuttal'] = next(x for x in read('03_round2/B2_末轮补充反驳.json')['companies'] if x['ticker']==t)
 if t=='SMCI': item['why_selected']+=' 相对未入选POET，也有已成规模收入和可检验正常利润，无需从资格批跨若干数量级收入来支撑估值。'
 item['coverage_roles']=[p for p in ['S1_ai_deep','S2_nonai_deep','B1_business_rebuttal','B2_valuation_rebuttal'] if any(x.get('ticker')==t for x in read('03_round2/'+p+'.json').get('companies',[]))]
 item['coverage_roles']+=['V1_evidence','V2_models','Astra_chair']
 if t in ['CLS','MOD','SMCI','ENPH']: item['coverage_roles'].append('B2_末轮补充反驳')
 if t=='ADBE': item['coverage_roles'].append('控制器_ADBE末位复活专项（非S1/S2）')
 final20.append(item)

pairs = [
('MU','NVDA','MU','现行季度收入/经济利润与2倍门槛之间距离较小；NVDA FY27非GAAP已含SBC，不能重复扣。','若MU量价/现金反转而NVDA前瞻盈利超目前门槛，顺序可逆。'),
('MU','SNDK','both_MU_first','两者都有盈利持续期重估；同类机会下MU现金与产品广度胜，SNDK纯度与10/29更近。','若NAND现金兑现明显胜DRAM/HBM且合同持久，可逆。'),
('KYTX','ALNY','KYTX','小权益的申报/PMS数据可改变风险价值；ALNY有真实药品但TTR版税约束利润，不能85%GM伪造低门槛。','ALNY若商业利润或临床功能数据支持净权益大跃升，可复活。'),
('KYTX','BNTX','both_KYTX_right_tail_BNTX_funding','KYTX绝对新增权益门槛小；BNTX多个后期读出且现金续航长，允许并存而非行业配额。','KYTX CMC/临床/融资恶化，BNTX上位；BNTX只旧信号不支持2倍。'),
('IREN','CRWV','both_IREN_first','IREN集中Horizon验收窗口更鲜明；CRWV运营/软件更成熟但债务和更新负担深。','IREN交付后不收费、CRWV同批GPU经济回报更清楚时逆转。'),
('CRWV','APLD','CRWV','真实云业务优于尚未闭合的项目NCI/优先资本瀑布，APLD通电非客户全部验收。','APLD权益瀑布/CHRN归属闭合且已收费现金优于CRWV，可换。'),
('IREN','NBIS','IREN','NBIS起点较高，2倍所需更远规模更大，非因质量不足。','NBIS订单/资金较快兑现而IREN延迟，可逆。'),
('AAOI','POET','AAOI','AAOI量产/收入基础更近，POET资格批与大融资不等收入证明。','POET验收量产及权益股数现金清楚而AAOI良率失败才复议。'),
('AAOI','COHR','AAOI_touch','AAOI更小收入盈利基数带来更陡六个月右尾，COHR成熟度不足弥补2倍规模/利润跳跃。','相近2倍证据时COHR较成熟利润/客户组合应优先。'),
('SMCI','CLS','both_SMCI_first','SMCI估值折价可由真实回款解除；CLS治理/平台好但2倍要更高经济盈利。','SMCI两季现金未修，CLS可优先。'),
('PSIX','GNRC','PSIX','PSIX产量恢复对小权益利润更敏感；GNRC多年合同/权证门槛不等当前保底采购。','PSIX治理/回款弱而GNRC现订单显著上修可替换。'),
('PSIX','PNR','PSIX','PSIX生产/EPS拐点较近，PNR Taco每股0.10–0.15增厚不足2倍。','PNR核心泳池真实补库存且利润上修、PSIX下滑时逆转。'),
('AMPX','TE/WOLF','AMPX','真实代工销量与CAMINUS Q1/27路径优于更重建设/融资或重整权利风险。','AMPX客户验收/应收失败、替代融资与交付均闭合则逆转。'),
('ENPH','NVTS','ENPH','既有电力电子业务及11月整机计划更可验证，但2027pilot非Q1量产。','SST无客户且核心弱、NVTS量产/现金出现实证可逆。'),
('VISN','FLNC/CC','VISN','现金存续业务可见性较FLNC新大幅预警后的融资修复、CC环境法律现金尾部更好。','VISN现金误用/成本不降，而FLNC资金及Houston兑现或CC责任/去债明显去风险可逆。'),
('UCTT','ICHR','UCTT','UCTT Q3现实收入EPS台阶更近；ICHR13.9至20.5%GM含更多尚未证明改善。','ICHR连续GM/自制件/现金兑现而UCTT归母率不提升可逆。'),
('UCTT','ACMR','both_UCTT_first','前者订单客户链更直接，后者backlog真增长但验收/政策/NCI较复杂，不能拿沪子全价值。','ACMR归母正常利润/回款超额实现时可上移。'),
('LEU','OKLO/SMR','LEU','已有浓缩业务与已签DOE框架，新增承购/融资可改变项目价值，非2027投产收入。','半年无新约束合同或成本失控则退候补。'),
('ADBE','CRDO/COHR/ALNY','ADBE','数学门槛更近且已有现金；相近机会先较小融资风险，仍须证明PE13至23的市场信念改变。','ADBE商业指标弱而替代出现真实超强利润上修，则逆转。'),
('AOSL','ICHR/PLAB/MRAM','AOSL_conditional','局部AI/server组合有本季验证，权益起点允许转型重估；承认仍亏而非假低风险。','整体GM/盈亏两季不改善、替代有现金/利润实证则换。'),
('CLS','COHR/TTMI','CLS_conditional','明确近投资者日、2027平台增长有现实基础，经济利润跨越仍很大，等待末轮成本反驳。','转售增收入不增值，或替代利润现金更强时换。'),
('RDW','AVAV/ASTS','RDW_touch_conditional','融资/优先转换让存续风险下降且较小基数有触及弹性；AVAV当前盈利更好但新订单已含指引。','RDW有机增长/已拨款订单不兑现，AVAV应换；期末低于触及。'),
('MOD','ICHR/CRDO','MOD_conditional','实际DC增长/低谷利润恢复较近，ICHR需更大GM改变、CRDO经济SBC压强盈利；不按非同分位压力价排序。','MOD冷却内容/费用恶化且ICHR自制件GM持续证明，ICHR复活。')]
pairwise=[dict(a=a,b=b,winner=w,ruling=r,reverse_if=x) for a,b,w,r,x in pairs]
reserve_list=[('ICHR','第一候补：首轮漏选，经控制器/B1/B2复活；GM与现金跨越仍大，待持续自制件改善可换MOD/AOSL。'),('AVAV','已盈利但FY27调整EPS3.02–3.34到2倍要求FY28强上修，LOCUST已含指引且负FCF；若RDW无有机改善可换。'),('CRDO','需求强但SBC后经济率和2倍前瞻收入/42倍要求高；强分支仍不足2倍，需新光收入/现金证明。'),('COHR','成熟光业务与NVIDIA非排他采购支持，但正常利润/规模到2倍跨度较大，等PhotonLink真实量产。'),('ALNY','真实商业现金和10/23早期数据保留；TTR版税毛利纠错后重审，单一期靶点不足2倍。'),('PLAB','归母利润和现金可检验，但大额JV现金非全归母，六个月高增长/倍数转变证据较弱。'),('PNR','低盈利估值修复有空间，Taco增厚小且并购资金成本真，核心泳池恢复未证实。'),('FLNC','真正困境高右尾仍在；9/16新预警使旧多头及接近盈亏平衡模型失效，先Houston/资金闭合。'),('NVDA','优质且可有右尾，按经济利润口径仍需较大前瞻规模重估，不因大市值自动排除。'),('AMBA','边缘AI可选性但近期改善含一次9M研发抵减，汽车量产窗不够清楚。'),('MRAM','政府/NRE跨期与工程进展是机会，但剔诉讼后仅0.438M季度经济净利，样片非量产。'),('CC','周期反转弹性大，但法律后续PV与高净债并存，同等机会VISN优先。'),('IONS','有10/26目标日且商业资产多样化；已失败项目不可复活，纯权益增值门槛仍高。'),('POET','融资改善续航但季度收入不足1M与大估值鸿沟大；等资格转真正量产。'),('APLD','项目运营与CHRN有价值，资本瀑布/NCI未闭合前不能把集团NOI全归普通股。'),('NBIS','业务基础有吸引力但起点/前瞻收入门槛高，融资与收购对价仍须闭合。'),('TTMI','M+N和并购扩张真实，Epiq融资与折旧/SBC后2倍门槛高。'),('AEIS','有盈利但800V大收入更远，六个月强分支仍未2倍，非技术质量否定。')]
reserves=[dict(reserve_rank=i+1,ticker=t,reason=r,revival_test=invalid.get(t,'出现更强订单、正常经济利润、现金或窗口内去风险证据后，与对应现选逐项复议；不是永久淘汰。'),model_coverage=t in v2,fact_coverage=t in v1) for i,(t,r) in enumerate(reserve_list)]
major_dissents=[
dict(issue='20席不足以支持20个高概率翻倍',ruling='明确A/B/C分层，C层条件等待；排名是本目标综合优先级，非校准翻倍概率或等权买入建议。'),
dict(issue='共享来源/票数不独立',ruling='首轮五角色扫描245、深读各不等；主席不重新宣称245全文核验，S1/S2相同结论不加权当独立事实。'),
dict(issue='强成功数字任意贴近2倍',ruling='V2独立四分支均研究假设，强成功并非预期；反解只显示门槛，新事实与同时相容性决定入选。'),
dict(issue='失败价格非同等严重程度',ruling='不按模型跌幅机械算赔率；ENPH/ICHR低利润PE压力未给残余资产价值，现金模型也非清算底。'),
dict(issue='低现金或负FCF是否一票否决',ruling='否。IREN/CRWV/AAOI等保留真实右尾，但清楚披露深跌与再融资条件；有相近证据才优先较稳者。'),
dict(issue='ALNY TTR版税被85%整体GM掩盖',ruling='主席发现后回流V2；未有相容组合前不凭526强价挤入。73–75%敏感性只能339.61–370.73，仍可凭新证据复活。'),
dict(issue='SMCI新强价135.84远高旧反驳81.6',ruling='输入和转换规则变化，不是新增公司事实。85B收入、12.5%GM、19倍联合兑现必须具体证明；近端GM约10.4–10.8%。'),
dict(issue='ADBE无小盘标签却复活',ruling='用户要求机制与相近机会下较少下行，不是小盘筛选；EPS增14.1%加PE13→23门槛可见，但ARR/净付费尚未证明。'),
dict(issue='FY28/29利润与半年窗口',ruling='允许市场提前定价完整前瞻年，必须由本窗事件降低不确定；绝不当4月已赚收入/已有现金。'),
dict(issue='剩余资本桥未完全审计',ruling='每卡保留V2状态。公式闭合不等未来现金、股数和经营条件已认证，不能给核验完成印章。')]
rounds=[
dict(round='R1',work='5个独立盲研角色各扫描245并深读重点；44并集作为竞争池，不是选票定论。'),
dict(round='R2',work='S1 AI深研、S2非AI深研；主席完整逐段读成熟正文，记录近期时间/成本约束。'),
dict(round='R3',work='B1业务和B2估值反驳；恢复ICHR等遗漏，对假下行和非GAAP盈利保持异议。'),
dict(round='R4',work='控制器定向重开原始/多空来源：AMPX、AAOI、KYTX/BNTX、FLNC、VISN、PSIX、RDW、AOSL/MRAM、CC、ADBE等。'),
dict(round='R5',work='V1事实/日历和V2独立38公司模型；主席逐卡读事实字段及模型正文，另反向算末位敏感性。'),
dict(round='R6',work='主席发现ALNY版税GM和UCTT NCI风险回流；B2复用角色补CLS/MOD/SMCI/ENPH，控制器重跑公式后方封卷。')]
change_log=[
dict(change='ADBE复活入条件席',reason='X5/B2反向估值+控制器独立专项+V1/V2，不能因非小盘先排除。'),
dict(change='ICHR复活后退第一候补、MOD暂入20',reason='有真实遗漏纠正，仍需GM13.9→20.5%与现金同时兑现；复活不等自动选入。'),
dict(change='VISN/BNTX相近机会下升层',reason='错误现金币种/退税/回购/总部费纠正后，仍有可核实留存资产，融资尾部较小。'),
dict(change='FLNC不入但可逆',reason='新Sept16warning改变旧UBS/接近平衡模型，强右尾保留而近期基本事实弱。'),
dict(change='CRDO/COHR质量不自动保位',reason='经济股酬、研发税与收入增长相容约束后，2倍要更远规模；ADBE等竞争。'),
dict(change='ALNY毛利纠错触发复议',reason='主席发现85%整体GM与Sanofi版税冲突，禁止不修模型即入选。'),
dict(change='最后5强反证',reason='分别固定收入下压盈利率/倍数：ADBE331.33、AOSL37.18、CLS600.59、RDW13.57、MOD306.16，均不足2倍，非硬贴成功价。')]
out=dict(status='DRAFT_UNSEALED_wait_V2_revision_B2_final_root_confirmation',role='Astra_chair_12',cutoff='2026-10-12 20:50 America/Los_Angeles',price_date='2026-10-12 normal session close',horizons=['2027-01-12','2027-04-12'],ranking_meaning='综合研究优先级，不是校准翻倍概率、确定收益预测或等权组合。所有情景为研究条件，工作中枢不是数学期望。',final20=final20,reserves=reserves,pairwise=pairwise,major_dissents=major_dissents,rounds=rounds,change_log=change_log,last_five_stress_file='05_chair/主席末位压力对决.md',evidence_scope='主席深读S1/S2/B1/B2全部正文、首轮汇总及选择性R1卡、控制器补充、V1逐卡核心字段、V2全文及选择性全模型；全245只读取结构化universe，不声称逐份重读。无主席独立外部访问，来源为角色/控制器真实访问之继承。',pending=['V2 ALNY版税与UCTT NCI修订','B2 CLS/MOD/SMCI/ENPH末轮','控制器修订后算术审核及关键纠错确认'],input_hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['04_verification/V1_evidence.json','04_verification/V2_models.json']})
out['major_dissents'][5]['ruling']='主席回流后V2将整体GM改72–75%、净利息改200–230M；强成功324.05低于2倍454.04，原强526.35撤回；更强右尾526.48仍存在，故可逆候补。'
out['rounds'][-1]['work']='主席ALNY版税GM与UCTT NCI异议被V2采纳；B2同角色完成CLS/MOD/SMCI/ENPH末轮原始及外部补审；控制器独立重写公式审核1120项0失败，仍区分算术与经济假设。'
out['change_log'].append(dict(change='末轮维持20与条件层',reason='B2承认四家公司右尾有机制，同时补SMCI80B融资、ENPH0.941B最低期权、CLS TRS/44B及MOD分拆口径约束；没有把强价当概率而机械换人。'))
out['pending']=['控制器最终关键纠错确认与V1最后事件边界复核']
out['input_hashes']['03_round2/B2_末轮补充反驳.json']=hashlib.sha256((ROOT/'03_round2/B2_末轮补充反驳.json').read_bytes()).hexdigest()
out['evidence_scope']+=' 已完整读取B2末轮四公司md/json与V2修订ALNY/UCTT/SMCI/ENPH，以及IREN/AAOI/CRWV/VISN资金复议；另深读冻结ADBE公司前200行、ALNY前105行及情景版税/利润相关段。'
for p in out['pairwise']:
 p['winner']={'both_MU_first':'两者入选，MU优先','both_KYTX_right_tail_BNTX_funding':'两者入选；KYTX右尾优先、BNTX融资更稳','both_IREN_first':'两者入选，IREN优先','AAOI_touch':'AAOI优先争取窗内触及','both_SMCI_first':'两者入选，SMCI优先','both_UCTT_first':'两者入选，UCTT优先','AOSL_conditional':'AOSL条件入选','CLS_conditional':'CLS条件入选','RDW_touch_conditional':'RDW条件入选，偏向触及','MOD_conditional':'MOD条件入选'}.get(p['winner'],p['winner'])
 if p['a']=='CLS' and p['b']=='COHR/TTMI': p['ruling']=p['ruling'].replace('等待末轮成本反驳','已接受末轮TRS、经济成本和44B收入反驳，仍仅条件入选')
for r in out['reserves']:
 if r['ticker']=='ALNY': r['reason']='真实商业现金和10/23早期数据保留；V2改74%强GM及220M净利息后强价324.05不足2倍454.04，更强右尾仍526.48。需要额外临床/商业证据，单一期靶点不足。'
if SEAL:
 out['status']='sealed_with_explicit_conditions_and_residuals'
 out['pending']=[]
 out['seal_boundary']='根控制器明确确认关键纠错与修订后算术审核后封卷；封卷是研究意见版本冻结，不代表经营预测、融资条件或全部资本桥已认证。'
 old_notes=read('05_chair/主席条件卡工作稿.json')
 old_notes['status']='superseded_working_notes_by_主席裁决.json'
 old_notes['purpose']='历史工作稿保留；当前20、顺序与条件全部以主席裁决.json/md为准。ACMR股数笔误已纠正，MOD补入避免补充文件遗漏。'
 old_notes['candidates']['ACMR']['change']=notes['ACMR']['change']
 old_notes['candidates']['MOD']=notes['MOD']
 (ROOT/'05_chair/主席条件卡工作稿.json').write_text(json.dumps(old_notes,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'05_chair/主席裁决.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# 主席裁决草稿：未封卷','',out['ranking_meaning'],'','信息截止2026-10-12 20:50洛杉矶；10/12正常收盘；检查2027-01-12、2027-04-12。V2修订、B2末轮及控制器确认前，以下20席可变。','','## 暂定20与条件价格','', '价格均USD/普通股或ADS；四分支不是概率分布，也不是统一严重程度下的风险区间。强分支高于2倍不证明更可能，工作中枢不是预期收益。','', '|排位|代码|层级|起点|2倍|失望|工作中枢|强成功|更强右尾|','|---:|---|---|---:|---:|---:|---:|---:|---:|']
for c in final20: md.append('|'+ '|'.join([str(c['rank']),c['ticker'],c['tier'],f"{c['price']:.2f}",f"{c['two_x_price']:.2f}"]+[f"{s['price']:.2f}" for s in c['scenario_summary']])+'|')
if SEAL:
 md[0]='# 主席裁决：20家公司分层优先级'
 md[4]='信息截止2026-10-12 20:50洛杉矶；10/12正常收盘；检查2027-01-12、2027-04-12。已吸收V1/V2修订、B2末轮及控制器关键纠错确认；条件与未闭合资本桥保留。'
 md[6]='## 最终20与条件价格'
md+=['','A层也不是高概率承诺；B层依赖强条件；C层尤其需要等待新增证明。既保留临床、工程、资本密集机会的高右尾，也允许有相近机制且融资稳的公司胜出。','','## 逐公司裁决']
for c in final20:
 md+=['',f"### {c['rank']}. {c['ticker']} — {c['tier']}",'',f"**选入机制与替代：** {c['mechanism']} {c['why_selected']} 具体竞争：{', '.join(c['alternatives'])}。",'',f"**三个月：** {c['three_month_vs_six_month']['three_month']}",'',f"**六个月：** {c['three_month_vs_six_month']['six_month']}",'',f"**触及与站稳：** {c['touch_2x']} 4/12仍在2倍：{c['hold_2x_april12']}",'',f"**失败左尾：** {c['left_tail']}",'',f"**重大异议与裁决：** {c['major_dissent']} {c['ruling']}",'',f"**移位/复活的新证据：** {c['new_evidence']}",'',f"**何时换人：** {c['invalidator']}",'',f"**核验边界：** V1：{c['v1_fact']} V2资本桥：`{c['capital_bridge_status']}`；成功输入与反解见JSON/V2，不是事实认证。",'','来源为其他角色实际原始访问的继承：'+'；'.join(f'[原始资料{i+1}]({u})' for i,u in enumerate(c['source_urls'][:3]))+'。']
 if c['ticker'] in ['IREN','AAOI','CRWV','UCTT','VISN']:
  md+=['',f"**资金残余：** {c['capital_bridge_residual'].get('numeric_gap','')} {c['capital_bridge_residual'].get('uncommitted','')}"]
md+=['','## 具体对决（可逆）']
for i,p in enumerate(pairwise,1): md+=['',f"{i}. **{p['a']} vs {p['b']} → {p['winner']}**：{p['ruling']} 逆转条件：{p['reverse_if']}"]
md+=['','## 最后五席主动反证','',f"详见[主席末位压力对决]({(ROOT/'05_chair/主席末位压力对决.md').as_posix()})。五席均存在收入达成仍不足2倍的成本/倍数组合，因此是条件席，不能用满20数量掩盖证据差异。",'','## 候补与复活']
for c in reserves: md+=['',f"- **{c['ticker']}**：{c['reason']}"]
md+=['','## 重大异议及处理']
for c in major_dissents: md+=['',f"- **{c['issue']}**：{c['ruling']}"]
md+=['','## 轮次、变化与读取范围']
for r in rounds: md+=['',f"- {r['round']}：{r['work']}"]
for r in change_log: md+=['',f"- {r['change']}：{r['reason']}"]
md+=['',out['evidence_scope'],'',out.get('seal_boundary','仍待：'+'；'.join(out['pending'])+'。')]
(ROOT/'05_chair/主席裁决.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
log=dict(role='Astra_chair',external_accesses=[],external_access_statement='主席无独立外部请求；没有把继承来源升级为本角色独开。',local_read_scope=out['evidence_scope'],inherited_logs=['07_logs/S1_sources.json','07_logs/S2_sources.json','04_verification/V1_evidence.json','04_verification/V2_models.json'],input_hashes=out['input_hashes'])
(ROOT/'07_logs/chair_sources.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':out['status'],'final20_count':len(final20),'pairwise_count':len(pairwise),'tickers':order},ensure_ascii=False))
