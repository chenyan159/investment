import csv,json,pathlib,re
R=pathlib.Path('D:/investment/实验室/2026-10-12_20家公司多角色实验')
U=list(csv.DictReader((R/'01_inputs/universe_screen.csv').open(encoding='utf-8-sig'))); U={x['ticker']:x for x in U}
F=R/'01_inputs/frozen'
deep='NVDA AVGO TSM ADBE CRM MSFT META AMZN GOOGL QCOM JBL FLEX CLS CRDO TEL HUBB MOD EME PNR VST PGR RNR ALNY ARGX BABA MU ORCL'.split()
paths={t:next((F/'基本面/公司调研/结果').rglob(t+'_*.md')) for t in deep}
# EPS proxies are independently selected 2027/FY28 operating outcomes, not quote vendor forward EPS.
# tuple: ticker, earnings/owner-cash per share scenarios, selected multiples, operating bridge, thesis, catalyst, kill, risk
rows=[
('ADBE',[16,21,25],[10,16,21],'FY27收入26/28.7/31B；含SBC营业率32%/35.4%/38%，税约22%，股数0.40/0.377/0.368B；经营净利每股取整16/21/25。利息与现金税差列为约1美元EPS敏感性。','创意残差减速已承认；Acrobat及企业工作流收费、扣SBC后仍强现金，使低价不必依赖AI新故事。','3–6月：提价周年续约及FY27指引；6–12月：AI积分实收与有机ARR。','连续两季剔并购ARR低于5%，且创意残差下滑/现金扣SBC低于6B年化。','专业席位永久收缩；并购和回购可能消耗现金；价格低无硬底。'),
('NVDA',[8,14,17],[16,23,29],'FY28收入400/625/730B，含SBC经营率58%/65%/68%，税17%，稀释24.5B，得到EPS7.9/13.8/16.8取整。剔战略投资重估；净现金不另加，生态净投资50B作为回报约束。','CUDA与整机网络价值捕获仍强，FY27Q2实际利润支持；主动削弱现金转换，避免把投资收益资本化。','3–6月：108B季度指引兑现、DSO回落；6–18月：Rubin交付和客户终端支付。','DSO连续两季>75天且经营现金/经营利润<50%，或毛利持续低于65%。','客户融资与采购担保同向；地缘禁运；最差尾部可比128美元悲观价更低。'),
('MU',[80,170,220],[6,8,10],'FY27独立归一收入165/260/315B，营业利润115/235/302B，税16%，稀释1.16B，EPS约83/170/219取整80/170/220。经营现金扣净capex46/55/65B后仍须保持正；不用报价207远期EPS。','短缺正在变成真实现金，SCA客户押金不计经营FCF；对成熟存储给低倍数，保留高弹性。','3–6月：FY27Q1收入61.5B指引及毛利；6–12月：HBM交付、传统DRAM净价。','两个季度合同价格连续跌且客户取消；净capex>60B而现金下降，重估周期峰值。','极高毛利不可能永久；FY28供给与价格同步反转，灾难尾部可能跌60%以上。'),
('PNR',[3.3,5,6.2],[10,15,18],'FY27营业利润0.871/1.146/1.316B，利息和整合现金约0.20/0.18/0.15B，税20%，股数0.163/0.161/0.158B；保守取经济EPS3.3/5/6.2，低于仅调整后盈利。','泳池去库存后恢复和过滤耗材现金，非AI利润来源；低价允许只实现温和修复。','3–6月：Taco交割融资、春季预订；6–12月：Pool终端售出/去库。','2027旺季Pool仍丢份额，恢复净价靠大返利，或经济现金<0.45B。','并购债务、渠道去库不等于消费恢复、CFO交接。'),
('TSM',[13.3,19.8,24],[18,26,30],'2027美元营业利润84/125/152B×82%/5.1864B ADS等价股=13.3/19.8/24。每ADS=5普通股；原普通股25.932B。美元利润模型避免把TWD财务与USD市值直接比；capex约70–90B限制倍数。','先进制造与封装同时收费，客户不能轻易复制；有盈利及现金实证，制造资本密度已扣。','3–6月：季度毛利/现金capex；6–18月：N2爬坡、封装与海外成本。','大客户取消与利用率下降并存；新节点良率和海外成本令营业率<45%。','台湾生产中断为不连续尾部，普通悲观情景不是风险下限。'),
('AVGO',[5.6,13.5,18.2],[20,29,33],'FY27经营税后利润27.36/66.29/89.25B，稀释约4.9B，EPS5.6/13.5/18.2。经营含SBC和摊销；悲观担保额外损失可令EPS再低1.6美元。','软件现金支持ASIC和网络放量；明确扣SBC、营运资金与客户信用支持，仍有利润扩张。','3–6月：Q4 AI收入21.7B及回款；6–18月：新XPU生产验收。','租赁/信用支持损失超过8B；增长但保理后现金不改善；XPU客户核心份额丢失。','客户集中与系统外购内容压毛利；采购承诺；无形摊销与SBC不能全部免费化。'),
('PGR',[10,15.6,19],[12,16,19],'2027NPE约86/92.2/99B，CR约95/91.5/89.5%，净投资约4B，税21%，普通股约0.58B；净利EPS约10/15.6/19。保险浮存金不额外计FCF，特殊股息不进入目标价。','数据、定价与渠道建立可重复承保；保费先收不当利润，仍可用正常化承保盈利估值。','3–6月：月度PIF、事故年CR；6–12月：续保/新业务与费率。','剔历史准备金释放车辆CR持续>97%，且保单增长停滞。','赔付通胀和费率竞争；特殊股息非永续；灾害相关损失。'),
('TEL',[9,12.8,15],[14,20,24],'FY27含SBC经济营业利润约3.5/4.7/5.5B，利息0.1B，税20%，稀释0.285B；EPS9/12.8/15。公司FCF工作3.29B，再扣SBC0.18B检验。','复杂连接器、车用和电力产品使AI增量不承担全部估值；设计认证与多行业现金分散。','3–6月：DDN订单到收入；6–12月：工业/汽车量与资本支出。','汽车量价同时恶化，DDN增速不足弥补，FCF/SBC后<2.5B。','新厂资本强度、汽车议价、并购协同延迟。'),
('MSFT',[17,20,25],[22,29,34],'FY27/FY28过渡营业利润160/186/232B，税20%，净利息2B，稀释7.4B；EPS约17/20/25。包括SBC；FY27租赁本金后现金42B使基准PE不扩张至软件历史高位。','企业身份、Office与云分发入口最稳；Copilot确有付费规模，但只按经营盈利给有限增长溢价。','3–6月：Azure增长与毛利；6–12月：Copilot续费净账单；12–18月：资本现金回收。','租赁后现金连续年低于40B且云增长放缓；折旧年限变化掩盖资产回报下降。','巨大未开始租赁承诺；OpenAI相关集中；新增AI资本回报未证明。'),
('RNR',[21,35,46],[8,10.5,12],'2027归属经营净利0.9/1.49/1.98B÷42.5M稀释股；EPS约21/35/46。已扣外部专户归属、税和优先股，不把合并承保利润全部归普通股。','软市中主动缩险而保留投资/资本管理费用，估值对平常年盈利较低；分散科技现金风险。','3–6月：巨灾净损失和1月续保价格；6–12月：责任险准备金与retained收益。','归属灾损及准备金补提累计超2B，或新签价格低于赔款趋势且不缩限额。','巨灾有跳跃尾部；责任险长尾；外部账户利润归属复杂。'),
('EME',[20,36,46],[16,24,29],'2027营业利润1.27/2.21/2.78B，税26%，净利息约0.02B，稀释44.5M；EPS20/36/46。FCF工作1.545B，但10天回款延迟占用约0.55B。','复杂机电工程的现场组织和预制能力可收费，低设备资本开支；以真实利润而非RPO全额估值。','3–6月：H2现金转换；6–12月：网络施工RPO转化和并购整合。','年度现金/净利<65%且合同资产不断增加，或核心项目毛利/工时显著恶化。','固定价工程、熟练人员、延期与客户信用；低capex不等于低营运资金。'),
('QCOM',[6,9,12],[13,20,24],'FY27收入40/46/53B，含SBC正常经营利润8/11.5/15.5B，净利息0.5B，税18%，稀释1.03B；EPS6/9/12。基准高于上游9.55B经营利润，明确要求Amazon及Android改善；Amazon权证2.4%额外稀释压力。','专利许可和汽车/IoT提供现金底盘，定制数据中心是期权；拒绝用一次性税项盈利。','3–6月：Amazon开始确认收入；6–12月：手机现金周转与汽车量产。','FY27数据中心收入不及3B且手机现金流继续下降；QTL费率或续约恶化。','苹果替代、客户让利/权证、库存与预付；当前价基准上涨有限。'),
('HUBB',[15,22,27],[16,23,27],'2027调整净利润0.813/1.216/1.457B÷53.1M股，正常化摊销/整合保留约0.5–1美元EPS折扣后取15/22/27；NSI债务利息已在桥中。','电网更新提供独立需求，高压项目及NSI扩展渠道；资本回报优于单纯AI概念。','3–6月：NSI整合和净债务；6–18月：电网产品交付。','有机订单转负、收购增长掩盖旧业务，FCF低于0.7B且持续回购。','并购杠杆、监管工程节奏；765kV大TAM不等于近期收入。'),
('CRM',[10,13,17],[14,21,26],'FY28收入约45/50/56B，GAAP经营率20/24/28%，净利息约1.5B，税22%，稀释0.80B；EPS约7.3/10.2/13.8。估值使用现金扣SBC经济EPS10/13/17，约8/10.4/13.6B股东现金，须区别GAAP；不把债务再扣第二次。','成熟订阅续费仍有现金，AI流程收费能延缓席位侵蚀；只在资本配置收敛下有价值。','3–6月：cRPO有机增速和ASR结算；6–12月：Agent净收费及整合。','净债务继续上升而有机增速<5%；FCF扣SBC<9B。','借债回购、并购摊销、股票报酬；披露AI ARR扩大口径。'),
('JBL',[12,17,21],[12,18,22],'FY27收入37/43/49B，core营业率5.3/6.1/6.7%，扣净利息/税与经济SBC后利润约1.25/1.77/2.18B÷104M股；经济EPS12/17/21。FCF仅约1.5–1.6B，限制基准倍数。','低毛利但制造组织与客户供料可令资本回报良好；比单一客户AI代工现金更成熟。','3–6月：FY27指引及营运资本；6–12月：云、医疗项目利润兑现。','应付融资不足覆盖库存应收，FCF<1B且资本开支持续增加。','客户供料与收入总额、应收出售、Amazon权证、增长不等于现金增长。'),
('VST',[4,9.7,13],[13,18,22],'2027成长后普通股现金1.4/3.3/4.4B÷341M股=4/9.7/13；基准从EBITDA8.4B扣利息1.35、税0.35、维持/燃料1.75、其他0.15、成长1.4、优先股0.1。以股东现金倍数估值，不称PE。','现成核电/燃气与零售对冲有真实现金；Meta PPA只计2027逐步重定价。','3–6月：Cogentrix交割和融资；6–18月：Meta逐步交付。','停机/保证金占用超2B且成长后现金<2B；交易债务迫使大额发股。','电价对冲限制短期弹性；环境责任；成长前FCF高估普通股所得。'),
('ARGX',[17,29,40],[23,32,39],'2027净产品销售5.8/7.0/8.2B，经营率25%/34%/41%，税22%，稀释64M ADS，每ADS=1普通股；EPS约17/29/40。保留SBC及研发，收购摊销待核。','VYVGART已有多适应症持续患者付款，扩张无需押注全部管线；应收现金要追踪。','3–6月：CIDP续治净价；6–12月：ITP读出；12–18月：C2数据。','CIDP停止/转药上升，净价下降>15%且患者量不能补；应收持续快于销售。','医保、返利、竞争免疫重置、制造/并购义务；单产品集中。'),
('ALNY',[3,7,12],[25,32,40],'2027收入5.0/6.5/8B，扣Sanofi版税、制造、研发及销售后经营利润0.55/1.25/2.15B，税20%，稀释142M股；EPS约3/7/12。nuc尚未商业化，不提前加免版税利润；融资版税义务需资本核验。','AMVUTTRA增长是真实患者支付，RNAi技术有后续选择权；主要价值捕获被版税削弱，排名靠后。','3–6月：TTR销售及净价；6–12月：处方医生扩散；12–18月：重复给药。','TTR新增患者停滞且净价降>10%；现金被版税/研发吸收、持续稀释>4%。','Sanofi/Blackstone经济权益、单供应商、临床及付款方限制。'),
('AMZN',[6.8,9.3,12],[22,30,36],'2027营业利润95/130/165B，扣净利息5B，税20%，稀释10.8–11B；EPS6.8/9.3/12。全投资FCF基准约-20B，因此只能等待capex效率，不把利润视可分现金。','AWS和广告是已付费利润池，零售规模产生协同；现金回收慢但经营选择权广。','3–6月：AWS付费用量与利润率；6–18月：现金capex增速拐点。','2027现金capex继续快于CFO增长且AWS降价毛利受损。','巨额建设/设备投资、承诺与新业务消耗；当前上行不够补偿全部现金风险。'),
('META',[20,30,39],[19,25,31],'2027集团营业利润70/101/125B，税20%，净利息4B，全部经济股数2.55B，EPS约20/30/39。经营含SBC/RL；capex约150B令基准FCF近零，不加净现金溢价。','广告推荐实际增加成交和付款，价值捕获比免费AI更直接；但资本配置决定普通股回报。','3–6月：广告价格/展示；6–12月：AI支出强度及现金。','广告量价减速而CapEx与SBC不收敛；两个季度经营率<30%。','创始人控制、AI资本过剩、RL亏损、隐私监管；只作等待候选。')
]
N=[]
for i,(t,e,m,bridge,thesis,cat,kill,risk) in enumerate(rows,1):
 p=[round(x*y,2) for x,y in zip(e,m)]
 n=dict(rank=i,ticker=t,thesis=thesis,horizon_months=15,bear_price=p[0],base_price=p[1],bull_price=p[2],valuation_formula={'formula':'price = normalized economic EPS (or owner cash/share) × multiple','per_share_scenarios':e,'multiples':m,'operating_bridge':bridge,'assumption_status':'R1 independent conditional assumptions, not company guidance','sensitivity':'经营每股值±10%则目标价同比±10%；倍数±20%则目标价同比±20%；不把二者当独立概率。','debt_and_dilution':'净利息已扣，股权估值不重复扣全债；稀释按各桥，债务再融资尾部另列。'},catalysts=[cat],kill_criteria=[kill],key_risks=[risk],evidence=[{'class':'company_research','path':str(paths[t]),'locator':'正文财务基线、现金/资本结构、经营模型与风险章节；详见R1_reading_notes.md'},{'class':'financial_snapshot','path':str(R/'01_inputs/universe_screen.csv'),'locator':'ticker='+t}],confidence='中；经营事实高于远期倍数及短期重估',anchor_price=float(U[t]['price']),price_date=U[t]['price_date'],action='条件提名；等待价格/现金验证' if p[1]/float(U[t]['price'])<1.2 else '分批研究候选；须最终核验',scenario_returns_pct=[round((v/float(U[t]['price'])-1)*100,1) for v in p],probabilities=None,probability_note='未校准且尾部不完备，不机械加权。')
 N.append(n)
