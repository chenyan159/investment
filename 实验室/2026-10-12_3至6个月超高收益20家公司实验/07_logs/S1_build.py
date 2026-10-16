import json, pathlib, datetime, hashlib
R=pathlib.Path(__file__).resolve().parents[1]
base=json.loads((R/'02_round1/X2_ai.json').read_text(encoding='utf-8-sig'))
universe={x['ticker']:x for x in json.loads((R/'01_inputs/universe.json').read_text(encoding='utf-8-sig'))}
old={x['ticker']:x for x in base['nominations']}
sources=[]
def src(i,t,date,url,note,status='opened_relevant_body',kind='primary'):
    sources.append(dict(id=i,tickers=t.split(','),event_date=date,url=url,access_status=status,source_type=kind,access_date_utc='2026-10-13',note=note))
src('P01','MU','2026-09-30','https://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Fiscal-Fourth-Quarter-and-Full-Year-2026-Results/default.aspx','财报、资产负债表及现金流指定段；非10-K全文。现金及投资73.453B、债5.179B、长期客户负债12.895B。')
src('P02','SNDK','2026-08-05','https://www.sec.gov/Archives/edgar/data/2023554/000162828026053346/sndkq4-26ex991xpressrelease.htm','Q4业绩/指引、资产负债表、现金流；Q4 CFO7.126B中refund1.360、contract0.731、应付税0.730B的贡献。')
src('P03','IREN','2026-06-01','https://iren.gcs-web.com/news-releases/news-release-details/iren-closes-365bn-investment-grade-gpu-financing','正文及脚注：6%债息；3.31%把1.94B预付当0%资金，均不含费用。')
src('P04','AAOI','2026-10-05','https://investors.ao-inc.com/news-releases/news-release-details/applied-optoelectronics-announces-completion-previously','ATM完成：5,694,845股，净587,999,985.89美元。')
src('P05','CRDO','2026-09-01','https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-First-Quarter-of-Fiscal-Year-2027-Financial-Results/default.aspx','业绩、指引、GAAP桥；Q2 525–535M，GAAP经营利润120.7M/479M，调整EPS不能直接等于经济NOPAT。')
src('P06','SMCI','2026-08-11','https://ir.supermicro.com/news/news-details/2026/Supermicro-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Financial-Results/default.aspx','初步公告正文财表，Q4 CFO0.747B/全年-6.810B，FY27收入65–72B。公告明确未经审计，最终10-K优先。')
src('P07','CRWV','2026-08-12','https://www.sec.gov/Archives/edgar/data/1769628/000176962826000366/crwv-20260630.htm','打开10-Q并定向读折旧/技术基础设施费用，Q2 PP&E D&A1.4B；未读3399行全文。')
src('P08','POET','2026-08-13','https://www.poet-technologies.com/news/poet-technologies-reports-second-quarter-2026-results-revenue-up-112-year-over-year-in-sixth-consecutive-quarter-of-sequential-growth','Q2收入0.570M、现金短投796.3M；同比高增长基数极小。')
src('P09','CLS','2026-07-27','https://celestica.gcs-web.com/news-releases/news-release-details/celestica-announces-second-quarter-2026-financial-results','直接打开业绩首段，收入4.70B同比62%；财务细节另继承冻结公司。')
src('P10','MOD','2026-10-01','https://investors.modine.com/news/news-details/2026/Modine-Completes-Spin-off-and-Combination-of-its-Performance-Technologies-Business-with-Gentherm/default.aspx','分拆完成、现金约156M用于还债；10/12新购不能享旧分派。')
src('P11','UCTT','2026-08-03','https://www.sec.gov/Archives/edgar/data/1275014/000162828026051853/q22026pressrelease.htm','Q2收入644.9M、GAAP经营率4.6%；Q3收入700–750M、调整EPS0.83–1.03。')
src('P12','COHR','2026-03-02','https://nvidianews.nvidia.com/news/nvidia-and-coherent-announce-strategic-partnership-to-develop-optics-technology-to-scale-next-generation-data-center-architecture','客户联合公告：非独家多年采购承诺另2B股权投资；与供应商同一联合事件不算两项独立订单。')
src('P13','APLD','2026-10-07','https://ir.applieddigital.com/news-events/press-releases/detail/163/applied-digital-reports-fiscal-first-quarter-2027-results','Q1业绩、10/1 250MW Ready for Service、权益与现金段；不是CRWV终端客户GPU验收。')
src('P14','NBIS','2026-08-12','https://www.sec.gov/Archives/edgar/data/1513845/000110465926094844/nbis-20260812xex99d2.htm','半年财表指定段：非受限现金8.0421B、受限1.056B；股权重估收益非云现金。未读全文。')
src('P15','NVDA','2026-08-26','https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027','Q2收入96.221B、Q3指引108B±2%；Rubin生产部署，公司披露不等于终端资本回报。')
src('P16','AVGO','2026-09-02','https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial','Q3收入29.591B、FCF13.665B；Q4收入34.8B为指引。')
src('P17','TTMI','2026-09-30','https://investors.ttm.com/sec-filings/all-sec-filings/content/0001193125-26-409136/d147406dex991.htm','Epiq完成1.1B现金并购，300M TLA+800M TLB和6.75%票据融资。')
src('P18','AEIS','2026-08-03','https://ir.advancedenergy.com/media/document/811571e0-756f-4f18-ab22-e3dea8229615/assets/AEIS_2026_Q2_2026_Earnings_Press_Release.pdf','PDF首页与资产负债表；Q2收入574M、现金1,396.5M、账面债1,264.2M。未做全PDF视觉复核。')
src('P19','MU,SNDK','2026-09-30','https://www.trendforce.com/presscenter/news/20260930-13258.html','独立行业预测：Q4 DRAM+10–15%、NAND+15–20%；消费弱/涨幅放缓亦在正文。',kind='industry_primary')
src('P20','MU,CRDO,AAOI,NVDA,AVGO,MOD','2026-10-12','https://blogs.microsoft.com/blog/2026/10/12/microsoft-to-expand-azure-maia-system-to-multi-gigawatt-deployments/','2027部署、8堆HBM4、167kW；支持需求同时展示降低每任务内存消耗，没有名单供应商分单证据。精确发布时间未核。')
src('P21','IREN','2026-08-27','https://iren.gcs-web.com/news-releases/news-release-details/iren-reports-fy26-results','Horizon1交付、H2–4 Q4目标；1B operating ARR/4B contracted ARR，脚注要求随后测试验收，不能当FY收入。')
src('P22','IREN','2026-05-07','https://nvidianews.nvidia.com/news/nvidia-and-iren-announce-strategic-partnership-to-accelerate-deployment-of-up-to-5-gigawatts-of-ai-infrastructure','30M股五年购买权@$70，最大2.1B，非现有现金/强制认购。')
src('P23','POET','2026-08-06','https://lumilens.com/news-insights/lumilens-emerges-with-900m-in-funding','客户披露累计900M+融资及首款产品已商业交付，未确认该产品含POET。')
src('P24','SNDK','2026-09-29','https://www.sandisk.com/company/newsroom/press-releases/2026/2026-09-29-sandisk-to-report-first-quarter-fiscal-year-2027-results-on-october-29-2026','成功打开官方财报日公告，确认10/29。')
src('P25','SMCI','2026-08-31','https://www.sec.gov/Archives/edgar/data/1375365/000137536526000022/smci-20260630.htm','成功打开10-K，长正文未全读；具体采购/最终稀释条款仍送V1。','opened_index_and_partial_body')
src('P26','COHR','2026-08-12','https://www.coherent.com/content/dam/coherent/site/en/documents/investors/financial-releases/2026/august-12/earnings-release-fy26-q4.pdf','PDF首页：Q4收入2.05B、GAAP GM38.5%、EPS1.19；非全15页阅读。')
src('P27','COHR','2026-09-21','https://www.coherent.com/news/press-releases/launches-photonlink-integrated-optics-platform-ai-infrastructure','成功打开产品发布；本轮未完整提取所有时间，Q4收入目标继承冻结公司段。','opened_partial_body')
src('P28','AAOI','2026-08-06','https://www.sec.gov/Archives/edgar/data/1158114/000168316826006055/aaoi_ex9901.htm','Q3 255–290M、非GAAP GM29–30.5%、92.8M指引股数；公告年底高速产能650k/月，媒体930k口径须对比电话会。')
src('P29','AAOI',None,'https://newsroom.ao-inc.com/news-releases/aoi-receives-first-volume-order-of-1-6t-data-center-transceivers-from-major-hyperscale-customer/','原始订单页面已打开；正文日期/金额将在V1追核，本轮不据此增加新订单。','opened_partial_body')
src('P30','CLS','2026-10-06','https://corporate.celestica.com/news-releases/news-release-details/celestica-hold-q3-2026-financial-results-and-2026-investor-and','财报及投资者日正式公告已打开，10/27会议为官方日历。')
src('P31','CLS','2026-10-12','https://corporate.celestica.com/news-releases/news-release-details/celestica-introduces-ds6005-data-center-switch-co-packaged','DS6005 CPO发布原始页面打开；没有新增量产收入金额，不能把演示增加到FY27模型。','opened_partial_body')
src('P32','IREN','2026-02-05','https://www.sec.gov/Archives/edgar/data/1878848/000187884826000015/exhibit103-partnerstatem.htm','合同2025-11-02生效；本轮查退款段：一般不退款但明确例外，未逐项重新阅读优先顺位。')
src('E01','MU,SNDK','2026-07-13','https://www.axios.com/2026/07/13/stocks-memory-earnings-ai','Bernstein Mark Newman认为低倍数定价盈利将崩塌；Gil Luria认为AI改变商业。报道不是独立订单证明；百字限额只作简述。','opened_relevant_body','external_view')
src('E02','MU,SNDK','2026-10-08','https://www.tipranks.com/news/why-memory-stocks-micron-sandisk-and-sk-hynix-are-moving-lower-today-october-8-and-what-wall-street-sees-next?mod=mw_quote_news','搜索署名Ben Yoffe但打开为Auto-Generated，署名冲突。Citi Atif Malik SNDK2100，MU共识1630.19为12个月；现货小跌与HDD扩产不直接等于NAND崩塌。','opened_relevant_body','external_view')
src('E03','IREN','2026-10-08','https://www.tipranks.com/news/why-is-iren-stock-sinking-today-october-8','Solomon Oladipupo：BTIG Gregory Lewis Buy电力/续约多头；Jones Kevin Dede Hold客户信用反方。研报未取得。','opened_relevant_body','external_view')
src('E04','IREN','2026-10-07','https://www.tipranks.com/news/iren-stock-plunges-as-semianalysis-flags-data-center-problems','Solomon Oladipupo引SemiAnalysis加拿大GPU故障，也载Texas设施较好；不是已核实SLA违约。','opened_relevant_body','external_view')
src('E05','IREN','2026-10-07','https://www.ai-primer.com/engineer/stories/iren-canadian-gpu-reliability','打开二手正文与原X链接入口；原X三帖点击均Internal Error。未获得原作者持仓/做空利益披露，不能自称已读空头原文。','opened_relevant_body_original_x_failed','external_view')
src('E06','CRWV','2026-10-05','https://www.tipranks.com/news/can-coreweave-stock-rally-180-crwv-gets-wall-street-high-250-price-target','Solomon Oladipupo引John McPeake10/1 Buy250：旧A100三年合同/涨价/企业软件是多头机制；研报全文与明确目标期限未取得，不当6月目标。','opened_relevant_body','external_view')
src('E07','CRWV','2026-10-12','https://www.zacks.com/stock/news/3004943/crwv-shares-slide-25-in-6-months-time-to-buy-hold-or-cut-losses','Shreya Majumder：资本开支35–39B、亏损融资压力；搜索可见摘要，打开反爬。精确发布时间未核，不断言收盘前。','search_excerpt_open_blocked','external_view')
src('E08','AAOI','2026-10-09','https://247wallst.com/investing/2026/10/09/applied-optoelectronics-has-fallen-hard-for-6-months-this-wall-street-analyst-expects-its-going-to-double-soon/','Alex Sirois转述Rosenblatt Mike Genovese220，12月目标不是6月；800G/1.6T/40%GM为路径，媒体产能口径930k须核。','opened_relevant_body','external_view')
src('E09','SMCI','2026-08-12','https://www.benzinga.com/analyst-stock-ratings/price-target/26/08/61150761/super-micros-guidance-signals-a-sharp-acceleration-easing-fears-its-losing-ground-to-rivals','Priya Nigam：Rosenblatt Sajal Dogra51 Buy、Needham Quinn Bolton46 Buy；Wedbush Matt Bryson40 Neutral，强调Q4组合毛利不可外推。未读券商全文，目标期限不明。','opened_relevant_body','external_view')
src('E10','CRDO','2026-09-02','https://www.benzinga.com/analyst-stock-ratings/price-target/26/09/61572886/these-analysts-revise-their-forecasts-on-credo-technology-group-following-q1-results','Avi Kapoor：Vivek Arya Buy275由340降、Mike Genovese Neutral235由215升；没有共同支持半年400。','opened_relevant_body','external_view')
src('E11','POET','2026-09-22','https://247wallst.com/investing/2026/09/22/one-under-the-radar-stock-with-100-upside-potential/','Vandita Jadeja：12个月18.11是媒体算法目标，50%信心未校准，不继承；有资金/客户多头，也指出产能时间风险。','opened_relevant_body','external_view')
src('E12','CLS','2026-10-06','https://www.fool.ca/2026/10/06/celesticas-revenue-jumped-62-and-i-like-the-stocks-outlook/','Rajiv Nanjapla多头以业绩/扩产为据；搜索摘要可见，打开失败；长期buy非半年2x。','search_excerpt_open_failed','external_view')
src('E13','MOD','2026-10-02','https://finance.yahoo.com/markets/stocks/articles/modine-advances-pure-play-transformation-150159919.html','Oppenheimer纯业务分拆/11月分析师日多头，二手摘要；打开失败，目标日期不可移植。','search_excerpt_open_failed','external_view')
src('E14','UCTT','2026-09-18','https://www.zacks.com/stock/news/2991879/uctt-rides-on-solid-growth-dynamics-should-you-buy-the-stock-now?cid=CS-MKTWTCH-HL-analyst_blog%7Cinvestment_ideas-2991879&mod=mw_quote_news','Supriyo Bose：2027 EPS估计6.59，2026 3.04；行业/盈利上修多头。打开反爬，仅搜索摘要。','search_excerpt_open_blocked','external_view')
src('E15','UCTT','2026-09-16','https://uk.finance.yahoo.com/research/reports/ARGUS_3475_QuantitativeReport_1789516800000','Argus量化目标下调62；仅搜索结果/付费下载入口，未读原因，不伪造空头论据。','search_excerpt_only','external_view')
src('E16','COHR','2026-09-30','https://www.benzinga.com/quote/COHR/price-targets','搜索评级表：Daniel Zhu Outperform350；9/24 Genovese Buy500；8/13 Meta Marshall EW375、Dave Kang Neutral345。各机构原文未取得。','search_excerpt_only','external_view')
src('E17','APLD','2026-10-08','https://finance.yahoo.com/markets/stocks/articles/applied-digital-apld-stock-gets-121122243.html','SimplyWallSt汇总：Needham70下调83，监管融资；打开429，只搜索摘要。','search_excerpt_open_429','external_view')
src('E18','APLD','2026-10-08','https://www.streetinsider.com/Analyst%2BComments/Applied%2BDigital%2B%28APLD%29%2BReiterated%2Bat%2BMarket%2BOutperform%2Bby%2BCitizens%2Bas%2BDevelopment%2BPipeline%2BTurns%2BInto%2BOperational%2BCapacity/27162627.html','Gregory Miller60 Market Outperform，摘要显示21x FY28 EBITDA；原付费全文未读，需权益瀑布。','search_excerpt_only','external_view')
src('E19','NBIS','2026-10-08','https://finance.yahoo.com/quote/NBIS/analyst-insights/','搜索表：Rosenblatt Buy304(10/8)、Rothschild Sell(9/21)、DA Davidson Neutral250(8/18)；未取得各自投资推理全文。','search_excerpt_only','external_view')
src('E20','NVDA','2026-10-05','https://www.zacks.com/stock/news/2999969/nvidia-corporation-nvda-is-attracting-investor-attention-here-is-what-you-should-know?cid=CS-CHARTMILL-FT-fundamental_analysis%7Cmost_searched_stocks-2999969','Zacks Equity Research，搜索只有标题/有限正文，打开反爬；不据此捏造目标或多空，外部观点覆盖不足。','search_excerpt_open_blocked','external_view')
src('E21','AVGO','2026-10-02','https://www.zacks.com/stock/news/2999575/why-is-broadcom-inc-avgo-down-38-since-last-earnings-report?art_rec=blog-realtime_blog-up_next-ID01-txt-2999575','Zacks Equity Research：搜索显示FY26 AI收入上修，打开反爬；外部空方独立全文不足。','search_excerpt_open_blocked','external_view')
src('E22','TTMI','2026-09-21','https://trendonify.com/news/ratings/needham-lowers-price-target-on-ttm-technologies-to-175-from-220-maintains-buy-rating-256070','James Ricchiuti Buy175由220降，搜索摘要；原因未取得不编造。','search_excerpt_only','external_view')
src('E23','AEIS','2026-10-08','https://www.zacks.com/stock/news/3003142/advanced-energy-soars-40-ytd-is-the-stock-worth-buying-now','Nilanshi Mukherjee：forward12m PE25.05高于板块21.39；搜索摘要可見，打开反爬，不直接沿用异期EPS。','search_excerpt_open_blocked','external_view')
src('F01','SNDK','2026-08-05','https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-fourth-quarter-2026-financial-results','IR失败后SEC P02成功。','open_internal_error')
src('F02','AAOI',None,'https://investors.ao-inc.com/news-releases/news-release-details/applied-optoelectronics-reports-second-quarter-2026-financial','失败后SEC P28成功。','open_internal_error')
src('F03','POET',None,'https://www.poet-technologies.com/news/poet-technologies-provides-business-update','尝试业务更新失败，不声称9/30新增已核。','open_internal_error')
src('F04','CLS',None,'https://celestica.gcs-web.com/node/17621/html','初次返回2217行元信息，二次打开/查找失败；不能算内容已充分核验，改用P09/P30。','initial_open_then_failed')
src('F05','CLS','2026-09-08','https://corporate.celestica.com/news-releases/news-release-details/celestica-host-2026-investor-and-analyst-day-october-27-2026','失败；改用10/6官方会议公告。','open_internal_error')

