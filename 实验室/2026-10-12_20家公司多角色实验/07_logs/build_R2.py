import json,csv,math
from pathlib import Path
B=Path(r'D:/investment/实验室/2026-10-12_20家公司多角色实验')
U=json.loads((B/'01_inputs/universe.json').read_text(encoding='utf-8-sig'))
by={x['ticker']:x for x in U}
deep='ADBE CRM ORCL BABA NVDA AVGO ALNY BNTX PNR ENPH PGR RNR ON MCHP SMCI BDC CLS MOD JBL MKSI MU SNDK STX WDC PLAB GFS QCOM VST'.split()
sources=[
('ADBE','2026-09-10','https://www.adobe.com/cc-shared/assets/investor-relations/pdfs/01906202/au56y4ter.pdf','Q3收入6.76B、GAAP EPS4.62、FY26 GAAP EPS指引18.12–18.17；不用27.67远期调整EPS直接估值'),
('NVDA','2026-08-26','https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2027/','Q2收入96.2B；已披露规模强，不证明客户全周期回报'),
('AVGO','2026-09-02','https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial','Q3收入29.591B、FCF13.7B；软件与AI权益分别估计'),
('ALNY','2026-07-30','https://investors.alnylam.com/press-release?id=ddc78e15-7847-4066-8fdb-3562023a60f4','TTR指引由4.4–4.7B下调到4.2–4.5B；二线积压正常化，不能仅看产品增长'),
('PNR','2026-07-28','https://www.sec.gov/Archives/edgar/data/77360/000007736026000042/q22026pressrelease.htm','Q2收入933M、约170M泳池渠道去库、35M退款；2026调整EPS指引4.60–4.80'),
('BDC','2026-07-30','https://investor.belden.com/financials/quarterly-results/default.aspx','Q2收入750M、订单836M，RUCKUS于7/1完成；动态页面仅采用Q2已公开内容'),
('BNTX','2026-08-04','https://www.sec.gov/Archives/edgar/data/1776985/000177698526000054/a991bntx_q22026pressreleas.htm','Q2资金证券16.6342B EUR；经营持续消耗现金，不当作清算底价'),
('MOD','2026-10-01','https://investors.modine.com/news/news-details/2026/Modine-Completes-Spin-off-and-Combination-of-its-Performance-Technologies-Business-with-Gentherm/default.aspx','PT分拆完成；9/28记录日每原MOD股0.44619 THRM；156M现金偿债；10/12新买MOD无历史分派权利'),
('PNR','2026-10-01','https://investors.pentair.com/news-releases/news-release-details/pentair-completes-acquisition-taco-group-holdings','Taco完成约1.4B收购；新买家承接新增债务及经营，无完整交割后报表'),
('MU','2026-09-30','https://www.sec.gov/Archives/edgar/data/723125/000072312526000018/a2026q4ex991-pressrelease.htm','Q4收入54.229B、GAAP净利37.70B、FY26收入133.188B；近期利润强但异常周期不能永续'),
('SMCI','2026-08-11','https://ir.supermicro.com/news/news-details/2026/Supermicro-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Financial-Results/default.aspx','FY27收入指引65–72B；独立工作模型仅60B，现金及优先融资另扣'),
('SNDK','2026-08-05','https://investor.sandisk.com/static-files/c75d1bee-c5c9-4e5a-8605-302c1aeac59b','Q4 PDF p11 NBM底价合同93.9B、季度末RPO59.8B及期后91.1B；不能将两个RPO相加')]
queries=['site.adobe.com investor 2026 Q3 earnings September 10 2026','site.investor.nvidia.com fiscal 2027 second quarter results 2026','site.investors.broadcom.com 2026 third quarter financial results','site.investors.alnylam.com 2026 second quarter financial results','site.investors.pentair.com 2026 second quarter results pool inventory 170','site.investors.biontech.de 2026 second quarter financial results cash 16.6','site.investor.belden.com 2026 second quarter RUCKUS','site.investors.modine.com October 2026 spin off Gentherm','site.investors.micron.com 2026 fourth quarter September 30 2026 54.229','site.investor.sandisk.com 2026 fourth quarter 93.9','site.ir.supermicro.com fiscal 2026 annual results 39.06','site.investors.pentair.com October 1 2026 Taco completes']
S=[dict(id='R2-W%02d'%(i+1),ticker=t,published_date=d,url=url,opened=True,source_level='原始IR/SEC；公司自述与公司预测仍非独立验证',finding=f) for i,(t,d,url,f) in enumerate(sources)]
log={'role':'R2_valuation','cutoff':'2026-10-12T19:40:00-07:00','queries':queries,'external_sources':S,'read_inputs':['01_inputs/universe_screen.csv','01_inputs/universe.json'],'local_sources':[{'ticker':t,'company':by[t]['sources']['company'],'read_scope':'首部经营/财务事实＋统一经营模型及资本结构相关段落；非全篇逐字阅读'} for t in deep],'additional_company_overviews':['AMZN','MSFT','ENS'],'six_source_classes':['产业背景：全球AI需求与Token经济框架、AI产业链瓶颈与反证指标总表','行业：核酸药物与免疫治疗','公司：28家公司模型深读','情景：ADBE、PNR、BNTX、MOD、VST及MU摘要','对比：ADBE、PNR、BNTX、MU摘要','金融：245公司完整冻结CSV/JSON'],'limitations':['没有读取其他研究者首轮；上游报告结论不是新的独立事实。','部分批量工具输出截断；随后对决定性模型分段重新读取，未将截断内容当作已见事实。','除外部核验的12个文档外，其余经营事实仍依赖冻结上游研究，留给V1核验。']}
(B/'07_logs/R2_sources.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')