alts=[('CRDO','光学与AEC强，但87.979M季度SBC、收购与客户集中降低现金可得；须验证FY27光收入。'),('CLS','2027高增有价值，但H1 FCF285M小于融资类薪酬现金326.3M，增发约9.7%，重新验证股本和现金。'),('FLEX','Axiom分拆有催化，但划出Q1 FCF为-229M、EPC并购及最终分拆融资尚不清。'),('MOD','165M客户预付贡献FY26现金；剔预付敏感性FCF为负，PT/Gentherm分配须重建总回报。'),('GOOGL','搜索/云强，但投资重估污染TTM PE、预计2027负FCF与股本融资；现金角色弱于MSFT。')]
exc=[('ORCL','客户预付11.4B推动CFO；剔除敏感性季度FCF -16.796B，低PE不证明资本回报。'),('BABA','TTM FCF -72.464B人民币；即时零售补贴和capex消耗，不能用ADR低P/S比较。'),('PLTR','P/S 81.59，现金成长即使强，近期重估风险压过下行缓冲。'),('NET','高P/S与高远期PE，需远超基准经营成果。'),('LWLG','营收基数极小且负EPS；未满足客户付款与经济现金门槛。'),('POET','极低收入/高P/S，商业认证及融资仍是主要变量。'),('OKLO','收入前期，3–18月主要是融资/许可重估，不满足本角色现金质量门槛。')]
out=dict(role='R1_cashflows',screened_count=len(U),deep_read_tickers=deep,nominations=N,alternates=[dict(ticker=t,reason=v) for t,v in alts],exclusions=[dict(ticker=t,reason=v) for t,v in exc],open_questions=['快照forward EPS口径及时间窗不能当已审计盈利；尤其MU/NVDA。','所有提名价格仅冻结快照锚，未逐笔独立查交易所；美元价格日期为2026-10-12。','MU FY26新10-K、ALNY未来版税负债归属、ARGX收购资本桥优先补核。','MSFT/AMZN/META经营利润虽强但成长后现金弱，主席不应因提名票数自动纳入立即买入。','风险情景不是绝对底；台湾、巨灾和药品安全可穿透普通悲观价。'],cutoff='2026-10-12 19:40 America/Los_Angeles',round='independent R1',benchmark='USD pretax price returns; dividends excluded here; SPY/QQQ comparison left to controller')
(R/'02_round1/R1_cashflows.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# R1：业务、现金创造与价值捕获独立提名','信息截止2026-10-12 19:40洛杉矶；245家公司均完成结构化初筛，27家公司从原报告正文作财务、资本和经营机制专题深读。没有读其他研究者首轮结论。深读不等于逐行审计，财务主要依赖冻结公司报告，7份官方财务材料另行实读。','本角色最优先ADBE、NVDA、MU、PNR、TSM。20项是提交争议池的候选，不是强行填满20个立即买入名额；现金转化不足或基准空间小的公司明确等待。独立的2027/FY28近端经营锚和倍数已重建，没有平移2029目标价。','现金规则：CFO减capex仍要观察SBC、融资类薪酬现金、预付/保理、成长投资、租赁本金及并购；保险以正常化承保归属盈利分析，不能把浮存金全部算股东现金。','|排名|公司|10/12价格|悲观/基准/乐观|对应价格回报|动作|','|---:|---|---:|---|---|---|']
for n in N: md.append(f"|{n['rank']}|{n['ticker']}|{n['anchor_price']}|{n['bear_price']}/{n['base_price']}/{n['bull_price']}|{n['scenario_returns_pct']}%|{n['action']}|")
for n in N:
 md += [f"\n## {n['rank']}. {n['ticker']}",n['thesis'],f"**12–18月场景**：{n['valuation_formula']['operating_bridge']}；每股经济收益/现金{n['valuation_formula']['per_share_scenarios']} × 倍数{n['valuation_formula']['multiples']}，得到美元价格{n['bear_price']}/{n['base_price']}/{n['bull_price']}。均为R1条件假设，不是统计概率。",'催化：'+n['catalysts'][0],'证伪：'+n['kill_criteria'][0],'风险：'+n['key_risks'][0],f"本地证据：[公司正文]({str(paths[n['ticker']]).replace(chr(92),'/')})；价格：[冻结全池](../01_inputs/universe_screen.csv)。"]