# 每项是本轮新增裁决；原轮情景只作为待核模型输入，不冒充认证。
reviews={
'MU':('保留-A','最强多头不是更高HBM想象，而是Q1指引61.5B收入/37.84 GAAP EPS已经把盈利年化推至高平台；12月和3月重复兑现，周期折价由8向11倍移动即可。','普通DRAM/NAND超额价格仍可提前见顶；Maia既多用HBM又优化每任务内存，不能单向外推。','净金融现金68.274B是真实9/3基础。隔离12.895B客户长期负债后55.379B，再留运营储备；70B作为4/12目标需至少14.621B新增留存现金，需扣两季净CapEx约25B、分红/回购/税及押金返还。合同负债是履约义务，不能不看现金流重复扣两次。','NOPAT68%对应税率15%时EBIT约80%，接近本季80.7%但不可永久；FY26Q4是14周，不能无调整乘4。','V1复核受限现金27M/客户押金分类及FY27H1 CapEx；V2按52周和正常税、成熟价格重算。','E01 E02 P01 P19 P20','SNDK：MU产品分散、现有净现金大；SNDK纯NAND右尾更陡，但NBM重置风险更集中。'),
'SNDK':('保留-A','不是HBF提前大量卖货；NBM最低价合同与企业SSD提价将过去现货周期股变为可见盈利，10/29兑现可推动前瞻倍数重估。','最低价不是免疫取消/重置；Edge仍大，消费缩容、2027供给使极高利润回落。','7/3现金4.762B+权益证券1.777B且无债。严格隔离退款1.5B、合同1.242B、应付税1.544B得2.253B，再留营运储备；此为压力现金口径非认定全部即刻到期。12B需至少9.747B随后净留存。Q4 CFO7.126B扣三项增量2.821B仅4.305B，尚要JV/CapEx及回购。','67%经济NOPAT在15%税下需78.8%EBIT，接近Q4 GAAP78.5%；GAAP EPS含0.804B证券收益，不能拿43.97直接作核心EPS。','V1 NBM退款与交付抵扣逐季桥、JV资金；V2固定/浮动底价、税正常化及证券价值不得双加。','E01 E02 P02 P19 P24','MU：相同风险优先MU；SNDK更近10/29事件与高NAND弹性让它仍值得保留。'),
'IREN':('保留-B条件','Horizon2–4验收把4B合同ARR由建设承诺转为账单；自有设施与已有微软Horizon1使去风险真实，低股权基数允许2x。','加拿大Prince George/Mackenzie被指GPU可靠性差；资本开支远早于回款，短合同高价未必覆盖全设备寿命和设施资本。','480M不是已核股本。每季桥=期初非受限现金+可提款债+实际预付+发股净款+CFO−设施/GPU CapEx−偿本−费用；14B资金包不能全当现金。微软债6%；预付抵账。NVIDIA30M@$70权利非已注资，2x69.60低于行权价。','EV/NOPAT必须先扣经济GPU折耗后税，但NOPAT不再扣利息；净债扣一次。25倍给8.5B收入/23%利润是成功路径，非2027已兑现。','V1 480M与各可转债/权证、提款条件；V2加拿大负载、故障持续/SLA及Texas区分。X原帖失败，未获得做空利益披露。','E03 E04 E05 P03 P21 P22 P32','CRWV：自有园区、低股权起点有更大倍数；CRWV软件/运营栈更成熟，若加拿大问题普遍化则切换。'),
'AAOI':('保留-B条件','800G真实规模起步，1.6T批量订单及融资完成让2027两三个季度经营杠杆可能极大；合理乐观分支不应仅因尚亏损删除。','从29–30.5%毛利跳到40%并非自然结果，客户压价、存储材料短缺及自建良率使收入增长未必到股东。','8/6指引92.8M是期间稀释口径，不能直接+5.694845M当10/12法定股数；本批净588M/新股同时计一次。102M未来经济股数需期初实际+ATM+SBC+可转工具−回购桥。','22%NOPAT可拆成40%GM−12.5%费用=27.5%EBIT，按20%税=22%；需同时兑现，不是只凭营收3.0B。媒体930k/月与官方650k/月口径有冲突。','V1当前基本/稀释股、三次ATM时间及库存应付；V2 650k/930k/月与40%GM路径、1.6T验收收入。','E08 P04 P28 P29 P20','COHR：触及2x小基数AAOI更强；期末站稳/下行资金质量COHR更好。'),
'SMCI':('保留-B条件','官方FY27收入65–72B已超过X2翻倍门槛收入63.1B；重点不是额外订单而是7.5%NOPAT/现金修复及估值15倍能否同时成立。','Q4 17.5%GM因企业组合，后季AI重回80%会稀释；出口审查与库存应收能令低PE成为陷阱。','6月债8.7B−现金7.5B≈1.2B，而X2净债7B是未来烧钱压力，不能称现有。800M股含强制可转优先/价内债必须反解转换阈值，转换后相应债务剔除。','7.5%NOPAT按20%税需9.375%EBIT；若GM10.6%，仅留1.225%销售给全部费用，偏激进；GM12.5%时3.125%费用才相容。','V1最终10-K优先于初步公告、优先股股息/if-converted；V2 FY27毛利组合与两季现金回收。','E09 P06 P25','CLS：SMCI起点更便宜/回款可催化倍数，CLS执行/治理更好；若现金无修复则宁可CLS。'),
'CRDO':('降级-B','AEC已有真利润，光DSP/PIC/模块三线商业化及1.6T下半年是近端新增利润池，不靠Maia供应商猜测。','GAAP经营率25.2%而X2成功经济NOPAT42%差距巨大；收购摊销有时可调整，但员工报酬/客户集中与模块低毛利不能全去掉。','194.378M GAAP稀释均股到210M未来代理允许约15.6M空间但不是封闭桥；现金764.3M到600M要扣Dust收购后开支与库存。','正常税15%下42%NOPAT需49.4%EBIT，接近非GAAP经营能力但未补SBC；更可审查的成功反解用35%×46倍，需收入约5.20B才2x；原4.6B/42%/45倍列强尾而非中枢。','V1 Dust现金/或有股、SBC/税；V2模块整机收入与内部DSP/PIC不得重复计。','E10 P05 P20','ALAB：CRDO AEC盈利与相对倍数较好；不能因此免除经济利润口径。'),
'CRWV':('保留-B条件','已交付大规模云加软件/企业客户、旧A100仍获三年合同和短约涨价可反驳GPU一更新即归零；2027指引和250MW新增设施能压风险折价。','同一设备收入、预付和融资可造成现金繁荣错觉；Q2折旧1.4B是真实资本消耗起点，ARR增长不等于股东FCF。','700M或850M股都需映射新债转换/并购SBC。净债45B是远期代理；2026 35–39B CapEx及滚动提款要逐季做，不把未来募集款当已有。','X2需31.47B收入/20%NOPAT/25倍/45B债才能2x。若850M股同条件收入需36.29B；旧卡可续约是残值证据，不能说明所有新卡同价六年。','V1贷款摊还、受限现金、可转债本金抵扣；V2旧卡续约净价/折旧敏感性与APLD验收差异。','E06 E07 P07 P13 P15','IREN：CRWV运营/软件更成熟且客户可见，但更高财务杠杆；保留不同成功机制而不机械只选一家。'),
'POET':('降级-候补事件期权','现金约796M和Lumilens买方900M+融资为真，买方已经商业交付首款产品，客户不是空壳愿景；量产资格一过可先于成熟利润重估。','没有证明Lumilens现行商业品含POET；500M五年潜力非确定订单，媒体18.11是12月算法目标，延期与客户激励很重。','300M股/650M现金只是压力代理；22.921408M客户权证同时影响净收入及稀释，不是双算同一成本：须区分既发权证价值与未来新激励，估值不可双罚。','2x需约3.196B EV，20x净销售需160M；这远高于H1 1.073M，需2027/28订单充分去风险。短期触及可能，6月末站稳低证据。','V1现有全部权证价内性/客户对价摊销；V2 9/30更新与2027资格/批量时间，净产品收入。','E11 P08 P23','AAOI：POET更大技术可选性/现金久期，AAOI实际销量更能支撑半年2x，故POET仅候补。'),
'CLS':('保留-B','10/27投资者日能给2027平台增长量化指引；1.6T与计算项目跨量产门槛，DS6005让平台工程价值增加，经营杠杆是真机制。','HPS属CCS不能另加；客户芯片转售放大收入，CPO提高技术含量不保证CLS份额，现金结算激励拖累股东现金。','8月股权融资34.5亿美元即3.45B，11.129031M新股；130M未来代理需含这批一次。净现金1B是部署后状态，融资收益不能既加现金又不加股。','8%税后NOPAT约需10%税前EBIT(20%税)，高于当前8.2%调整EBIAT且还含SBC调整；2x39.89B收入路径要更高利润率或更远FY28提前定价。','V1股数、TRS/现金SBC只扣一次；V2 10/27日历及2027收入/净材料权益。','E12 P09 P30 P31','SMCI：更好现金治理，估值起点较高；若SMCI现金未修复，CLS优先。'),
'MOD':('保留-B','分拆已完成使纯冷却业务更易估值；数据中心90%增速、产能/零件改善将14.8%EBITDA率恢复，是近期可观察的利润变化。','45℃温水架构减少机械冷水机内容，CDU替代收入不能全部叠加；此前FCF依赖165M预付。','新买不含THRM历史0.44619股及其特殊分红；156M已用于降债。56M股/350M净债要承接存续主体，不混旧集团。','18%NOPAT要求22.5%EBIT(20%税)，已经高于冻结FY28全集团约20.3% EBITDA，故X2成功379并非普通恢复；需份额/产品组合额外上修。','V1分拆后净债、保留成本；V2仅存续业务FY28/29收入4.37B门槛及冷却内容蚕食。','E13 P10 P20','VRT：MOD较低起点/利润恢复弹性更强，VRT现成规模更稳；选择MOD因6月去风险可识别。'),
'UCTT':('保留-B提升研究顺位','Q3指引700–750M比Q2再上台阶，AI/HBM设备复杂子系统需求与费用摊薄可形成盈利持续上修；比尚无收入电源概念更近。','大客户集中/低GM，Q2 GAAP税18.1M占税前30M，少数权益3.2M不能遗漏；正常化EPS不能只取nonGAAP。','47M股/500M净债代理须按库存、贷款、少数权益桥；设备客户CapEx不是本公司不可取消订单。','Zacks摘要2027 EPS6.59若实现，20x=131.8可2x，但先扣常态SBC与确认财年。X2 8%税后利润/21倍对应3.85B收入；当前GAAP OP4.6%到10%需规模改善。','V1少数权益和常态税/SBC；V2客户订单/Products GM与库存周转。','E14 E15 P11','ACMR：UCTT近端指引与美国客户现金链更直接，ACMR自有产品毛利更好但少数/跨境现金复杂。'),
'COHR':('保留-B','已交付光业务加NVIDIA真实多年采购、PhotonLink平台爬坡，既不是只有概念也不只卖单颗激光器；未来两季可提高FY28收入可信度。','多路线共存和NVIDIA同时扶持LITE反驳独家；高库存/CapEx令FY26 FCF约-1.02B，营收冲高仍可能新增债。','6月非受限现金+投资1.987B减账债3.2222B≈净债1.2352B；SiC受限606M别并入可用；2B前瞻净债是扩产条件。','25%NOPAT按20%税需31.25%EBIT，相较40%GM只留8.75%费用，远高于现有GAAP利润率；X2 15.87B收入为强成功而非普通量产。','V1各优先/少数权益及投资新股；V2产能增量与良率、PhotonLink CYQ4到底量产还是少量收入。','E16 P12 P26 P27','AAOI/LITE：相近右尾下COHR技术组合与融资缓冲较好，AAOI更有小基数2x弹性；无单一总胜者。'),
'APLD':('候补-保留复活','250MW实交付、300MW年底目标及CHRN约96%权益的GPU云提供被租赁单线模型遗漏的可选性；若项目融资去风险可翻倍。','普通股在项目债和Macquarie优先之后；累计租约/项目NOI不是母公司收入或可分配现金。','8/31实际297.067M股；现金多在TopCo2，不能算母公司安全垫；12.75%优先资本/13.5%项目权益先建瀑布。公司正文2.0109B可赎回NCI证实资本层级。','P46.50×350M=16.275B普通股权益；若12B项目净债/优先合计，28.275B资产价值在20x NOI需1.414B NOI（仅诊断，合并少数/CHRN另拆）。这比当季58.8M NOI年化高6倍。','V1项目本金摊还/PIK/最低回报与合并消除；V2 CHRN融资落实及服务起始，2027Q3 ARR不能计4月已赚。','E17 E18 P13','IREN：APLD不承担所有GPU更新风险但高优先资本压普通股；瀑布闭合前IREN路径更可审查。'),
'NBIS':('候补','软件能力/大客户承诺和2027大增长真实；许可与融资去风险可触发前瞻估值，不因负FCF机械剔除。','210.06股价已资本化大量成功；可用现金8.04B仍需大CapEx，Vineland合规和第三方承接不能与专用合同重复。','380M/12B净债模型不是现有；6月底8.042B非受限现金与1.056B受限分开，EigenAI报酬/可转债按目标价转换。','2x420.12、380M股、12B债、20%NOPAT/30倍需28.608B收入；冻结2027强路径17.9B仍不足，须提前资本化2028且融资闭合。','V1逐季资金与若转换则债减少；V2 NJ许可、客户最低付款/预付抵扣和2028交付证据。','E19 P14 P15','CRWV/IREN：NBIS质量有吸引力但起点更高，半年2x需跨更远盈利年，不优先。'),
'NVDA':('候补-优质缓冲','已实现高利润、Rubin进入生产和生态可能让FY28盈利快速上修；不是市值大就不能翻倍。','2x约11T股权必须由数百B利润支撑；Maia/TPU与客户融资高度相关，份额和毛利不能永不下降。','24.3B股/150B净现金前瞻代理，要扣回购分红/投资和或有融资责任；不能把担保全部当债，也不能置零。','X2 61%NOPAT需约73.5%EBIT(17%税)接近甚至超过75%GM留费用，强分支820B收入/61%明显偏激进；若55%NOPAT/25倍需约789B收入，仍是FY28跃迁。','V1现金桥/投资收益与承诺；V2 FY28收入季度爬坡、DSO60天回款；署名外部多空全文覆盖不足。','E20 P15 P20','AVGO：通用生态和现金获取优先，AVGO ASIC分散路线可相互替代；本实验2x先给小中型有事件者。'),
'AVGO':('候补','ASIC与网络客户多代合作叠加软件现金，FY27/FY28更高盈利可被近期正式指引提前定价。','系统内容提高收入却稀释毛利，软件前置许可证和租赁支持让盈利质量/客户信用需重新评估。','5.1B股/40B净债代理，126.8B采购和29B租赁支持不等于马上欠债但影响现金压力；分红/回购也在桥内。','2x需241.95B收入×54%NOPAT×28；54%NOPAT按17%税要求65.1%经济EBIT，与66%调整营业率几乎无SBC余地，尾部利润率需下修或收入进一步上修。','V1经济SBC/摊销、租赁敞口；V2独立客户采购和系统净毛利，外部空方全文不足。','E21 P16 P20','NVDA：ASIC路径分散性有价值，但相同半年上行选NVDA现金与平台；不能以Maia自研默认AVGO供应。'),
'TTMI':('保留-B条件','Q4 M+N400M交付台阶与2027目标重定锚可使成熟PCB业务获得更高复杂度份额估值，国防与AI双现金来源。','Q4达到全年4.4B指引需约1.4B营收/约2美元调整EPS，基数陡且可能确认前置；Epiq EBITDA增厚不等于EPS增厚。','112M股/1.5B净债代理；已完成1.1B现金收购且新增TLA/TLB，不把待收购当免费选项；本息先占现金。','16%NOPAT需20%EBIT(20%税)，高于当前利润率；X2 6.55B收入是2027/28成功。买价隐含Epiq独立EBITDA约54M，而6–7%利息66–77M，先稀释EPS。','V1收购后净债和6.75%债不得重加；V2 M+N4.5B是三年累计非年度、Q4量与良率。','E22 P17','CLS：TTMI小基数与M+N更陡，但CLS平台/现金可见性更强；不因国防标签抵消收购融资。'),
'AEIS':('保留-B条件','当前半导体和数据中心电源已有574M季度收入，泰国合格产能及2027新品放量可先于800V释放利润。','800V显著收入最早2028，不能用它解释未来半年销售；库存和一次性退款会制造毛利/FCF错觉。','本金净现金109.8M，非1.4B；40M股低于当季部分稀释口径，需可转债桥和42–44M压力检验。','22%NOPAT需27.5%EBIT按20%税，制造规模改善才达。若44M股、0净债、4B收入/22%/27x，价格540低于2x561.54；需4.16B收入。','V1本金/账面差、可转债、退款/SBC；V2泰国认证与800V最早商业日期。','E23 P18','NVTS：已有盈利和近期产能更可靠，NVTS极强右尾但时间更远；AEIS在本窗口优先。')
}

