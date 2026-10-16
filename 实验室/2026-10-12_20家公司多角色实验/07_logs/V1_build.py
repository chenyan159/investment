import json
from pathlib import Path
B=Path(r'D:\investment\实验室\2026-10-12_20家公司多角色实验')
all_sources={}
for name in ['S1_sources','S2_sources','B1_sources']:
    for s in json.loads((B/'07_logs'/f'{name}.json').read_text(encoding='utf-8-sig'))['sources']:
        all_sources[s['id']]={**s,'discovery_log':name}
sources={}
def src(key, note, status='independent_body_read', date=None, url=None):
    s=all_sources.get(key,{})
    sources[key]={'id':key,'source_url':url or s['url'],'published_date':date or s.get('published') or s.get('publication_date') or s.get('published_date'), 'access_status':status,'read_by':'V1','reading_note':note,'discovery':s.get('discovery_log','V1 new discovery'), 'accessed':'2026-10-12 LA, cutoff 19:40; accessed after freeze, use only pre-cutoff publication'}

src('NVDA_Q2','FY27 non-GAAP包含SBC；Q2收入96.221B，CFO24.077B，AR占用22.346B；投资证券净收益7.771B非经常经营利润。')
src('MU_REMARKS','26份SCA；32B客户承诺；约35%至2030累计收入、其3/4有定价框架。Q1GM86.25%为公司预计全年低点，Q4客户存款12.3B在融资现金流。')
src('AVGO_Q3','Q3调整OP20.095B与SBC2.019B，经济OP18.076B是保留SBC、允许其他调整的研究口径。')
src('CLS_Q2','Q2收入4.70B；GAAP EPS3.17含TRS税前0.90/股；TRS104.1M、SBC19.3M不同项目。2027收入增长超过65%为管理层展望。')
src('S2-01','收入6.76B、ARR27.50B，GAAP与non-GAAP EPS4.62/6.13；用经济薪酬口径估值。')
src('PNR_CLOSE','Taco10/1按1.4B完成；并表Water Solutions；协同/交叉销售未变成既有利润。',date='2026-10-01',url='https://investors.pentair.com/node/27181/pdf')
src('S2-28','已交割；0.44619 THRM/旧MOD股，9/28登记；新购MOD不含该历史分派。')
src('IREN_FY26','4B contracted ARR vs1B operating；两年回收期仅GPU与配套除直接成本；FY26 CFO2.1004B含递延收入增加1.8417B。')
src('B1-10','逐期最低GPU、5天验收、15工作日纠正、延期抵扣及终止权；公司IR与同合同SEC不算独立根事件。')
src('S2-07','TTR销售指引从4.4–4.7B降4.2–4.5B；二线积压需求正常化，仍为高增长。')
src('SNDK_Q4','Q1收入10.3–10.8B、nonGAAP GM83–85%、EPS44–46、约155M股均为公司指引。')
src('PSIX_Q2','Q2收入152.5M、GM27.1%、净利16.9M/EPS0.73。2026Q2税费5.6M；29.2M税备抵释放是2025同期，不能再从2026Q2扣。')
src('S2-17','现金证券EUR16.6342B、流通251.204M；H1净亏EUR1.3527B。不能把欧元当美元或现金全算永久底。')
src('S2-13','ALKIVIA联合IMNM/DM主要终点p=.0011、优势15.4点；IMNM p=.0048、DM p=.1093。DM效应相似但未单独显著。')
src('B1-16','UNITY 10/8因无效停止，属于Sjögren项目；不抹除gMG/CIDP已销售价值。')
src('S2-12','Q2全球产品销售1.516B，H1 2.813B；已扩gMG全血清型；MMN Q4读出为预期。')
src('S2-16','9/24 KYSA8一年已公布，26人单臂；49% T25FW改善，95%持续率分母是早期改善者，92%免慢性免疫治疗。')
src('S2-26','Q2 DC订单+300%以上；有机收入+3%，调整OP同比-6%，全年23B收入/2.90调整EPS为指引。')
src('S2-21','Q2收入2.6097B同比-1%，恒汇率-3.7%；22M关税退款、20M融资未来收入前置；2026 EPS5.50–5.75为指引。')
src('S2-34','云收入RMB48.437B+45%；重划分云包含T-Head，不可将新增分部口径不加辨别地拼旧年数据。')
src('S2-31','8月CR89.3 vs83.1，事故年损失率70.6 vs日历68.8；往年有利发展131M，净已赚保费7.354B。')
src('FLNC_RESET','9/16覆盖8月指引：收入2.4B，调整EBITDA亏200M；2027 CFO中性或正仅目标。')
src('S2-25','Q2收入750M、有机+8%，订单836M、B/B1.11；RUCKUS7/1在季后交割。')
src('S2-27','收入1.485B、环比13.2%，库存185→175天，Gen6定点6→12；定点不等收入。')
src('S2-29','Agentforce ARR改含Slackbot/Headless360；FY27收入46.1–46.4B含待收购，cRPO指导不含二项待收购。')
src('TSM_SEPT','9月NT511.857B、同比54.6%，1–9月+41.1%；月收入不是利润或ADR EPS。')
src('POET_FS','客户供应协议预期采购up to500M，不是无条件确认收入；22.921408M客户权证、30.142069M客户对价按收入摊销。')
src('SMCI_Q4','8/11发布Q4 GM17.5%、调整17.6%，EPS1.62/1.70，FY27收入65–72B指引；当时属未审计估计。',date='2026-08-11',url='https://ir.supermicro.com/news/news-details/2026/Supermicro-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Financial-Results/default.aspx')
src('SMCI_10K','8/31 BDO财报无保留、内控否定；3旧弱点修复，1ITGC仍存；FY26 CFO-6.8099B，净利2.2305B。',date='2026-08-31',url='https://www.sec.gov/Archives/edgar/data/1375365/000137536526000022/smci-20260630.htm')
src('VST_Q2','8/3套保2027 94%、2028 72%；2027 EBITDA7.4–7.8B机会中点区间排除Cogentrix及Meta PPA增量。',date='2026-08-07',url='https://investor.vistracorp.com/2026-08-07-Vistra-Reports-Second-Quarter-2026-Results')
src('B1-02','GSK日本批准bepirovirsen；≤3000 HBsAg群体19%功能性治愈，非全部HBV人群，批准不等Ionis全销售。')
src('B1-03','Roche sefaxersen三期37周蛋白尿主要终点阳性，105周eGFR仍盲法继续，不能宣称长期肾功能终点已成功。')
src('B1-15','AZ原文CM主要终点失败；不同药物/项目价值不能连带归零。')
src('B1-01','9/4 pelacarsen Lp(a) HORIZON主要终点失败；不预计里程碑；Spinraza分给RPRX比例2028从25%升45%，累计550M后归还。')
# Outside-company root chains, all independently reopened by V1.
src('B1-04','AWS 2027–28计划额外200万GPU，需求外部根链；计划不等不可取消合同，也不排斥自研。')
src('TF_MEMORY','9/30行业预测Q4DRAM+10–15%、NAND+15–20%；AI与消费分化，LTA上限可能限制ASP涨幅。')
src('S2-02','Affinity专业photo/vector/layout工具免费；竞争存在，不证明Adobe必然无法收费。')
src('S2-08','BridgeBio Q2 Attruby222.4M，初治增长；ALNY一线竞争根链，不能跨试验判优。')
src('S2-06','POOL Q2销售1.822938B vs1.784530B、库存+4%；不能以宏观下行解释全部PNR表现。')
src('LUMILENS','客户累计融资>900M，已生产数据中心交付；不证明每个Lumilens模块含POET或所获份额。')
src('B1-06','保诚9/9全面推出阿里云AI核保；客户实际采用，不披露阿里盈利或合同金额。')
src('META_POWER','客户20年PPA、2.1GW现有核电；433MW扩容预计2030年代初，不能计18个月新增出力。',date='2026-01-09',url='https://about.fb.com/news/2026/01/meta-nuclear-energy-projects-power-american-ai-leadership/')
src('TI_Q2','竞争者收入5.46B、环比13%同比23%，工业/数据中心/汽车推动，独立支持嵌入式周期复苏。',date='2026-07-22',url='https://www.ti.com/about-ti/newsroom/news-releases/2026/2026-07-22-ti-reports-second-quarter-2026-financial-results-and-shareholder-returns.html')
src('ALL_Q2','Allstate汽车CR83.3、underlying87.6；新单+8.8%、保单+2.8%，PGR仍受价格/渠道竞争。',date='2026-08-05',url='https://www.sec.gov/Archives/edgar/data/899051/000089905126000117/allcorp63026earningsreleas.htm')
src('S2-23','USDA9/3净现金农收176.4B名义+.4%，实际-2.5%；不能由总农收推每地区大机械预算。')
src('MAIA','10/12微软客户自研推理多GW计划；2027 Maia300 N2P+8HBM4，支持TSM/HBM机制但没锁MU份额。',date='2026-10-12',url='https://blogs.microsoft.com/blog/2026/10/12/microsoft-to-expand-azure-maia-system-to-multi-gigawatt-deployments/')
src('B1-09','8/31 LEAG Boxberg400MW/1.6GWh，HyperStrong与Siemens参与；FLNC客户市场是多供应商。')
src('S2-20','BMS10Q合约记载全球利润亏损平分；与BNTX联合临床稿非两项独立试验，独立核经济权利。')
src('CMI_Q2','竞争者向Circe HPC提供天然气机组，2026–30交付；需求真实且有大竞争者，不能替PSIX背书订单。',date='2026-08-04',url='https://investor.cummins.com/news/detail/701/cummins-reports-strong-second-quarter-2026-results-raises')
src('CSCO_DECK','2/19材料校园订单加速、下一代产品ramp；WiFi7及工业以太网与RUCKUS/BDC竞争，非BDC订单佐证。',date='2026-02-19',url='https://investor.cisco.com/files/doc_presentation/2026/02/Cisco-Investor-Relations-Deck-2-19-26.pdf')

