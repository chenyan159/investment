from pathlib import Path
from datetime import datetime
import csv, difflib, hashlib, json, re

ROOT=Path('D:/drive/Investment');OUT=Path(__file__).parent;SORT=ROOT/'分析报告/公司排序';BASE=ROOT/'基本面/行业调研/研究方法'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8'))
issues=[];base=load(OUT/'实施前快照.json')
special=[r for r in base['protected'] if r['path'].startswith('备份/24家公司最新投资价值多情景评估_2026-08-19/')]
for r in base['protected']:
    p=ROOT/r['path']
    if not p.is_file() or sha(p)!=r['sha256']:issues.append(f'Protected file changed: {r["path"]}')
spdir=ROOT/'备份/24家公司最新投资价值多情景评估_2026-08-19'
assert {r['path'] for r in special}=={p.relative_to(ROOT).as_posix() for p in spdir.rglob('*') if p.is_file()},'Special file set changed'

entries=list(csv.DictReader((SORT/'00_待运行研究方案注册表.csv').open(encoding='utf-8-sig')))
assert len(entries)==26 and len({r['method_id'] for r in entries})==26
updated=[r for r in entries if r['prompt_file']];assert len(updated)==15
review=[]
for r in updated:
    p=ROOT/r['prompt_file'];s=p.read_text(encoding='utf-8');assert sha(p)==r['sha256']
    assert not (ROOT/r['expected_output_file']).exists(),'Unexpected result for unrun plan'
    for text in ['3个月','6个月','原文事实','主观概率','风险是否解除','观察','NA','来源','市场','唯一输出位置']:
        if text not in s:issues.append(f'{r["method_id"]}: missing {text}')
    for text in ['research-runner','file-run','公司评估/结果','基本面/分析报告','公司评估\\结果','与前一版相同','下一节']:
        if text in s:issues.append(f'{r["method_id"]}: forbidden/stale {text}')
    for t in ['PENG','SMCI','SOMMY','AEHR']:
        if t in s:issues.append(f'{r["method_id"]}: backtest company in rule {t}')
    assert len(re.findall(r'^# ',s,re.M))==1
    assert s.count('\n## 本方法：')==1
    assert r['expected_output_file'].replace('\\','/') in s
    review.append(p)

cs=load(BASE/'会议/00_会议方案注册表.json');assert len(cs)==4
for r in cs:
    p=ROOT/r['prompt_file'];s=p.read_text(encoding='utf-8')
    assert sha(p)==r['sha256'] and sha(ROOT/r['common_source'])==r['common_sha256']
    common=(ROOT/r['common_source']).read_text(encoding='utf-8')
    # Apart from title/name/year instantiation and one dedicated section, common text is copied.
    stripped=re.sub(r'\n## (?:DAC|FMS|RSS|Farnborough) 的专属研究重点\n.*?(?=## 一、资料收集范围)', '',s,flags=re.S)
    assert len(stripped)>len(common)*0.95
    for token in ['最早公开日','独立复现','零条可执行投资机会','改变哪条产业/公司假设','HHmmss']:
        assert token in s,(p,token)
    assert '2026-08-18.md' not in s
    review.append(p)
review += sorted(BASE.glob('产业背景：*.md'))+[BASE/'会议调研方案.md']
for p in BASE.glob('产业背景：*.md'):
    s=p.read_text(encoding='utf-8')
    assert '## 本背景的责任' in s and '## 决定性结论的交付边界' in s
    assert '外部资料独立' in s and '未来3个月' in s
    for bad in ['保持乐观底色','保持乐观假设','抱有偏乐观','强制美元计价']:
        if bad in s:issues.append(f'{p.name}: stale {bad}')

newpaths=[ROOT/r['prompt_file'] for r in updated]+[ROOT/r['prompt_file'] for r in cs]+[
    SORT/'00_待运行研究方案注册表.csv',SORT/'91_通用研究方案/2026-09-07_新方案使用说明.md',
    BASE/'00_背景与会议研究入口.md',BASE/'会议/README.md',BASE/'会议/00_会议方案注册表.json',BASE/'会议/版本/2026-09-07/会议通用研究方案.md']
changed=[]
for r in base['editable']:
    p=ROOT/r['path'];backup=OUT/'原文件备份'/r['path'];assert sha(backup)==r['sha256']
    if sha(p)!=r['sha256']:changed.append(p)
allpaths=changed+newpaths
diffs=[]
for p in allpaths:
    old=OUT/'原文件备份'/p.relative_to(ROOT)
    a=old.read_text(encoding='utf-8-sig').splitlines(keepends=True) if old.exists() else []
    b=p.read_text(encoding='utf-8-sig').splitlines(keepends=True)
    diffs.extend(difflib.unified_diff(a,b,fromfile='before/'+p.relative_to(ROOT).as_posix(),tofile='after/'+p.relative_to(ROOT).as_posix()))
(OUT/'全部正式修改.diff').write_text(''.join(diffs),encoding='utf-8')

# Check newly introduced local document links, not pre-existing unmaintained historical links.
linkfiles=[SORT/'91_通用研究方案/2026-09-07_新方案使用说明.md',BASE/'00_背景与会议研究入口.md',BASE/'会议/README.md']
linkfiles += [p for p in OUT.glob('0*.md')]
index=(SORT/'00_总索引.md').read_text(encoding='utf-8').split('## 七月结果与既有状态')[0]
linktexts=[(p,p.read_text(encoding='utf-8')) for p in linkfiles]+[(SORT/'00_总索引.md',index)]
links=0
for p,s in linktexts:
    for m in re.finditer(r'\]\((<[^>]+>|[^)]+)\)',s):
        v=m.group(1).strip('<>')
        if v.startswith(('https://','http://','#')):continue
        v=re.sub(r':\d+$','',v)
        target=Path(v) if re.match(r'^[A-Za-z]:[/\\]',v) else p.parent/v
        links+=1
        generated_here={OUT/'正式修改清单.json',OUT/'交付核验.json'}
        if not target.exists() and target not in generated_here:issues.append(f'Broken link in {p}: {v}')

runtime=load(OUT/'运行入口预检.json')
assert len(runtime['checked'])==25 and not runtime['queue_written'] and not runtime['research_started']
assert load(OUT/'回测重新核验.json')['universe_checks']==192
manifest=[{'path':p.relative_to(ROOT).as_posix(),'operation':'update' if p in changed else 'create','sha256':sha(p)} for p in allpaths]
(OUT/'正式修改清单.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
report={'checked_at':datetime.now().astimezone().isoformat(),'modified_existing_formal_files':len(changed),'new_formal_files':len(newpaths),
    'new_sorting_plans':len(updated),'new_conference_plans':len(cs),'background_plans':5,'generic_conference_plans':1,
    'protected_file_hashes':len(base['protected']),'special_file_hashes':len(special),'runtime_entry_checks':25,'new_local_links_checked':links,
    'backtest_checks':{'company_returns':192,'top30_metrics':56,'conference_observations':15,'original_sorting_plan_hashes':26},
    'issues':issues,'scope':'Source edits and in-memory file-run checks only. No research executed or future efficacy proved.'}
(OUT/'交付核验.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(1 if issues else 0)
