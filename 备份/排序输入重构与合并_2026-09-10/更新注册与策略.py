import csv,json,pathlib,hashlib,shutil,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(__file__).resolve().parents[2]
OUT=pathlib.Path(__file__).resolve().parent
S=ROOT/'分析报告/公司排序'
specs=json.loads((OUT/'新方案清单.json').read_text(encoding='utf-8-sig'))
byid={x['id']:x for x in specs}
before=json.loads((OUT/'修改前文件清单.json').read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for x in before:
 if x['role']=='management' and sha(ROOT/x['path'])!=x['sha256']:
  raise RuntimeError('Management changed since snapshot: '+x['path'])
def readcsv(p):
 with p.open(encoding='utf-8-sig',newline='') as h:
  r=csv.DictReader(h); return r.fieldnames,list(r)
def writecsv(p,fields,rows):
 with p.open('w',encoding='utf-8-sig',newline='') as h:
  w=csv.DictWriter(h,fieldnames=fields);w.writeheader();w.writerows(rows)
roles={
 '01':'赔率和极简基准双判断；吸收04、06F、E04/E05，独立公司事实建模，不平均投票。',
 '02':'既有经营预期的兑现可靠性及价格采纳，独立重建经营和市场隐含要求。',
 '06':'仅事件右尾与重估；06F并入U01，06G并入U07；旧三视图成绩不归给新方案。',
 '07':'收入与现金双判断，加入经营非线性及主评分漏选挑战；吸收06G，不新增成长票。',
 'N02':'独立形成待审主张，证据与尾部风险分列；吸收E06，不作收益赞成票。',
 'N03':'同一经济对象和预测终点的新增证据及预期修订，非静态成长榜。',
 'N06':'前沿机制、24至60个月经营与稀释后价值，单独判断3/6个月参与理由。',
 '09':'价格弹性限定实验；公司经营及估值独立建模，价格门槛与权重保持。',
 'N05':'市场状态限定实验；独立公司模型，明确原始价格/同口径IV覆盖与中性回退。'
}
fields,rows=readcsv(S/'00_待运行研究方案注册表.csv')
absorptions={'04':('01','U01'),'E04':('01','U01'),'E05':('01','U01'),'E06':('N02','U08')}
clear=['version_id','prompt_file','expected_output_dir','expected_output_file','sha256','base_method_id','input_set','control_prompt_file','control_expected_output_file','control_sha256']
for r in rows:
 mid=r['method_id']
 if mid in byid:
  s=byid[mid]
  r.update(method_name=s['name'],lifecycle='常规研究：未验证' if s['mode']=='routine' else '实验：暂停常规运行',
    plan_status='待运行_未验证' if s['mode']=='routine' else '仅显式实验运行_新版本未运行',
    version_id=s['version'],prompt_file=s['prompt'],expected_output_dir=s['output'].rsplit('/',1)[0],
    expected_output_file=s['output'],sha256=sha(ROOT/s['prompt']),note=roles[mid],
    execution_mode=s['mode'],execution_unit=s['unit'],absorbed_by='',base_method_id='',input_set='BCDE',
    control_prompt_file='',control_expected_output_file='',control_sha256='')
 elif mid in absorptions:
  dest,unit=absorptions[mid]
  for f in clear:r[f]=''
  r.update(lifecycle='已并入：停止独立运行',plan_status='已并入_无独立入口',execution_mode='absorbed',
    execution_unit=unit,absorbed_by=dest,
    note='职责并入'+unit+'；旧方案、已完成结果及回测留原路径，新任务使用公司调研独立输入。')
writecsv(S/'00_待运行研究方案注册表.csv',fields,rows)
sf,sr=readcsv(S/'00_方案状态总表.csv')
for r in sr:
 mid=r['method_id']
 if mid in byid:
  s=byid[mid]
  r['status']='常规研究：待新结果验证' if s['mode']=='routine' else '实验：暂停常规运行'
  r['role']=roles[mid]
  r['next_action']='使用待运行注册表中的'+s['unit']+'公司调研输入新入口；本行历史结果、收益及时间不归属于新版本。'
 elif mid=='04':
  r['status']='已并入：停止独立运行'
  r['role']='极简基准判断并入U01；本行结果及收益仅为历史证据。'
  r['next_action']='不再独立入队或计票；使用U01双判断新方案，原研究方案和结果保留。'
writecsv(S/'00_方案状态总表.csv',sf,sr)
pf,pr=readcsv(S/'00_站点发布策略.csv')
for r in pr:
 if r['method_id']=='04':
  r.update(site_publish='false',site_group='不发布',site_default='false',consensus_eligible='false',
   evidence_label='职责合并；旧结果留存',reason='极简基准职责并入U01，撤回独立公开和重复计票；历史结果保留，新版本未运行。')
 elif r['method_id']=='06':
  r.update(site_group='历史候选',site_default='false',consensus_eligible='false',
   evidence_label='历史三视图；新入口未运行',reason='旧06F/G/E仅作历史展示；未来06只研究事件，F/G职责并入U01/U07，旧三视图不继续作为独立收益共识。')
writecsv(S/'00_站点发布策略.csv',pf,pr)
print(json.dumps({'routine':sum(r['execution_mode']=='routine' for r in rows),'experiment':sum(r['execution_mode']=='experiment' for r in rows),'paired':sum(r['execution_mode']=='paired_experiment' for r in rows),'active_prompts':sum(bool(r['prompt_file']) for r in rows)},ensure_ascii=False))