# ticker, source, claim/result, classification, impact, uncertainty, external source IDs, external interpretation
raw='''NVDA|NVDA_Q2|FY27 non-GAAP已含SBC；Q2 CFO24.077B远低于经营利润63.734B，AR占用22.346B；投资证券收益7.771B不能永续。|fact|保留强增长，纠正重复扣SBC；估值须给收入-利润-收现桥。|客户融资及应收何时收回，Maia侵蚀多少推理份额无法真值核定。|B1-04,MAIA|AWS额外GPU部署与微软自研同时成立；不能二选一讲产业。
MU|MU_REMARKS|26SCA与32B客户承诺原文成立；>35%至2030收入并非每年35%；Q1GM86.25%全年低点是公司预测。|fact_and_guidance|允许高毛利延续中枢；不得自动周期腰斩，也不得将指导称实现。|ASP、位元、合同覆盖及客户履约；存款融资不等股东FCF。|TF_MEMORY,MAIA|独立行业仍看涨价格；微软架构用HBM但供应商未知。
ADBE|S2-01|Q3收入6.76B、ARR27.50B和持续收费已实现；调整EPS6.13高于GAAP4.62不可视全部经济利润。|fact|保留价值修复，SBC后利润及创意残差决定倍数空间。|AI积分真实增收与既有席位流失、Semrush并表贡献未完全披露。|S2-02|免费Affinity建立真实替代压力，不能仅拿AI图像新工具作竞争全集。
AVGO|AVGO_Q3|Q3调整OP20.095B剔SBC2.019B后18.076B；Q4 AI21.7B/总34.8B为指引。|fact_and_guidance|支持放量，但应从经济OP起算；不能把信用承诺直接全计当期损失。|系统物料收入、软件前置确认与客户支持义务现金影响待分季。|MAIA,B1-04|客户多架构部署支持定制机会，但微软并未证明使用AVGO或锁定份额。
PNR|PNR_CLOSE|Taco10/1以1.4B已交割，非pending；协同/融资后增利仍预测。|fact_and_inference|交易状态封口，温和复苏可保留；并表收益必须匹配债息。|是否丢份额、各期融资真实利率与协同达产速度。|S2-06|渠道POOL销售与库存改善；不能证明PNR库存或份额一定正常。
CLS|CLS_Q2|GAAP EPS3.17含TRS税前0.90/股；TRS104.1M和SBC19.3M应分离。2027>65%增长为公司展望。|fact_and_guidance|保留强AI制造弹性，GAAP最高/调整最低均不能机械取用。|新客户量产份额、物料过账与资金占用。|SMCI_Q4,CSCO_DECK|制造竞争者毛利恢复、网络平台资本投入支持需求但不保证CLS独占。
ALNY|S2-07|TTR年度指导降至4.2–4.5B，原因二线积压需求正常化；降指引与持续高增长并存。|fact_and_guidance|保留平台价值但不能把积压释放永久外推；版税融资避免双扣。|新启动中一线份额、净价、持续治疗年及版税级差。|S2-08,B1-15|Attruby真实初治增长是竞争；eplontersenCM失败减少另一近端竞争。
SNDK|SNDK_Q4|Q1收入10.3–10.8B、GM83–85%、EPS44–46是明确公司指引。|guidance|保留超景气利润场景，定价/位元拆开；不把指引当全年锁定。|NBM实际最低保障、资本/JV现金、正常税率与价格持续。|TF_MEMORY|企业SSD与消费分化，同业报告支持当前价格上行但不担保2028利润。
IREN|IREN_FY26|4B contracted ARR和1B operating ARR不同；FY26 CFO2.1004B含递延收入增加1.8417B。|fact_and_guidance|仍可有大幅收入跃迁；净现金底或两年全部资本回本不成立。|GPU换代、设施投入、本金及验收，待逐项目股权现金模型。|MAIA,B1-04|云客户确实扩算力且自研同时推进；不保证每家neo-cloud续约价。
PSIX|PSIX_Q2|Q2 GM27.1%环比+420bp，EPS.73；Q2税费5.6M，税释放29.2M属2025同期。|fact|保留真实爬坡，不从已正常税Q2再次扣历史税益；旧高TTM不作基准。|power收入非全DC，客户验收、SAR及关联交易质量仍影响利润。|CMI_Q2|CMI真实HPC机组交付证明需求兼竞争，非PSIX专属订单。
BNTX|S2-17|EUR16.6342B现金证券、251.204M股与H1净亏EUR1.3527B；平台有资金但需要继续烧钱。|fact|允许18月临床去风险，不要求当期盈利；现金须滚动烧钱和汇率。|各资产地域权益、随机读出、资本使用及2028后商业化时点。|S2-20|BMS自方文件独立验证50/50经济分配；不把联合临床稿当独立重复证据。
ARGX|S2-13|ALKIVIA联合组及IMNM显著；DM单独p=.1093；不能把全试验否定或称DM单独成功。|fact|保留适应症扩张乐观价值并限制标签；UNITY失败独立处理。|监管标签与商业转化，单独DM补证是否需要。|S2-16|KYTX小样本gMG持久缓解提供远期竞争，不能据此否定现有FcRn支付。
MOD|S2-28|10/1已拆PT并组合Gentherm；0.44619THRM属旧股分派。|fact|必须用剩余持续业务估值；当前新购不加历史分派。|剩余业务利润、净债以及订单爬坡；未完成V2桥前只能条件名额。|S2-26|CARR DC订单强且集团经济不同；冷却总需求不等MOD净内容/独占。
CARR|S2-26|DC订单同比>300%，有机收入+3%，调整OP同比-6%；不能用订单涨幅当集团利润涨幅。|fact_and_guidance|双恢复路径可信，集团23B基数限制AI弹性。|H2DC验收、住宅渠道售出、欧洲利润改善。|S2-28|MOD拆分后更聚焦形成直接冷却替代；不证明CARR订单流失。
AGCO|S2-21|Q2恒汇率收入-3.7%，关税退款22M，融资业务前置收益20M需辨认。|fact|允许低谷后利润恢复，剔一次性但不抹去欧洲较强盈利。|北美经销商去库存、农民区域现金、PTx付费装机。|S2-23|USDA实际净现金农收-2.5%但高于长期均值，既非崩溃也非全面强复苏。
BABA|S2-34|云48.437B人民币同比45%；新分部合并T-Head，集团资本与应用亏损不能忽略。|fact|保留地域/云重估，必须用扩股后ADS和RMB利润桥。|云外部客户收入、AI应用亏损和电商补贴持续期。|B1-06|保诚已全面上线为客户采用实证，不证明阿里合同净利润。
VST|VST_Q2|最新套保2027 94%、2028 72%；2027 EBITDA7.4–7.8B机会区间排除Cogentrix和Meta增量。|fact_and_guidance|可保留PPA/并购上涨，不能把全电量吃新现货价，也不能漏掉明确排除增量。|截止日并购最终交割/净债桥由V2核，PPAs分季生效。|META_POWER|客户确认长期需求，但433MW新增扩容在2030年代初、窗口外。
KYTX|S2-16|KYSA8一年26人数据9/24已发布：T25FW改善49%、92%免治疗；95%是早期改善者子集持续率。|fact_and_guidance|一年读出不能重复当未来催化；BLA完成/受理/CMC仍可带来事件重估。|小样本单臂、标签批准、制造一致性、融资和付款均未解决。|S2-12|ARGX现有广gMG标签及支付商业规模是真实替代；不能用于否定无获批SPS机会。
PGR|S2-31|8月CR89.3，往年有利发展131M使事故年损失率比日历年高1.8点。|fact|承保盈利真实，建议正常化CR单变量+2/+4点；浮存金非股东净现金。|获客成本、价格下降和保单增长能否持续。|ALL_Q2|Allstate新单+8.8%、强underlying盈利说明竞争恢复，非PGR永久独占。
FLNC|FLNC_RESET|9/16指引收入2.4B、调整EBITDA-200M，2027 CFO中性正为目标。|guidance|旧8月模型作废；只可高风险等待修复席，与IONS/SMCI机会成本比较。|产能修复、赔偿/质保成本、现金与外部融资需求仍未封口。|B1-09|LEAG多供应商扩储能真实；行业增长不证明FLNC执行恢复。
IONS|B1-02|日本bepirovirsen批准及19%特定群体功能性治愈真实；失败CM/pelacarsen不等全部管线失败。|fact|支持重新竞争名额；按产品权益、净价与版税现金重新估值。|自身商业化付费治疗年、Roche长期eGFR、债务/版税安排。|B1-03,B1-15|GSK/Roche/AZ为不同合作项目根链；Roche37周阳性不能当105周肾功能成功。
SMCI|SMCI_10K|BDO8/31财报无保留；三旧内控弱点修复，ITGC一项仍未修复；FY26 CFO-6.8099B。|fact|旧无审计/全未修复淘汰理由撤销；现金转化仍强反证，只可条件复活。|Q4高毛利能否维持及返利性质、应收库存回款、SEC调查后续。|CLS_Q2|CLS真实增长与经济利润可作直接制造替代，比较资本占用而非收入倍数。
POET|POET_FS|客户协议expected up-to500M及客户权证是有条件安排；客户对价30.142M以后摊销。|fact|允许小基数多倍右尾，但不能把客户整单按POET收入或跳过净收入抵减。|采购不可取消性、量产良率、收费净毛利和完全稀释。|LUMILENS,CSCO_DECK|客户融资和交付真实、竞争路线真实；都未证POET具体份额。
BDC|S2-25|订单836M、B/B1.11和有机收入+8%真实；RUCKUS7/1季后并表。|fact|允许并购后去杠杆弹性，不沿用收购前净债配合收购后利润。|新增债息、整合成本、有机增长及订单现金兑现。|CSCO_DECK|Cisco校园/WiFi7/工业以太网竞争与需求独立存在，BDC不是唯一渠道。
MCHP|S2-27|库存185→175天、销售环比+13.2%、净债降170M；12个PCIe6定点尚非收入。|fact|周期复苏已在报表，仍可回归并替代农业周期；需每股经济利润优势。|库存为公司指标非完整渠道天数、优先股息/利息和定点投产季度。|TI_Q2|TI工业/汽车同时改善支持周期，未证明MCHP市场份额和独家定点。
CRM|S2-29|Agentforce ARR定义扩至Slackbot/Headless360，收入指导纳入待收购；增长不能简单全部有机AI化。|fact_and_guidance|不因定义扩展抹去收费，但与ADBE同SBC经济口径后再争席。|AI收费是否补席位流失、并购息费和持续SBC。|S2-01,B1-06|ADBE企业工作流和保诚定制AI为不同替代实施路径，均不证明CRM必败。
TSM|TSM_SEPT|9月收入NT511.857B同比54.6%，1–9月+41.1%支持先进制造现实增长。|fact|最强AI候补之一；客户架构迁移可跨供应商受益，非仅NVDA附属。|海外折旧/成本、台海尾部以及先进封装盈利分配。|MAIA,B1-04|微软明确N2P+HBM4、AWS追加GPU需求为客户根链；不能当已验收销售。'''
checks=[]; companies=[]
for i,line in enumerate(raw.splitlines(),1):
    t,k,result,kind,impact,uncertainty,ext,note=line.split('|')
    s=sources[k]
    checks.append(dict(id=f'V1-{i:02}',ticker=t,claim=result,source_url=s['source_url'],published_date=s['published_date'],access_status=s['access_status'],result='核实并限定口径：'+result,fact_or_guidance_or_inference=kind,decisive_impact=impact,remaining_uncertainty=uncertainty))
    companies.append(dict(ticker=t,verified_thesis=result,strongest_counterevidence=uncertainty,independent_external_chain=[dict(source_id=x,source_url=sources[x]['source_url'],published_date=sources[x]['published_date'],access_status=sources[x]['access_status'],interpretation=note) for x in ext.split(',')],selection_implication=impact))
