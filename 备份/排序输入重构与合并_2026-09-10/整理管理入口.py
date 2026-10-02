import pathlib,json,csv,hashlib,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
root=pathlib.Path.cwd(); out=root/'备份/排序输入重构与合并_2026-09-10'; sroot=root/'分析报告/公司排序'
manifest=json.loads((root/'备份/16份排序结果横评_2026-09-09/16份结果清单.json').read_text(encoding='utf-8-sig'))
specs={x['id']:x for x in json.loads((out/'新方案清单.json').read_text(encoding='utf-8-sig'))}
records=json.loads((out/'修改前文件清单.json').read_text(encoding='utf-8-sig'))
existing={x['path'] for x in records}; changed=[]
for mid,x in manifest.items():
 key=mid.split('-')[0]
 base=pathlib.Path(x['prompt'].split('/迭代版本/')[0]); relbase=base.relative_to(root)
 if str(base) in changed:continue
 changed.append(str(base))
 dest={'04':'01','E04':'01','E05':'01','E06':'N02'}.get(key,key)
 n=specs[dest]
 if key=='06':
  state='当前06只负责事件右尾与重估；原06F性价比并入U01、06G成长并入U07。'
 elif key in ['04','E04','E05','E06']:
  state='本目录的独立执行入口已撤回，职责并入'+n['unit']+'。'
 else:state='当前研究使用公司调研独立输入的新版本；旧版本只用于历史追溯。'
 link='D:/drive/Investment/'+n['prompt']
 guide='# 当前执行入口\n\n'+state+'\n\n- 当前职责：'+n['unit']+' '+n['name']+'。\n- 当前完整方案：[公司调研输入方案](<'+link+'>)。\n- 执行身份：'+('常规研究' if n['mode']=='routine' else '限定实验')+'；新版本尚未运行、未验证。\n- 实际配置以[待运行注册表](<D:/drive/Investment/分析报告/公司排序/00_待运行研究方案注册表.csv>)为准。\n- 本目录的旧研究方案、结果和回测原样保留；旧成绩不继承给新正文。\n'
 targets=[base/'00_方案状态.md']
 if (base/'00_方案说明.md').exists():targets.append(base/'00_方案说明.md')
 for p in targets:
  rel=p.relative_to(root).as_posix()
  if p.exists() and rel not in existing:
   dst=out/'修改前快照'/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
   records.append({'path':rel,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'role':'management'})
   existing.add(rel)
  if p.exists():
   h=base/'历史管理资料/2026-09-10_输入重构前'/p.name
   h.parent.mkdir(parents=True,exist_ok=True)
   if h.exists():raise RuntimeError('Archive already exists '+str(h))
   shutil.copy2(p,h)
  p.write_text(guide,encoding='utf-8')
# New routine roots that did not exist before also receive a current navigation file.
for n in specs.values():
 base=root/n['prompt'].split('/迭代版本/')[0]
 if not (base/'00_方案状态.md').exists():
  text='# 当前执行入口\n\n'+n['unit']+' '+n['name']+'；公司调研独立输入。\n\n当前完整方案：[研究方案](迭代版本/'+n['version']+'/01_研究方案.md)。新版本尚未运行、未验证。\n\n未来配置以[待运行注册表](<D:/drive/Investment/分析报告/公司排序/00_待运行研究方案注册表.csv>)为准，历史结果不得绑定为本版本成绩。\n'
  (base/'00_方案状态.md').write_text(text,encoding='utf-8')
(out/'修改前文件清单.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
p=sroot/'00_待运行研究方案注册表.csv'
with p.open(encoding='utf-8-sig',newline='') as h:r=csv.DictReader(h);fields=r.fieldnames;rows=list(r)
for r in rows:
 if r['prompt_file']:r['sha256']=hashlib.sha256((root/r['prompt_file']).read_bytes()).hexdigest()
with p.open('w',encoding='utf-8-sig',newline='') as h:w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(rows)
print(json.dumps({'old_method_roots_redirected':len(changed),'snapshot_files':len(records),'new_plans':len(specs)},ensure_ascii=False))