# 金额及股数统一十亿美元/十亿股；全部未来参数是R2研究假设。
R=[]
def add(t,h,mode,vals,thesis,anchor,cat,kill,risk,lines,status='条件参与',confidence='中'):
    z=dict(rank=len(R)+1,ticker=t,thesis=thesis,horizon_months=h,operating_assumptions=anchor,catalysts=cat,kill_criteria=kill,key_risks=risk,confidence=confidence,status=status,price=float(by[t]['finance']['最新价格']),currency='USD',financial_currency=by[t]['finance']['financial_currency'],price_date=by[t]['finance']['价格日期'],evidence=[{'path':by[t]['sources']['company'][0],'lines':lines,'level':'冻结上游研究，事实与其经营模型分开；本轮仅对部分事实重新打开原始来源'}]+[{'url':s['url'],'published_date':s['published_date'],'id':s['id'],'level':'本轮已打开原始来源'} for s in S if s['ticker']==t])
    scenarios={}
    for name,v in zip(['bear','base','bull'],vals):
        if mode=='earnings':
            ni,shares,mult=v;p=ni/shares*mult;formula=f'归属正常化净利{ni}B / 稀释股数{shares}B × P/E {mult} = {p:.2f}'
        elif mode=='ev':
            eb,mult,nd,shares=v;p=(eb*mult-nd)/shares;formula=f'(EBITDA {eb}B × EV/EBITDA {mult} - 净优先索取权{nd}B) / 稀释股数{shares}B = {p:.2f}'
        elif mode=='cash':
            fcf,shares,mult=v;p=fcf/shares*mult;formula=f'付息后且扣SBC经济成本的FCFE {fcf}B / 经济稀释股数{shares}B × 股权现金倍数{mult} = {p:.2f}'
        elif mode=='bntx':
            cash,profit,mult,prob,shares=v
            pipe=profit*mult*prob/(1.14**5);p=(cash+pipe)*1.1206/shares;formula=f'(2028-04目标净资金EUR {cash}B + 2033归属正常化NOPAT EUR {profit}B × {mult}倍 × 临床/支付兑现折扣{prob} / 1.14^5) × USD/EUR 1.1206 / {shares}B ADS = {p:.2f}'
        scenarios[name]={'price':round(p,2),'formula':formula,'inputs':v,'input_status':'E：R2条件假设；非公司指引/非校准概率','upside_pct':round((p/z['price']-1)*100,1)}
        z[name+'_price']=round(p,2)
    z['valuation_formula']={'method':mode,'unit':'USD/share；经营金额B、股数B；BNTX经营为EUR并单独换汇','scenarios':scenarios,'net_debt_treatment':'利润/FCFE倍数已扣利息，不能再次全额扣净债；EV方法另扣目标日净债及优先索取权。','share_treatment':'目标股数均为明确假设；当前快照股数仅作起点，不把回购授权视为已执行。','probability':'不计算机械概率加权收益；BNTX兑现折扣为估值敏感参数，非统计成功率。'}
    z['wait_price_for_30pct_base_upside']=round(z['base_price']/1.3,2)
    R.append(z)