extras=[('IREN','B1-10','验收/最低数量/延期抵扣/终止条款已独立实读；融资+预付覆盖率不可跨合同相加。','有合同不等无条件现金，最低付款机制仍强于普通意向。'),('SMCI','SMCI_Q4','Q4财报新闻稿GM17.5%、调整17.6%；当时未审计；最终10K财报已审计，不沿用新闻稿未审计状态。','Q4改善成立但本轮未完整拆单季返利，17.6%不直接四倍。'),('ARGX','B1-16','10/8 UNITY因无效停止，与8/17 ALKIVIA为不同适应症。','删除Sjögren近期收入但保留已付费gMG/CIDP。'),('IONS','B1-03','37周蛋白尿终点阳性；105周eGFR未读出。','近期申报机会可保留，不赋已确证长期肾功能价值。'),('PSIX','PSIX_Q2','B1所称38.3M税益须先定位TTM/FY25；已核2026Q2税费5.6M与2025Q2税益29.2M。','禁止重复扣历史一次性；保持Q2已正常税盈利。'),('MU','MU_REMARKS','12.3B Q4存款在融资现金流、12.7B期末存款满足购买条件后归还；非收入/FCF。','不是虚假经营现金，但净现金归属须还原可返还义务。')]
for t,k,r,imp in extras:
    s=sources[k]; checks.append(dict(id=f'V1-{len(checks)+1:02}',ticker=t,claim=r,source_url=s['source_url'],published_date=s['published_date'],access_status=s['access_status'],result=r,fact_or_guidance_or_inference='fact_and_inference',decisive_impact=imp,remaining_uncertainty='详见该公司主核验与V2经济利润/证券计算。'))