records=[]
for t,v in reviews.items():
    rec=dict(ticker=t,reference_price=float(universe[t]['finance']['最新价格']),recommendation=v[0],strongest_bull=v[1],strongest_bear=v[2],funding_bridge=v[3],valuation_constraint=v[4],verification_questions=v[5],source_ids=v[6].split(),alternative=v[7])
    rec['source_urls']=[s['url'] for s in sources if s['id'] in rec['source_ids']]
    rec['frozen_company_path']=universe[t]['sources']['company'][0]
    if t in old:
        b=old[t]
        for k in ['catalyst_window','catalyst_date_status','three_month_case','six_month_case','double_hurdle_formula','disappointment_price','central_price','upside_price','multibagger_price','model']:
            if k in b: rec['inherited_'+k]=b[k]
        rec['model_status']='X2条件算例已逐项审查；未声称资本结构闭合；S1 valuation_constraint优先于旧成功价。'
    else:
        rec['inherited_catalyst_window']='2026Q4/2027Q1交付与季度业绩、融资条款；具体未来日期未确认。'
        rec['model_status']='候补仅反解门槛；尚无通过审查四分支估值，不据门槛列正式优先20。'
    rec['touch_2x']='条件成功分支可以先由订单/交付去风险触及；没有校准概率。'
    rec['hold_2x']='2027-04-12站稳需实际收入毛利现金与融资共同证实，弱于窗口触及；不把FY28利润当届时现金。'
    records.append(rec)

