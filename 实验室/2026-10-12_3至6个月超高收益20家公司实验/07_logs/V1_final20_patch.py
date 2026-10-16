import json, shutil
from pathlib import Path
R=Path(r"D:\investment\实验室\2026-10-12_3至6个月超高收益20家公司实验")
backup=R/"04_verification/V1_pre_final20_review"
backup.mkdir(exist_ok=True)
for relative in ["04_verification/V1_evidence.json","04_verification/V1_evidence.md","07_logs/V1_sources.json","07_logs/V1_reading_notes.md"]:
    target=backup/Path(relative).name
    if not target.exists(): shutil.copy2(R/relative,target)
p=R/"04_verification/V1_evidence.json"
d=json.loads(p.read_text(encoding="utf-8-sig"))
clsurl="https://corporate.celestica.com/news-releases/news-release-details/celestica-hold-q3-2026-financial-results-and-2026-investor-and"
for c in d["companies"]:
    if c["ticker"]=="CLS":
        c["event_3m"]="官方确定：2026-10-26盘后发布Q3业绩；2026-10-27 08:00 ET召开业绩兼投资者/分析师日电话会，午间另有线下论坛。确认FY26指引及2027路径。"
        c["published"]="Q2业绩2026-07-27 16:38EDT；日历公告2026-10-06 16:15EDT"
        c["source_urls"]=list(dict.fromkeys(c["source_urls"]+[clsurl]))
        c["local_correction"]+=" 最终20复查纠正V1原先约10月估计写法；日历已亲自读取公告正文，不再仅继承S1。"
    if c["ticker"]=="ACMR":
        c["security_notes"]="美股A普通股非ADS；8/4封面A64.657388M+B4.991808M=69.649196M经济股，旧B5.021811M为2025年底；报表USD、订单RMB；Shanghai73.2%，NCI须剔除一次。"
d["final20_review"]="2026-10-13 UTC；原版保留于04_verification/V1_pre_final20_review，日历与ACMR股数修订，不改变其余证据状态。"
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
sfile=R/"07_logs/V1_sources.json"
s=json.loads(sfile.read_text(encoding="utf-8-sig"))
s["web_access_manifest"] += [
{"batch":"final20","ticker":"CLS","tool_reference":"turn456view0","url":clsurl,"access":"original_primary_relevant_body_read","published":"2026-10-06T16:15:00-04:00","notes":"正文86至96行确认10/26盘后及10/27 08ET会议；非仅网页标题"},
{"batch":"final20","ticker":"ACMR","tool_reference":"turn455view1","url":"https://www.sec.gov/Archives/edgar/data/1680062/000162828026054832/acmr-20260630.htm","access":"original_primary_cover_read","notes":"59至60行A+B=69.649196M"}
]
for entry in s["decisive_sources"]:
    if entry["ticker"]=="CLS":
        entry["source_urls"]=list(dict.fromkeys(entry["source_urls"]+[clsurl]))
        entry["published"]="2026-07-27；日历2026-10-06 16:15EDT"
sfile.write_text(json.dumps(s,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

