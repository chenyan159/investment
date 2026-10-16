import json,pathlib,re,csv,hashlib,datetime
R=pathlib.Path(__file__).resolve().parents[1]
def read(p): return json.loads((R/p).read_text(encoding='utf-8-sig'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def ck(name,ok,detail=None): checks.append(dict(check=name,ok=bool(ok),detail=detail))
doc=(R/'06_final/最终20家公司超高收益研究.md').read_text(encoding='utf-8')
final=read('06_final/最终20家公司完整卡.json');cards=final['companies'];tickers=[x['decision']['ticker'] for x in cards]
u=read('01_inputs/universe.json');u={x['ticker']:x for x in u}
model=read('04_verification/V2_models.json');m={x['ticker']:x for x in model['companies']}
chair=read('05_chair/主席裁决.json');audit=read('04_verification/控制器_模型独立复算.json')
ck('final20_unique_in_universe',len(tickers)==20 and len(set(tickers))==20 and set(tickers)<=set(u))
ck('chair_sealed','DRAFT' not in chair['status'] and not chair.get('pending'))
ck('chair_order_matches',[x['ticker'] for x in chair['final20']]==tickers)
ck('ranks_contiguous',[x['decision']['rank'] for x in cards]==list(range(1,21)))
ck('model_independent_audit_hash',audit['model_sha256']==digest(R/'04_verification/V2_models.json'))
ck('model_independent_audit_passed',audit['checks']==1120 and not audit['failures'])
ck('model_38x4',len(m)==38 and all(len(x['scenario_inputs'])==4 for x in m.values()))
for path,expected in chair['input_hashes'].items(): ck('chair_input_hash_'+path,digest(R/path)==expected)
for x in cards:
    t=x['decision']['ticker'];cov=x['role_coverage']
    ck(t+'_multi_role',all(cov[k] for k in ['B1','B2','V1','V2']) and (cov['S1'] or cov['S2'] or t=='ADBE'))
    ck(t+'_price_anchor',abs(m[t]['price']-float(u[t]['finance']['最新价格'].replace(',','')))<1e-9)
    ck(t+'_primary_source',len(x['facts']['source_urls'])>=1 and x['facts']['independent_access']=='original_primary_relevant_sections')
    ck(t+'_alternative_and_invalidation',bool(x['decision'].get('alternative')) and bool(x['decision'].get('invalidator')))
    ck(t+'_four_prices_match_chair',all(abs(a['price']-b['result']['price'])<1e-8 for a,b in zip(x['decision']['scenario_summary'],m[t]['scenario_inputs'])))
ck('20_markdown_cards',len(re.findall(r'^## \d+\. [A-Z]+ ',doc,re.M))==20)
ck('no_internal_web_citations',not re.search(r'cite|turn\d+(?:search|view)',doc))
broken=[]
for target in re.findall(r'\]\(([^\n]+?)\)',doc):
    if re.match(r'[A-Za-z]:/',target) and not pathlib.Path(target).exists(): broken.append(target)
ck('local_report_links_exist',not broken,broken)
trajectory=read('06_final/245家公司筛选轨迹.json')
ck('245_unique_trajectory',len(trajectory)==245 and len({x['ticker'] for x in trajectory})==245)
ck('trajectory_final20',set(x['ticker'] for x in trajectory if x['final_rank'])==set(tickers))
with (R/'06_final/最终20家公司数值总表.csv').open(encoding='utf-8-sig',newline='') as f: table=list(csv.DictReader(f))
ck('csv20_order',len(table)==20 and [r['代码'] for r in table]==tickers)
for row in table:
    t=row['代码'];ck(t+'_csv_success_price',abs(float(row['强成功价'])-m[t]['scenario_inputs'][2]['result']['price'])<0.000051)
with (R/'06_final/未来回溯模板.csv').open(encoding='utf-8-sig',newline='') as f: table=list(csv.reader(f))
ck('followup_template_shape',len(table)==21 and len(set(map(len,table)))==1)
prev=read('00_control/preservation_audit.json')
ck('preservation_no_differences',all(x.get('differences') in ([],0) for x in prev.values() if isinstance(x,dict) and 'differences' in x))
ck('preservation_expected_counts',prev['previous_experiment']['checked']==1321 and prev['frozen_core']['checked']==945 and prev['frozen_extra']['checked']==200 and prev['sealed_round1']['checked']==25)
report=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=len(checks),failures=[x for x in checks if not x['ok']],details=checks,limitations='Content/coverage/price/model/link checks; not predictive accuracy or complete financing audit.')
(R/'06_final/最终交付校验.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='details'},ensure_ascii=False))
if report['failures']: raise SystemExit(1)
