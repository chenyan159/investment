import json
from pathlib import Path
p=Path(r'D:\investment\实验室\2026-10-12_20家公司多角色实验')
s1=json.loads((p/'07_logs/S1_sources.json').read_text(encoding='utf-8-sig'))['sources']
s2=json.loads((p/'07_logs/S2_sources.json').read_text(encoding='utf-8-sig'))['sources']
src={s['id']:s for s in s1+s2}
# 每行独立问题，竖线依次ticker/替代/多方主张/公平乐观路径/核验挑战/方法/暂决/来源id。
raw='''NVDA|AVGO|R5收入600–680B却采用18EPS基准|Rubin与推理扩张可使收入越过680B；非GAAP已含SBC|600–680B、73%GM不足支持18EPS，投资收益也不能经常化|按季度建rev×GM−含SBC费用−净利息，税16–18%，约24B股；18EPS反解收入|保留高位，修正基准EPS而非否决公司|NVDA_Q2
MU|SNDK|低倍数加结构性存储短缺|SCA和HBM可令高毛利维持超过传统周期|已修正219.3B EBIT/185.3085B净利，剩余争议是88%GM持续性与现金归属；不得复用90%OPM|FY27Q1 GM86.25%为起点，分价格/bit/成本桥至2028；融资性客户存款单列、SBC保留|保留前列；不能因周期一律压回谷底|MU_Q4
ADBE|CRM|低调整PE意味着巨大预期差|存量订阅与AI增售、回购可同时驱动每股复苏|调整45%OP含8.3ppt薪酬加回；免费剔SBC高估经济利润；回购是否仅抵稀释|GAAP35%→加合理非经常项→经济OP；与CRM同口径FCF减SBC比较，AI净增ARR单列|保留，经济EPS倍数重排|S2-01
PNR|CARR|Taco提升水处理增长|交叉销售和泵阀组合可提升渠道价值|1.4B已交割，不能只加540M收入及含协同20%EBITDA而不计债务利息|交易前后净债桥、利率与协同爬坡分开；54–84M假设年息做敏感性|保留，融资后EPS过关才领先CARR|S2-04,S2-05
AVGO|NVDA|高调整OPM及ASIC放量|定制ASIC与软件共同支持现金利润扩张|Q3调整OP20.095B剔除2.019B SBC后经济OP18.076B；FD股数不替代持续薪酬成本|GAAP15.955B→无形摊销及合理一次性调整→18.076B；2028 SBC用收入占比/授予计划预测|保留，经济估值可能逊NVDA|AVGO_Q3
CLS|SMCI|AI交换机业务强增长及经营杠杆|产品组合升级可提高毛利与周转|GAAP Q2 OP458.3M含TRS收益，现金流反向调整104.1M；调整利润又剔SBC，两端都不能照搬|剔TRS非经营重估，保留SBC；拆现金结算与股权结算薪酬，核营运资本和新股|保留；不能用被TRS抬高GAAP证明低估|CLS_Q2
IREN|NVDA|合同ARR与预付降低扩张资金压力|按时验收和较高利用率可实现极强经营杠杆|ARR非收入，45–55%预付和90%特定融资不能叠加为全部135%；现金附履约义务|逐项目capex/预付款/贷款/权益融资桥；扣GPU经济更新、利息、稀释后与NVDA比较|小额条件保留，净现金底不成立|IREN_FY26
PSIX|CARR|发电瓶颈使低市值利润弹性大|Q2较Q1销售+18.6%、毛利+420bp，H2生产计划向上|同比销售−21%、毛利27.1%，2025税收益1.27EPS不重现；SAR重估也影响费用|去税收益及SAR非持续收益，订单转收入再扣工厂爬坡成本；不用40%GM|保留高弹性；要真实订单门槛|PSIX_Q2
SNDK|MU|NAND超景气与大回购|企业SSD和新商务协议延长现金兑现|Q4增长约2/3来自价格，不能全归结构性bit增长；GAAP43.97高于调整39.25需剔非持续项|对价格/bit/成本三维敏感性；Q1 EPS44–46与高点PE折价分别列，回购须资金约束|候补偏保留，MU优先但可逆|SNDK_Q4
ALNY|ARGX|AMVUTTRA扩张将利润杠杆兑现|沉默剂竞争减弱及心肌病新患者持续增长|账面未来版税/开发融资负债约1.720B与1.011B可转债；不能既全扣负债又重复扣全部同现金流，或完全忽略|产品净价×患者数→COGS/商业/R&D/SBC→版税融资实际支付、现金税、FD；对手ARGX用同口径|保留；12.42EPS不能直接作证据|S2-07
ARGX|ALNY|商业化现金与适应症扩张兼具|H1已真实盈利并有0.7B经营现金，扩适应症不是全靠融资|H1基本EPS13.47不等于摊薄未来EPS；税益、地区权益、特许权成本决定31EPS质量|USD报表，ADS比例由20F核；税前产品利润→正常税→FD，新增适应症仅按时点贡献|保留；盈利质量暂优临床期权|S2-12
BNTX|KYTX|现金缓冲与肿瘤读出右尾|多条管线成功及合作分担研发减少单点风险|16.6342B欧元证券不是美元；剩余烧钱、合作权益和或有里程碑不得三重叠加|ADS1:1已核，251.204M流通股；欧元净现金滚到2028后换汇，管线分地区/权益/概率计rNPV|保留但现金不是无损底|S2-17,S2-20
KYTX|BNTX|小市值一次治疗临床期权|若SPS注册批准及制造支付顺利，小体量可有多倍收益|2028跑道包含未提款；rNPV0.9B必须展示成功概率与销售峰值，不能纯指派EV|现金199.427M−烧钱−债务+融资；分审批/制造/支付概率，融资价格4–8美元影响新股|仅小额期权；不作缓冲核心|S2-15
BABA|CRM|云与电商现金双驱动重估|外部云收入与利润加速可抵消零售补贴|RMB利润/USD ADS错配及配售会造假低PE；云资本开支与快商补贴不能同时零化|8普通股/ADS逐条原文件核，19.8925B普通股转2.4866B ADS，净利归属/汇率/资本开支敏感性|保留条件席位，证券桥须通过|S2-34
MOD|PNR|分拆后纯冷却业务重估|数据中心增长更集中可享更高经营质量倍数|Oct1分拆后买家没有旧股0.44619THRM分配；旧合并EPS不能估新MOD|交割公告/备考持续业务EPS、对价及净债、FD股数桥；旧回报含THRM只用于原股东|待持续业务模型，不能用错误高目标抢席|S2-28
VST|PNR|稀缺电力资产和并购提升现金收益|数据中心长期合同可锁价并提高利用率|并购EBITDA若加全额而净债留交易前，EV/EBITDA会虚低；套保/核燃料成本不可漏|交易交割前后债务、现金、少数权益/回购；EBITDA到维护capex、税、利息的股权FCF|条件保留；与PNR比较融资后收益|LOCAL
BDC|MCHP|订单改善与解决方案转型|工业网络/数据基础设施需求推动毛利质量提升|订单836M不能按全部当年收入；调整EPS受收购摊销及SBC口径影响|订单取消/交付、毛利、营运资本、收购债务后每股经济FCF；MCHP用同口径|保留，需订单转现金|S2-25
MCHP|BDC|库存去化后利润修复|固定成本吸收带来大于收入的盈利弹性|低谷后调整EPS大升可能主要吸收改善，净债及支付利息/股息限制回购|渠道sell-through、库存天数、产能利用、GAAP到经济EPS；扣债务利息不省略|保留，比较真实去库存速度|S2-27
AGCO|DE|农业低谷与精准技术期权|渠道正常化、成本控制带来EPS复苏|Q2名义收入−1%但剔FX−3.7%；22M关税退款不可年化，技术展示非销售|区域量价/FX、退款、融资利息及经销商库存独立；以正常化利润比较DE|条件保留，需库存周期证据|S2-21
PGR|RNR|承保优势与规模复利|保单份额扩张、家庭捆绑可抵消费率软化|低灾害CR及投资收益不可永续；投资资产绝非股东净现金|已赚保费×正常化承保率+经常投资收益−税，扣优先/少数；与RNR统一灾损概率|保留分散席位，排名取决正常化EPS|S2-31
CRM|ADBE|低估现金流与Agentforce变现|既有客户分发与数据平台提供增售入口|含收购ARR不等于有机AI收入；FCF加回SBC不能与ADBE经济利润直接比较|拆有机ARR/收购/转签，FCF减持续SBC及并购投入，收入增长与回购贡献分开|强候补可复活，ADBE并非天然更好|S2-29
POET|CRDO|光引擎认证成功后的非线性增长|融资带来跑道，多客户量产可支撑明显高于现金的EV|basic173.058M/全潜在261.415M已含78.734968M权证，不再加客户22.921408M；不得全用26.25行权价|逐批行权价/归属/采购条件表；模型选全转换股数+对应现金或库藏股法，不能混搭|候补小额右尾，股数核验后才排序|POET_FS,POET_WARRANT
FLNC|BDC|储能订单与低价反转|制造改善与库存释放可带来经营现金迅速改善|9/16已将收入降2.4B、EBITDA−200M；旧−10M模型作废，现金中性是目标|逐季度GM/违约赔款/担保现金/预付款，穿透Up-C及税收应收协议；融资后FD|暂候补，恢复证据可复活|FLNC_RESET
SMCI|CLS|低价服务器和液冷放量|若17.6%GM及现金回收持续，估值可迅速超CLS|单季EPS1.70和GM17.6%未由本角色原10K复核；收入增长可被应收/存货吃掉|V1核原10K；V2剔一次性毛利、供应商返点/融资，FCF对净利、稀释和客户集中|强复活，证据不足是待核不是否决|LOCAL
IONS|ALNY|自主商业化抵消失败管线|多产品启动成功可显著提升可控利润|版税融资和2028债务不能被销售倍数模型隐藏；失败CM试验需从资产价值剔除|按产品权益收入减商业/R&D/版税分出，债务575M及到期安排；付费患者而非启动数|候补复活，赔率可能优于ALNY但缓冲弱|S2-10
CARR|PNR|制冷和热管理渠道转型|数据中心与商业HVAC可抵消住宅周期|并购整合及有机/汇率增长需拆；不能直接给全部业务数据中心倍数|分部利润与净债/利息、商誉摊销桥；同期限PNR融资后EPS比较|强候补，PNR融资后若不占优应回归|S2-26
CRDO|POET|AEC渗透及高增毛利|客户扩张和组合改善仍可保持高增长|调整OP48.2%不含87.979M SBC，经济OP约29.8%；当季收购授予可能不全经常|授予归属明细拆一次性与持续，保持两种SBC敏感性，不把87.979M直接永久四倍|候补；经济利润核后与POET比较|CRDO_Q1
TSM|AVGO|先进工艺稀缺性|高利用率及定价可覆盖海外厂成本|USD ADR对应5普通股；TWD净利不能除ADR股数后不换汇，非经营收益不可年化|净利TWD÷普通股×5÷USD/TWD；经营利润/税/海外补贴敏感性|复活候选；可替代最高估值AI供应链|TSM_Q2,TSM_ADR
RNR|PGR|低倍数和回购|费率韧性与第三方收费能支持高ROE|合并利润含外部资本，低灾害/投资涨价不等于普通股经常EPS|净利→非控股/优先/已实现与未实现→正常化灾损；同PGR风险资本比较|候补；不可机械取最低PE|S2-32
VRT|MOD|液冷和电力系统积压订单|规模服务与交付可推动超预期利润|高估值已反映部分增长，backlog不等FCF；重组加回不可常年零成本|积压订单转化GM/营运资本、SBC和持续重组成本；MOD持续业务同倍数比较|复活候选，MOD权益不清可优先|VRT_Q2
ON|MCHP|工业汽车复苏加并购|终端恢复与组合升级带来利润弹性|旧ON 4.7EPS不能用于交换股及融资后的新权益；稀释是否抵消协同|原公告交换比例、FD、债务利息/整合费用，分期协同；同MCHP利润恢复比较|复活候选，先核证券桥|LOCAL'''
dis=[]
for i,line in enumerate(raw.splitlines(),1):
 t,a,c,b,q,m,v,ids=line.split('|')
 refs=[src[x]['url'] for x in ids.split(',') if x in src]
 if not refs: refs=['02_round1/R5_diversification.json','03_round2/S1_ai_upside.json','03_round2/round1_union.json']
 dis.append(dict(id=f'B2-{i:02}',ticker=t,claim=c,why_it_changes_selection=f'{t}与{a}争夺席位；'+q,bull_case_fairly_stated=b,challenge=q,verification_method=m,sources=refs,source_ids=ids.split(','),alternative_ticker=a,provisional_verdict=v,unresolved='2028-04-12观察点的完整证券/经济利润桥与替代同口径模型仍交V1/V2；本反驳不宣称已完成全部模型'))
