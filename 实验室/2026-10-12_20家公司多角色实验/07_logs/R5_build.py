import json,csv,pathlib
B=pathlib.Path('D:/investment/实验室/2026-10-12_20家公司多角色实验')
U=json.loads((B/'01_inputs/universe.json').read_text(encoding='utf-8-sig')); U={x['ticker']:x for x in U}
deep='MRNA BNTX ALNY IONS ARGX KYTX COST WMT BJ KR TJX PGR TRV CB WRB RNR WM RSG WCN CWST AGCO PNR ADBE NVDA AVGO MU ON BABA MOD'.split()
# EPS below are independent scenario assumptions, not the screen's vendor forward EPS.
rows=[
('NVDA','平台现金创造与估值压缩后的盈利增长', [13,18,23],[12,20,24],'FY28收入600–680bn工作区间、毛利约73%；用约24bn摊薄股数及税/费用归属检验18 EPS。','2027 Rubin交付、推理预算及现金回款','客户融资支持损失与采购承诺同时上升；现金转换持续落后利润','净流动资产56.586bn减债33.366bn约23.22bn；战略股权不是现金','客户资本开支周期、信用支持、出口政策'),
('ADBE','低倍数订阅现金流与AI付费修复',[18,22,27],[9,15,19],'FY27收入28.7bn/GAAP经营利润10.15bn，本模型22 EPS要求税后约8bn、约0.37bn股；高端需AI净增。','2026Q4–2027付费净新增、文档与Firefly付费','核心创意留存连续恶化且降价不能拉回付费','现金短投5.639bn对债6.363bn，非净现金；可停回购保现金','AI替代、SBC、并购和回购挤占现金'),
('ALNY','已盈利TTR商业化遭去积压预期打击后再增长',[4,8.5,12],[25,34,40],'2027收入约6–7bn、正常税后利润约1.1bn/约0.13bn股形成8.5 EPS；Sanofi增量版税已限制毛利，不预计nuc CM上市。','2026Q4–2027一线新患者及净价；2027末PN试验进展','连续两季TTR收入不增且付费患者/净价同步下降','流动性约3.3bn但2027/28可转债约0.363/0.661bn，版税融资现金义务仍在','支付准入、口服竞品、已释放积压、基因编辑'),
('BNTX','有消耗但资本充足的多资产肿瘤临床期权',None,None,'ADS 1:1已原始确认。12–18月每ADS=(剩余净可用现金EUR13/15/16bn+肿瘤及疫苗EV EUR0/12/26bn)*假设FX1.15 / 摊薄0.26bn股；得到57.50/119.42/185.77美元。EV为研究情景而非DCF已核准值。','2026Q4 gotistobart确证阶段中期及T-Pam读数；2027监管推进','主要独立读数均失败且年现金消耗超过EUR3bn，或治理转移损害权益','EUR16.6342bn现金证券非闲置现金；先扣未来消耗、退出/合同、债务与必要现金；未重复加BMS已收款','多个试验相关失败、BMS分成、ADC权利、汇率与资本浪费'),
('PNR','泳池去库后恢复加成熟水业务现金',[3.7,5.3,6.2],[10,15,18],'2027经营利润约1.146bn，扣利息约0.15bn并按税率/约0.16bn股检验5.3 EPS；高端是渠道恢复，不靠AI TAM。','2026Q4–2027 Pool渠道正常化、Taco交割和协同','终端同业恢复而PNR继续丢份额；收购融资侵蚀每股收益','成熟业务有现金，但Taco约1.425bn交易增加债务，不能称现金盒子','渠道控制、份额、利率、收购整合'),
('ARGX','CIDP和gMG盈利增长为临床扩张供资',[20,31,40],[25,32,36],'2027归属净利约2bn/约64m股=31；2028较成熟销售约8bn仅作邻近验证，不移植2030突破。','2026Q4–2027 CIDP转化、肌炎申报、自动注射器','已批准病种净价和持续治疗年同步下滑；收购后现金持续下降','6月流动资产5.184bn无金融借款；Forte宣布值2.2bn须扣，不能用旧余额','美国支付、单分子集中、UNITY失败、细胞疗法'),
('AVGO','定制芯片放量与软件现金并存',[10,15.5,20],[20,28,32],'FY27集团收入约157bn、经营利润约99bn的上游工作路径；归属税后和摊薄约4.8bn股约15.5 EPS，剔除非经常项另核。','2027 ASIC项目验收和软件续费现金','客户项目延期伴随支持损失、现金利润持续背离','软件能供资但供应采购及租赁支持有义务；不是无债现金盒子','客户集中、融资/租赁支持、供应承诺'),
('MU','存储供需错配仍可能持续但用周期估值',[65,160,220],[6,7,9],'FY27独立EPS条件；由FY26收入133.188bn与高毛利起点推演，基准不永久维持86.8%季度毛利。价格下跌与倍数压缩联动，不能拿4.79倍当安全证明。','2027合约重定价、HBM交付与新产能爬坡','普通DRAM/NAND合约价转跌且客户库存升','经营现金强，但客户押金12.747bn为履约/返还义务，巨额资本开支优先','供给扩张、普通存储价格、盈利顶部'),
('ON','汽车工业周期恢复和电源内容提升',[3,4.7,6],[13,20,24],'2027原ON收入7.35bn、经营利润1.96bn为经营锚；约4.7 EPS需并购后稀释/利息独立复算，高端不要求2030毛利目标提前。','2027工厂利用率、EPP量产、Synaptics整合','利用率不升且降价/收购稀释吞掉经营复苏','现金3.5145bn，须扣原债及目标净债约0.395bn；全股收购仍稀释','汽车需求、SiC过剩、并购交换比'),
('AGCO','农机库存周期拐点与PTx跨品牌升级',[4,8.5,12],[12,16,18],'2027正常税后利润约0.60bn/70m股=8.5；依赖欧洲盈利维持、北美亏损缩小，非立即软件平台化。','2027农机经销商去库、PTx改装订单、融资到期处理','经销商库存增而终端销量继续降；净债上升无盈利修复','6月净债2.154bn；2027债券0.4bn和授信到期，需留融资余量','农户收入、商品价格、渠道库存、融资'),
('IONS','自主药品采用与新批准产品代替失败管线',None,None,'12–18月 EV=2028销售1.3/1.9/2.6bn × 3.5/6/8；加剩余净现金0/0.2/0.4bn，除摊薄0.19/0.20/0.21bn股=23.95/58/100.95。销售为向前一年观察估计，债务和版税负担保留；不是2030移植。','2027 TRYNGOLZA付费启动、ZANVASTRO销售、合作审批','TRYNGOLZA付费治疗年斜率不能支持2028约2.4万门槛且合作款落空','2028年6月0.575bn债务；RP自2028分享SPINRAZA比例升45%，现金平衡不等于无需融资','降价后放量、基因编辑竞争、债务与版税融资'),
('BABA','电商现金与中国云重估的不同地域驱动',[6.5,10,13],[10,15,18],'情景美元ADS EPS为独立假设；必须核8普通股/ADS及人民币汇率和配售新股后才能执行。当前P/S货币错配不用。','2026Q4–2027云外部收入与利润、即时零售补贴收敛','云利润增长却自由现金持续恶化且反复融资','广义净流动性RMB207.975bn不是全可用；8月配售稀释约3.57%','政策、资本开支、补贴竞争、FX和VIE'),
('MOD','冷却交付与利润率恢复的经营杠杆',[6,10,13],[12,21,26],'FY27Q1 DC收入348.6m但EBITDA率14.8%；10 EPS要求2027交付增长和利润率恢复、分拆后证券归属需核，未重复加4bn协议。','2027客户验收、分拆及现金回款','销售增但现金及毛利持续恶化；客户扩产延期','净债432.9m；165m预付款有履约负担，不当免费现金','客户集中、零件齐套、分拆归属'),
('KYTX','小额高风险SPS注册/免疫重置期权',None,None,'12–18月股价=(融资后剩余现金0.05/0.07/0.10bn+风险调整管线EV0.05/0.90/1.60bn)/摊薄0.095/0.085/0.080bn股=1.05/11.41/21.25。先计从61.57m股增发到80–95m；EV研究假设，非成熟DCF。','2026Q4完整BLA；2027受理/审批；gMG入组，关键结果可能2027末–2028','CMC/安全实质阻断、需新增随机SPS试验而无融资','6月199.427m，H1烧81.903m，借款25m；额度150m非可用现金；预计新增融资150–190m','临床归因、单臂样本、制造/支付、重度稀释；灾难近零'),
('PGR','风险定价优势与家庭捆绑份额增长',[10,16,21],[13,17,19],'EPS不按低灾害CR87.2永久外推；2027净已赚保费约90–95bn、CR正常化约91–93%、投资收入与税后归属支持中枢。','2027月度保单、承保质量及家庭捆绑','保单失速并CR持续高于96%，长尾储备追加','32.9bn法定盈余支持承保；99.7bn投资资产对应大量保单负债，不是净现金','降价竞争、维修/诉讼通胀、巨灾'),
('BJ','较合理估值的会员新店复制',[4,5.1,6],[16,24,28],'FY27经营利润0.89bn、净利0.618bn；约121m股=5.1，较强为Texas续费/新店成熟快。','2027新店首轮正常价续费与同店商品量','会员增但租赁后FCF/股下降，汽油利润掩盖商品差','净债/EBITDA低于1倍是政策目标且不含租赁；真实H1现金182.1m低于调整值','新店资本、租赁、汽油利润、会员折扣'),
('RNR','低倍数再保险与第三方资本收费右尾',[18,35,50],[8,11,12],'2027普通股EPS需扣外部并表资本和优先股；35 EPS把灾损正常化，50仅低灾害/费率韧性条件，非照搬合并收入。','2027年1月续保价格、分出成本和回购','灾害和责任险储备共振侵蚀普通股资本','保险资产/浮存金不得当现金；第三方资本不全归普通股','大灾、责任险长尾、软市场、资本退出'),
('KR','低估食品零售的电商盈利与资本回报修复',[4.2,5.8,7],[9,14,16],'2027 EPS5.8须营运现金改善，剔除退款/折旧减记；不是用回购独自支撑。','2027电商净利润、营运资本恢复、Giant Eagle交割','件数继续下降、法律支出及收购吞噬FCF','现金1.676bn对含租赁债16.997bn，简化净债15.321bn；明显不是现金盒子','法律索赔、促销、并购/整合、调整现金流'),
('CB','分散承保与数字效率的较低倍数复利',[22,29,36],[10,14,16],'2027归属核心盈利约10.8bn/约0.37bn股=29；未来巨灾与责任险已正常化，36需海外和效率兑现。','2027中小险/海外增长、费用率下降与资本回报','责任险趋势持续超过费率且旧年储备反复上调','175bn现金投资对应赔款等巨额负债；只看可上划资本与普通股权益','长尾赔款、灾害、软化费率、寿险保证'),
('WM','再投资高峰回落、医疗整合和自动化兑现',[7.5,9.5,11],[21,27,29],'2027经营现金/利润改善支持9.5 EPS；不是把RNG全部项目毛收益加给股东。','2027医疗协同、RNG余下项目和资本开支下降','收费不能覆盖成本，医疗客户流失，协同靠调整项','6月总债23.356bn现金0.557bn，净债22.799bn；成熟收费缓冲非现金下限','负债、项目回报、环境责任；机会成本高于临床/周期弹性'),
]
special={'BNTX':[57.50,119.42,185.77],'IONS':[23.95,58,100.95],'KYTX':[1.05,11.41,21.25]}
n=[]
for rank,(t,th,eps,pe,formula,cat,kill,capital,risk) in enumerate(rows,1):
    prices=special[t] if eps is None else [round(a*b,2) for a,b in zip(eps,pe)]
    path=U[t]['sources']['company'][0]
    n.append(dict(rank=rank,ticker=t,thesis=th,horizon_months=[12,18],bear_price=prices[0],base_price=prices[1],bull_price=prices[2],price_anchor=float(U[t]['finance']['最新价格']),valuation_formula=('研究情景EPS '+str(eps)+' × P/E '+str(pe)+'；' if eps else '')+formula,catalysts=cat.split('；'),kill_criteria=[kill],key_risks=[risk,capital],capital_buffer_audit=capital,evidence=[path+'（正文经营、资本与反证章节）'],confidence='中低' if t in ['BNTX','IONS','KYTX','BABA','MOD','MU','ON'] else '中',scenario_status='独立条件估值；非校准概率；EPS/倍数均为假设，非Yahoo预测',action='小额临床期权，非缓冲核心' if t=='KYTX' else ('证券/分拆归属核验后配置' if t in ['BABA','MOD'] else '可进入终轮比较，不因预测不确定一律等待')))