md+=['\n## 候补与淘汰']+[f'- {t}：{v}' for t,v in alts+exc]+['\n## 共同资料与局限','六类本地资料均使用：产业背景（全球AI需求与Token经济框架）、行业（AI创作与文档、保险）、公司正文、公司情景决策（ADBE）、公司对比（ADBE）、金融快照。情景/对比只用于发现旧口径和反证，不直接采用其2029价格。路径与阅读定位见R1_reading_notes.md；外部URL和核验结果见07_logs/R1_sources.json。','最大组合风险是看似多元的芯片、服务器、云和电力仍共同暴露AI资本预算。单独的保险、泳池水处理和药品给不同现金来源；仍无无风险底。情景概率未赋值，不能擅自把三点算期望。价格回报未加股息、税费和汇率，不能冒称完整总收益。','所有基准均对倍数敏感：盈利不变而倍数下调20%，目标价也降20%。ARGX/ALNY新药可选权未另行加总；TSM ADS1:5、ARGX ADS1:1依据公司正文，最终证券核验应回官方原件。']
(R/'02_round1/R1_cashflows.md').write_text('\n'.join(md),encoding='utf-8')
with (R/'07_logs/R1_full_universe_screen.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['ticker','category','price','forward_pe','ps','coverage','screen_result','cashflow_caveat']); w.writeheader()
 for t,u in U.items():
  tag='深读提名' if t in [n['ticker'] for n in N] else '深读候补/淘汰' if t in deep else '全池结构化初筛后未进入本角色深读'
  reason='负收益/尚未证明自我融资' if '负' in u['forward_pe'] else '跨币种PS不可直接比较' if u['currency']!=u['financial_currency'] else '估值不是现金；需SBC/成长投入/客户回款核验'
  w.writerow(dict(ticker=t,category=u['category'],price=u['price'],forward_pe=u['forward_pe'],ps=u['ps'],coverage=u['company_md'],screen_result=tag,cashflow_caveat=reason))
notes=['# R1 原报告阅读与审计笔记','时间截止同实验章程。先遍历245行全池，再挑27家公司跨现金类型深读；不是仅读dossier开头。以下为正文中用于审查的财务、现金、资本、股本和模型定位。自动提取目录便于复核，不代表每个引用均获外部独立认证。']
for t,p in paths.items():
 a=p.read_text(encoding='utf-8-sig').splitlines(); notes+=['\n## '+t,str(p),'重点结论：'+next((n['thesis']+' 风险：'+n['key_risks'][0] for n in N if n['ticker']==t),next((v for z,v in alts+exc if z==t),'现金专题已读'))]
 hits=[f'{i+1}: {s}' for i,s in enumerate(a) if re.search('CFO|FCF|SBC|经营现金流|自由现金流|稀释|^##.*(模型|资本|财务|风险)',s)]
 notes+=hits[:28]
for pat in ['全球AI需求与Token经济框架*.md','行业调研_AI创作与文档生产软件*.md','行业调研_财产险、特色险与再保险*.md']:
 p=next(F.rglob(pat)); notes+=['\n公共机制来源：'+str(p)+'，前50行；终端付款≠云/芯片收入加总；免费工具压价格；保险承保与准备金不能用工业FCF口径。']
for d in ['公司情景投资决策','公司对比']:
 p=next((F/'分析报告'/d/'结果').rglob('ADBE*.md'));notes+=['来源：'+str(p)+'，前75行；只作远期估值与口径反证，未平移2029价格。']
(R/'07_logs/R1_reading_notes.md').write_text('\n\n'.join(notes),encoding='utf-8')
print('written',len(N),'nominations;',len(U),'screened;',len(deep),'deep company reports')

