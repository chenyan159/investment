from pathlib import Path
import csv,json,hashlib
ROOT=Path('D:/drive/Investment'); SORT=ROOT/'分析报告/公司排序'; OUT=Path(__file__).resolve().parent
m=json.loads((OUT/'新方案清单.json').read_text(encoding='utf-8'))
def read(name):
 with (SORT/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write(name,rows):
 with (SORT/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def text(name,body):
 p=SORT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body,encoding='utf-8')
regular=['01','02','04','06','07','N02','N03','N06']; experimental=['09','N05']
absorbed={'03':'N02','05':'N02','08':'N02','N01':'01','N04':'07'}
names={'01':'赔率与基准承载','02':'预期兑现','04':'极简基准兑现','06':'价值成长事件三视图','07':'收入台阶与现金转化','N02':'证据与经济风险审查','N03':'预期差增量','N06':'早期非线性成长'}
unit={'01':'U01','02':'U02','04':'U04','06':'U06','07':'U07','N02':'U08','N03':'U09','N06':'U10'}
roles={'01':'共享经营与价值模型，保留赔率和基准承载两种判断，不平均投票。','02':'独立判断市场预期与具体兑现条件。','04':'保留简单基准检验复杂度增量。','06':'一份研究三种视图，同一家族只计一次。','07':'共用收入桥，保留收入跃迁与现金每股价值两种判断。','N02':'联合审查证据与经济坏路径，吸收03/05/08；不产生收益赞成票。','N03':'识别可比时点的真实新增证据及预期差。','N06':'发现早期非线性成长并解释3/6个月参与理由。'}
pending=read('00_待运行研究方案注册表.csv')
for r in pending:
 k=r['method_id'];r.update(execution_mode='historical',execution_unit='',absorbed_by='',base_method_id='',input_set='',control_prompt_file='',control_expected_output_file='',control_sha256='')
 if k in regular:
  r.update(execution_mode='routine',execution_unit=unit[k],lifecycle='常规研究：未验证',plan_status='待运行_未验证',note=roles[k],input_set='ABCDE')
  if k in m['merged']:
   r.update(m['merged'][k]);r['version_id']=Path(r['expected_output_dir']).name
 elif k in experimental:
  r.update(execution_mode='experiment',lifecycle='实验：暂停常规运行',plan_status='仅显式实验运行',note='不自动进入常规批次或收益共识；旧版本原样保留。',input_set='ABCDE')
 elif k in absorbed:
  target=absorbed[k];r.update(execution_mode='absorbed',execution_unit=unit[target],absorbed_by=target,lifecycle='已并入：停止独立运行',plan_status='已并入_无独立入口',note=f'职责并入{unit[target]}；历史方案留原路径，未运行旧方案不再作为默认入口。')
  for field in ['version_id','prompt_file','expected_output_dir','expected_output_file','sha256']:r[field]=''
for e in m['experiments']:
 r={k:'' for k in pending[0]};r.update(method_id=e['experiment_id'],method_name=e['label']+'输入隔离',lifecycle='输入对照：待验证',plan_status='成对方案已创建_未运行',version_id='R01_2026-09-08_输入隔离',execution_mode='paired_experiment',base_method_id=e['base_method_id'],input_set='BCDE',note='独立版与ABCDE对照版必须同截止、公司池、价格、模型设置和资源预算；实验不重复投票。',**e['BCDE'])
 r.update(control_prompt_file=e['ABCDE']['prompt_file'],control_expected_output_file=e['ABCDE']['expected_output_file'],control_sha256=e['ABCDE']['sha256'])
 pending.append(r)
write('00_待运行研究方案注册表.csv',pending)
byid={r['method_id']:r for r in pending}

state=read('00_方案状态总表.csv')
for r in state:
 k=r['method_id']
 if k in regular:r.update(status='常规研究：待新结果验证',role=roles[k],next_action='使用待运行注册表中的'+unit[k]+'入口；旧结果和旧回测不绑定到新方案。')
 elif k in absorbed:r.update(status='已并入：停止独立运行',role='职责并入'+unit[absorbed[k]]+'；旧结果仅作历史追溯。',next_action='不再独立入队或投票，原研究方案与结果保持只读。')
 elif k in experimental:r.update(status='实验：暂停常规运行',role='保留限定实验，不参与常规收益共识。',next_action='仅在明确实验批次按原规则开展，独立检验增量。')
write('00_方案状态总表.csv',state)
registry=read('00_运行与榜单注册表.csv')
for r in registry:
 k=r['method_id']
 if k in regular:r.update(lifecycle='常规职责；此行为历史结果',status='旧结果留存；新入口待验证',role=roles[k])
 elif k in absorbed:r.update(lifecycle='已并入：历史结果',status='停止独立运行与投票',role='当前职责并入'+unit[absorbed[k]]+'；此行只绑定原始旧结果。')
 elif k in experimental:r.update(lifecycle='实验：历史结果',status='暂停常规运行',role='仅供实验及历史比较，不作常规收益支持票。')
write('00_运行与榜单注册表.csv',registry)
policy=read('00_站点发布策略.csv')
for r in policy:
 k=r['method_id']
 if k in absorbed or k in experimental or k=='N02':
  r.update(site_publish='false',site_group='不发布',site_default='false',consensus_eligible='false',reason='独立职责已并入联合研究/审查或仅保留实验；不再公开旧独立收益名次或重复计票。')
  r['evidence_label']='职责调整；旧结果留存'
 if k=='01':r.update(site_default='true',reason=r['reason']+' 原默认05停止独立发布后，改用01旧榜作为展示默认；不代表新方案已有结果。')
write('00_站点发布策略.csv',policy)

lines=['# 公司排序方案总索引','','当前执行安排：2026-09-08。8个常规研究单元、09/N05两个限定实验、E04—E06三组成对输入实验。常规是研究安排，不代表方法已获得有效性证明。','',
'## 当前执行入口','',
'[待运行研究方案注册表](00_待运行研究方案注册表.csv)是未来任务配置入口。只按execution_mode选择批次，禁止遍历所有非空prompt_file直接运行。routine恰好8行；experiment为09/N05；paired_experiment为E04—E06；absorbed和historical禁止默认入队。该表不证明已有结果，也不自动写队列。','',
'|单元|负责人代号与职责|当前方案|状态|','|---|---|---|---|']
for k in regular:
 r=byid[k];rel=Path(r['prompt_file']).relative_to('分析报告/公司排序').as_posix()
 lines.append(f'|{unit[k]}|{k} {names[k]}|[研究方案]({rel})|未运行；未验证|')
lines+=['','## 职责收拢','','- N01并入U01，保留基准承载对照判断。','- N04并入U07，保留现金转化判断。','- 03/05/08与N02统一到U08；证据与经济风险结论分列，不是收益榜。','- 09、N05暂停常规执行，保留显式实验入口。','- 原目录与旧版全文留原路径，避免破坏历史绝对路径及兼容junction；旧目录名称不是当前状态。原始文件不做覆盖或迁移。','','## BCDE独立输入实验','','选择01、04、N02是因为此前39个收益区间、两种起点的旧Top30收益均位列前三，不代表新方法已有效。每组各有ABCDE与BCDE完整方案，研究规则一致；只允许A输入权限有差异。N02保持生存审查排序，不改成上涨预测。','', '|实验|方法|ABCDE对照|BCDE独立|','|---|---|---|---|']
for e in m['experiments']:
 a=Path(e['ABCDE']['prompt_file']).relative_to('分析报告/公司排序').as_posix();b=Path(e['BCDE']['prompt_file']).relative_to('分析报告/公司排序').as_posix()
 lines.append(f'|{e["experiment_id"]}|{e["base_method_id"]} {e["label"]}|[对照方案]({a})|[独立方案]({b})|')
lines+=['','执行与比较规则见[当前使用说明](91_通用研究方案/2026-09-08_八单元与输入隔离使用说明.md)。E01—E03是七月历史输入扩展实验，不因建立新实验而重启。','','## 结果、证据与公开契约','','- [运行与榜单注册表](00_运行与榜单注册表.csv)继续绑定26个历史方法、28张真实旧榜。未把新方案绑定旧结果，也未创建空结果。','- [方案状态总表](00_方案状态总表.csv)记录当前职责，原有回测数值仍保持原值和时间。','- [当前正式评估指针](00_当前评估.json)保持原评估包，不能将其旧指标归到9月新方案。','- [站点发布策略](00_站点发布策略.csv)取消03/05旧独立榜公开和计票，默认展示由05切换01；旧公开共识保留01/02/04/06/07五个家族，06仍只算一票。联合审查及输入实验不入收益共识。','- [站点数据](站点数据/current.json)由本目录生成器编译；本次不部署网站。新产物需先适配实际合格集、NA、条件选择和多视角语义，不能直接填进旧192行排名解析器。','',
'历史依据及本次改动明细见[实施报告](../../备份/排序八单元与BCDE对照实施_2026-09-08/00_实施报告.md)。所有历史研究全文、结果和效果证据保留，不因为目录收拢被删除。','']
text('00_总索引.md','\n'.join(lines))
instructions='''# 八单元与输入隔离执行说明

## 选择任务

以00_待运行研究方案注册表.csv为准。execution_mode=routine的8行构成常规批次；experiment仅09/N05；paired_experiment为E04—E06，每行含两份方案。absorbed和historical不默认运行。不要按目录名称、方法代号是否以N开头、prompt_file是否非空推断执行身份。保持file-run通用执行，不增加domain或排序包装方案。

常规单元可从该行prompt_file、expected_output_dir、expected_output_file创建任务。成对实验使用该行BCDE的prompt_file，以及control_prompt_file指向的ABCDE对照；control_expected_output_file指定对照输出，其父目录即对照expectedOutputDir。运行ID包含实验、输入组和版本。当前只准备方案，没有入队，没有生成研究结果。

每次实际研究均用未被占用的独立版本目录；已有结果不得覆盖。新结果通过内容验收后才更新真实运行注册，不能将新方案版本与七月旧结果拼接。03/05/N01/N04/08只保留历史复现，常规入口已移入对应单元。

## 成对输入对照

E04=01风险调整赔率，E05=04极简基准兑现，E06=N02尾部生存。三组均以9月7日相应规则为固定方法基线，不以新U01的双判断与旧01比较，也不以U08联合审查代替N02单独实验，避免同时改变方法与输入。正文已完整展开，不读取旧方案补规则。

两组共享B/C/D/E允许范围、公司池、截止T、价格主快照和证券口径，使用相同模型版本、推理设置、时间及计算预算。预先冻结这些设置和可得来源目录/快照清单，记录精确文件版本/校验值，不向某一组单独补事后证据。按各自提示允许独立选择相关证据，不要求实际阅读顺序相同；记录实际来源及覆盖差异。共同输入的修订必须同时新建两组版本。

ABCDE额外允许读取A中的经营事实和情景模型，但不直接照抄投资建议；BCDE全程排除A及其模型/建议的间接转述。因此实验检验的是A提供的分析模型是否有增量，不是允许对照组无条件复制评级。两版仅输入节第3条及唯一输出路径不同，其余正文逐字一致。

每组必须在隔离的新研究上下文执行，不能先读A后在同一会话改称BCDE；不得给独立组传递对照组结果、摘要、名次或模型。两份输出完成冻结之前不互相查看。输入血缘审计不是已证明无污染；若模型实际读到受禁建议，标记实验污染，不能用于输入独立性结论。相同设置仍有随机性；一对结果只能提供初步诊断，不把差异全部归因于输入。必要的重复实验必须预先规定轮次和预算，不追跑到满意为止。

## 比较与下游

完成后由独立评估读取两份冻结产物：先看事实错误、缺失和独立经营模型差异，再比较3/6个月研究顺序、Top20/30重合与独有候选、真实合格集、条件入场、来源覆盖、耗时和成本。不得把未合格者填满Top30。对不同意见沿来源→假设→经营/价值桥→门槛→选择追溯，区分A帮助补事实、提供有用模型、继承过度乐观、同源重复确认等机制。

E06的生存分和审查顺序不是收益名次；评估坏路径识别、误拒成长、原合格集变化，并另列防守次序与实际收益/损失关系，不能与买入组合混为一个指标。U08联合审查也不进入收益共识。U01/U07双判断和06三视图是家族内对照，不多计票。

生成后使用各公司可确认复权价，统一可交易入场时点、成本假设、3个月及6个月窗口；列SPY/QQQ/SOXX及同公司池，逐股贡献、回撤和错过赢家同时披露。旧七月至九月数据已用于选方法，不能再当新方案样本外证据。新方案现在没有成绩。

历史26方法/28榜继续使用现有结果注册与站点契约；新实验只登记未来入口。新结果需先适配研究身份、合格集、NA、审查和多视角语义，不能通过补192个名次直接混入旧榜。站点仅消费生成后的站点数据/current.json，不扫描新方案目录。
'''
text('91_通用研究方案/2026-09-08_八单元与输入隔离使用说明.md',instructions)
old_use=(SORT/'91_通用研究方案/2026-09-07_新方案使用说明.md').read_text(encoding='utf-8')
text('91_通用研究方案/2026-09-07_新方案使用说明.md','> 历史说明：本页的15份默认批次已由[当前八单元与输入隔离说明](2026-09-08_八单元与输入隔离使用说明.md)替代。不要按本页旧批次创建当前任务。\n\n'+old_use)
old_readme=(SORT/'07_输入扩展对照方案_待验证/README.md').read_text(encoding='utf-8')
text('07_输入扩展对照方案_待验证/README.md','# 输入对照实验管理\n\n当前新增E04—E06为ABCDE/BCDE隔离实验，各含两份完整方案，未运行、不投票。入口见[总索引](../00_总索引.md)，执行规则见[当前说明](../91_通用研究方案/2026-09-08_八单元与输入隔离使用说明.md)。E01—E03及下文旧路径、限制仅解释七月历史实验，不是当前输入契约。\n\n## 七月历史管理说明\n\n'+old_readme)
agents=(SORT/'AGENTS.md').read_text(encoding='utf-8')
agents=agents.replace('当前目录结构于 2026-07-12 重构。','历史目录结构保留用于追溯；当前执行身份以待运行注册表的execution_mode和总索引为准。')
pos=agents.index('## 入口与状态')
agents=agents[:pos]+'''## 当前运行职责

- 8个常规单元以00_待运行研究方案注册表.csv的execution_mode=routine为准；常规不表示收益有效，也不自动获得投票资格。
- 08_常规研究单元/保存U01双判断、U07双判断、U08联合审查的新正文；其余五个单元直接使用注册的完整方案。
- 03/05/08/N01/N04的独立入口已撤回，旧目录及全文仍在原路径只读保留。absorbed不入默认批次。原目录名、旧索引和历史运行的is_current不决定新任务执行身份。
- 09/N05仅experiment；E04—E06为paired_experiment，每行含BCDE入口与ABCDE对照。E01—E03只留历史，不默认重启。
- E04—E06是输入实验身份，不新增独立方法票。不得将其放进尚未生成结果的运行与榜单注册表。控制组与独立组必须隔离上下文、冻结同批输入和相同研究资源设置。
- 新研究优先用91_通用研究方案/2026-09-08_八单元与输入隔离使用说明.md。下列旧分区保留导航用途，遇当前执行身份冲突时以前述注册字段为准。

'''+agents[pos:]
agents=agents.replace('N01–N06候选方法及其当前运行；已有结果但尚无当前版本生成后的独立样本，不属于现役方法，不参与投票。','N01–N06的历史目录；当前独立运行、合并与实验身份见待运行注册表，新结果未验证不自动投票。')
agents=agents.replace('E01–E03输入A/B对照方案及其当前运行','E01–E03历史输入扩展及E04–E06输入隔离方案')
text('AGENTS.md',agents)
print(json.dumps({'routine':sum(r['execution_mode']=='routine' for r in pending),'experiment':sum(r['execution_mode']=='experiment' for r in pending),'paired_experiment':sum(r['execution_mode']=='paired_experiment' for r in pending),'absorbed':sum(r['execution_mode']=='absorbed' for r in pending),'historical_result_rows':len(registry),'site_consensus':[r['method_id'] for r in policy if r['consensus_eligible']=='true']},ensure_ascii=False))
