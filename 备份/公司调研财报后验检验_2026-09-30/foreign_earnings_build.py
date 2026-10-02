import json
from pathlib import Path

base=Path(r'D:\investment\备份\公司调研财报后验检验_2026-09-30')
inv=json.loads((base/'report_inventory.json').read_text(encoding='utf-8'))
companies={x['symbol']:x for x in inv['companies']}
rows=[
('SKHY','2026-07-29','2026 Q2/H1','https://news.skhynix.com/en/category/ir/','官方IR列表最新完整业绩为Q2，7月29日。'),
('AJNMY','2026-08-06','FY2026 Q1, ended 2026-06-30','https://www.ajinomoto.co.jp/company/en/ir/news.html','官方IR消息列表。'),
('ASGLY','2026-08-04','FY2026 Q2/H1','https://www.agc.com/en/ir/index.html','官方最新业绩及日历，下一次Q3为11月5日。'),
('HOCPY','2026-07-31','FY26 Q1, ended 2026-06-30','https://www.hoya.com/en/investor/library/','9月25日上传FY26 Q1财报后FAQ，非新期间财报。'),
('PCRHY','2026-07-30','FY2027 Q1, ended 2026-06-30','https://holdings.panasonic/global/corporate/investors/release.html','官方财务公告当前最新为FY2027 Q1；日期由官方2026-08-26回顾文章确认。'),
('SHECY','2026-07-24','FY2026 Q1, ended 2026-06-30','https://www.shinetsu.co.jp/en/ir-calendar/','官方季度结果7月24日，下一次半年报10月27日。'),
('SMTOY','2026-07-31','FY2026 Q1, ended 2026-06-30','https://sumitomoelectric.com/ir/library','官方IR资料库完整列表。'),
('SOMMY','2026-08-04','FY2026 Q1, ended 2026-06-30','https://www.sumitomo-chem.co.jp/english/ir/event/','官方IR活动日历与当前资料。'),
('ASMIY','2026-07-28','2026 Q2/H1','https://www.asm.com/investors/results-center','官方Results Center完整2026列表。'),
('DSCSY','2026-07-23','FY2026 Q1, ended 2026-06-30','https://www.disco.co.jp/eg/ir/index.html','10月6日预告单体销售/出货快报；10月22日完整Q2，均在截止日之后。'),
('TOELY','2026-07-30','FY2027 Q1, ended 2026-06-30','https://www.tel.com/ir/library/report/i242su0000000goz-att/fy27q1tanshin-e.pdf','正式结果PDF第一页注明7月30日；官网结果目录已检查。TOELY已涉及9月17日ADR迁移，不据代码静态推断公司。'),
('ASMVY','2026-07-29','2026 interim/H1','https://www.asmpt.com/en/investor-relations/announcements-circulars/','6月25日为将于7月29日发布结果的预告，8月28日为同一期半年报补充上传。'),
('BESIY','2026-07-23','2026 Q2/H1','https://www.besi.com/investor-relations/financial-calendar/details/besis-2026-second-quarter-results/','官方发布日及Q2 webcast/materials。'),
('MICLF','2026-07-14','2026 Q2/H1','https://www.mycronic.com/news-events/our-press-releases/','官方全部新闻列表截至9月15日；8月31日财务目标是新指引而不是新实绩。'),
('IFNNY','2026-08-05','FY2026 Q3, ended 2026-06-30','https://www.infineon.com/press-release/2026/infpr202608-125','官方实绩公告；官方财务日历下一次Q4及全年11月10日。'),
('MRAAY','2026-07-31','FY2026 Q1, ended 2026-06-30','https://corporate.murata.com/en-sg/newsroom/news/irnews/irnews/2026/0731','官方实绩公告及结果资料库。'),
('ST','2026-07-29','2026 Q2/H1','https://investors.sensata.com/overview/default.aspx?languageid=1','Sensata（并非STM）；官方最新季度为Q2。'),
('TTDKY','2026-07-31','FY3/27 Q1, ended 2026-06-30','https://www.tdk.com/en/ir/ir_library/financial/index.html','官网FY3/27标签下最新Q1；网页正文有重复FY标题，采用经济期间明确的当前栏。'),
('ABBNY','2026-07-16','2026 Q2/H1','https://global.abb/group/en/investors/quarterly-results','官方最新结果及全年2026档案。'),
('MIELY','2026-07-31','FY2027 Q1, ended 2026-06-30','https://www.mitsubishielectric.com/investors/library/results/','官方当前FY2027 Q1。'),
('SBGSY','2026-07-30','2026 H1','https://www.se.com/ww/en/about-us/investor-relations/financial-results/','最新HY实绩；下一Q3收入10月29日，不在截止内。'),
('HTHIY','2026-07-29','FY2026 Q1, ended 2026-06-30','https://www.hitachi.com/en/ir/','官方IR最新季度资料。'),
('RYCEY','2026-07-30','2026 H1','https://www.rolls-royce.com/investors/results-reports-and-presentations/financial-results','官方当前2026列表。'),
('DKILY','2026-08-04','FY2026 Q1, ended 2026-06-30','https://www.daikin.com/investor','9月28日新发Integrated Report 2026，不是新季度经营实绩。'),
('FANUY','2026-07-31','FY2026 Q1, ended 2026-06-30','https://www.fanuc.co.jp/en/ir/announce/','官方当前FY2026 Q1结果与电话会资料。'),
('SMCAY','2026-08-07','FY2026 Q1, ended 2026-06-30','https://www.smcworld.com/ir/en-jp/calendar.html','下一Q2为11月13日。'),
('YASKY','2026-07-10','FY2026 Q1, ended 2026-05-31','https://www.yaskawa-global.com/ir','9月30日新发YASKAWA Report 2026，不是新季度；Q2实绩预定10月9日。'),
('ASML','2026-07-15','2026 Q2/H1, ended 2026-06-28','https://www.investor.asml.com/quarterly-results','官方最新Q2；Q3预定10月14日。'),
('ASX','2026-07-30','2026 Q2/H1','https://www.sec.gov/Archives/edgar/data/1122411/000095010326011351/dp250868_6k.htm','官方SEC Q2实际发布日；公司IR域名无法通过web工具打开，报告后SEC由根代理全量检查。'),
('ATEYY','2026-07-29','FY2026 Q1, ended 2026-06-30','https://www.advantest.com/en/investors/','官方最新Q1；下一Q2预定10月28日。'),
('IMOS','2026-08-11','2026 Q2/H1','https://chipmostechnologiesinc.gcs-web.com/news-releases/','9月29日另外披露8月未审计月度利润，详见增量财务信息；不计为新季度财报。'),
('NOK','2026-07-23','2026 Q2/H1','https://www.nokia.com/about-us/investors/results-reports/','官方当前最新Q2。'),
('STM','2026-07-23','2026 Q2/H1','https://investors.st.com/events/event-details/q2-2026-financial-results','官方结果公告、季度事件及SEC由根代理检查。'),
('UMC','2026-07-29','2026 Q2/H1','https://www.umc.com/upload/media/08_Investors/Financials/Quarterly_Results/Quarterly_2020-2029_English_pdf/2026/Q2_2026/UMC26Q2_report.pdf','9月29日6-K是原9月10日发布的8月持股交易/质押资料，无新利润；完整官方IR目录web不可用，根代理已检查SEC。'),
('TSM','2026-07-16','2026 Q2/H1','https://investor.tsmc.com/english/quarterly-results/2026/q2','官方财务日历下一Q3为10月15日；9月24日6-K由根代理核查。'),
('BABA','2026-08-20','FY2027 Q1/June quarter, ended 2026-06-30','https://www.alibabagroup.com/en-US/ir-news-filings','官方全部业绩消息列表；9月29日6-K由根代理核查。'),
('ARM','2026-07-29','FY2027 Q1, ended 2026-06-30','https://investors.arm.com/financials/quarterly-annual-results','官方最新季度列表。'),
('SIMO','2026-07-30','2026 Q2/H1','https://ir.siliconmotion.com/news?c=191982&nyo=0&p=irol-news','官方最新财务消息与SEC列表截至9月22日；无报告后新期间结果。'),
('GFS','2026-08-05','2026 Q2/H1','https://investors.gf.com/','官方IR当前最新Q2；根代理已检查SEC。'),
('POET','2026-08-13','2026 Q2/H1','https://www.poet-technologies.com/news-media','官方最新完整结果Q2，最新新闻9月4日。'),
]
output=[]
for symbol,release,period,url,note in rows:
    c=companies[symbol]
    output.append(dict(symbol=symbol,name=c['name'],report_date=c['report_date'],latest_full_earnings_release_date=release,latest_financial_period=period,primary_source_url=url,new_full_earnings_after_report=False,coverage='official IR results/news/calendar or official earnings with SEC supplemental scan',note=note))
