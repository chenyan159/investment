import json,pathlib
P=pathlib.Path(r'D:\investment\实验室\2026-10-12_20家公司多角色实验')
u=json.loads((P/'03_round2/round1_union.json').read_text(encoding='utf-8-sig'))
raw='''NVDA^客户GPU采购意愿有AWS交叉证明，真正争议是供货商支持融资后现金何时回收，而非AI有没有需求^逐季核应收天数、经营现金/经营利润、担保兑现；将AWS 2027–28部署按季度而非一次确认^AVGO^保留核心；现金折扣不等于推翻增长
MU^高利润已实现；35%累计收入协议不是每年35%锁价，更不能把HBM当全部利润^拆DRAM/NAND/HBM价格和位元、SCA保障、税及资本支出；普通存储ASP回落10/20%单变量敏感性^SNDK^保留核心；不采用无证据腰斩基准
ADBE^低估值修复需要创意净收费稳定，集团和AI ARR增长会被并购、文档、提价掩盖^按恒汇率剔Semrush，跟踪非BP&C数字媒体残差、续约席位与积分净收入、保留SBC利润^CRM^保留核心；倍数修复不能独立担负全部上涨
AVGO^前置软件许可证与ASIC整机收入增长可能没有同等经常性利润；采购和租赁信用暴露相关^拆软件前置/经常收入与现金；逐客户验收及支持义务匹配，不将126.8B承诺当当期损失^NVDA^保留；低于只按AI收入总量排序
PNR^同行销售增长使仅去库存解释不足；2027恢复可能其实要求夺回份额^连续两季PNR渠道售出、售入及库存联查；剔34.9m退款、Taco新增息费后复算^CARR^保留但降低确定性；若份额持续丢失由CARR替代
ALNY^上市积压释放转一线患者决定增速；30%高段版税限制利润，nucresiran不能提前贡献2027CM盈利^按初治/转药、患者持续年、净价核销售；从PN/CM注册日期桥接批准与收入^ARGX^保留成长名额；RNAi平台不整体赋成功概率
ARGX^UNITY无效已发生，肌炎DM亚组不显著；现有gMG/CIDP收费仍独立有效^剔Sjögren收入；分IMNM/DM标签；CIDP12周87%留存不代替一年续费^ALNY^保留；收购与新适应症只作有条件上行
BNTX^近端临床去风险可以重估，但pumitamig主要全球验证在2028–29，现金烧损与权益分享不可遗漏^逐资产3–18月读出、随机性、经济权益；现金扣18月预算，BMS利润50%而非总销售相加^KYTX^保留分散右尾；不是2027盈利反转股
KYTX^26人单臂强信号足以支持高风险机会，但95%持续率有筛选分母，BLA/CMC比总TAM关键^核完整26人一年功能与免疫治疗停用、安全；申报受理和制造核查；融资后每股而非企业值^BNTX^保留小额事件名额；不能等批准才承认全部期权价值
PSIX^毛利回升真实；电力不等于数据中心，税备抵转回不可支持持续EPS^剔38.3m税利好，跟踪电力收入、订单/机罩交付、27%毛利与应收、关联交易^MOD^保留进攻名额；需正常税率后盈利
FLNC^9月预警1.9亿美元EBITDA下降仅6500万是递延毛利，其余损失不会随收入自动回来^逐项重算延迟赔偿65m/新品35m/质量25m；现金与质保准备；订单验收而非管线^PSIX^第20条件名额；先验证修复，不因风险高直接否决
POET^Lumilens客户融资真实增强需求，但下游数十亿合同不是POET收入；OpenLight替代路线已送样^核不可取消采购与客户激励抵减后收入、良率和毛利；充分稀释股数；不能套完整光模块单价^CRDO^候补；订单及净收入兑现后可回归
IREN^最低付款有约束力但需验收；设施成本/更新GPU/本金会削弱GPU两年回本说法^按各期SOW验收、最低量、延迟抵扣、退款与融资做项目股权现金；设施残值另作敏感性^NBIS^保留右尾；排位高于更昂贵且未闭合融资者
CLS^新平台进入生产不是CLS取得全部系统价值；HPS包含于CCS且客户高度集中^分1.6T网络/AMD/OpenAI量产份额、物料过账与8–9%经营率；核客户供料/营运资金^JBL^保留；S1补充支持其取代部分高PS光学股
SNDK^NBM比普通订单更强；上涨仍依赖高价执行、现金税正常化与客户履约^读底价/上限/担保和位元覆盖，拆价格/数量及JV投入；不把HBF样品计入2027大收入^MU^保留；与MU共同存储风险须限合计
CRDO^AEC已盈利，光是第二引擎而非已同等成熟；SBC后盈利与200.84价格的基准空间不足^核新光产品独立收入/毛利、大客户应收集中，新增采购变现；反算价格需要的经济EPS^CLS^强候补；收入与利润超模型或降价回归
AAOI^800G仅Q2约12.8m，净利转正主要税收益，1.6T资格订单不能当已交付^核Q4 1.6T资格、70–80m实际发货、正税前利润、Digicomm回款及增发^CRDO^暂缓；产品兑现可迅速回归，非永久淘汰
MOD^液冷总需求不保证冷水机内容；拆分后不能重复计算MOD与分给股东的Gentherm^核最新分拆交割证券、每MW冷机/CDU净内容、14.8%利润率回升、剔预收现金^CARR^保留；必须独立证券核验再定目标
BDC^RUCKUS整合提高规模也提高利息与执行负担，工业底座不自动保护杠杆权益^用收购后债务和息费，拆RUCKUS有机收入/EBITDA与协同，核FCF去杠杆^CARR^候补；执行改善后可替换周期名额
MCHP^库存修复已进财报，但固定成本吸收与PCIe定点不能都按最快兑现^核渠道天数、利用率与终端消耗；12定点逐项投产季度；扣优先股/利息^AGCO^候补；需更强每股收益或价格优势
AGCO^PTx跨品牌能力真实，但20亿美元目标已后移；核心利润主要在欧洲^剔汇率、关税退款与融资收益；北美去库存和经销商售出，PTx付费安装/毛利^MCHP^保留非AI周期弹性；不以2029目标当12月成果
VST^PPA是更强客户证据，但已对冲电量不会同步吃到AI现货价上涨^逐电厂2027–28解锁电量/容量价格、PPA起期、并购债息与普通股FCF^PNR^保留；低于直接全部重估电量的估值
PGR^极低CR可能包含准备金释放；份额优势可延续但近期增长不等于新单持续强劲^剔往年有利发展，分承保批次留存/新单/获客；常态CR+2/4点敏感性^RNR^保留一个保险名额；不是浮存金现金底
CRM^Agentforce ARR口径扩展与并购令增长难比；GAAP经营利润停滞且债息上升^恒口径ARR、付费消耗减席位流失；剔战略投资收益，新增息费/SBC后EPS^ADBE^候补；暂由ADBE承担软件价值修复
BABA^保诚真实上线反驳AI全无采用，但云利润与模型应用亏损/扩股现金缺口必须合并^分云外部收入、AI应用亏损、capex与电商补贴；用扩股后ADS及汇率桥^ADBE^保留地域/估值分散；不能称净现金无下行
CARR^2026数据中心20亿目标意味着H2约15亿交付；非数据中心仍左右集团利润^核H2验收/产能、住宅售出与欧洲利润；不要把跨分部DC重复加总^MOD^保留；相对较低预期且有双恢复路径
IONS^pelacarsen失败不等于平台失效；bepirovirsen日本批准、sefaxersen三期中期阳性有真实新价值^删除失败里程碑；TRYNGOLZA4万美元标价下付费治疗年/净价，DAWNZERA竞争；分GSK/Roche权益及2028债务^ALNY^第一梯队回归候补；新药现金桥通过可替换FLNC/较低回报防御股
SMCI^收入增长能很大但普通股回报取决薄利润及资金占用，不能因过往争议机械排除^独立审计和客户验收、存货应收、每季经营现金；边际毛利覆盖融资成本^CLS^候补；现金/审计核验通过可争夺第20
COHR^客户支持增强量产，但融资/采购支持与经营现金是不同证据^核激光/模块产能良率、订单兑现、客户支持条款；每股现金而非客户总capex^CRDO^候补；光学二选一需价格优势
NBIS^签约增长真，当前价格可能已资本化多数乐观部署^按实际已供电机房验收、capex资金与完全稀释股数对合同爬坡建模^IREN^候补；融资无损闭合或价格修正回归
ASTS^发射成功与运营商计费之间仍有覆盖及容量门槛^逐卫星运行/许可/覆盖、付费用户和资费分成，不以测试通话替代收入^KYTX^非AI右尾候补；商业收费证据可回归
AMPX^航空客户已有收入但新合同未必转为足额盈利^核Stark采购约束、交付和良率、现金跑道与股数^PSIX^候补；毛利和批量订单过关回归
ENPH^住宅修复是近端核心，AI SST主要不在12个月利润窗口^剔safe-harbor提前备货和45X，核安装消耗与欧洲渠道^FLNC^候补；终端复苏可回归
RDW^国防无人机比航天远景更近，但整合/合同利润决定权益^分已拨款订单与管线、并购后现金及新股^PSIX^候补；有资金订单转现金可回归
NVTS^800V架构右尾合理但量产2028–29多在窗口外^核已付费设计NRE、订单投产表及2027收入不重复计TAM^POET^等待；3–18月实际定点收入足够才回归
AMZN^AWS增长不能独立证明新增AI资本回报^折旧更新周期与资本开支后FCF，客户付费而非供给容量^NVDA^优质候补；现价相对上行不足
BJ^新店复制有成长，会员数/费收入可能被促销和新店成本抵消^核同店、续费与新店回收期^AGCO^候补；高收益偏好下让位周期弹性
KR^低PE可修复但食品竞争与资本回报决定重估^核电商边际利润、同店销量与债务后回购^PNR^候补；稳定但右尾不足
QCOM^专利现金可靠，数据中心支付门槛不是确定销售^剔税项、逐合同资格及汽车/IoT利润^AVGO^候补；新业务商业兑现回归
RNR^低倍数受灾害和软市合理约束^分灾害常态损失、续约价格与第三方资本费用^PGR^候补；不同时堆多个保险
CB^承保分散有质素但价格未提供足够右尾^核事故年盈利和保费增长质量^PGR^候补；估值回落或增长上修
DOV^液冷是增量，法规强制替换延后影响兑现^核真实订单/耗材需求，剔法规拉货^CARR^候补；较低经营弹性
EME^积压高但工程合同风险在成本及现场人力^按项目固定价比例/人工成本/现金预付款拆积压^MOD^候补；价格要求较高
GFS^硅光增长不能直接填平成熟制造回报^核长期协议最低量、利用率与补贴后资本回报^MCHP^候补；盈利兑现再比较
HUBB^电网需求持久但基准上行偏薄^核公用事业订单交期和并购有机增长^VST^候补；价格改善
JBL^成熟现金优于纯故事但当前基准约等于价格^分客户供料、AI增量利润与回购^CLS^候补；价格或盈利出现差异
META^广告收费真实但AI支出缺少单独回收披露^增量广告利润减AI capex、SBC和折旧^ADBE^候补；估值空间不够
MKSI^复苏与降债有双弹性但现金回收需实现^核WFE/PCB分项销量、净债及息费^BDC^候补；周期订单更强可回归
MSFT^质量高不等于12个月高收益^核Azure增长对capex/折旧与Copilot净增付费^NVDA^候补；高预期限制回报
PENG^内存与系统集成经济不同不能混用高倍数^拆过账采购与自有毛利、运营现金^MU^候补；现金转正再升位
PLAB^现金含少数权益，扩产会消耗而不立即增利^归属现金、CAPEX与高端设计订单^MCHP^候补；低风险叙事不足选进20
RMBS^内容提升真实但新平台采用是时间门槛^核MRDIMM出货、IP收入确认及每DIMM价值^MU^候补；基准低于价格
TEL^多行业底座增强但稀释AI弹性^核AI实际连接器内容、车用订单和利润^CARR^候补；相对回报不足
TSM^先进制造实证强但当前价格与地缘尾部限制名额^核海外成本/折旧、先进封装利用率与ADR^NVDA^候补；价格改善可回归
TTMI^高层板真实瓶颈但收购后净债增加^核良率、M+N交付、收购债息/股数^CLS^候补；现金与去杠杆达标回归
UCTT^产能不是订单，应收库存可能先吞现金^核客户采购、库存变现、经营现金和融资^MKSI^候补；现金流转正回归
WDC^供给纪律强但高盈利锚可能仍在高估正常现金^剔SNDK证券收益、每TB价格/成本与现金税^SNDK^候补；合同价格与更优买价回归
WM^成熟收费及capex下行利好，收益弹性不如进攻候选^核医疗整合协同/客户留存、RNG实际利润^PGR^候补；防守价值不等于本轮最优名额'''
rows={}
for line in raw.splitlines():
 t,c,v,a,p=line.split('^');rows[t]=(c,v,a,p)
