from pathlib import Path
import csv,json,hashlib,re,difflib
ROOT=Path('D:/drive/Investment'); SORT=ROOT/'分析报告/公司排序'; OUT=Path(__file__).resolve().parent
s=json.loads((OUT/'修改前快照.json').read_text(encoding='utf-8'));m=json.loads((OUT/'新方案清单.json').read_text(encoding='utf-8'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
generator='分析报告/公司排序/生成站点数据.mjs'
protected=[r for r in s['protected'] if r['path']!=generator]
assert all(sha(ROOT/r['path'])==r['sha256'] for r in protected),'Historical/protected file changed'
g=next(r for r in s['protected'] if r['path']==generator)
assert sha(OUT/'原文件'/generator)==g['sha256']
assert all(sha(OUT/'原文件'/r['path'])==r['sha256'] for r in s['editable'])
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
p=read(SORT/'00_待运行研究方案注册表.csv');count={mode:sum(r['execution_mode']==mode for r in p) for mode in ['routine','experiment','paired_experiment','absorbed','historical']}
assert count=={'routine':8,'experiment':2,'paired_experiment':3,'absorbed':5,'historical':11},count
for r in p:
 if r['prompt_file']:
  assert sha(ROOT/r['prompt_file'])==r['sha256'];assert not (ROOT/r['expected_output_file']).exists()
 if r['execution_mode']=='absorbed':assert not r['prompt_file'] and r['absorbed_by']
 if r['control_prompt_file']:
  assert sha(ROOT/r['control_prompt_file'])==r['control_sha256'];assert not (ROOT/r['control_expected_output_file']).exists()
def normalize(t):
 t=re.sub(r'(?m)^3\. (允许读取|禁止读取或继承).+\n','3. INPUT_ACCESS\n',t)
 return t.split('## 唯一输出位置')[0]
paired=[]
for e in m['experiments']:
 a=(ROOT/e['ABCDE']['prompt_file']).read_text(encoding='utf-8');b=(ROOT/e['BCDE']['prompt_file']).read_text(encoding='utf-8')
 assert normalize(a)==normalize(b),e['experiment_id']
 assert '禁止读取或继承' in b and '经营模型入口为' not in b and '缺少新版公司报告' not in b
 assert '全研究阶段禁止读取' in b and '输入污染' in b
 paired.append({'id':e['experiment_id'],'rules_identical_outside_input_and_output':True})
for r in m['created']:
 t=(ROOT/r['prompt_file']).read_text(encoding='utf-8')
 assert not re.search(r'file-run|research-runner|上一版|前一版|来源方案|与某方案相同',t,re.I),r['prompt_file']
 assert t.count('## 唯一输出位置')==1
 assert (ROOT/r['expected_output_file']).as_posix() in t
 assert '{INPUT}' not in t and '{access}' not in t
old=read(OUT/'原文件/分析报告/公司排序/00_运行与榜单注册表.csv');now=read(SORT/'00_运行与榜单注册表.csv')
keys=['method_id','list_id','run_id','run_date','plan_path','result_path','expected_row_count','is_current']
assert [[r[k] for k in keys] for r in old]==[[r[k] for k in keys] for r in now]
stateold=read(OUT/'原文件/分析报告/公司排序/00_方案状态总表.csv');statenow=read(SORT/'00_方案状态总表.csv')
assert [{k:v for k,v in r.items() if k not in ['status','role','next_action']} for r in stateold]==[{k:v for k,v in r.items() if k not in ['status','role','next_action']} for r in statenow]
diff=[]
for r in s['editable']+[g]:
 a=OUT/'原文件'/r['path'];b=ROOT/r['path']
 if b.suffix!='.json':diff.extend(difflib.unified_diff(a.read_text(encoding='utf-8-sig').splitlines(True),b.read_text(encoding='utf-8-sig').splitlines(True),fromfile='before/'+r['path'],tofile='after/'+r['path']))
(OUT/'改动.diff').write_text(''.join(diff),encoding='utf-8')
result={'protectedFilesUnchanged':len(protected),'generatorOriginalBackedUp':True,'editableOriginalsBackedUp':len(s['editable']),'executionModes':count,'newPlans':len(m['created']),'pairedRules':paired,'historicalResultRowsUnchanged':len(now),'historicalPerformanceColumnsUnchanged':True,'newResearchResults':0}
(OUT/'文件核验.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