for k,r in [('B1-01','pelacarsen：Lp(a) HORIZON主要终点失败；Royalty Pharma不预计支付里程碑，2028 Spinraza分成45%、累计550M后归还。'),('B1-15','eplontersen：CARDIO-TTRansform ATTR-CM主要复合终点失败；单药预设亚组仅名义显著；既有hATTR-PN适应症不能随之归零。')]:
    s=sources[k]; checks.append(dict(id=f'V1-{len(checks)+1:02}',ticker='IONS',claim=r,source_url=s['source_url'],published_date=s['published_date'],access_status=s['access_status'],result=r,fact_or_guidance_or_inference='fact',decisive_impact='分别移除失败资产现金，不混为一个试验；GSK和Roche成功独立保留。',remaining_uncertainty='剩余产品付费患者、净价、商业费用与版权现金桥。'))
for c in companies:
    if c['ticker']=='IONS':
        c['verified_thesis']='日本bepirovirsen已批准；另两失败必须分别处理：pelacarsen的Lp(a) HORIZON与eplontersen的CARDIO-TTRansform ATTR-CM，均不等于全平台失败。'
        s=sources['B1-01']; c['independent_external_chain'].append(dict(source_id='B1-01',source_url=s['source_url'],published_date=s['published_date'],access_status=s['access_status'],interpretation='Royalty Pharma合同对手方明确失败后的Spinraza分成及里程碑变化。'))