extra=[dict(symbol='IMOS',event_date='2026-09-29',period='August 2026',type='unaudited monthly profitability disclosure due to TWSE trading-information threshold',source_url='https://www.sec.gov/Archives/edgar/data/1123134/000119312526405910/discloses_financial_info.htm',currency='TWD',unit='million',revenue=2786,pretax_profit=530,parent_net_profit=433,ordinary_share_eps=0.62,revenue_yoy=33.3,pretax_profit_yoy=114.6,parent_net_profit_yoy=117.6,eps_yoy=121.4,new_information='Revenue already disclosed Sept10; profitability/EPS are new. Not a complete quarter or audited results.'),dict(symbol='UMC',event_date='2026-09-29',original_announcement_date='2026-09-10',type='August insider share trading and pledge report; no changes',source_url='https://www.sec.gov/Archives/edgar/data/1033767/000119312526405903/umc-ex99_1.htm',new_information='No new business profitability information.')]
doc=dict(cutoff_local=inv['cutoff_local'],cutoff_utc=inv['cutoff_utc'],count=len(output),new_full_earnings_count=0,companies=output,other_new_financial_disclosures=extra,qualification='未发现完整季度/半年度/年度新实绩；逐家官方IR/业绩源检查与根代理SEC扫描合并使用，不将不存在检索结果当作绝对不存在证明。')
(base/'foreign_earnings.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf-8')
notes=['# 海外与OTC公司财报更新核查','',f"核查截止：{inv['cutoff_local']}（{inv['cutoff_utc']}）。覆盖{len(output)}家。",'', f'{len(output)}家均未发现公司调研报告后、截止日前新发布的完整季度、半年度或年度经营财报。该判断须与根代理的SEC全量扫描合并使用。IMOS新月度利润可提供额外经营验证，单列而不混入完整财报样本。','', '| 股票 | 公司调研日期 | 最近完整实绩公布日 | 期间 | 官方证据及备注 |','|---|---|---|---|---|']
for r in output:
    notes.append(f"| {r['symbol']} | {r['report_date']} | {r['latest_full_earnings_release_date']} | {r['latest_financial_period']} | [官方资料]({r['primary_source_url']})。{r['note']} |")
