import json,hashlib,collections
from pathlib import Path
ROOT=Path(__file__).parent
inv=json.loads((ROOT/'report_inventory.json').read_text(encoding='utf-8'))
sec=json.loads((ROOT/'sec_scan.json').read_text(encoding='utf-8'))
foreign=json.loads((ROOT/'foreign_earnings.json').read_text(encoding='utf-8'))
calendar=json.loads((ROOT/'calendar_scan.json').read_text(encoding='utf-8'))
foreign_map={r['symbol']:r for r in foreign['companies']}
sec_map={r['symbol']:r for r in sec['companies']}
events={
 'MU':{'type':'新季度及全年实绩','date':'2026-09-30','period':'FY2026Q4/FY2026，期末2026-09-03','source':'https://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Fiscal-Fourth-Quarter-and-Full-Year-2026-Results/default.aspx','note':'另有FY27Q1及资本支出新指引，未来值不可计为命中'},
 'JBL':{'type':'新季度及全年实绩','date':'2026-09-30','period':'FY2026Q4/FY2026，期末2026-08-31','source':'https://investors.jabil.com/news/news-details/2026/Jabil-Posts-Fourth-Quarter-and-Fiscal-Year-2026-Results/default.aspx','note':'初步未审计实绩；FY27指引是未来目标'},
 'IMOS':{'type':'新月度利润信息','date':'2026-09-29','period':'2026年8月，未审计','source':'https://www.sec.gov/Archives/edgar/data/1123134/000119312526405910/discloses_financial_info.htm','note':'9/10已知收入；9/29新增利润/EPS；不是完整Q3'},
 'ADBE':{'type':'同财季10-Q新增细节','date':'2026-09-22','period':'FY2026Q3，期末2026-08-28；实绩已9/10发布','source':'https://www.sec.gov/Archives/edgar/data/796343/000079634326000156/adbe-20260828.htm','note':'新增收购对价及成本桥；不能计为新的季度预测验证'},
}
other_notes={'TSEM':'9/23 6-K为11月技术研讨会预告','TSM':'9/24 6-K为8月持股、资本拨款等月末资料','UMC':'9/29 6-K重复9/10公告的8月持股及质押信息','BABA':'9/29 6-K为翌日股份变动披露','HOCPY':'9/25为旧Q1财报后的FAQ','DKILY':'9/28为Integrated Report 2026','YASKY':'9/30为YASKAWA Report 2026','SIMO':'9/22同日6-K非报告日期之后事件'}
rows=[]
for c in inv['companies']:
 s=sec_map[c['symbol']];f=foreign_map.get(c['symbol']);e=events.get(c['symbol'])
 sources=[]
 if s['status']=='sec_checked':sources.append({'type':'SEC recent submissions','url':f"https://data.sec.gov/submissions/CIK{s['cik']:010d}.json"})
 if f:sources.append({'type':'issuer official IR/financial result','url':f['primary_source_url']})
 assert sources,c['symbol']
 row={k:c[k] for k in ['symbol','name','category','report_date','path','sha256']}
 row.update({'screening_status':e['type'] if e else '未检出上述新增财务结果','event':e,'sources':sources,'latest_full_earnings_release_date_if_directly_verified':f['latest_full_earnings_release_date'] if f else None,'note':other_notes.get(c['symbol'],e['note'] if e else (f['note'] if f else 'SEC无新财务候选；Nasdaq全窗口无对应报告后财报日')),'sec_after_report_filings':s.get('filings',[]),'hash_unchanged':hashlib.sha256(Path(c['path']).read_bytes()).hexdigest()==c['sha256']})
 rows.append(row)
assert len(rows)==221 and len({r['symbol'] for r in rows})==221
assert all(r['hash_unchanged'] for r in rows)
assert not any(r['error'] for r in calendar['days'])
assert all(s['symbol'] in foreign_map for s in sec['companies'] if s['status']!='sec_checked')
count=dict(collections.Counter(r['screening_status'] for r in rows))
data={'cutoff_utc':inv['cutoff_utc'],'cutoff_local':inv['cutoff_local'],'count':len(rows),'status_counts':count,'scope':'Latest formal company reports; complete inventory/date/text structure screening. Deep manual comparison of reports with meaningful new financial information; not a manual substantive quality score of all 221 reports.','method':'SEC ticker-CIK verified recent submissions for 200 companies; issuer official IR check for 40 including all 21 absent SEC matches; Nasdaq calendar 13-day cross-check, calendar is discovery only. Classification is based on actual issuer release contents.','limitation':'No-new-result means none found in the checked official channels by cutoff; not proof of absence on all websites. New 10-Q details and monthly profit are separate from new quarterly actuals.','companies':rows}
(ROOT/'全量筛查.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
lines=['# 项目221家公司最新公司调研报告财报后更新筛查','',f"核查截止：{inv['cutoff_local']}（{inv['cutoff_utc']}）。",'',f"当前索引221家，全部存在正式结果报告。分类：{count}。",'','使用正文研究截止日；成稿日期、监管提交日期、首次业绩公开日分别核验。目录/日期/文本结构全量检查，深读范围是出现相关增量财务信息的公司，未为221家公司逐份作完整质量评级。','', 'SEC覆盖200家，官方IR补核40家（含全部21家未匹配SEC ticker者），两组重叠19家；Nasdaq 9/18—9/30的13份日历仅用于候选发现。SEC候选逐份辨别公告内容，日历条目不作为实际发布证明。','', '“未检出”限定于已核查渠道及截止时间；其来源与原报告可逐行打开。AMBA等跨日成稿情况记录在 cross_report_audit.json，未改变正文研究截止日。','', '| 股票 | 公司 | 报告截止日 | 报告后财务更新类别 | 更新日期/期间 | 官方核查渠道 | 备注 |','|---|---|---|---|---|---|---|']
for r in rows:
 e=r['event'];dateperiod=f"{e['date']}；{e['period']}" if e else '—'
 sources='；'.join(f"[{x['type']}]({x['url']})" for x in r['sources'])
 if e:sources=f"[新增披露]({e['source']})；"+sources
 lines.append(f"| [{r['symbol']}]({r['path'].replace(chr(92),'/')}) | {r['name']} | {r['report_date']} | {r['screening_status']} | {dateperiod} | {sources} | {r['note'].replace('|','/')} |")
(ROOT/'全量筛查.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(count)
print('221 sources covered; 221 frozen hashes unchanged; 13 calendar calls successful.')