calc=[
 dict(id='NVDA-EPS',formula='(revenue*0.73-opex)*(1-0.17)/24',unit='USD B / B shares',inputs={'revenue':[600,680],'opex':[40,50],'tax':.17,'shares':24},result_range=[(600*.73-50)*.83/24,(680*.73-40)*.83/24],eps18_required_revenue=(18*24/.83+45)/.73,interpretation='经济利润示范；opex40–50、税17%、24B股为可辩护测试假设不是指导；不扣重复SBC，不计公允价值收益'),
 dict(id='AVGO-OP',formula='20.095-2.019',economic_op_B=20.095-2.019,economic_margin=(20.095-2.019)/29.591,gaap_op_B=15.955,interpretation='允许无形摊销/一次性重组加回但保留SBC；不是纯GAAP估值'),
 dict(id='CRDO-OP',formula='230.641-87.979',economic_op_M=230.641-87.979,economic_margin=(230.641-87.979)/479,interpretation='收购相关加速SBC需拆，不能机械永久年化本季度高点'),
 dict(id='ADBE-OP',formula='45%-8.3%',economic_op_margin=.45-.083,interpretation='非经常成本允许加回，持续薪酬保留；税口径仍需另桥'),
 dict(id='BNTX-CASH',formula='16634.2/251.204366',cash_EUR_per_share=16634.2/251.204366,interpretation='ADS1:1；未扣未来烧钱/负债，不是美元下限；FX须情景化'),
 dict(id='PNR-INTEREST',formula='1.4B*rate*(1-24%)/160M',rates=[.04,.05,.06],eps_drag=[1400*r*.76/160 for r in [.04,.05,.06]],interpretation='全债务融资与160M股为压力示范非已核融资事实；若现金支付须计现金机会成本；另计协同，不能双扣'),
 dict(id='KYTX-DILUTION',formula='150M / issue_price',issue_prices=[4,6,8],new_shares_M=[150/4,150/6,150/8],interpretation='仅演示150M融资不固定25M股；融资净现金加入但同时扣烧钱/债务；不能凭空得到rNPV'),
 dict(id='POET-COUNTS',formula='261.415-173.058',incremental_potential_M=261.415-173.058,warrants_M=78.734968,other_potential_M=261.415-173.058-78.734968,interpretation='父控制器已纠正股数作为待原文件逐批核验输入；22.921408M客户权证不能再加；现金依各行权价和实现条件')]
