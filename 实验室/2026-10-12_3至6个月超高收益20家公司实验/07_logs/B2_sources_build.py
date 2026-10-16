import json
from pathlib import Path
R=Path(r'D:\investment\实验室\2026-10-12_3至6个月超高收益20家公司实验')
rows=[]
def s(i,t,date,url,status,note,typ='primary',term=None):
    rows.append(dict(id=i,tickers=t.split(),event_date=date,url=url,access_date_utc='2026-10-13',access_status=status,source_type=typ,note=note,opinion_horizon=term,cutoff_rule='首次公开<=2026-10-12 20:50 LA；动态行情/其他新闻不使用'))
s('B2P01','MU','2026-09-30','https://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Fiscal-Fourth-Quarter-and-Full-Year-2026-Results/default.aspx','opened_relevant_body','读Q4/Q1指引、资产负债表和现金流；现金投资73.453B减债5.179B，客户长期义务12.895B另桥，非10-K全文。')
s('B2P02','KYTX','2026-08-11','https://www.sec.gov/Archives/edgar/data/1994702/000119312526344572/kytx-ex99_1.htm','opened_relevant_body','读现金199.4M、贷款可提款续航2028与Q4 rolling BLA计划；本轮未独立读贷款全部先决条件。')
s('B2P03','VISN','2026-08-06','https://www.sec.gov/Archives/edgar/data/1517228/000119312526336705/visn-ex99_1.htm','opened_relevant_body','读集团/core EBITDA、总部费用及出售业务现金混入注释。35.8M与45.5M差9.7M，不能用core替集团。')
s('B2P04','AMPX','2026-10-05 08:00 ET','https://www.prnewswire.com/news-releases/caminus-signs-contract-manufacturing-agreement-with-amprius-technologies-for-us-pouch-cell-production-302897828.html','opened_relevant_body','已读合作方公告正文：资格构建已开始、volume production计划1Q27；不披露新增收入/数量，不等已认证。find 2027无匹配因原文写1Q27，后find Amprius已取得。')
s('B2P05','FLNC','2026-09-16','https://www.sec.gov/Archives/edgar/data/1868941/000110465926108270/tm2625477d1_ex99-1.htm','opened_relevant_body','读修订指引/目标段：FY26收入2.4B与EBITDA-200M；FY27无额外资本/CFO中性至正只是目标。')
s('B2P06','ALNY','2026-08-06','https://investors.alnylam.com/press-release?id=ddc78e15-7847-4066-8fdb-3562023a60f4','opened_relevant_body','读10/23HTT02及10/26官方日历、Q2收入/GAAP净利164.494M；人体机制不是功能疗效。日期为Q2公告，正文date字段尚未单独摘录。')
s('B2P07','ADBE','2026-09-10','https://www.sec.gov/Archives/edgar/data/796343/000079634326000147/adbeex991q326.htm','opened_relevant_body','读业绩/指引和GAAP调节：FY26EPS18.12–18.17 vs24.45–24.50，SBC调整5.42/股。必须留经济成本。')
s('B2P08','PNR','2026-10-01','https://investors.pentair.com/news-releases/news-release-details/pentair-completes-acquisition-taco-group-holdings','search_excerpt_open_failed','搜索返回官方完成收购正文摘要，直接打开Internal Error；不冒称本轮全文。1.4B交易完成已知。')
s('B2P09','PNR','2026-07-28','https://investors.pentair.com/static-files/c02242e3-5891-418c-81e9-62a4da417ea3','opened_pdf_extracted_relevant','PDF打开29页文本，搜索交易页提取Taco2027调整EPS增厚0.10–0.15、现金债融资；未视觉通读。之后find失败。')
s('B2P10','PLAB','2026-08-26','https://photronicsinc.gcs-web.com/node/19681','opened_relevant_body','读Q3损益与现金相关表：净利润43.883M中少数14.967M，归母28.916M；不是将合并利润全部归母。')
s('B2P11','PLAB','2026-08-26','https://stockanalysis.com/stocks/plab/transcripts/681790-q3-2026/','search_excerpt_only','管理层逐字稿搜索摘录：673M现金短投含504M持股50.01%JV；Allen末季初始收入目标。非完整逐字稿阅读。','management_transcript')
s('B2P12','ICHR','2026-08-04','https://www.sec.gov/Archives/edgar/data/1652535/000165253526000069/ichr-20260626.htm','opened_relevant_body','读损益/净利息及MD&A：Q2净利息1.453M、税前5.410M、税4.412M；20%正常税只是未来假设。并读冻结公司前部和资金/前景定向段。')
s('B2P13','SMCI','2026-08-11','https://ir.supermicro.com/news/news-details/2026/Supermicro-Announces-Fourth-Quarter-and-Full-Fiscal-Year-2026-Financial-Results/default.aspx','opened_relevant_body','读FY27Q1:GAAP745M股、nonGAAP761M股、税20.1/20.5%；FY27收入65–72B。基本650M不能作稀释。')
s('B2P14','CRDO','2026-09-01','https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Technology-Group-Holding-Ltd-Reports-First-Quarter-of-Fiscal-Year-2027-Financial-Results/default.aspx','opened_relevant_body','读利润调节：GAAP经营率25.2%、nonGAAP48.2%，SBC87.979M；42%税后率不是现有经济利润。日期继承S1，未单独重查页首日时。')
s('B2P15','ACMR','2026-09-30 07:00 ET','https://www.globenewswire.com/news-release/2026/09/30/3371760/0/en/index.html','opened_relevant_body','读9/29backlog17.1B人民币/2.5B美元同比88.2%；含已发未按中国GAAP确认。10/28美国盘前初报官方确定，不等已确认订单全转收入。')
s('B2F01','KYTX',None,'https://ir.kyvernatx.com/news-releases/news-release-details/kyverna-therapeutics-announces-initiation-rolling-sps-bla','open_failed','Internal Error，改从SEC Q2公告核验；不据失败猜内容。','failed_access')
s('B2F02','PNR','2026-07-28','https://investors.pentair.com/node/27096/pdf','opened_metadata_then_403','初开返回401文本行/7页，但本轮未取得相关EPS正文；后find失败、open403。经营细节回查本地冻结报告，明确继承。','failed_access')
s('B2E01','FLNC','2026-09-17','https://ca.investing.com/news/stock-market-news/bmo-cuts-fluence-energy-stock-price-target-on-guidance-reduction-93CH-4843030','opened_relevant_body','读BMO新FY27R2.8B/EBITDA-10M、FY28R3.6B/68M、目标7。文章AI辅助+编辑审核，无个人署名；尾部混旧UBS/MS不使用。BMO原研报未得。','secondary_opinion','通常12个月目标；FY28模型，非2027-04目标')
s('B2E02','ADBE','2026-09-11/14','https://www.pricetargets.com/NASDAQ/ADBE/','opened_rating_rows','有署名日期：9/14Gil Luria Buy290；9/11Keith Weiss Underweight、Keith Bachman MarketPerform270、Mark Moerdler Outperform373。页面另有同机构冲突行，目标仅分歧证据，不取算法均值。研报正文未得。','secondary_rating_aggregator','12个月意见，不转成6个月目标')
s('B2E03','PNR','2026-10-12/09;2026-07-29','https://www.pricetargets.com/NYSE/pnr/','opened_rating_rows','Andrew Kaplowitz10/12 Buy69由85降，John Mackay10/9 Neutral60由73降，Joseph Giordano7/29 Sell65。目标不同不等对称概率；10/12精确发布时分未核。','secondary_rating_aggregator','通常12个月；10/12信息是否收盘后未证，不声称价格已反映')
s('B2E04','PLAB','2026-05-29','https://www.investing.com/news/analyst-ratings/craighallum-cuts-photronics-stock-price-target-to-42-on-nearterm-headwinds-93CH-4716959','opened_relevant_body','已核正文日期May29：Craig-Hallum42是旧Q2意见，非Aug27最新观点。搜索另一地区表39与42时点不同，未用于最终价格。个人分析师署名未得。','secondary_opinion','旧12个月目标，只作历史争议；不作当前半年背书')
s('B2P16','LEU','2026-09-09','https://www.sec.gov/Archives/edgar/data/1065059/000110465926107103/tm2625019d5_ex99-2.htm','opened_relevant_body','读完整定价公告相关条款：四档226.8625/272.235/317.6075/362.98，各档执行额约500M；2倍价仅首档价内。模型四分支按价内性解隐式方程，不在失望价预加融资。')
for x in rows:
    if x['id']=='B2P06': x['event_date']='2026-07-30'; x['note']+=' 日期由X1S25交叉核，修正初始占位8/6。'
inherited=[]
for p in [R/'07_logs/S1_sources.json',*[R/f'07_logs/{x}_sources.json' for x in ['X1','X2','X3','X4','X5']]]:
    if p.exists(): inherited.append({'path':str(p.relative_to(R)),'status':'本轮只继承被引用卡的证据，未冒称重新全文打开所有source','do_not_count_as_new_independent_source':True})
out={'role':'B2','access_date_utc':'2026-10-13','new_accesses':rows,'inherited_source_catalogs':inherited,'reading_boundary':'本轮新读相关正文/财表与定向原文；非35/36家公司全原始报告阅读全文。原始发布/搜索摘要/失败分别留痕。估值倍数是B2判断。'}
(R/'07_logs/B2_sources.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print({'sources':len(rows)})