add('ADBE',12,'earnings',[(15.0*.400,.400,11),(19.65*.390,.390,17),(23*.380,.380,22)],'保留SBC后的现有订阅盈利就可支持修复，无需AI业务成为独立巨头。','FY27基准收入28.7B、GAAP EBIT10.15B；扣净费用0.2B与23%税约7.66B净利。悲观收入约26B/创意缩水，净利6B；乐观收入30B/利润8.74B。12月价格资本化FY27获利，未搬用2029目标。',['3–6月：年报/CEO交接、提价周年后的ARR','6–12月：文档与企业付费抵消创意席位流失'],['连续两季有机ARR低于5%且创意订阅下降','GAAP利润率跌破30%而费用无法调整'],['专业席位被替代','净债务及并购占用现金','倍数不修复'], '315–350；首部17–24')
add('PNR',12,'earnings',[(.50102,.164,11),(.75932,.162,15),(.92332,.160,19)],'泳池渠道纠偏叠加非泳池现金，估值无需把Taco全部当AI业务。','2027收入4.322/4.822/5.132B；调整EBIT .871/1.146/1.316B。分别扣持续摊销重组.12/.10/.08B、利息.14/.12/.11B、税18%，净利=(EBIT-摊销重组-利息)×82%=.50102/.75932/.92332B。摊销和重组桥为R2假设，须核实公司原adjusted口径避免重复扣减。',['3–6月：2027泳池季订单、渠道库存','6–12月：Taco全年贡献及偿债'],['Pool终端份额连续两季落后同业且去库不收敛','Taco协同不及利息负担且杠杆上升'],['非全面终端复苏','新增收购债务','退款不可重复'], '260–300；340–348')
add('NVDA',12,'earnings',[(150,24.5,16),(310,24.2,23),(430,24.0,28)],'以低于上游FY28工作利润估值，当前价格对高增长的容错优于多数AI半导体。','FY28收入410/600/760B；含SBC及特殊损失后的经营利润约185/378/525B，税与净费用合计后净利150/310/430B。上游640B收入/415.7B EBIT作为经营参照，基准下调交付量；不是现成共识EPS。',['3–6月：Rubin交付及回款','6–12月：客户投产和FY28收入指引'],['DSO连续两季超过75天且客户融资恶化','关键客户资本支出削减同时库存/采购承诺增加'],['客户/供应商融资同向','担保或有损失','ASIC替代和毛利下滑'], '305–360')
add('MU',12,'earnings',[(42.9,1.17,7),(148,1.16,10),(220,1.15,12)],'近期高利润存在原始财报支持，但以正常化利润折扣承担价格周期；高弹性而非下行有限。','悲观取FY28快速降价EBIT53.6B×80%=42.9B；基准185B EBIT×80%=148B，低于上游FY28 232.3B；乐观275B×80%=220B。基准普通DRAM/NAND净价回落且位元增长，PE也降至10。',['3–6月：Q1及后续ASP/位元','6–12月：长协履约和竞争供应量'],['连续两个季度同口径普通内存ASP下降且位元增长不足以补偿','押金退出、客户取消与资本支出同时上升'],['80%以上毛利不可当永久常态','FY28供给增加','高资本承诺'], '305–356',confidence='中低')
add('BNTX',18,'bntx',[(11.5,.5,10,.25,.265),(13.5,2.0,15,.55,.260),(15.0,4.0,18,.65,.258)],'足够现金支持多项随机临床验证，现金烧损后仍提供部分缓冲；18月收益来自临床去风险而非近期盈利。','起点净现金16.5213B EUR，18个月后净资金11.5/13.5/15B假设。2033利润0.5/2/4B是权益、支付、持续研发后的正常化估值桥；基准明显高于上游2033约1.07B突破算例，因此仅作为更强临床组合重估状态，不能称最可能。5年折现包含未来投入风险，附加兑现折扣。',['3–6月：gotistobart/T-Pam/BNT113数据与CEO接任','6–18月：随机证据、注册路径及合作权利明确'],['核心随机结果无效或不可接受安全性','净资金低于10B EUR且现金烧损不受控','重要IP以不利条款转出'],['药物独立失败','BMS分成','长期研发吃掉现金','基准模型要求较强临床去风险'], '318–419；情景221–223',status='小额事件型；等待完整随机证据',confidence='低')
add('AVGO',18,'earnings',[(40,4.95,16),(95,4.90,22),(135,4.90,26)],'ASIC与软件形成真实获利，但股价弹性必须跨过FY28交付与信用暴露。','FY27收入107/157/197B及净利27/66/89B为起点；18月看FY28年化收入170/230/290B、扣SBC/摊销/利息后净利40/95/135B。基准约230.5B收入和139.8B业务利润，扣10B SBC、5.8B摊销、2B利息及17%税，约101B；再留6B风险余量。',['3–6月：ASIC客户量产','6–18月：软件续约现金和FY28订单转交付'],['软件前置许可没有后续现金','客户支持安排发生实质损失且采购义务无法削减'],['客户集中','担保与采购承诺','含材料内容压利润率'], '290–344')
add('MKSI',12,'earnings',[(.239,.072,16),(.921,.071,22),(1.208,.073,27)],'前道、PCB、化学耗材复苏与降债可合力提高权益价值，不能只套调整EPS。','2027收入4.4/5.75/6.5B；含SBC的调整EBIT .766/1.548/1.897B，扣摊销重组及利息、20%税后净利 .239/.921/1.208B。股份假设高于当前67.62M以容纳转换净稀释。',['3–6月：设备/PCB订单交付与可转债安排','6–12月：经济FCF用于降债'],['经济FCF低于600M且应收周转恶化','转债本金现金需求缺乏覆盖'],['周期共同回落','再融资','客户议价'], '364–419')
add('SMCI',12,'earnings',[(.178,.95,8),(3.488,.82,12),(5.490,.85,15)],'股价对收入不收费、对薄利润及资本占用收费；交付/回款恢复有大弹性，绝非便宜即安全。','FY27收入42/60/73B，净利 .480/3.790/5.792B，再扣优先股现金股息 .302B；将普通股稀释代理提高到.95/.82/.85B。当前646.87M不是完全稀释口径。目标中转换本金/利息需V2按合约重建；不确定精确FD不伪装为事实。',['3–6月：新财报与内控整改','6–12月：库存/应收转现金及优先证券稀释'],['经营现金持续大额为负且新增融资不可得','出口/审计调查导致客户或融资中断'],['灾难尾部可接近零','客户订单可取消而采购刚性','股数模型误差大'], '315–359',status='仅卫星；现金及FD核验前等待',confidence='低')
add('SNDK',12,'earnings',[(13.97,.151,7),(23,.150,11),(32.89,.151,14)],'NBM底价与财务保障比普通订单更强，但必须给NAND正常化及履约风险定价。','FY28经营模型收入29.38/约43/55.58B，税后净利13.97/23/32.89B；基准低于上游26.9B并提高股数。合同覆盖为位元约2/3，非所有收入无条件保底。',['3–6月：NBM交付及现金税','6–12月：客户实际采购、2027下半年供需'],['NBM集中重谈底价或延期且现金保障不足','供给增加与消费/客户端位元下降持续并发'],['异常高毛利','JV资金义务','保证金不是可自由分配现金'], '298–350',status='等待更低价或合同兑现；不凭5.59x买入',confidence='中低')
add('CRM',12,'cash',[(7,.86,16),(10.24,.85,22),(13,.84,27)],'旧订阅和数据工作流现金可对抗AI替代叙事，但必须扣SBC及新增债息。','FY28工作收入49.7B、GAAP EBIT11.519B、FCF14.54B；扣SBC4.3B后10.24B。悲观旧业务低增/AI不能抵消席位，经济FCFE7B；乐观收费与成本改善13B；不计战略投资估值收益。',['3–6月：有机cRPO、同口径AI ARR','6–12月：付费消耗、现金降债'],['有机增长低于3%且经济FCFE下降','继续借债大幅回购同时主营停滞'],['高净债务','AI指标定义变动','收购整合'], '325–401',status='偏价值修复；较低价更佳')
add('BDC',12,'ev',[(.423,8,2.50,.041),(.736,10,2.10,.041),(.893,12,1.90,.041)],'工业自动化利润加RUCKUS整合可产生去杠杆权益弹性；承认收购后下行放大。','2027收入3.24/4.035/4.38B，EBITDA .423/.736/.893B；目标净债2.5/2.1/1.9B仅为偿债假设，非已披露余额。倍数8/10/12兼顾设备与网络，不赋软件ARR倍数。',['3–6月：RUCKUS盈利及周转','6–12月：净杠杆走向2.9x目标'],['净债/EBITDA持续高于4x','RUCKUS EBITDA不足以覆盖新增债息和整合'],['高杠杆','退款影响基期','匿名AI客户合同'], '342–393',status='小额杠杆修复；不作下行缓冲核心')
add('PGR',12,'earnings',[(6.5,.586,12),(9.103,.584,17),(12.0,.582,21)],'高频再定价与成本优势支持存量盈利，但准备金释放与车险硬周期正常化需先扣。','2027工作NPE增长、CR走向约92%区间；正常化净利9.103B。压力CR接近95%、税后6.5B；较强承保和增长12B。无证券价格收益，无浮存金净现金加项。',['3–6月：每月CR/保单增长','6–12月：竞争加剧后的事故年盈利'],['剔除往年准备金后CR持续超过96%且保单增长失速','损失通胀系统性高于费率'],['准备金不足','房主险灾损','倍数已反映质量'], '313–349',status='分散与质量候选，现价上行中等')
add('VST',18,'ev',[(6.7,8,25,.350),(8.7,10.5,22,.345),(9.8,12,20,.345)],'现有电源/容量收入和已签PPA比远期新核项目更可估，18月观察交割与现金。','2027EBITDA工作8.4B来自既有7.6+Cogentrix .55+Meta .25；18月基准8.7B，不把Meta全量和容量收入重复相加。压力6.7B含停机/成本，上行9.8B要求兑现。净优先索取权25/22/20B含收购和优先权益的研究代理，须核验完整债务桥。',['3–6月：Cogentrix交割、年度指引','6–18月：Meta既有电量爬坡及现金偿债'],['机组可用率持续低于假设且补购电支出上升','全资本开支后现金不覆盖债务及强制分配'],['Moss环境责任','政策压电价','对冲限制短期上涨'], '374–409',confidence='中低')
add('MOD',18,'ev',[(.365,9,.50,.056),(.757,14,.25,.055),(.977,18,.10,.055)],'独立热管理业务有真实放量，但当前价格已经要求利润率修复；等待更佳价或交付证据。','存续FY28收入2.87/3.73/4.37B、EBITDA .365/.757/.977B，净债假设.50/.25/.10B；SBC由55–56M稀释代理体现并须防止重复经济扣除。已剔除PT，不加THRM历史分派。',['3–6月：存续公司指引与投资者日','6–18月：DC利润率和现金不靠新增预付'],['DC毛利/EBITDA率连续低于17%且现金弱','温水架构降低单位MW价值又未由CDU补足'],['大客户集中','已含强增长估值','扩产/预付款负担'], '316–386；情景10、20',status='等待≤145美元或经营上修')
add('MCHP',18,'earnings',[(.77,.56,14),(1.81,.56,23),(2.43,.57,29)],'嵌入式库存周期恢复而非2029纯AI兑现；已有现金提供生存缓冲，但债息和优先股压每股回报。','FY28收入5.4/7/8.3B，扣SBC EBIT1.229/2.454/3.158B；减利息约.23/.19/.17、税约15%、优先股息.111后净利近 .77/1.81/2.43B，保留摊销口径差异作为风险。',['3–6月：渠道/公司库存','6–18月：PCIe Gen6订单转收款'],['渠道库存与公司库存同时回升而收入失速','维持分红导致净债上升'],['周期反转','优先股','Hailo投入'], '357–426',status='等待≤57美元或FY28盈利上修')
add('ON',18,'earnings',[(.82,.445,14),(1.72,.445,23),(2.15,.445,29)],'汽车工业复苏与AI电源有机制，但并购稀释后需要更好的买价。','原ON2027净利 .85/1.62/1.98B；合并后Synaptics与协同净贡献假设-.03/.10/.17B；445M股近似当前389M÷88%并留少量稀释，非已完成交割FD。基准毛利约44.1%，不提前使用2030年53%。',['3–6月：利用率、SiC净价','6–18月：并购后含SBC协同/AI实际销售'],['汽车/工业改善只来自补库','并购后的含SBC净协同为负并持续增加股数'],['换股稀释','SiC过剩','AI内容宣传口径'], '320–386',status='等待≤65美元或合并数据')
add('PLAB',18,'earnings',[(.0434,.060,12),(.1209,.060,17),(.1727,.061,22)],'DUV/AMOLED升级与部分归属现金提供缓冲，但美国扩产、少数权益和资本开支限制上行速度。','FY28收入.788/.973/1.151B、EBIT .097/.217/.308B；正常化归母净利.0434/.1209/.1727B，已扣少数股东。现金不再追加，避免利息收入与净现金双计。',['6–12月：高端IC外部净增与工具利用','12–18月：韩国8nm客户资格与FPD复购'],['高端占比升但集团利润继续降','合资分红不可得且资本开支持续超现金'],['50.01%合资现金非全归母','技术外包边界','高资本开支'], '299–331',status='等待≤26美元或现金分配证据')
add('QCOM',18,'earnings',[(5.2,1.10,14),(9.0,1.10,21),(12.5,1.12,27)],'专利现金支持转型，Amazon合作的真正价值在交付/利润，而非把60B支付门槛当订单。','FY27研究净利7.50B；18月FY28取正常化5.2/9/12.5B，基准汽车增长及DC初步放量但不提前用FY29 15B DC目标。含SBC及客户激励；1.10–1.12B股预留认股权证稀释。',['3–6月：Android与苹果基带替代净影响','6–18月：定制业务收入与毛利、付款'],['新定制收入不能补苹果利润且营运资本占用扩大','QTL实收或费率持续恶化'],['股权激励客户','大客户议价','低毛利材料转售'], '308–380',status='等待≤132美元或新业务利润核验')
add('GFS',18,'earnings',[(.32,.580,16),(1.25,.580,24),(1.95,.585,29)],'特色制造/硅光机会比通用成熟制程更强，但现价不能由低forward PE独立证明。','FY28收入6.45/8.7/10.1B、调整EBIT .436/1.656/2.532B；保留SBC/净息税调整后净利 .32/1.25/1.95B研究假设。股数580M含政府发行与持续奖励，2028年末10亿硅光runrate不当全年收入。',['6–12月：光通信实际放量','12–18月：汽车恢复、补助/稀释和ROIC'],['硅光收入增长但资本回报不改善','新投资持续依赖发股且原客户下调长约'],['控制股东','资本密集','政府股票与补助里程碑'], '266–322',status='等待≤40美元或更强盈利证据')
add('WDC',18,'earnings',[(2.87,.395,10),(7.71,.395,18),(10.98,.400,23)],'纯HDD供给纪律和密度升级可产生现金，但必须把Sandisk证券收益及高forward EPS剔掉。','FY28收入12.792/20.23/25.14B、EBIT3.515/9.350/13.286B，扣.06净息和17%税=2.87/7.71/10.98B。基准EPS19.52显著低于快照32.91；不能为了现价反推高利润。',['3–6月：40TB交付与合同价格','6–18月：HAMR资格、可用TB与客户库存'],['每TB净价下降快于成本且客户消化库存','合同重议或质量赔偿侵蚀高毛利'],['市场已计更高盈利','SSD替代','转债股数'], '297–332；408–410',status='等待≤270美元或经营超越模型')