top=['NVDA','MU','ADBE','AVGO','PNR','ALNY','ARGX','BNTX','IREN','PSIX','CLS','BABA','BDC','MCHP','PGR','AGCO','KYTX','SNDK','CRM','VST']
out=dict(role='B2_valuation_rebuttal',cutoff='2026-10-12 19:40 America/Los_Angeles',price_date='2026-10-12',proposed_common_observation_date='2028-04-12',date_control='章程原统一12个月；控制器提出最终18个月。S1仍为2027-10-12，所有价格必须重新建模而非改标签；2030目标禁直接平移。',covered_tickers=[d['ticker'] for d in dis],disputes=dis,independent_demonstration_recalculations=calc,provisional_top20=top,top20_status='讨论席位，非已证实排序或立即买入清单；未经V1/V2及主席不得终选',resurrection_candidates=['SMCI','CARR','MOD','IONS','CRDO','POET','FLNC','TSM','RNR','VRT','ON'],method='纠正事实/算术确定错误；对预测保留多路径，不能以最悲观假设叠加成基准；经济利润保留持续SBC同时允许合理非现金摊销调整。')
(p/'03_round2/B2_valuation_rebuttal.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
readids=['NVDA_Q2','AVGO_Q3','CRDO_Q1','CLS_Q2','S2-01','S2-15','S2-17','S2-12','S2-07','S2-21','MU_Q4','IREN_FY26','PSIX_Q2','FLNC_RESET','SNDK_Q4']
notes=['FY27 nonGAAP已含SBC；Q2其他收益7.773B不经常化','Q3 GAAP OP15.955B，调整20.095B，SBC2.019B','调整OP230.641M，SBC87.979M，GAAP OP120.700M','Q2 TRS收益104.1M，SBC19.3M，GAAP OP458.3M','FY26 GAAP OP35%，调整45%，SBC8.3ppt','199.427M现金证券；24.883M贷款，2028跑道含未提款','现金证券16.6342B EUR；251.204366M股；ADS1:1','H1基本EPS13.47 USD，经营现金0.7B、金融资产现金5.2B','未来版税/开发融资负债0.258570+1.461510B；可转债1.010981B','Q2剔FX收入−3.7%，北美22M关税退款','Q1 GM86.25%调整/85.95%GAAP；客户存款12.747B列融资流','ARR明示并非GAAP收入，预付款比例基于GPU及附属capex','Q2销售152.5M、GM27.1%、EPS0.73；2025税收益1.27EPS','9/16收入指导2.4B，EBITDA−200M，现金中性只是目标','Q4收入8.965B，价格贡献约2/3增长；Q1调整EPS44–46']
sources=[]
for sid,n in zip(readids,notes):
 s=src[sid]
 sources.append(dict(id=sid,url=s['url'],publication_date=s.get('published',s.get('publication_date')),read_status='B2 independently opened and read relevant original body/table with web tool',short_reading_note=n))
sources.append(dict(id='S2-28',url=src['S2-28']['url'],read_status='opened title/body inventory; detailed securities verification delegated V1/V2'))
sources.append(dict(id='S2-04/S2-05',url=src['S2-04']['url'],read_status='opened successfully but follow-up body extraction internal error; facts attributed to S2, not counted toward 15 body reads'))
(p/'07_logs/B2_sources.json').write_text(json.dumps(dict(role=out['role'],cutoff=out['cutoff'],independent_primary_documents_body_read=15,sources=sources,other_sources='Dispute references not in above body-read list are specialist/round1 provenance or verification leads, not falsely represented as independently body-read.'),ensure_ascii=False,indent=2),encoding='utf-8')
md=['# B2 估值、证券与数字反驳','',f'覆盖{len(dis)}家公司；15份外部原始正文/表格独立实读。截止2026-10-12 19:40 LA，价格Oct12。候选观察日2028-04-12，S1原12个月价格不可直接移植。','',out['method'],'','## 最能改变名单的已核问题','', 'NVDA 18EPS收入桥不成立；AVGO/CRDO/ADBE持续SBC不可免费排除；CLS连GAAP利润也有TRS公允价值收益，不应机械采用最低利润；BNTX欧元现金不能直接当美元每ADS现金；KYTX现金跑道含条件性未提款。','', '## 逐家公司交叉问题','']
for d in dis:
 md += [f"### {d['id']} {d['ticker']} 对比 {d['alternative_ticker']}",'',f"多方主张：{d['claim']}。公平乐观路径：{d['bull_case_fairly_stated']}。",'',f"反问：{d['challenge']}。核验：{d['verification_method']}。",'',f"暂决：{d['provisional_verdict']}。保留异议：{d['unresolved']}。",'', '来源：'+'；'.join(f'[{u}]({u})' if u.startswith('http') else u for u in d['sources']),'']
md += ['## 独立示范重算','', '以下是算术复核与假设敏感性，不冒充完整18个月估值。','']
for c in calc: md += ['```json',json.dumps(c,ensure_ascii=False,indent=2),'```','']
md += ['## 暂定20讨论席与复活','',', '.join(top),'','复活候选：'+', '.join(out['resurrection_candidates'])+'。MOD/SMCI等未核完应保留等候位置，不能因未知等同否决；这些候补能在证券桥通过后替换边缘入选者。','', '本轮不提供假精确概率与目标价；本角色负责提出可改变选择的具体问题，V1/V2完成统一观察日事实及计算，主席裁决。']
(p/'03_round2/B2_valuation_rebuttal.md').write_text('\n'.join(md),encoding='utf-8')
(p/'07_logs/B2_stage_notes.md').write_text('# B2阶段笔记\n\n已读根AGENTS及章程，禁止实验目录外写入/Git/spawn。父消息给定纠错优先于首轮旧数。\n\n第一批向控制器交付NVDA/AVGO/ADBE/SBC、日期统一问题；第二批交付CRDO/CLS TRS/BNTX ADS/KYTX跑道。\n\n独立阅读15份正文，另PNR二文件后续正文提取失败明确降级；MOD公告仅打开不冒充全证券核验。所有外部材料发表于截止前。31家逐一反问，每家有具体替代、公平多头路径和核验法。8个算术敏感性示范由脚本计算。未使用2030价或机械最悲观基准。\n',encoding='utf-8')
print(json.dumps({'covered':len(dis),'top20':len(top),'body_read':len(readids),'files':['03_round2/B2_valuation_rebuttal.md','03_round2/B2_valuation_rebuttal.json','07_logs/B2_sources.json','07_logs/B2_stage_notes.md']},ensure_ascii=False))