rows['ON']=('汽车/工业复苏与AI电源内容提升可共存，但并购与资本占用限制每股杠杆','核车用/工业终端消耗、SiC利用率、收购后股数债息与AI真实收入','MCHP','候补；盈利或价格更优再回归')
top=['NVDA','MU','ADBE','AVGO','PNR','CLS','ALNY','SNDK','IREN','PSIX','BNTX','ARGX','MOD','CARR','AGCO','BABA','VST','KYTX','PGR','FLNC']
deep='NVDA MU ADBE AVGO PNR ALNY ARGX BNTX KYTX PSIX FLNC POET IREN CLS SNDK CRDO AAOI MOD BDC MCHP AGCO VST PGR CRM BABA CARR IONS SMCI COHR NBIS ASTS AMPX ENPH RDW NVTS'.split()
sources=[]
def S(i,t,url,date,n):sources.append(dict(id=i,tickers=t.split(),url=url,published_date=date,access='B1 independent web open + relevant body/find read; URL discovered from frozen report or prior log, not independent root event',reading_notes=n,independent_visit=True))
S('B1-01','IONS','https://www.royaltypharma.com/news/royalty-pharma-announces-update-on-novartis-phase-3-topline-results-for-pelacarsen/','2026-09-04','HORIZON主要终点失败；不预计再付里程碑；Spinraza分享2028升45%，累计550m后回归。')
S('B1-02','IONS','https://www.gsk.com/en-gb/media/press-releases/hibsago-bepirovirsen-approved-in-japan-as-first-and-only-functional-cure-for-chronic-hepatitis-b/','2026-08-24','日本首次批准；限定病毒标志物和前治疗条件，三期功能性治愈19%；Ionis授权，不是全部GSK销售归Ionis。')
S('B1-03','IONS','https://www.roche.com/media/releases/med-cor-2026-09-23b','2026-09-23','37周蛋白尿中期终点阳性；105周eGFR仍继续，不能当已确证长期肾功能获益。')
S('B1-04','NVDA AVGO','https://press.aboutamazon.com/aws/2026/8/aws-and-nvidia-to-deliver-2-million-additional-gpus-and-next-generation-infrastructure-for-agentic-and-physical-ai','2026-08-26','客户侧计划2027–28追加200万GPU，同时使用AWS自研芯片及EFA；支持需求，不提供不可取消采购金额。')
S('B1-05','NVDA','https://mlcommons.org/2026/09/mlperf-inference-v6-1-results/','2026-09-16','Rubin/Vera Rubin为Preview，性能成绩与商业规模验收分开。')
S('B1-06','BABA','https://www.prudential.com.hk/en/about-us/newsroom/prudential-launches-brand-new-ai-underwriter-powered-by-alibaba-cloud/','2026-09-09','真实客户全面上线；数日缩至分钟，未披露阿里净合同收入/利润。')
S('B1-07','PNR','https://ir.poolcorp.com/pool-corporation-reports-second-quarter-results-confirms-annual-earnings-guidance-range-excluding-ceo-transition-costs/','2026-07-23','Q2销售+2%，维护稳定，库存同比+4%由Q1+14%下降；不是PNR专属库存。')
S('B1-08','PNR','https://investor.hayward.com/investor-news/news-details/2026/Hayward-Holdings-Reports-Second-Quarter-Fiscal-Year-2026-Financial-Results-and-Confirms-2026-Guidance/default.aspx','2026-07-29','北美销售+9%，价格及数量共同增长；反对把PNR下跌全归宏观。')
S('B1-09','FLNC','https://www.leag.de/de/news/details/spatenstich-fuer-gigabattery-boxberg-400-leag-clean-power-startet-grossbatterieprojekt-in-sachsen/','2026-08-31','Boxberg 400MW/1600MWh，HyperStrong合作；客户多供应商，不是FLNC独占。')
S('B1-10','IREN','https://www.sec.gov/Archives/edgar/data/1878848/000187884826000015/exhibit103-partnerstatem.htm','2026-02-05','SOW验收最低GPU数量、5天验收/15工作日修复及延期抵扣/终止条款，合同不是无条件现金。')
S('B1-11','POET CRDO AAOI COHR','https://openlightphotonics.com/newsroom/openlight-introduces-3-2t-dr8-silicon-photonics-pics-as-well-as-1-6t-dr8-lro-and-lpo-variants','2026-03-10','3.2T原型及1.6T资格样品订单；替代路线推进，不证明大规模收入，但否定唯一技术路线。')
S('B1-12','BNTX','https://www.sec.gov/Archives/edgar/data/1776985/000177698526000054/a991bntx_q22026pressreleas.htm','2026-08-04','现金证券16634.2m欧元、251.204m流通股、ADS1:1；回购不能等同未来全面缩股。')
S('B1-13','ADBE','https://www.adobe.com/cc-shared/assets/investor-relations/pdfs/01906202/au56y4ter.pdf','2026-09-10','Q3收入6.76B、GAAP经营利润2.35B、ARR27.50B、CFO2.52B；当前收费真实。')
S('B1-14','MU','https://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Fiscal-Fourth-Quarter-and-Full-Year-2026-Results/','2026-09-30','Q4收入54.23B、GAAP净利37.70B、CFO43.97B；高利润非只分析师远期预测。')
S('B1-15','ALNY IONS','https://www.astrazeneca.com/media-centre/press-releases/2026/update-cardio-ttransform-phase-iii-trial.html','2026-07-09','主要CM复合终点失败；基线稳定剂患者无治疗效果；不能以所有沉默疗法自动优于标准治疗。')
S('B1-16','ARGX','https://argenx.com/news/2026/press-release-3376934','2026-10-08','UNITY因无效停止，无新安全信号；不推翻既有gMG/CIDP收入。')
S('B1-17','POET','https://lumilens.com/news-insights/lumilens-emerges-with-900m-in-funding','2026-08-06','客户宣布累计融资超过900m、生产数据中心交付及数十亿协议；自身披露不等于POET供应份额。')
dis=[]
for idx,c in enumerate(u['candidates'],1):
 t=c['ticker']; ch,ve,alt,ver=rows[t]
 paths=list((P/'01_inputs/frozen/基本面/公司调研/结果').rglob(t+'_*.md'))
 local=[{'path':str(paths[0].relative_to(P)),'locator':'正文核心判断及决定性观察，约5–30行；明确仅重点27家实际段落深读，其余读取首轮主张后快速差异审查','access':'B1 local segment read' if t in deep[:27] else 'inherited R1-R5 thesis / not claimed full body read'}] if paths else []
 dis.append(dict(id=f'B1-D{idx:02}',ticker=t,claim=' / '.join(v.get('thesis','') for v in c['views']),why_it_changes_selection='直接改变近端收入/现金/每股兑现或当前价格容错；与'+alt+'竞争同一风险预算，而不是单列无后果风险',bull_case_fairly_stated=c['views'][0].get('thesis',''),challenge=ch,verification_method=ve,primary_sources=[s for s in sources if t in s['tickers']],local_evidence=local,alternative_ticker=alt,provisional_verdict=ver,unresolved='以上执行核验尚未全完成；外部已实读事实见primary_sources，未读原始来源的事项仍属冻结上游主张',depth='重点论辩' if t in deep else '快速差异图',price_anchor=c['reference_price'],price_interpretation='不由股票涨跌断言市场隐含；首轮条件基准/现价仅检验容错',horizon='3–6月看季度/事件验证；6–12月看收入和现金；12–18月看经营兑现，窗口外平台价值只作期权'))
