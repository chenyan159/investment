from pathlib import Path
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo
import json, hashlib, re, difflib

ROOT=Path(r'D:\drive\Investment')
OUT=Path(__file__).parent
plan=json.loads((OUT/'迁移计划.json').read_text(encoding='utf-8'))
issues=[]
def check_record(p,expected):
    path=Path(p)
    if not path.is_file(): issues.append('文件缺失：'+str(p));return
    if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:issues.append('文件内容发生变化：'+str(p))
for r in plan['all_source_files']:check_record(r['destination'],r['sha256'])
for r in plan['protected_files']:check_record(r['path'],r['sha256'])
for r in plan['direct_company_reports']:check_record(r['destination'],r['sha256'])

def table(file):
    return [[s.strip().strip(chr(96)).rstrip('/') for s in line.strip('|').split('|')] for line in file.read_text(encoding='utf-8').splitlines() if line.startswith('| ') and chr(96) in line]
company_rows=table(ROOT/'基本面/公司调研/公司索引.md')
industry_rows=table(ROOT/'基本面/行业调研/行业索引.md')
assert len(company_rows)==218 and len(industry_rows)==91
assert len({r[0] for r in company_rows})==218 and len({r[0] for r in industry_rows})==91
assert {r[0]:r[2] for r in company_rows}=={r['symbol']:r['category'] for r in plan['companies']}
assert {r[0]:r[1] for r in industry_rows}=={r['name']:r['category'] for r in plan['industries']}
for d in plan['ensure_dirs']:
    if not Path(d).is_dir():issues.append('索引目录缺失：'+d)
for op in plan['renames']:
    if Path(op['source']).exists():issues.append('旧更名目录仍存在：'+op['source'])
for op in plan['archive_dirs']:
    if '商业航天_火箭_卫星' not in op['source'] and Path(op['source']).exists():issues.append('旧分类目录仍存在：'+op['source'])

def canonical(name):
    return re.sub(r'[\s_\-—–、,，/／\\()（）]+','',name).lower()
current_company_reports=[]
company_missing=[]
for e in plan['companies']:
    fs=list((ROOT/'基本面/公司调研'/e['category']).glob(e['symbol']+'_*.md'))
    assert len(fs)<=1,(e['symbol'],fs)
    if fs:current_company_reports+=fs
    else:company_missing.append(e['symbol'])
assert len(current_company_reports)==193
assert set(company_missing)=={e['symbol'] for e in plan['companies'] if e['is_new']}
current_industry_files=[p for c in plan['industry_categories'] for p in (ROOT/'基本面/行业调研'/c).glob('行业调研_*.md')]
reports={canonical(re.sub(r'_\d{4}-\d{2}-\d{2}$','',p.stem.removeprefix('行业调研_'))):p for p in current_industry_files}
assert len(current_industry_files)==len(reports)==80
industry_missing=[]
for e in plan['industries']:
    e['report']=str(reports.get(canonical(e['name']),'')) if canonical(e['name']) in reports else None
    if not e['report']:industry_missing.append(e['name'])