for ch in checks:
    if ch['ticker']=='VST': ch['fact_or_guidance_or_inference']='fact_and_management_opportunity_not_formal_guidance'
unresolved=['以上原始实读验证的是决定性已披露事实和管理层目标的归类，不是对2028盈利预测作真值认证。','PNR融资最终条款、MOD剩余利润、VST截止日并购状态及净债由V2完成，尚不能称完成证券桥。','SMCI单季17.6%毛利来源及FY26巨额负CFO后的回款，FLNC制造恢复与资金需求仍会改变席位。','KYTX单臂小样本、BLA/CMC及融资；ARGX DM独立显著性；IONS各项目权益及付费人数均留条件。','每家公司外部根链有不同针对性：有些是直接客户，有些是竞争者；不是独立重复证实其全部投资论点。','IONS自方CARDIO-TTRansform网页本轮失败，改读AZ合作方原始稿；PNRHTML失败改读官方PDF，不冒充原链接成功。']
out=dict(role='V1_primary_verification',cutoff='2026-10-12 19:40 America/Los_Angeles',observation_date='2028-04-12',covered_tickers=[x['ticker'] for x in companies],checks=checks,companies=companies,unresolved=unresolved,source_count=len(sources),method='B1/B2/S1/S2提问题与发现URL；V1独立重新打开原始页面并find/open相关段落。来源重复版本不算新根事件；含未核预测不自动否决。',reviewed_inputs=['00_control/实验章程.md','00_control/终选裁决准则.md','03_round2/B1_business_rebuttal.md','03_round2/B2_valuation_rebuttal.md','03_round2/Controller_10月12日产业新证据.md'])
(B/'04_verification').mkdir(exist_ok=True)
(B/'04_verification/V1_primary_verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'07_logs/V1_sources.json').write_text(json.dumps(dict(role=out['role'],cutoff=out['cutoff'],sources=list(sources.values()),access_failures=[dict(url=all_sources['S2-04']['url'],result='HTML internal error; official PDF success'),dict(url=all_sources['S2-10']['url'],result='internal error; AZ partner primary used')]),ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# V1 原始事实与催化独立核验','',f'覆盖27家公司、{len(checks)}项主张及{len(sources)}个独立实读URL。截止2026-10-12 19:40 LA；共同观察日2028-04-12。URL数量不是独立根事件数量。','', '最重要新增纠错：SMCI最终财报已获BDO无保留审计，三项弱点修复、一项ITGC未修复；其FY26 CFO仍-6.8099B。PSIX2026Q2已正常计税，不能再扣2025税益。VST最新2027/2028套保为94%/72%，旧比例作废。','', '## 每家公司封口与保留异议','']
for c,ch in zip(companies,checks):
    lines += [f"### {c['ticker']}",'',f"**原始实读结论**：{c['verified_thesis']} [{ch['published_date']}原始来源]({ch['source_url']})",f"**对终选影响**：{c['selection_implication']}",f"**最强反证/待核**：{c['strongest_counterevidence']}",'**公司之外根链**：'+ '；'.join(f"[{x['source_id']} / {x['published_date']}]({x['source_url']})" for x in c['independent_external_chain'])+'。'+c['independent_external_chain'][0]['interpretation'],'']