alternates=[{'ticker':t,'reason':r} for t,r in [('TJX','净现金和折扣渠道较好，但主力成交弱、24.6倍前瞻估值使高回报证据弱于BJ。'),('WCN','价格/自动化及环境支出回落可修复；EPA新增工程令2027现金恢复有歧义，若确认现金见底可替代WM。'),('TRV','12.2倍有价值，但低灾害与准备金贡献解释大部分利润跃升，增长弱于PGR；可替代RNR降低巨灾弹性。'),('WRB','专业险经营优良、投资收入韧性；14.9倍并不明显优于CB，责任险长尾仍在。'),('COST','高质量净现金约15.1bn，但38.4倍、约10%经营增长不足以支持本任务的高收益优先级。')]]
exclusions=[{'ticker':t,'reason':r} for t,r in [('MRNA','INT阳性与新流感批准是实质亮点，但213.74美元价格对当前烧钱业务要求高，30亿美元新债和流动性门槛削弱现金底；10月24日完整数据仍未知。'),('WMT','广告和电商利润实质改善，但35倍前瞻估值、高capex及回购超FCF，使资本缓冲/预期差较弱。'),('RSG','服务网络成熟，但27倍、ES利润弱与收购投资后现金缺口，不如WM的近期整合兑现。'),('CWST','每股完整现金增长弱于总规模，增发与三地处置容量退出风险；59倍前瞻EPS难补偿。'),('CRWV','融资依赖及客户信用与AI预算高度相关，不满足本角色独立缓冲'),('NET','极高倍数，缺少足够近端现金定价缓冲'),('SMR','商业化和融资时点难在3–18月形成可审计下行缓冲')]]
out=dict(role='R5_diversification',screened_count=245,deep_read_tickers=deep,deep_read_method='29家公司正文的经济机制、财务资本、近期模型和反证章节选择性深读；不是全篇逐字核验',nominations=n,alternates=alternates,exclusions=exclusions,open_questions=['ALNY 2027 GAAP/经济EPS桥需逐项复算，不能直接拿vendor 12.42 EPS。','BNTX EV临床情景需核各地域权益；现金估值用FX情景非现汇。','BABA ADS比率及配售、MOD分拆权利、ON交换股数交给证券核验。','保险普通股利润需统一巨灾、准备金、外部资本；不能比较未经正常化的PE。','KYTX最新贷款契约/融资价格及FDA实际审评日需核；当前尚无确定PDUFA日。'],cutoff='2026-10-12 19:40 America/Los_Angeles',price_date='2026-10-12')
(B/'02_round1/R5_diversification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# R5：不同经营驱动与资本缓冲的20家首轮提名','', '全245扫描；29家选择性正文深读（含新增医药6、零售5、保险5、环保4）。首轮未读取其他角色报告。价格为冻结10/12收盘；事实截止10/12 19:40洛杉矶。','', '重点结论：高收益不必等同AI。ALNY/ARGX现有商业现金、BNTX癌症读数、KYTX小额注册期权、PNR渠道修复、AGCO库存/PTx周期分别有不同触发机制。把成熟保险/环保放在名单后端，要求其机会成本经过终轮比较，不为行业配额强留。','', '估值是独立12–18月条件点，不是2030目标价折搬。EPS×PE均为研究者输入；3条临床EV模型尤其低置信，不是假装精确的DCF。熊市点不是清算底；KYTX灾难可近零，其他临床/AI也可能超出熊点。未赋主观概率，故不计算假期望收益。','', '|序|代码|收盘|熊|基|牛|基准价格回报|逻辑|','|---:|---|---:|---:|---:|---:|---:|---|']
for x in n: lines.append(f"|{x['rank']}|{x['ticker']}|{x['price_anchor']}|{x['bear_price']}|{x['base_price']}|{x['bull_price']}|{(x['base_price']/x['price_anchor']-1):.1%}|{x['thesis']}|")
lines += ['', '价格回报不含股息、税费或汇兑。基准回报只是条件场景输出，不代表概率加权收益；例如RNR基准回报偏低而右尾高，其最终是否占20名应与其他角色高弹性候选竞争。','', '## 每家公司可核验的条件']
for x in n:
    lines += ['',f"### {x['rank']}. {x['ticker']}：{x['thesis']}",x['valuation_formula'], '催化剂：'+'；'.join(x['catalysts']), '资本审计：'+x['capital_buffer_audit'],'反证/退出：'+x['kill_criteria'][0]+'。风险：'+x['key_risks'][0],f"本地正文：[公司研究](../{x['evidence'][0].split('（')[0]})；外部核验见07_logs/R5_sources.json。"]