for d in dis:
 c=next(c for c in u['candidates'] if c['ticker']==d['ticker'])
 d['original_model_horizons']=[{'role':v.get('researcher'),'months':v.get('horizon_months'),'base_price':v.get('base_price')} for v in c['views']]
 d['normalized_comparison']='主席统一18个月；原12/15/18月目标不可直接比较总上行或机械按时间放大。须重建截至2028-04-12现金/股数/临床事件；B1未完成此独立计算。'
# CLS由S1补充重要性：在首轮并集之外，另留独立争议。
if 'CLS' not in [d['ticker'] for d in dis]:
 ch,ve,alt,ver=rows['CLS'];dis.append(dict(id='B1-D59',ticker='CLS',claim='S1补充：网络/AI系统交付利润在窗口内放量',why_it_changes_selection='S1中枢483.08相对347.5存在约39%条件空间，优于部分光学高PS候选；非本轮独立估值',bull_case_fairly_stated='现有HPS/CCS交付真实，新客户平台已进入生产阶段',challenge=ch,verification_method=ve,primary_sources=[],local_evidence=[{'path':str(next((P/'01_inputs/frozen/基本面/公司调研/结果').rglob('CLS_*.md')).relative_to(P)),'locator':'正文9–25行，B1实读'}],alternative_ticker=alt,provisional_verdict=ver,unresolved='继承S1估值和外部核验，不算B1独立访问；需终轮证券计算',depth='重点补充',price_anchor=347.5,horizon='6–18月'))