lines += ['## 关键附加核验','']
for ch in checks[27:]: lines += [f"- {ch['id']} {ch['ticker']}：{ch['result']} {ch['decisive_impact']} [原文]({ch['source_url']})"]
lines += ['','## 尚未解决','']+['- '+x for x in unresolved]
(B/'04_verification/V1_primary_verification.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(B/'07_logs/V1_stage_notes.md').write_text('# V1阶段笔记\n\n1. 已读根AGENTS与实验章程/裁决准则；仅读上游，只写实验。\n2. 第一批独立封口KYTX/ARGX临床分母、NVDA SBC、CLS TRS、FLNC9月重置，已报root。\n3. 第二批发现PSIX跨期税益不应双扣、PGR准备金1.8点、SMCI旧淘汰理由部分失效、VST最新套保，已报root。\n4. 读完B1全表与B2覆盖27家的具体争议；外部根链均重新打开，不继承为实读。\n5. 核验结果不压成最保守预测：MU全年GM地板仍属公司指导但保留结构性中枢，SMCI/IONS允许回归。\n6. 完成JSON/Markdown及来源日志；无Git、外部写入或子代理。\n',encoding='utf-8')
assert len(companies)==27 and len({x['ticker'] for x in companies})==27
assert all(c['independent_external_chain'] for c in companies)
print(json.dumps({'companies':len(companies),'checks':len(checks),'sources':len(sources),'files':['04_verification/V1_primary_verification.md','04_verification/V1_primary_verification.json','07_logs/V1_sources.json']},ensure_ascii=False))