alts=[('AMZN','AWS与广告经营强，但现金资本开支220B及2027–28投产回收尚未给当前价格明显现金赔率；候补平台'),('MSFT','成熟软件现金与30M付费Copilot有证据；资本密度、租赁及OpenAI集中限制短窗上行，候补质量平台'),('JBL','FY27管理层core EPS17.55低于快照forward22.17；312美元对应更远利润，1.51B现金不能直接支持极低估值'),('CLS','真实增长但FY27上游模型扣融资类股酬/租赁后资金变化约-0.438B；8月34.5亿美元发股后需重新计算每股现金'),('RNR','8.15x forward PE受低灾损及准备金释放影响；2027普通股利润正常化约1.49B，不视为净现金地板')]
ex=[('ORCL','12.49x forward PE掩盖新增租赁、预付款和资本开支；现金缓冲不符合本角色优先级'),('BABA','人民币财报/美元ADS、增发及负FCF需重建；低PE不足以证明AI投资回报'),('ALNY','商业化真实但Sanofi超1.5B部分30%版税与研发使独立2028 GAAP EBIT约1.6B；12.42 forward EPS口径需核验'),('ENPH','2027收入11.53亿模型仅0.29亿近GAAP EBIT；45X和safe harbor依赖，不把SST试点作为2027盈利'),('STX','HAMR优势与行业高价不可混同；当前753美元已经要求FY27/28高利润延续'),('TSLA','173x forward PE主要由远期新业务支持，当前现金盈利无法提供短窗估值缓冲'),('SKHY','币种/上市证券/ADR比例未充分重建，P/S明确currency_mismatch，不做相对便宜排名'),('CBRS','市值/股数校验bad53%且远期倍数高，先核实证券总股本')]
out={'role':'R2_valuation','screened_count':len(U),'deep_read_tickers':deep,'nominations':R,'alternates':[{'ticker':t,'reason':r} for t,r in alts],'exclusions':[{'ticker':t,'reason':r} for t,r in ex],'open_questions':['V2核验所有目标稀释股数，特别SMCI优先股、MCHP优先股、ON换股、WDC转债。','PNR目标净利取整与费用桥、VST收购后净优先索取权、BDC净债路径须逐项复核。','BNTX核心基准盈利依赖高于上游2033模型的临床组合，若不接受应降为候补或以现金/更低买价等待。','所有目标倍数均为研究判断，未做历史分位或统计校准；需用10–20%倍数压缩敏感性。','报价沿用冻结10/12收盘，未逐一向交易所复核；数据商forward EPS时期/调整口径不透明，不用作决定性定价。'],'reasoning_summary':['先完整245筛选，深读28并额外读3公司概览。','优先正常化盈利/现金能支持价格，不将上游2029–2030目标缩短。','20名是独立送审名单，排名末端明确等待，不宣称均适合现价买入。','对于周期、药物与杠杆股票悲观损失可达50–90%，高风险偏好不等于这些有可靠下行底。'],'assumptions':{'all_targets':'12或18个月目标日市场价格情景；BNTX采用远期经营桥折回目标日，其余主要资本化目标附近年度获利。','prices_not_total_returns':'目标价不含未确认未来股息；美元税前总收益比较需主席加入同口径股息、成本并对照SPY/QQQ。','multiples':'所有倍数是估值假设；跌价不是经营反证但会改变安全边际。','no_probabilities':'不以主观概率制造精确期望收益；BNTX折扣仅参数。'}}
(B/'02_round1/R2_valuation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# R2 估值、隐含预期与周期正常化：独立首轮','', '冻结：2026-10-12 19:40 PDT；245家公司全池扫描，28家公司模型深读，额外3家公司概览。未读取其他首轮。全部未来参数为研究假设。','', '**最强取舍：ADBE、PNR的现有业务盈利可承担修复；NVDA/MU仍有相对估值弹性，但信用与周期尾部远大于低PE显示。20个提名是送审池，并非20个现价买入指令。** 末端多家公司须等待价格或经营证据，不能用更远期利润硬凑上行。','', '六类来源、12条查询及12个已打开原始IR/SEC文档见 `07_logs/R2_sources.json`；中间判断见 `07_logs/R2_progress.md`。', '', '## 统一情景表','', '|排名|证券|现价|月数|悲观|基准|乐观|基准变化|状态|','|---:|---|---:|---:|---:|---:|---:|---:|---|']
for z in R:md.append(f"|{z['rank']}|{z['ticker']}|{z['price']:.2f}|{z['horizon_months']}|{z['bear_price']:.2f}|{z['base_price']:.2f}|{z['bull_price']:.2f}|{z['valuation_formula']['scenarios']['base']['upside_pct']:+.1f}%|{z['status']}|")
md+=['','这些目标不含未来股息；不等于统计置信区间或价值地板。倍数统一下调20%时，利润/现金模型目标直接下调20%；EV模型因净债固定，股权损失大于20%。股数上调10%时每股目标下降9.1%。BNTX汇率再下调10%，美元目标同比下降10%。','', '## 逐家公司推导与证伪']
for z in R:
    md += ['',f"### {z['rank']}. {z['ticker']} — {z['thesis']}",'',z['operating_assumptions'],'']
    for k,label in [('bear','悲观'),('base','基准'),('bull','乐观')]:md.append(f"- {label}：{z['valuation_formula']['scenarios'][k]['formula']}")
    md += ['', '催化剂：'+'；'.join(z['catalysts'])+'。','证伪：'+'；'.join(z['kill_criteria'])+'。','风险：'+'；'.join(z['key_risks'])+f"。信心：{z['confidence']}。基准需30%上行时对应买价≤{z['wait_price_for_30pct_base_upside']}美元（仅价格敏感性，不是触发买单）。",'', '来源：'+ '; '.join((f"[{e.get('id','原始来源')}]({e['url']})（{e['published_date']}）" if 'url' in e else f"`{e['path']}`，{e['lines']}") for e in z['evidence'])]