notes.extend(['','## 新月度利润与容易误判的文件更新','','IMOS于2026-09-29新披露2026年8月未审计税前利润5.30亿元新台币、归母净利4.33亿元、普通股EPS0.62；同一公告的收入27.86亿元此前已于9月10日公布，Q2及TTM栏也是旧期间数据。只能验证8月盈利水平，不能代替Q3毛利、营业利润、现金流和订单兑现验证。','','UMC于9月29日向SEC提交的是原9月10日公告的8月董事/高管/大股东持股交易及质押信息，无变动，无新盈利。','','HOYA于9月25日更新Q1财报后FAQ；Daikin于9月28日发布Integrated Report 2026；Yaskawa于9月30日发布YASKAWA Report 2026。文件新公开可能带来策略、治理或问题答复信息，但三者不是新季度经营实际，不能作为预测命中样本。','','数据源覆盖限制：ASX公司IR域名和UMC部分IR路径在web工具不可访问，采用SEC实际披露、原报告官方季度资料与根代理最新SEC提交清单。少数英文网站财年标题重复或更新不及时，采用具体经济期间与原始业绩PDF日期核对。'])
(base/'foreign_notes.md').write_text('\n'.join(notes)+'\n',encoding='utf-8')
print('companies',len(output),'new full earnings',0)