# 针对审查发现的成本或股本漏洞作单变量/少量变量压力反解；不是下修后的预测。
stress={'MU':{'net_debt_B':-55.379},'SNDK':{'net_debt_B':-2.253},'CRDO':{'economic_NOPAT_margin':.35,'EV_NOPAT_multiple':46},'MOD':{'economic_NOPAT_margin':.16},'NVDA':{'economic_NOPAT_margin':.55},'AVGO':{'economic_NOPAT_margin':.48},'AEIS':{'shares_B':.044},'CRWV':{'shares_B':.85},'SMCI':{'economic_NOPAT_margin':.06},'COHR':{'economic_NOPAT_margin':.20},'CLS':{'economic_NOPAT_margin':.065},'TTMI':{'economic_NOPAT_margin':.13},'UCTT':{'economic_NOPAT_margin':.065},'AAOI':{'economic_NOPAT_margin':.18},'IREN':{'economic_NOPAT_margin':.20}}
for rec in records:
    if rec['ticker'] not in stress: continue
    b=next(m for m in rec['inherited_model'] if m['branch']=='success').copy()
    b.update(stress[rec['ticker']])
    b['price']=round((b['revenue_B']*b['economic_NOPAT_margin']*b['EV_NOPAT_multiple']-b['net_debt_B'])/b['shares_B'],2)
    b['required_revenue_for_2x_B']=round((2*rec['reference_price']*b['shares_B']+b['net_debt_B'])/(b['economic_NOPAT_margin']*b['EV_NOPAT_multiple']),3)
    b['economic_NOPAT_B']=round(b['revenue_B']*b['economic_NOPAT_margin'],4)
    b['status']='S1压力反解；假设仍未经过逐季资金桥认证，不是新目标价或概率判断。MU/SNDK现金隔离仅现金价值敏感性；其他为成本/稀释约束检验。'
    rec['S1_constraint_sensitivity']=b
