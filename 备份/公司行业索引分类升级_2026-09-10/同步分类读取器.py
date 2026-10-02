from pathlib import Path
ROOT=Path(r'D:\drive\Investment')

def read(p):
    raw=p.read_bytes().decode('utf-8')
    return raw.replace('\r\n','\n'), '\r\n' if '\r\n' in raw else '\n'
def write(p,text,newline):
    p.write_bytes(text.replace('\n',newline).encode('utf-8'))
def replace_once(text,old,new):
    assert text.count(old)==1,old[:160]
    return text.replace(old,new,1)

p=ROOT/'tools/research-runner/index-updater.mjs'
text,newline=read(p)
text=text.replace('下 10 个正式分类目录','下 '+chr(36)+'{COMPANY_CATEGORIES.length} 个正式分类目录')
text=text.replace('下 4 个正式分类目录','下 '+chr(36)+'{INDUSTRY_CATEGORIES.length} 个正式分类目录')
text=replace_once(text,'"| 股票代号 | 公司名称 | 目录 |",','"| 股票代号 | 公司名称 | 目录 | 业务标签 | 关联行业 | 交易身份与登记备注 |",')
text=replace_once(text,'"|---:|---|---|",','"|---|---|---|---|---|---|",')
text=replace_once(text,'"| 行业名称 | 目录 |",','"| 行业名称 | 目录 | 研究范围提示 | 专题类型 | 分类变更备注 |",')
text=replace_once(text,'"|---|---|",','"|---|---|---|---|---|",')
lines=text.splitlines()
company_row='    ...orderedEntries.map((entry) => "| " + [tableCell(entry.subject), tableCell(entry.displayName), "'+chr(96)+'" + tableCell(entry.category) + "/'+chr(96)+'", tableCell(entry.businessTags), tableCell(entry.industrySubjects), tableCell(entry.listingNote)].join(" | ") + " |"),'
industry_row='    ...orderedEntries.map((entry) => "| " + [tableCell(entry.subject), "'+chr(96)+'" + tableCell(entry.category) + "/'+chr(96)+'", tableCell(entry.researchScope), tableCell(entry.topicType || "行业"), tableCell(entry.classificationNote)].join(" | ") + " |"),'
for i,line in enumerate(lines):
    if '...orderedEntries.map((entry)' in line:
        lines[i]=company_row if 'entry.displayName' in line else industry_row
    if 'orderedEntries.length' in line and '个行业名称和分类目录' in line:
        lines[i]='    "# " + orderedEntries.length + "个行业与横向专题名称和分类目录",'
text='\n'.join(lines)+'\n'
write(p,text,newline)

p=ROOT/'tools/site/etl/build-data.mjs'
text,newline=read(p)
start=text.index('const companyToIndustryCategory = {')
end=text.index('\n};',start)+3
mapping={
 'AI计算芯片_EDA_IP_custom_ASIC':'AI服务器_存储_芯片',
 'AI服务器_存储_EMS':'AI服务器_存储_芯片',
 'AI网络_光互联_连接器':'AI网络_光互联_铜互联',
 '电子材料_化学品_基板_PCB':'半导体与电子制造_设备_材料_测试',
 '晶圆制造_前道设备':'半导体与电子制造_设备_材料_测试',
 '封测_检测_计量_光罩':'半导体与电子制造_设备_材料_测试',
 '功率半导体_电源管理_传感器':'AI园区电力_机电_冷却',
 '配电_电源系统_电气设备':'AI园区电力_机电_冷却',
 '电力_发电_能源_储能':'AI园区电力_机电_冷却',
 '热管理_流体_水处理':'AI园区电力_机电_冷却',
 '工程建设_机电安装':'AI园区电力_机电_冷却',
 '机器人_工业自动化_智能硬件':'工业自动化_机器人_感知',
 '航空航天_卫星_高可靠系统':'商业航天_火箭_卫星',
 '云算力_IDC_边缘云':'AI服务器_存储_芯片',
 '企业软件_数据平台':'AI应用_软件_数据平台',
 '网络安全_身份权限_治理':'AI应用_软件_数据平台',
}
newblock='const companyToIndustryCategory = {\n'+''.join(f'  "{k}": "{v}",\n' for k,v in mapping.items())+'};'
text=text[:start]+newblock+text[end:]
old='    name: cleanCell(row["公司名称"]),\n    category: cleanCell(row["目录"]).replace(/[\\\\/]+$/, ""),'
new=old+'\n    businessTags: cleanCell(row["业务标签"]),\n    relatedIndustryNames: cleanCell(row["关联行业"]).split("；").map((name) => name.trim()).filter(Boolean),'
text=replace_once(text,old,new)
old='    name: cleanCell(row["行业名称"]),\n    category: cleanCell(row["目录"]).replace(/[\\\\/]+$/, ""),'
new=old+'\n    topicType: cleanCell(row["专题类型"]) || "行业",'
text=replace_once(text,old,new)
text=replace_once(text,
 '    const relatedIndustrySlugs = relatedIndustryCategory ? industryByCategory.get(relatedIndustryCategory) || [] : [];',
 '    const relatedIndustrySlugs = row.relatedIndustryNames?.length\n'
 '      ? [...new Set(row.relatedIndustryNames.map((name) => industryReports.get(canonicalIndustryKey(name))?.slug).filter(Boolean))]\n'
 '      : relatedIndustryCategory ? industryByCategory.get(relatedIndustryCategory) || [] : [];')
text=replace_once(text,
 '      category: row.category,\n      relatedIndustrySlugs,',
 '      category: row.category,\n      businessTags: row.businessTags || "",\n      relatedIndustrySlugs,')
text=replace_once(text,
 'async function buildIndustryReports(indexRows) {\n',
 'async function buildIndustryReports(indexRows) {\n  const indexedByName = new Map(indexRows.map((row) => [canonicalIndustryKey(row.name), row]));\n')
text=replace_once(text,'        category: meta.category || category,',
 '        category: indexedByName.get(canonical)?.category || category,\n        topicType: indexedByName.get(canonical)?.topicType || "行业",')
write(p,text,newline)
print('Updated index serialization and site classification mapping; no research methods or outputs generated.')