lines += ['', '## 候补与排除']+[f"- {x['ticker']}：{x['reason']}" for x in alternates+exclusions]
lines += ['', '## 组合推断与需核验处','医药5家并非完全独立：支付政策、风险偏好和生物技术融资共同相关；ARGX与KYTX在gMG远期又可能互相蚕食。KYTX只能是小额右尾，不宜与BNTX/IONS同权。NVDA、AVGO、MU、MOD仍共享AI资本开支；ON/AGCO/PNR更暴露制造、农业、住房周期。保险三家共享长尾通胀和风险资本，不能把三票当三套独立缓冲。', '合理中枢并非每项取最低：ALNY基准承认需求恢复、ARGX保留CIDP增长与肌炎窄标签；BNTX保留确证读数重估；AGCO不要求2027已成为软件公司。相反，MRNA不因临床成功就忽略已经较高的股价门槛。', '价格假设需要终轮对EPS口径、稀释和ADR作审计；无法通过时保留经营提名但将价格置空，而不是换用未经核验的供应商数字。']
(B/'02_round1/R5_diversification.md').write_text('\n'.join(lines),encoding='utf-8')
with (B/'07_logs/R5_245_screen.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['ticker','category','price','forward_pe','validation','r5_disposition'])
 for t,x in U.items():
  tag='nominated' if t in [z['ticker'] for z in n] else ('deep_read_alternate_or_excluded' if t in deep else 'screened_not_shortlisted')
  w.writerow([t,x['category'],x['finance']['最新价格'],x['finance']['Forward PE'],x['finance']['估值校验'],tag])
assert len(n)==len({x['ticker'] for x in n})==20 and len(U)==245 and len(deep)>=25
print('saved 20 nominations, 29 deep reads, 245 screen rows')
sources=[
('BNTX','2026-08-04','https://www.sec.gov/Archives/edgar/data/1776985/000177698526000054/a991bntx_q22026pressreleas.htm','现金和证券EUR16.6342bn；ADS 1:1；251.204m股；FY26收入指引1.6–1.9bn；2026晚期读数计划','现金支持多轮验证，但不能视作股价地板；管线EV为独立假设'),
('KYTX','2026-03-26','https://www.sec.gov/Archives/edgar/data/1994702/000119312526126216/kytx-ex99_1.htm','旧公告279.3m现金，贷款150m只有初始25m；原计划H1完整提交','旧融资跑道不覆盖最新支出与提交延迟；不沿用旧日期'),
('IONS','2026-07-29','https://www.sec.gov/Archives/edgar/data/874015/000087401526000251/form10q.htm','2028年6月575m债券本金；2030年770m；RP 2028起SPINRAZA分享45%','新销售盈利不能替代债务再融资；模型保留融资/版税'),
('MRNA','2026-07-31','https://www.sec.gov/Archives/edgar/data/1682852/000168285226000147/exhibit9912026q2pressrelea.htm','年底现金指引4.7–5.2bn且不含剩余贷款提款；norovirus中期未达提前成功','其后新增可转债只增加现金与债务，不创造经营价值'),
('PGR','2026-09-18','https://www.sec.gov/Archives/edgar/data/80661/000008066126000322/pgr202608ex99earningsrelea.htm','8月累计CR87.2；此前事故有利发展1393m','正常化CR比报告高；仍保留份额增长积极分支'),
('KR','2026-09-11','https://www.sec.gov/Archives/edgar/data/56873/000110465926108926/kr-20260815x10q.htm','现金1676m；流动债1838m及长期债15159m（含融资租赁）','简化净债15321m；低PE并非低资本风险'),
('ARGX','2026-07-23','https://argenx.com/news/2026/press-release-3331862.html','H1产品销售2813m，经营利润887m','已商业盈利的增长路径与纯临床赌博应区别；未来价量仍假设'),
('AGCO','2026-07-30','https://www.sec.gov/Archives/edgar/data/880266/000088026626000068/agco-20260630.htm','长债2180.3m、短债546.7m；2027年400m票据；循环授信2027-12到期','周期拐点要同时观察终端和融资'),
('KYTX','2026-08-11','https://www.sec.gov/Archives/edgar/data/1994702/000119312526344607/kytx-20260630.htm','二季度资产负债、现金流、债务与潜在稀释原文已打开；199.427m合计需现金和证券相加','不把150m额度全部加现金；首轮金额交叉使用冻结公司正文，终轮应复加'),
('KYTX','2026-09-24','https://ir.kyvernatx.com/news-releases/news-release-details/kyverna-therapeutics-reports-positive-one-year-data','标题及原文页面可打开；单独find暂返回internal error；一年临床结果见冻结正文并保留同源边界','26人单臂与gMG7人不能推永久治愈；积极证据允许小额右尾'),
('ARGX','2026-10-08','https://argenx.com/news/2026/press-release-3376934','UNITY独立委员会建议因无效停止；没有新安全信号','不推翻既有gMG/CIDP收入；不把全平台机会视作确定'),
('IONS','2026-09-03','https://www.fda.gov/news-events/press-announcements/fda-approves-first-drug-treat-alexander-disease','FDA批准Zanvastro治疗Alexander病，季度鞘内给药；49人随机研究及4名低龄子研究','新获批是正向事实；人群小，不能单药填整个集团收入'),
('ALNY','2026-07-30','https://investors.alnylam.com/press-release?id=ddc78e15-7847-4066-8fdb-3562023a60f4','TTR收入1030m；全年指引降至4.2–4.5bn；美国需求增129m但库存约-20m；增长不完全是压货','同时承认去积压减速和真实新需求；不机械把下调解释终局'),
('AGCO','2026-10-06','https://investors.agcocorp.com/events/event-details/agco-2026-technology-event','技术日日期/演示与转录文件存在；仅索引实读，没有声称完成PDF核验','PTx机会依据冻结正文，索引不算技术商业化证明'),
('WM','2026-07-28','https://investors.wm.com/static-files/7330b8ac-17d7-4959-bdb4-f05f7cb39906','Q2调整EBITDA2.067bn、CFO1.73bn；RNG/回收增40m；上调利润率但降收入区间','现金改善与新增项目是实际亮点；仍需扣真实资本与环境责任')]
log={'role':'R5','retrieved_at_local_date':'2026-10-12','cutoff':'2026-10-12 19:40 America/Los_Angeles','queries':['直接打开冻结正文引用的SEC/IR/FDA网址；逐项find cash、2028、87.2、1676、2813、2180、futility、September','site.investors.alnylam.com 2026 July 30 second quarter TTR 4.2 4.5','site.investors.agcocorp.com 2026 October technology day PTx','site.ir.bjs.com 2026 September 14 financial policy（未取得可用新增结果）','site.investors.wm.com 2026 second quarter 2027 synergies'],'sources':[dict(id='R5-S%02d'%(i+1),ticker=t,published_date=d,url=url,fact=f,research_inference=h,access='原始来源页面打开及相关段落查读；明确限制见fact') for i,(t,d,url,f,h) in enumerate(sources)],'limitation':'未声称各公司全部事实外部双重核验；证券/资本公式需终轮审计；没有使用晚于截止的内容。搜索出现非原始来源，未作为事实证据。'}
(B/'07_logs/R5_sources.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'07_logs/R5_stage2.md').write_text('完成245行扫描，29家正文重点章节选择性深读，新增20家全部覆盖；20唯一提名、5候补、7排除；15原始页面访问（其中AGCO技术日为索引不计实质事实来源，KYTX临床find失败已记）。经营亮点和反证双向保留；临床EV为低可靠条件输入，绝非校准目标。仅写实验目录，无Git/生产队列。',encoding='utf-8')
