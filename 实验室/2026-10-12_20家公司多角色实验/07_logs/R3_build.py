import json,csv,datetime,pathlib
R=pathlib.Path('D:/investment/实验室/2026-10-12_20家公司多角色实验')
U=json.loads((R/'01_inputs/universe.json').read_text(encoding='utf-8-sig')); by={x['ticker']:x for x in U}
stamp=datetime.datetime.now().astimezone().isoformat()
sources=[
('ADBE','2026-09-10','https://www.adobe.com/cc-shared/assets/investor-relations/pdfs/01906202/au56y4ter.pdf','Adobe 2026 third quarter results','Q3收入6.76B、GAAP EPS4.62；FY26 GAAP EPS指引18.12–18.17，非GAAP24.45–24.50。不能直接采用快照27.67为经济EPS。'),
('ALNY','2026-07-30','https://investors.alnylam.com/press-release?id=ddc78e15-7847-4066-8fdb-3562023a60f4','Alnylam 2026 second quarter results','TTR全年收入指引从4.4–4.7B降至4.2–4.5B，积压二线需求正常化；反驳持续外推上市初速。'),
('PNR','2026-07-28','https://investors.pentair.com/node/27096/pdf','Pentair 2026 second quarter results','Pool季度收入下降42%；FY26调整EPS指引4.60–4.80，反驳无条件低PE安全垫。'),
('IONS','2026-04-29','https://ir.ionis.com/news-releases/news-release-details/ionis-reports-first-quarter-2026-financial-results-and','Ionis 2026 olezarsen approval','Q1收入246M、现金短投1.9B，峰值销售是公司目标。此源过时，只作前后对照，不能沿用待审批清单。'),
('ENPH','2026-07-28','https://newsroom.enphase.com/news-releases/news-release-details/enphase-energy-reports-financial-results-second-quarter-2026','Enphase 2026 second quarter financial results','收入291.9M包含safe-harbor84.3M；Q3指引290–320M含75M，AI SST仅RFI/RFP。'),
('BNTX','2026-08-04','https://investors.biontech.de/node/18731/pdf','BioNTech 2026 second quarter results','现金及证券16.6B欧元；FY26收入指引1.6–1.9B欧元，研发2.0–2.3B与SG&A0.7–0.8B；现金持续消耗。'),
('BJ','2026-08-21','https://investors.bjs.com/press-releases/press-release-details/2026/BJs-Wholesale-Club-Holdings-Inc--Announces-Second-Quarter-Fiscal-2026-Results/default.aspx','BJ 2026 second quarter results','FY26 EPS指引4.60–4.80；资本开支800M，新店扩张并非资产轻。'),
('PNR','2026-10-01','https://investors.pentair.com/news-releases/news-release-details/pentair-completes-acquisition-taco-group-holdings','Pentair completes Taco October 1 2026','Taco已完成14亿美元收购，纠正9/26公司报告的待交割状态；不能因此假设协同已实现。'),
('DOV','2026-08-28','https://www.epa.gov/hfcs/technology-transitions-hfc-restrictions-sector','EPA 2026 HFC restrictions 2032','超市系统2027先实施1400 GWP门槛，较严150/300延至2032；取消2027全面CO2强制替换的收益假设。'),
('NVDA','2026-08-26','https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027','NVIDIA second quarter fiscal 2027','Q2收入96.221B、数据中心89.023B；Q3指引108B和74%毛利。强交付证据仍非买方投资回报证明。'),
('IONS','2026-09-04','https://www.novartis.com/news/media-releases/novartis-announces-lpahorizon-phase-iii-topline-results-pelacarsen-patients-elevated-lpa-and-established-cardiovascular-disease-cvd','Novartis pelacarsen Lp(a)HORIZON results','读取合作方公告核对本地所列主要终点失利；旧管线成功概率不可沿用。'),
('VST','2026-08-07','https://www.sec.gov/Archives/edgar/data/1692819/000169281926000017/vistra-20260630xearningsre.htm','Vistra 2026 second quarter results','2026 EBITDA6.8–7.6B、FCFbG3.925–4.725B指引；2027发电94%已对冲，Helix最多承诺1B。FCFbG不是扣全部增长投资后的股东现金。'),
('CRM','2026-08-26','https://investor.salesforce.com/news/news-details/2026/Salesforce-Delivers-Record-Second-Quarter-Fiscal-2027-Results/default.aspx','Salesforce fiscal 2027 second quarter results','股数指引计入ASR初交103M股但排除最终结算；需防把回购缩股与运营增长重复计入。')]
logs=[dict(id=f'R3S{i+1:02}',ticker=t,published_date=d,url=url,query=q,accessed_at=stamp,read_status='opened_primary_document',summary=s) for i,(t,d,url,q,s) in enumerate(sources)]
(R/'07_logs/R3_sources.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2),encoding='utf-8')
deep='ADBE ALNY IONS PNR BNTX PGR RNR BJ KR AGCO ENPH FLNC BABA ORCL CRM MCHP SMCI NVDA AVGO MU VST ENS MOD BDC UCTT AMKR PLAB CARR DOV AVAV'.split()
# All parameters below are independent conditional estimates, not company guidance.
rows=[
('ADBE',[17,21,24],[10,15,20],'成熟订阅被AI替代叙事折价，真实文档与企业收费尚在增长。用保留SBC的盈利估值，不为AI ARR单独再加价。','6–12月FY27续约与提价周年；12–18月净席位和积分收费','连续两季可比ARR低于5%且经济利润下滑','创意席位减少、并购掩盖有机增速、管理交接','分批候选','高'),
('NVDA',[9,14,18],[13,21,27],'平台收费能力与当前盈利比高PS小型光芯片更可核验；反共识在相对估值，不在否认市场已经预期高增长。','3–6月Rubin交付与回款；6–12月FY28预算','DSO持续高于70天且现金转换继续恶化，或毛利跌破65%','客户融资、资本开支循环、出口与集中度','分批候选','中高'),
('PNR',[3.5,5,6],[10,14,17],'渠道修复与Taco现金整合可在18个月内检验，买价不需要把全部水业务重估为AI。','3–6月2027指引；6–12月泳池季；12–18月去杠杆','泳池sell-through持续落后竞争者或并购后净债务未按计划下降','品牌份额损失、债务、一次关税退款','分批候选','中'),
('BDC',[6.5,8.5,11],[10,16,20],'工业网络现金基础加RUCKUS整合，优于纯靠光模块远期份额的定价；但大收购意味着必须按利息后收益估值。','3–6月RUCKUS独立现金桥；6–12月交叉销售与光订单交付','并购毛利提升但利息后现金持续减少','杠杆、整合、关税退款、匿名大客户','等待并购后现金验证','中'),
('MCHP',[2.8,4,5.2],[14,22,26],'MCU库存修复比机器人远期TAM更快兑现；PCIe定点提供附加弹性，不能把12个定点都按最大项目推算。','3–6月库存与产能利用率；6–12月Gen6订单','库存金额继续增加而收入转降；债务契约余量缩小','约54亿债务、分红占款、订单取消','分批候选','中'),
('CARR',[2.5,3.5,4],[14,21,25],'数据中心订单与住宅修复两条路径，当前16.8倍快照远期PE低于纯数据中心热管理；集团基数降低单一技术风险。','3–6月数据中心交付加速；6–12月住宅补库','下半年数据中心销售显著无法接近公司目标且住宅再次转弱','欧洲低利润、交付、回购与债务争现金','分批候选','中'),
('MOD',[6,9,12],[14,23,28],'有预付款支持的实际数据中心交付比多数冷却概念更强，盈利爬坡形成弹性。','3–6月EBITDA率回升；6–12月新厂交付','收入高增但数据中心利润率长期低于15%或核心客户延迟','客户集中、165M预付款不可重复、技术配置变化','等待剔除预付款后现金改善','中'),
('AVGO',[12,17,22],[15,23,28],'定制计算与基础软件双利润池，作为昂贵ASIC设计与光互联个股的替代；折扣估值需保留SBC与战略投入。','3–6月AI交付和软件续约；6–12月多客户项目','AI收入增长但营运资本与客户信用支持吞噬现金','系统混合降低毛利、客户集中、软件提价反弹','分批候选','中'),
('VST',None,None,'现成发电资产及对冲现金优于未商业化SMR；容量和并购贡献可观察，但不把AI现货涨价作用到全部已锁价电量。','3–6月2027现金指引；6–12月容量与并购协同','增长投资持续超过可用现金且净债务升高；重大非计划停机','对冲、气价、监管、1B Helix承诺','等待全投资后现金桥','中'),
('CRM',[9,12,15],[15,23,28],'企业数据权限与执行层仍有续费价值；折价成熟平台优于高倍数应用叙事，但仅列ADBE后的补充。','3–6月同口径Agentforce收费；6–12月降债','剔除并购后的增长低于4%且净债务不降','39.5B债务、AI指标口径变化、投资收益','条件分批','中'),
('ALNY',None,None,'已盈利RNAi平台是对AI资本开支链的独立替代；下调TTR指引后需证明一线患者持续增长，非无条件低PE。','3–6月TTR新患者；6–12月净价与现金；12–18月PN试验进展','TTR再次实质下修且非一次因素；净价下降抵消患者增长','Sanofi高阶梯30%版税、稳定剂竞争、递延税项','等待季度验证；目标价暂缺','中低'),
('BNTX',None,None,'大型现金与多资产肿瘤读数给非AI右尾，但mRNA标签不是整个平台成功，BMS分享权益必须扣除。','3–6月具体随机读数；6–18月注册推进','关键随机试验失败并持续扩大费用预算','现金消耗、双抗50%权益、ADC地域权利、创始人交接','等待明确读数与ADS/FX复算','中低'),
('BJ',[4.3,5.2,6],[16,23,27],'约20倍快照PE与COST约38倍形成会员制直接替代；新市场复制比纯消费防御更有成长弹性。','3–6月会员费和续费；6–18月Texas新店完整年度','成熟续费率低于88%或新店资本回报明显下修','汽油扰动、800M资本开支、费用共享','分批候选','中高'),
('AGCO',[4,8,10.5],[11,16,19],'农业下行中欧洲品牌和跨品牌PTx提供复苏期权，比近28倍远期PE的DE要求更低；利润恢复仍有区域差异。','3–6月年末现金与渠道；6–18月北美/拉美减亏','欧洲利润实质衰退且其他区域继续烧现金','农户预算、汇率、关税退款与融资收益','等待Q4现金证据','中'),
('PGR',[10,15,18],[12,17,20],'高频重新定价与车险份额增长提供独立利润源，组合价值来自降低AI共同因子，而非浮存金作价格底线。','3–6月月度保单和CR；6–12月续保与家庭捆绑','剔除准备金释放后CR持续超过97%且保单增长停滞','赔付通胀、准备金、竞争、巨灾','分批候选','中'),
('KR',[4.2,5.4,6.2],[9,14,17],'低倍数食品现金业务与效率修复，比为零售AI广告支付高增长倍数更朴素；回报主要是现金和温和重估。','3–6月食品件数；6–12月电商盈利持续与资本纪律','食品实物销量持续流失且回购/收购提高杠杆','价格竞争、药房口径、收购执行、租赁','分批候选','中'),
('DOV',[8.5,11,13],[14,21,24],'成熟工业耗材和制冷交付修复提供现金支持；剔除已延后的法规强制替换，液冷只是补充。','3–6月工厂整合；6–12月有机订单恢复','工厂交付延迟转为客户转单且有机增长停滞','工厂执行、并购增长、法规推迟','分批候选','中'),
('UCTT',[3,5,7],[9,15,20],'先进设备外包扩张的较低倍数载体，提供高弹性但不把40亿产能当收入。','3–6月库存转回款；6–12月合格产能放量','连续两季收入增长而库存/应收更快增长及ATM融资','采购义务非客户订单、集中度、可转债稀释','等待FCF转正，小额风险预算','中低'),
('PLAB',[1.6,2.2,2.8],[10,17,21],'高端DUV/显示光罩升级较少被纯AI叙事定价，但晶圆数量不直接生成光罩费；真实高端设计订单才是驱动。','6–12月高端IC/FPD组合；12–18月韩国能力','高端增长无法抵销主流下滑且设备资本开支持续吃掉现金','中国政策、资本强度、汇兑收益与少数股东','条件分批','中'),
('ENPH',[1,2,3],[12,18,24],'仅保留受损住宅渠道修复的高弹性期权；AI SST不计入基准收益，safe-harbor和45X必须拆开。','3–6月非safe-harbor收入止跌；6–12月G5区域交付','剔除safe-harbor后两季继续明显下降或45X资格受损','政策补助、安装融资、库存、SBC','严格等待，不能按现有14倍PE直接买入','低')]
noms=[]
for rank,(t,eps,mults,thesis,cat,kill,risk,status,conf) in enumerate(rows,1):
    price=float(by[t]['finance']['最新价格'])
    prices=[round(a*b,2) for a,b in zip(eps,mults)] if eps else [None]*3
    formula={'method':'economic diluted EPS x conditional P/E','eps_bear_base_bull':eps,'pe_bear_base_bull':mults,'period':'2027年末前后可见的未来12个月经营盈利，目标交易日2027-10-12','definition':'独立估算，含利息税和正常SBC；剔除一次投资收益/关税退款。以现有资本结构附近为起点，不额外假设回购；稀释增加5%则价格除以1.05。债务利息已在EPS，不能再减净债务。','limitation':'首轮近端压缩模型；不是已完成收入-利润-股本三表模型。进入终选前须核验税率、SBC和完全稀释股数。'}
    if t=='VST':
        prices=[100,190,275]; formula={'method':'all-investment-after equity FCF / diluted shares x P/FCF','fcf_bn':[2.4,4.2,5.5],'shares_bn':[0.336,0.331,0.320],'multiples':[14,15,16],'unrounded_prices':[100,190.33,275],'definition':'FCF须扣利息税、维护及增长资本支出、Helix承诺和其他权益分配；不可直接采用FCFbG。3个现金点均为研究假设，非公司指引。净债务不重复扣。','limitation':'基准全投资后4.2B需核验，故等待；稀释5%降低目标约4.8%。'}
    if t in ['ALNY','BNTX']:
        formula={'method':'暂不量化','reason':'ALNY快照forward EPS可能混税项/调整口径，缺近端经济盈利桥；BNTX需要同日EUR/USD、ADS比率和分资产rNPV。不能拿2030价格移到18个月。','needed':'最新完全稀释股数、净债务及受限制现金、2027费用、临床/销售节点'}
    loc=by[t]['sources']['company'][0]
    evidence=[{'type':'frozen_company_analysis_not_primary','path':loc,'lines':'5-40及经营财务/风险相关段落'}]+[{'source_id':s['id'],'url':s['url'],'published_date':s['published_date']} for s in logs if s['ticker']==t]
    noms.append(dict(rank=rank,ticker=t,price_anchor=price,price_date='2026-10-12',currency='USD',thesis=thesis,horizon_months=12,bear_price=prices[0],base_price=prices[1],bull_price=prices[2],valuation_formula=formula,catalysts=cat,kill_criteria=kill,key_risks=risk,evidence=evidence,confidence=conf,entry_status=status,base_price_return_pct=round((prices[1]/price-1)*100,1) if prices[1] else None))
alts=[('ENS','剔除45X和关税退款后核心EPS远低于表观，成熟产品好但近端赔率不及PNR/CARR；若回到140附近且业务未坏可上调。'),('RNR','8倍前瞻PE不足以排除价格软化与准备金风险；可替代PGR但先需正常灾损/归属普通股利润桥。'),('AMKR','已有客户预付款支持，但美国120亿美元计划与近端FCF错配；18个月相对更偏MCHP/BDC。'),('IONS','旧两大心血管管线失利与TRYNGOLZA降价必须重置基线；等待付费治疗年而非峰值目标。'),('AVAV','LOCUST真实采购提高右尾，但BlueHalo减值、订单重授及负现金使现价不优于本名单。'),('ORCL','OCI交付真实但预付款提高CFO而资本开支更大；低PE不代表低资金风险。'),('BABA','AI云收费增长伴随AI实验室亏损与负FCF；仅低PE无法优于ADBE，另有ADS/币种约束。')]
exc=[('MU','不因4.79倍远期PE列首选：FY26Q4毛利86.8%、普通存储超额利润是脆弱锚；需报价/合约与中周期利润模型。'),('SMCI','7.51倍PE对应FY26负FCF约6.97B、不可取消采购与可取消订单错配，暂不接受低估值论。'),('FLNC','9/16下修并非纯收入延后：赔偿/质量/新品成本不会自动回来，等现金与交付恢复。'),('PLTR','81.59倍销售和89.16倍前瞻盈利要求持续高增长，3–18月容错不及成熟软件。'),('RKLB','54.63倍销售已支付很大成功价值，发射成功不等于股东收益。'),('BE','24.81倍销售与53倍前瞻盈利已反映很强短缺，改选现存发电VST/混合冷却CARR。'),('MRNA','38.3倍销售且仍亏损，同医药风险预算优先ALNY/BNTX。'),('TSLA','173倍前瞻PE内含远期自动驾驶机器人成功，与18个月可核验现金窗口不匹配。')]
out=dict(role='R3_external',screened_count=len(U),deep_read_tickers=deep,nominations=noms,alternates=[dict(ticker=t,reason=s) for t,s in alts],exclusions=[dict(ticker=t,reason=s) for t,s in exc],open_questions=['独立估值首轮是压缩敏感性，不能冒称完成收入/利润/资本三表核验。','ALNY forward EPS税项/调整口径须重新归一；BNTX近端rNPV/ADS/FX未完成，保留null和等待。','市场拥挤仅以倍数与明确共识基线推断；没有持仓/资金流证据，不能称实测拥挤。','一组主观概率尚未校准；本轮不报伪精确加权收益。','20家公司不是等权可执行组合：多只需等待现金/读数验证，金融快照价格仅作冻结锚未逐只外网核价。'],as_of='2026-10-12T19:40:00-07:00',generated_at=stamp)
(R/'02_round1/R3_external.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# R3：外部视角与反共识首轮独立提名','',f'冻结信息截止2026-10-12 19:40 PDT；价格锚为当日正常收盘。生成时间 {stamp}。扫描245家，定向深读30家公司经营、财务、风险关键段落；六类资料均已进入阅读。没有读取其他研究者首轮结论。','', '## 裁决逻辑','', '先寻找当前盈利和现金能支持的近端修复，再加入有实证的高增长。反共识不是一律做空AI：NVDA/AVGO仍入选，但不把市场已预期的增长误称惊喜。对MU、SMCI、ENPH等，低PE须先经过利润周期、现金和补贴检查。18个月并不容许把2029/2030远期目标原样挪用。','', '本名单有软件、药品、会员/食品零售、保险、农机、工业、水设备、电力及半导体。共同AI预算因子并未消失；MCHP/BDC/CARR也不是纯消费防御。ALNY与BNTX保留估值空值，等待条件成立才可转为可执行候选。','', '## 能改变取舍的外部证据','']
for s in logs: md.append(f"- **{s['id']} {s['ticker']}，{s['published_date']}**：{s['summary']} [原文]({s['url']})")
md+=['','明确过时修正：PNR公司报告9/26的待交割已被10/1完成公告替代。IONS4月路线图仅作历史对照，9月失败的管线不能继续当待开奖催化。EPA当前分项表优先于仍展示旧2027门槛的旧版摘要PDF。','', '## 20家独立提名','', '|顺序|公司|收盘锚|悲观/基准/乐观 USD|基准价格收益|动作|','|---|---|---:|---|---:|---|']
for n in noms:
    pp='/'.join('待核验' if n[k] is None else str(n[k]) for k in ['bear_price','base_price','bull_price'])
    md.append(f"|{n['rank']}|{n['ticker']}|{n['price_anchor']}|{pp}|{n['base_price_return_pct'] if n['base_price_return_pct'] is not None else '—'}%|{n['entry_status']}|")
md+=['','所有目标为研究条件交易价格，非公司指引；12个月比较点为2027-10-12，催化最多延长至18个月。价格收益未含股息/税费/汇兑，不能称总收益。悲观不是损失上限；永久损伤和融资危机下可更低。','', '## 逐家公司依据、反证和估值','']
for n in noms:
    md += [f"### {n['rank']}. {n['ticker']} — {n['entry_status']}",'',n['thesis'],f"- 催化与窗口：{n['catalysts']}",f"- 证伪：{n['kill_criteria']}",f"- 风险：{n['key_risks']}；判断置信度：{n['confidence']}（非概率）。",f"- 估值：{json.dumps(n['valuation_formula'],ensure_ascii=False)}",f"- 本地证据：[{n['ticker']}公司研究]({n['evidence'][0]['path']})，5–40行及财务/风险段；外部关联：{', '.join(e['source_id'] for e in n['evidence'][1:]) or '本轮未独立重核，进入终选须补原始核验'}。",'']
md+=['## 直接与跨行业替代','', '- ADBE优先于CRM：当前经济现金便宜程度更高，CRM债务与并购指标复杂；两者均优于仅因AI而高估值的PLTR/SNOW。','- BJ相对COST/WMT：成熟会员收费同样存在，买价约20倍而非35–38倍前瞻PE，但低估值一部分来自较小规模和新区域风险；KR提供更便宜、更低增长的食品现金替代。','- PNR/CARR相对VRT/BE：接受较少纯AI曝险，换取泳池/住宅修复和较低倍数；若只追求AI增长，NVDA更直接。','- ALNY/BNTX相对AI硬件：临床、支付和处方是不同驱动；BNTX现金会消耗，ALNY增长也已下调，均不能当无风险对冲。','- VST优于OKLO/SMR的近端发电现金；AGCO优于为机器人TAM提前付费；但二者均有周期和债务风险。','', '## 候补与淘汰','']
for t,s in alts:md.append(f'- 候补 **{t}**：{s}')
for t,s in exc:md.append(f'- 暂不选 **{t}**：{s}')
md+=['','## 方法、完整性和待核验','', '全池初筛采用分类、正/负盈利、倍数、币种校验和现阶段商业化门槛。缺失PE不自动排除，先进入证券/财务口径核验；REIT不使用PE跨行业机械排序。筛选结果保存R3_screen_245.csv。深读定义为阅读公司事实/财务/风险关键段落并与替代业务比较，并非全文逐行尽调。',f"深读公司：{', '.join(deep)}。",'六类输入：公司调研、行业调研（核酸/会员零售/冷却水处理）、产业背景（AI Infra Summit）、金融冻结快照、公司情景和公司对比。后两者仅用于发现假设与日期冲突，不将其目标价或评级当事实。','']+['- '+x for x in out['open_questions']]
(R/'02_round1/R3_external.md').write_text('\n'.join(md),encoding='utf-8')
nomset={n['ticker'] for n in noms}; altmap=dict(alts); exmap=dict(exc)
with (R/'07_logs/R3_screen_245.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['ticker','category','stage','reason'])
    for x in U:
        t=x['ticker']; v=x['finance']; pe=v.get('Forward PE',''); cur=v.get('financial_currency','')
        stage='nomination' if t in nomset else 'alternate' if t in altmap else 'excluded' if t in exmap else 'screened_not_deep_selected'
        reason=altmap.get(t,exmap.get(t,'')) or ('定向深读后提名，见报告' if t in nomset else '初筛比较商业阶段、估值与行业预算共同因子；不代表已完成公司尽调。')
        if cur!='USD':reason+=' 财务币种非USD，PS原值不可直接使用。'
        reason+=f' 冻结Forward PE={pe}。'
        w.writerow([t,x['category'],stage,reason])
assert len(U)==245 and len(noms)==20 and len(set(deep))>=25
assert all(n['ticker'] in by for n in noms)
print(json.dumps({'nominations':len(noms),'deep_read':len(deep),'screened':len(U),'primary_documents':len(logs),'files_written':['02_round1/R3_external.md','02_round1/R3_external.json','07_logs/R3_sources.json','07_logs/R3_screen_245.csv']},ensure_ascii=False))