md+=['','## 候补与淘汰','']+[f'- {t}：{r}' for t,r in alts+ex]+['','## 公司行动与必须保留的异议','','MOD已于10/1分拆PT；10/12新买家不获0.44619 THRM的历史分派，存续模型不能重复PT利润。PNR已10/1完成Taco，需纳入债息、费用和新业务；交割后净债仍是模型值。相应原始公告已在来源表打开核验。','']+['- '+s for s in out['open_questions']]
(B/'02_round1/R2_valuation.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
addendum='''
## 新增研究方向的回应：中枢不应等于最低口径

以上是估值角色的独立价格压力模型，不宣称“保留全部会计摊销后的最低EPS”是市场唯一正确中枢。PNR/ADBE基准有实际经营恢复；NVDA基准600B收入相对上游640B，主要是交付/验收与ACIE信用风险，需由客户投产证据决定是否恢复到640B；MU的185B基准EBIT可由245B收入×83%毛利－18.35B经营费用形成，比上游283.6B×86.1%利润低，关键是商品净价及份额，而非“所有预期统一打折”。这组价格正常化是模型判断，尚未取得相同比例的独立订单证据，不应冒充被验证的预测。

AVGO的18月基准使用FY28约230B收入/95B净利而非较低FY27净利，明确承认订单转量产；ON允许Synaptics净利润增量，MCHP允许利用率与PCIe兑现；SNDK承认NBM底价、保障及客户合同优于旧周期。因此高风险投资者完全可以在更强的外部增长证据下采用更高中枢。后续专项应验证客户预算、合格产出、经济权益和到款，再上调对应经营参数，避免仅将倍数调高。

BNTX尽管已给高于上游的2033利润桥，18月基准仍接近现价；其排名代表事件弹性关注，不代表本角色已证明现金+临床中枢有正收益。QCOM/WDC等负基准回报必须保留，可被主席淘汰或改为等待，不能为20名额抬高目标。
'''
with (B/'02_round1/R2_valuation.md').open('a',encoding='utf-8') as f:f.write(addendum)
nom={x['ticker']:x for x in R};a=dict(alts);e=dict(ex)
with (B/'07_logs/R2_full_pool_screen.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['ticker','category','price','forward_eps','forward_pe','currency','financial_currency','screen_decision','reason']);w.writeheader()
    for x in U:
        t=x['ticker'];q=x['finance'];status='提名送审' if t in nom else '候补' if t in a else '明确排除' if t in e else '初筛未优先'
        reason=nom[t]['thesis'] if t in nom else a[t] if t in a else e[t] if t in e else ('财报币种与报价币种不同/部分ADR比例和财务转换仍需核验，本轮未据错误P/S提名' if q.get('currency')!=q.get('financial_currency') else '完整池已比较价格/估值/研究覆盖；相对优先候选，现价短窗估值缓冲或可量化盈利/催化剂证据未胜出；并非经营失败判定')
        w.writerow(dict(ticker=t,category=x['category'],price=q.get('最新价格'),forward_eps=q.get('forward_eps'),forward_pe=q.get('Forward PE'),currency=q.get('currency'),financial_currency=q.get('financial_currency'),screen_decision=status,reason=reason))
assert len(R)==20 and len({z['ticker'] for z in R})==20 and len(U)==245
assert all(z['ticker'] in by for z in R)
print(json.dumps({'screened':len(U),'deep_read':len(deep),'nominations':len(R),'primary_opened':len(S),'targets':[{'ticker':z['ticker'],'base':z['base_price'],'upside':z['valuation_formula']['scenarios']['base']['upside_pct']} for z in R]},ensure_ascii=False))
