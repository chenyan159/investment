import pathlib,json,csv,hashlib,re,sys
sys.stdout.reconfigure(encoding='utf-8')
R=pathlib.Path(__file__).resolve().parents[2]; O=pathlib.Path(__file__).resolve().parent; S=R/'分析报告/公司排序'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,ok,detail=None):
 checks.append({'check':name,'ok':bool(ok),'detail':detail})
rows=list(csv.DictReader((S/'00_待运行研究方案注册表.csv').open(encoding='utf-8-sig',newline='')))
active=[x for x in rows if x['execution_mode'] in ['routine','experiment']]
check('当前入口为7常规2实验共9份',len(active)==9 and sum(x['execution_mode']=='routine' for x in active)==7 and sum(x['execution_mode']=='experiment' for x in active)==2)
check('没有成对入口及控制组残留',all(x['execution_mode']!='paired_experiment' and not x['control_prompt_file'] and not x['control_expected_output_file'] and not x['control_sha256'] for x in rows))
check('非活动方法无当前提示文件',all(not x['prompt_file'] for x in rows if x not in active))
check('所有新方案均为BCDE',all(x['input_set']=='BCDE' for x in active))
check('提示与输出路径各自唯一',len({x['prompt_file'] for x in active})==9 and len({x['expected_output_file'] for x in active})==9)
dry=json.loads((O/'file-run干运行记录.json').read_text(encoding='utf-8-sig'))
assembled={x['id']:x for x in dry}
for row in active:
 p=R/row['prompt_file']; out=R/row['expected_output_file']; t=p.read_text(encoding='utf-8-sig')
 check(row['method_id']+' 完整正文与哈希',p.is_file() and h(p)==row['sha256'] and all(x in t for x in ['## 研究目标与期限','## 输入与独立性边界','## 从公司事实形成独立判断','## 比较、缺失与选择规则','## 研究组织与交付','## 本方法','## 唯一输出位置']),{'path':row['prompt_file'],'sha256':h(p),'chars':len(t)})
 check(row['method_id']+' 输出独立且尚未生成',not out.exists() and out.parent==p.parent and t.count('## 唯一输出位置')==1 and 'D:/drive/Investment/'+row['expected_output_file'] in t)
 check(row['method_id']+' 无执行器与历史补丁语义',not re.search(r'research-runner|file-run|runner|队列|重跑|上一版|前一版|本次对话|继承假设',t))
 method=t[t.index('## 本方法'):t.index('## 唯一输出位置')]
 check(row['method_id']+' 专属方法无公司情景投资依赖','公司情景' not in method and '**公司经营研究的主输入是' in t and '**禁止读取或继承' in t)
 d=assembled[row['method_id']]
 m=re.search(r'(?m)^Prompt debug: (.+)$',d['output'])
 dp=pathlib.Path(m.group(1).strip()) if m else None
 dt=dp.read_text(encoding='utf-8-sig') if dp and dp.is_file() else ''
 check(row['method_id']+' 通用执行器实际组装通过',d['exit_code']==0 and dt.startswith(t.strip()) and '本次输出' in dt and row['expected_output_file'] in dt,{'debug_path':str(dp) if dp else None,'debug_sha256':h(dp) if dp and dp.exists() else None})
# Current company source coverage.
idx=(R/'基本面/公司调研/公司索引.md').read_text(encoding='utf-8-sig')
entries=re.findall(r'^\|\s*([A-Z0-9.\-]+)\s*\|[^\n]*?`([^`]+)`',idx,re.M)
missing=[ticker for ticker,folder in entries if not list((R/'基本面/公司调研'/folder).glob(ticker+'_*.md'))]
check('公司索引中193家公司均能定位正式报告',len(entries)==193 and not missing,{'indexed':len(entries),'missing':missing})
for p in ['基本面/公司调研','基本面/行业调研','金融资料/每日金融数据']:
 check('允许输入目录存在 '+p,(R/p).is_dir())
before=json.loads((O/'修改前文件清单.json').read_text(encoding='utf-8-sig'))
protected=[x for x in before if x['role']=='protected']
changed=[x['path'] for x in protected if h(R/x['path'])!=x['sha256']]
check('历史32份研究全文及结果和9个运行控制文件未改',len(protected)==41 and not changed,changed)
backups=[x['path'] for x in before if h(O/'修改前快照'/x['path'])!=x['sha256']]
check('修改前59份快照哈希一致',len(before)==59 and not backups,backups)
# Historical result and evaluation fields must not get rebound to new versions.
oldrows=list(csv.DictReader((O/'修改前快照/分析报告/公司排序/00_方案状态总表.csv').open(encoding='utf-8-sig',newline='')))
newrows=list(csv.DictReader((S/'00_方案状态总表.csv').open(encoding='utf-8-sig',newline='')))
skip={'status','role','next_action'}
check('状态总表历史指标和结果绑定原样保留',len(oldrows)==len(newrows) and all(all(a[k]==b[k] for k in a if k not in skip) for a,b in zip(oldrows,newrows)))
policy=list(csv.DictReader((S/'00_站点发布策略.csv').open(encoding='utf-8-sig',newline='')))
check('旧04及旧06不继续重复计收益共识',all(x['consensus_eligible']=='false' for x in policy if x['method_id'] in ['04','06']) and next(x for x in policy if x['method_id']=='04')['site_publish']=='false')
# Inspect local markdown links in active management and new research files.
files=[S/'00_总索引.md',S/'AGENTS.md',S/'07_输入扩展对照方案_待验证/README.md',S/'91_通用研究方案/README.md',S/'91_通用研究方案/2026-09-10_公司调研输入与九方案使用说明.md']
files += [R/x['prompt_file'] for x in active]
broken=[]
for p in files:
 for raw in re.findall(r'\]\(([^\n)]+)\)',p.read_text(encoding='utf-8-sig')):
  target=raw.strip('<>').split('#')[0]
  if not target or target.startswith(('http:','https:')):continue
  target=re.sub(r':\d+$','',target)
  if target.startswith('/D:/'):target=target[1:]
  dest=pathlib.Path(target) if re.match(r'^[A-Za-z]:/',target) else p.parent/target
  if not dest.exists() and dest.name!='00_实施报告.md':broken.append([str(p),target])
check('现行导航和方案链接可解析',not broken,broken)
summary={'checks':len(checks),'passed':sum(x['ok'] for x in checks),'failed':[x for x in checks if not x['ok']],'items':checks}
(O/'验证结果.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:summary[k] for k in ['checks','passed','failed']},ensure_ascii=False))
if summary['failed']:sys.exit(1)