out=dict(role='B1_business_rebuttal',cutoff='2026-10-12 19:40 America/Los_Angeles',covered_tickers=[c['ticker'] for c in u['candidates']]+(['CLS'] if 'CLS' not in [c['ticker'] for c in u['candidates']] else []),disputes=dis,resurrection_candidates=[{'ticker':t,'condition':rows[t][1],'alternative_to_replace':('FLNC' if t=='IONS' else rows[t][2]),'reason':rows[t][0]} for t in ['IONS','POET','AAOI','CRDO','SMCI','BDC','MCHP','NBIS','ASTS']],provisional_top20=top,excluded_reasons={t:rows[t][3]+'；回归核验：'+rows[t][1] for t in rows if t not in top},factor_concentration={'AI_capex_direct':['NVDA','MU','AVGO','CLS','SNDK','IREN','PSIX','MOD'],'AI_secondary':['CARR','VST','FLNC','BABA'],'biopharma':['ALNY','ARGX','BNTX','KYTX'],'not_equal_weight_recommendation':True,'warning':'20个名称远少于20个独立风险；GPU部署/客户融资冲击会同时影响芯片、内存、代工、电力设备和云。MU+SNDK同一存储价因子；生物医药仍分临床与支付，不是完全独立。'},external_independent_body_reads=17,inherited_reports=['02_round1/R1_cashflows.json','02_round1/R2_valuation.json','02_round1/R3_external.json','02_round1/R4_upside.json','02_round1/R5_diversification.json','03_round2/S1_ai_upside.md'],limitations='经营反驳与条件名额，不是完成估值核验或最终可立即买入20；未读取S2，尚未生成时不等待。')
(P/'03_round2/B1_business_rebuttal.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'07_logs/B1_sources.json').write_text(json.dumps({'role':'B1','sources':sources,'failed_access':['Intellia FDA acceptance URL: internal error','Kyverna one-year-data URL: internal error','Tower September 17 URL: internal error'],'independent_visit_not_independent_root_event':True},ensure_ascii=False,indent=2),encoding='utf-8')
md=['# B1 经营、催化与替代反驳','',out['cutoff'],'','重点不是把风险最大的股票排光，而是识别哪个事实能在3–18个月改变收益分布。首轮58家全部有差异问题；CLS按S1补充单列。17个外部原始/客户/竞争者页面在B1实际打开并查读相关段落；他人来源不冒充独立访问。','', '## 暂定20与裁决变化','',', '.join(top),'','这是条件研究名额，不是等权持仓或全部即刻买入。FLNC为第20条件席，IONS和SMCI最有机会竞争；若最终原始与证券核验不过，不能借此表自动过关。NVDA/MU/AVGO/CLS保留进攻性；不为防守凑满保险和消费。CARR/AGCO用于提供有经营弹性的非纯AI路径。','', '## 首要决策问题','', '1. PNR恢复不是无争议的渠道自然回补。POOL和Hayward增长反驳纯宏观说，但不能据此直接证明PNR永久丢份额；最有价值的新证据是PNR产品售出与渠道推荐。','2. MU当前利润是真钱，SNDK锁价机制比普通订单强。应拆合同覆盖、普通内存价格、资本和税，不能将所有周期悲观叠成基准，也不能把短缺永续。','3. IREN合同最低付款很有价值，但SOW明确验收、延期抵扣与终止条件；设施、GPU更新、本金共同决定股东现金。','4. FLNC恢复收入不等于恢复现金。6500万递延毛利以外的1.25亿赔偿/质量/新品成本需要单独解决；在高风险偏好下仍可留条件右尾席。','5. IONS允许回归。失败削去旧里程碑和扩展，但GSK批准、Roche阳性是合作方直接证据；最强反方是新药低净价需大量付费治疗年、未来版税分成与债务。','6. BNTX/KYTX可因临床去风险先重估，不要求18个月已经盈利；也不把窗口外商业化当近期现金。','', '## 每家公司差异图与可执行核验','', '|公司|公允乐观论据|决定排名的挑战|核验/回归条件|最强替代|暂判|','|---|---|---|---|---|---|']
for d in dis:md.append('|'+ '|'.join(str(d[k]).replace('|','/') for k in ['ticker','bull_case_fairly_stated','challenge','verification_method','alternative_ticker','provisional_verdict'])+'|')
md+=['','## 来源与实读记录','']
for s in sources:md.append(f"- {s['id']} | {','.join(s['tickers'])} | {s['published_date']} | [{s['reading_notes']}]({s['url']})")
md+=['','## 原模型期限，必须交主席统一','', '|公司|原提名的月数|','|---|---|']
for d in dis:
 md.append('|'+d['ticker']+'|'+'; '.join(str(x['role'])+': '+str(x['months']) for x in d.get('original_model_horizons',[]))+'|')
md+=['','统一比较点应为2028-04-12（18个月）。12/15/18个月回报不可直接比大小，不对临床事件与周期盈利机械线性拉长；统一模型需重建股数、现金消耗及可兑现事件。上述暂定顺序以经营机制和价格容错为定性参考，不是期限统一后的数学排名。','', '已阅读Controller_平台候补复活审查.md；GOOGL新增争议为剔投资收益和融资后普通股权益，Cloud增长强不代表资本开支自给；与ADBE比较现有利润折价，与IREN比较融资质量。AMZN/MSFT/TSM保留可逆候补，不能因本轮名单已有20而拒绝强证据回归；控制器实读不计入B1的17次访问。','', '## 保留异议','',out['factor_concentration']['warning'],'','“已在价格体现”无法从价格本身证实。本轮用首轮与S1条件中枢/现价检验验错空间：CRDO、AAOI、POET当前中枢空间较弱，但其右尾未被否认；价格下行或新增利润验证均可逆转排位。没有将这三个候选永久排除。','',out['limitations']]
(P/'03_round2/B1_business_rebuttal.md').write_text('\n'.join(md),encoding='utf-8')
(P/'07_logs/B1_stage_notes.md').write_text('阶段1：读取章程、58并集与首轮逐家公司主张。已向控制器发送七项优先争议。\n阶段2：正文核心段落深读NVDA MU ADBE AVGO PNR ALNY ARGX BNTX KYTX PSIX FLNC POET IREN CLS SNDK CRDO AAOI MOD BDC MCHP AGCO VST PGR CRM BABA CARR IONS。完整正文非全部通读，不能宣称58家重新独立研究。\n阶段3：17外部原始/客户/竞争者页面实读，三次失败不计访问成功；网址从冻结正文/日志取得，根事件可能与他人重合。\n阶段4：读取S1开头及候选表，新增CLS高优先；全部目标价仍继承，B1不冒充独立估值。\n输出全部在实验目录，无Git、无其他目录写入。',encoding='utf-8')
print(json.dumps({'covered':len(out['covered_tickers']),'disputes':len(dis),'top20':len(top),'sources':len(sources),'missing_union':sorted(set(c['ticker'] for c in u['candidates'])-set(rows))}))