out={'role':'S1_ai_deep','status':'sealed_for_next_round','cutoff':'2026-10-12T20:50:00-07:00','price_date':'2026-10-12','check_dates':['2027-01-12','2027-04-12'],'coverage':18,'companies':records,'limitations':['18家公司各有已打开原始页面；不等于18个全文审计。','外部观点有署名与日期，但NVDA/AVGO及数个候补仅受限摘要，未满足全部多空原文闭合；须V2补足。','没有访问X4/X5或旧实验，不修改首轮；继承X2模型明确标记。','未取得SemiAnalysis原帖/利益披露，未把二手技术指控写成确定事实。','资本桥给已知起点与恒等式/缺口，不伪造未来逐季现金流；所有最终估值须V1。']}
(R/'03_round2').mkdir(exist_ok=True)
(R/'03_round2/S1_ai_deep.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'07_logs/S1_sources.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# S1 AI/计算链逐公司专项审查','', '信息截止2026-10-12 20:50 LA；10/12收盘；检查2027-01-12/04-12。状态：封存交下一轮。', '', '**优先保留MU/SNDK真实盈利持续性重估，IREN/AAOI/SMCI保留有融资和交付条件的强成功分支。CRDO利润口径需要降级；POET转候补。UCTT值得提高研究顺位；不是18家都具同等半年翻倍证据。**', '', '## 统一估值和资金规则','', '经济NOPAT = (GAAP经营利润 + 确有非经济摊销调整 − 额外经济折耗调整 − 尚未计入的正常股权报酬) × 正常税率。GAAP费用已含SBC则不再扣；若把未来SBC作为经济费用，股数仅含已发权益/现有奖励及明确融资，不再把同一未来奖励永久全额重复稀释。历史/已发奖励的股数与未来员工服务成本可同时存在，必须按奖励批次区分。NOPAT是付息前，不再减利息；企业价值减净债一次。换用净利润/PE时不再另减同一债务的利息资本化。GPU折旧不等于零，增长CapEx不等于全额维持CapEx。','', '期末可用现金 = 期初非受限现金 + 实际CFO + 已可提款债/预付/股权净款 − CapEx − 偿本 − 分红回购 − 收购；对应期末股数 = 当前实际股数 + 已发ATM + 归属/价内转换 + 新筹资 − 回购。预付随后抵扣账单必须桥接，不把预付作为永久利润。每家公司下文区分已知起点与尚未闭合的预测。', '', 'MU70B现金与SNDK12B不能机械一律归为虚构：MU已有68.274B金融净现金，SNDK要跨越未来现金积累。隔离履约资金的压力口径不是把所有营运负债再重复从企业价值扣除。', '', '|公司|10/12|2倍门槛|S1裁决|','|---|---:|---:|---|']
for r in records: lines.append(f"|{r['ticker']}|{r['reference_price']:.2f}|{2*r['reference_price']:.2f}|{r['recommendation']}|")
for r in records:
    lines+=['',f"## {r['ticker']} — {r['recommendation']}",'',f"**最强多头：** {r['strongest_bull']}",'',f"**最强反方：** {r['strongest_bear']}",'',f"**资金/股数：** {r['funding_bridge']}",'',f"**反解约束：** {r['valuation_constraint']}",'',f"**事件：** {r.get('inherited_catalyst_window','')} {r.get('inherited_catalyst_date_status','')}",'',f"**窗口与期末：** {r['touch_2x']} {r['hold_2x']}",'',f"**最近替代：** {r['alternative']}",'',f"**交V1/V2：** {r['verification_questions']}"]
    if isinstance(r.get('inherited_model'),list):
        lines+=['','下表保留X2四分支供复算，**未通过S1资本/利润口径认证，不是新的目标价背书**。S1要求和反解约束优先。','','|分支|收入B|经济利润率|EV/NOPAT|净债B|股数B|原条件价|','|---|---:|---:|---:|---:|---:|---:|']
        for m in r['inherited_model']: lines.append(f"|{m['branch']}|{m['revenue_B']}|{m['economic_NOPAT_margin']:.1%}|{m['EV_NOPAT_multiple']}|{m['net_debt_B']}|{m['shares_B']}|{m['price']}|")
    elif r['ticker']=='POET': lines+=['','X2期权分支3/6.8/14/22美元保留为假设；本轮已降为候补，不能从媒体目标强推6月站稳。']
    if 'S1_constraint_sensitivity' in r:
        z=r['S1_constraint_sensitivity']
        lines+=['',f"**S1约束敏感性（不是预测）：** 收入{z['revenue_B']}B、经济NOPAT率{z['economic_NOPAT_margin']:.1%}、倍数{z['EV_NOPAT_multiple']}、净债{z['net_debt_B']}B、股数{z['shares_B']}B，条件价{z['price']}；保持这些利润/资本条件，2x所需收入{z['required_revenue_for_2x_B']}B。目的为暴露原成功分支的成本或融资敏感性，不能把本组输入当成新的事实。"]
    lines+=['','**决定性证据与有日期外部观点：**']
    for s in sources:
        if s['id'] in r['source_ids']: lines.append(f"- [{s['id']} {s['event_date'] or '日期未核'}]({s['url']})：{s['note']} 访问：{s['access_status']}。")
lines+=['','## 本轮新增/改变及缺口','', '1. 新打开MU与SNDK完整公告相关现金表，区分现有净现金与未来积累；净现金偏差对MU2x收入门槛影响很小，核心仍是周期利润与倍数。','2. IREN运营质疑有具体加拿大地点；同一研究者认可Texas冗余，不能扩大成微软合同已经违约。未获得故障起止、规模、赔付金额；原X失败与利益披露缺失不作为否定质疑的证据。','3. AAOI官方650k/月与媒体930k/月需核口径，不取较大数为事实；ATM完成修正已单次纳入。','4. CRDO、MOD、NVDA、AVGO多头成功利润率隐藏了经济成本/税的约束；允许远期高盈利提前定价，但近两季必须显著抬升对这些盈利的可信度。','5. POET买方融资/出货亮点真实；不能断言现行产品包含POET。APLD还有CHRN权益的云分支，未因租赁主线而遗漏，仍需独立融资与权益瀑布。','6. 外部观点不足处明示。只有摘要/付费入口不得称阅读全文，券商12个月目标不能充当4/12目标；媒体算法置信度不用作概率。','', '没有额外项目内公司复活入正式优先池；UCTT相对首轮提高审查顺位。APLD/POET/NBIS条件明确改变时可回流。']
(R/'03_round2/S1_ai_deep.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
notes=['# S1阅读及封存记录','','阅读root AGENTS与实验章程；X2 MD/JSON、控制器多空memo；18家公司冻结公司开头和定向段落。大批输出存在截断，未显示部分不计读完。未读X4/X5或旧实验。','','原始网页逐家公司至少一项实际打开；SEC长文仅所标定位。所有源的事件日期、访问状态见S1_sources.json。访问2026-10-13 UTC，信息集不扩展至截止以后。','','重点未闭合：V1逐季资金/转换/经济SBC桥；V2原始多空全文，特别IREN X原帖、GPU可靠性和NVDA/AVGO有署名观点。','','S1没有将数学可得2x等同于合理中枢。原X2模型保留只便于后续反驳与复算。']
for t in reviews: notes.append(f"- {t}: {universe[t]['sources']['company'][0]}；定向阅读，非全文认证。")
(R/'07_logs/S1_reading_notes.md').write_text('\n'.join(notes)+'\n',encoding='utf-8')
print(json.dumps({'companies':len(records),'sources':len(sources),'files':['03_round2/S1_ai_deep.md','03_round2/S1_ai_deep.json','07_logs/S1_sources.json','07_logs/S1_reading_notes.md']},ensure_ascii=False))
