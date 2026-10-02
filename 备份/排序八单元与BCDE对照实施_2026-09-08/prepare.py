from pathlib import Path
import os,json,csv,hashlib,shutil
ROOT=Path('D:/drive/Investment'); SORT=ROOT/'分析报告/公司排序'; OUT=Path(__file__).resolve().parent
EDIT=['00_总索引.md','AGENTS.md','00_待运行研究方案注册表.csv','00_方案状态总表.csv','00_运行与榜单注册表.csv','00_站点发布策略.csv','站点数据/current.json','07_输入扩展对照方案_待验证/README.md','91_通用研究方案/2026-09-07_新方案使用说明.md']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=OUT/'修改前快照.json'
assert not manifest.exists(),'Snapshot already exists; do not overwrite'
protected=[]
for base,dirs,files in os.walk(SORT,followlinks=False):
 dirs[:]=[d for d in dirs if not (os.lstat(Path(base)/d).st_file_attributes & 0x400) and d!='tmp']
 for n in files:
  p=Path(base)/n
  if p.relative_to(SORT).as_posix() not in EDIT:protected.append(p)
protected += list((ROOT/'备份/24家公司最新投资价值多情景评估_2026-08-19').rglob('*'))
protected += list((ROOT/'基本面/行业调研/研究方法').glob('*.md'))
protected=[p for p in protected if p.is_file()]
editable=[]
for n in EDIT:
 p=SORT/n; dest=OUT/'原文件'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 editable.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
manifest.write_text(json.dumps({'editable':editable,'protected':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in protected]},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'editable':len(editable),'protected':len(protected)}))