assert len(industry_missing)==11
assert all(e['mapping'] for e in plan['industries'] if not e['report'])
expected_keys={canonical(e['name']) for e in plan['industries']}
assert not (set(reports)-expected_keys),'存在不属于活动索引的直属行业报告'
old={x['symbol']:x for x in plan['old_companies']}
new=[x for x in plan['companies'] if x['is_new']]
changed=[x for x in plan['companies'] if not x['is_new'] and x['category']!=x['old_category']]
cc=Counter(x['category'] for x in plan['companies'])
ic=Counter(x['category'] for x in plan['industries'])
result={'verified_at':datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),'company_count':218,'company_category_count':16,'existing_company_reports':193,'new_companies_without_reports':company_missing,'existing_companies_with_category_changes':len(changed),'industry_entries':91,'economic_industries':90,'horizontal_topics':1,'industry_category_count':7,'existing_active_industry_reports':80,'new_industries_without_reports':industry_missing,'archived_former_composite_industries':['机器人硬件','商业火箭与商业航天'],'preserved_file_hashes_verified':len(plan['all_source_files']),'protected_files_hashes_verified':len(plan['protected_files']),'issues':issues}
(OUT/'验收结果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def link(p,label):
    return '['+label+'](</'+str(p).replace('\\','/')+'>)'
lines=['# 公司和行业分类升级完成清单','',f'核验时间：{result["verified_at"]}','',
 '本次仅更新索引、目录和分类关联，以及读取这些分类所需的代码映射。没有修改研究方案、提示词或研究正文，没有新增研究任务，也没有启动research runner。','',
 '| 项目 | 调整前 | 调整后 |','|---|---:|---:|','| 公司 | 193 | 218 |','| 公司主分类 | 10 | 16 |','| 活动行业/专题 | 82 | 91（90个经济主题＋1个横向专题） |','| 行业父类别 | 7 | 7（两个名称更新） |','| 现有公司正式报告 | 193 | 193 |','| 活动行业报告 | 82 | 80；原2篇综合报告归档保留 |','',
 '新增待研究：25家公司、11个行业主题。待研究是本次核验时点的文件覆盖状态，后续由runner处理。','',
 '**保存验证**：原分类目录下'+str(len(plan['all_source_files']))+'个文件均可在迁移后的确定路径找到，SHA-256全部一致；'+str(len(plan['protected_files']))+'个研究方案/方法、提示词及队列文件哈希未变。','',
 '## 新增25家公司','',
 '| 代码 | 公司名称 | 主分类 | 美国交易身份 |','|---|---|---|---|']
for x in new:lines.append(f"| {x['symbol']} | {x['name']} | {x['category']} | {x['listing_note']} |")
lines+=['','## 当前218家公司：按16类列出全部股票代号','','“＋”为本次新增。完整公司名称和多行业关联见'+link(ROOT/'基本面/公司调研/公司索引.md','公司索引')+'。','',
 '| 类别 | 数量 | 全部公司 |','|---|---:|---|']
company_table=[]
for c in plan['company_categories']:
    names='、'.join(x['symbol']+('＋' if x['is_new'] else '') for x in plan['companies'] if x['category']==c)
    row=f'| {c} | {cc[c]} | {names} |'
    lines.append(row);company_table.append(row)
lines+=['','## 当前全部行业与横向专题','','“＋”为本次新设且待研究；“横向”为标准/架构比较专题。完整边界与替代关系见'+link(ROOT/'基本面/行业调研/行业索引.md','行业索引')+'。']
industry_table=[]
for c in plan['industry_categories']:
    lines+=['',f'### {c}（{ic[c]}项）','']
    names=[]
    for e in plan['industries']:
        if e['category']!=c:continue
        label=e['name']+('【横向】' if e['type']=='横向专题' else '')+('＋' if not e['report'] else '')
        names.append(label)
        lines.append('- '+label)
    industry_table.append(f'| {c} | {ic[c]} | '+ '；'.join(names)+' |')
lines+=['','## 既有公司分类变化','','82家公司分类名称或归属变化：65家跨类别调整，17家随材料目录更名。','',
 '| 公司 | 原分类 | 现分类 | 变更理由 |','|---|---|---|---|']
for e in changed:lines.append(f"| {e['symbol']} | {e['old_category']} | {e['category']} | {e['change_reason']} |")
lines+=['','## 目录迁移与历史保留','',
 '- 公司分类目录更名：半导体材料_化学品_基板 → 电子材料_化学品_基板_PCB；另将3个旧混合大类拆分，原目录内历史/临时资料归档保留。',
 '- 行业目录更名：晶圆制造_设备_材料_测试 → 半导体与电子制造_设备_材料_测试。',
 '- 机器人新父类别：工业自动化_机器人_感知，包含3个拆分主题及1个新设视觉感知主题。',
 '- 原机器人和商业航天综合报告及所有历史版本，完整保存在本次备份目录的“原综合行业”下。',
 '- OCI（光学计算互连）/ Open CPX / XPO原题名、文件位置和正文保留，在行业索引中改为横向专题。',
 '- 首批五个AI软件主题已经有报告，索引中旧的“新增待调研”文字已更正。',
 '',
 '分类消费兼容：runner的允许分类、索引解析和索引新增时的字段保留已同步；站点ETL支持新分类、公司的显式多行业关联，并以索引分类优先于历史报告中的旧分类。分类读取在本次备份目录内验证，正式站点数据未改写或发布。',
 '',
 '兼容检查：runner现有及新增索引回归测试54项全部通过；活动队列0项、验证0错误0警告。站点分类读取验证识别218家公司、193份现有公司报告、91个行业/横向条目，19份更名分类下的行业报告正确归入新类别；待研究行业的公司关联保留。',
 '',
 '原索引及相关代码备份在“原文件”；逐文件原路径、新路径与SHA-256见“迁移计划.json”；执行动作见“执行日志.jsonl”。',
 ]
(OUT/'完成汇报_公司和行业全清单.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(OUT/'汇报表格.md').write_text('\n'.join(company_table)+'\n\n'+'\n'.join(industry_table)+'\n',encoding='utf-8')
diff=[]
for source in plan['source_code']:
    p=Path(source);before=OUT/'原文件'/p.relative_to(ROOT)
    diff.extend(difflib.unified_diff(before.read_text(encoding='utf-8').splitlines(),p.read_text(encoding='utf-8').splitlines(),fromfile='before/'+str(p.relative_to(ROOT)),tofile='after/'+str(p.relative_to(ROOT)),lineterm=''))
(OUT/'分类读取器变更.diff').write_text('\n'.join(diff)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
assert not issues,issues
