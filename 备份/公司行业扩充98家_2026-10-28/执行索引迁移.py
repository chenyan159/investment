"""一次性执行已批准的98家公司扩充；重复运行会拒绝。"""
import collections
import hashlib
import json
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).resolve().parent
PROPOSAL = ROOT / '备份/纳指100与标普500新增98家公司候选_2026-10-28'
load = lambda p: json.loads(p.read_text(encoding='utf-8'))
companies = load(PROPOSAL / '候选公司.json')
topics = load(PROPOSAL / '行业建议.json')
by_id = {t['id']: t for t in topics}
industry_rows = load(OUT / '行业入队映射.json')
index = ROOT / '基本面/公司调研/公司索引.md'
original = index.read_text(encoding='utf-8')
lines = original.splitlines()
rows = [line.split('|')[1:-1] for line in lines if line.startswith('| ') and '`' in line]
rows = [[v.strip() for v in r] for r in rows]
assert len(rows) == 252 and len(companies) == 98
assert len({c['ticker'] for c in companies}) == 98
assert not ({r[0] for r in rows} & {c['ticker'] for c in companies})
snapshot = OUT / '修改前/基本面/公司调研/公司索引.md'
assert not snapshot.exists()
snapshot.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(index, snapshot)

new_categories = ['消费科技_数字平台_文娱', '金融服务_支付_资本市场', '医疗器械_诊断_医疗服务', '消费品牌_食品饮料_餐饮', '工业服务_交通运输_航空制造', '能源资源_工业材料', '房地产_基础设施租赁']
category = {r['id']: r['category'] for r in industry_rows if r['id'].startswith('N')}
category.update({'M01':'企业软件_数据平台','M02':'企业软件_数据平台','M03':'保险_财产险_特色险_再保险','M04':'机器人_工业自动化_智能硬件','M05':new_categories[4],'M06':'航空航天_卫星_高可靠系统','M07':'电力_发电_能源_储能','M08':'零售_会员制_食品_折扣渠道','E1':'网络安全_身份权限_治理','E2':new_categories[0], 'N19':'航空航天_卫星_高可靠系统'})
renames = {t['original_name']:t['name'] for t in topics if t['id'].startswith('M')}
changes=[]
for row in rows:
    before=row[4]
    assoc=[renames.get(v,v) for v in before.split('；') if v]
    for topic in topics:
        if row[0] in topic['related_existing_companies'] and topic['name'] not in assoc:
            assoc.append(topic['name'])
    if row[0] == 'GE':
        # 现有业务标签明确为航空发动机；GE Aerospace与GE Vernova分别登记。
        assoc=[by_id['N19']['name'],by_id['M06']['name']]
    row[4]='；'.join(dict.fromkeys(assoc))
    if row[4] != before:
        changes.append({'ticker':row[0], 'before':before, 'after':row[4]})

secondary={'JNJ':['N09'],'BRK.B':['N06'],'RTX':['N19'],'MELI':['N04']}
for c in companies:
    assoc=[by_id[c['topic']]['name']]+[by_id[x]['name'] for x in secondary.get(c['ticker'],[])]
    if c['ticker']=='BRK.B': assoc.append('特色险、超额剩余险与全球再保险')
    rows.append([c['ticker'],c['name'],f"`{category[c['topic']]}/`",by_id[c['topic']]['name'],'；'.join(assoc),'2026-10-28新增登记；研究状态以正式报告为准'])
assert len(rows)==350 and len({r[0] for r in rows})==350
counts=collections.Counter(r[2].strip('`').rstrip('/') for r in rows)
assert len(counts)==27
first=next(i for i,l in enumerate(lines) if l.startswith('| ') and '`' in l)
last=max(i for i,l in enumerate(lines) if l.startswith('| ') and '`' in l)
lines[first:last+1]=['| '+' | '.join(row)+' |' for row in rows]
body='\n'.join(lines)+'\n'
body=body.replace('# 252家公司','# 350家公司',1).replace('更新日期：2026-10-22','更新日期：2026-10-28',1).replace('共252家公司、20个正式主分类','共350家公司、27个正式主分类',1)
body=body.replace('；分类名称保持不变。','。既有父分类目录保持稳定，新增公司按本次覆盖增加7个父分类；具体研究范围以关联行业为准。',1)
note='2026-10-28按已批准的合并方案新增98家公司，并同步19个新增行业主题、8个改名扩围主题的关联；修正GE Aerospace与电力设备主题的误关联。本次新增登记不代表研究报告已完成。\n\n'
body=body.replace('主类别用于项目研究归属',note+'主类别用于项目研究归属',1)
stats='\n'.join(f'- {k}：{v} 家' for k,v in counts.items())
body=re.sub(r'(## 目录统计\n\n).*?(\n\n## 索引表)',lambda m:m[1]+stats+m[2],body,flags=re.S)
index.write_text(body,encoding='utf-8',newline='\n')

domain=ROOT/'tools/research-runner/domains/company.mjs'
code=domain.read_text(encoding='utf-8')
assert all('"'+c+'"' not in code for c in new_categories)
anchor='  "环境服务_固废_回收_资源化",\n];'
assert anchor in code
code=code.replace(anchor,'  "环境服务_固废_回收_资源化",\n'+''.join(f'  "{c}",\n' for c in new_categories)+'];',1)
domain.write_text(code,encoding='utf-8',newline='\n')
for c in new_categories: (ROOT/'基本面/公司调研/结果'/c).mkdir(parents=True,exist_ok=True)

archives=[]
source_root=(ROOT/'基本面/行业调研/结果').resolve()
archive_root=(ROOT/'基本面/行业调研/备份').resolve()
for t in industry_rows:
    if not t['original_name']: continue
    folder=source_root/t['category']
    matches=list(folder.glob('行业调研_'+t['original_name']+'_*.md'))
    assert len(matches)==1, (t['original_name'],matches)
    for source in matches:
        target=archive_root/t['category']/source.name
        assert source.resolve().is_relative_to(source_root) and target.resolve().is_relative_to(archive_root)
        assert not target.exists(),target
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.move(str(source),str(target))
        assert hashlib.sha256(target.read_bytes()).hexdigest()==digest
        archives.append({'from':source.relative_to(ROOT).as_posix(),'to':target.relative_to(ROOT).as_posix(),'sha256':digest,'new_subject':t['subject']})
assert len(archives)==8
result={'companies_before':252,'companies_after':350,'new_company_count':98,'company_categories':27,'industries_before':102,'industries_after':121,'industry_categories':18,'new_industries':19,'renamed_industries':8,'existing_company_associations_changed':changes,'archived_unchanged_reports':archives,'new_company_categories':new_categories}
(OUT/'索引迁移核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if not isinstance(v,list)},ensure_ascii=False))
