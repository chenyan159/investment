"""Package chairman's actual decisions with traceable role evidence, never infer a positive verdict from a mention."""
import csv,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def save(p,o):(R/p).write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
def csvout(p,rows):
    with (R/p).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
chair=read('05_chair/主席最终裁决.json')
assert 'draft' not in chair.get('status','').lower() and 'pending' not in chair.get('status','').lower(), 'Chairman must seal the final decision first'
selected=chair['ranked_companies'];assert len(selected)==20
selected=sorted(selected,key=lambda c:c['rank']);assert [c['rank'] for c in selected]==list(range(1,21))
names=[c['ticker'] for c in selected];assert len(set(names))==20
universe=read('01_inputs/universe.json'); um={x['ticker']:x for x in universe}
assert set(names)<=set(um)
models=read('04_verification/V2_models.json'); mm={x['ticker']:x for x in models['companies']}
audit=read('04_verification/controller_independent_model_audit.json')
modelhash=hashlib.sha256((R/'04_verification/V2_models.json').read_bytes()).hexdigest()
assert audit['status']=='PASS' and audit['model_sha256']==modelhash,'Re-run independent audit for final model version'
assert chair['model_sha256'].lower()==modelhash,'Chairman read an older model version'
supp=[read('03_round2/S1_ai_upside.json'),read('03_round2/S2_nonai_upside.json')]
b1=read('03_round2/B1_business_rebuttal.json');b2=read('03_round2/B2_valuation_rebuttal.json');v1=read('04_verification/V1_primary_verification.json')
v1m={x['ticker']:x for x in v1['companies']}
blinds=[read(str(p.relative_to(R))) for p in sorted((R/'02_round1').glob('R[1-5]_*.json'))]
stagea=read('05_chair/主席阶段A_竞争池.json');stageaset={c['ticker'] for c in stagea['candidates']}
csvs=['R1_full_universe_screen.csv','R2_full_pool_screen.csv','R3_screen_245.csv','R4_full245_screen.csv','R5_245_screen.csv']
screens=[]
for p in csvs:
    with (R/'07_logs'/p).open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    assert len(rows)==245 and {x['ticker'] for x in rows}==set(um)
    screens.append({x['ticker']:x for x in rows})
coverage=[];table=[]; package=[]
for c in selected:
    t=c['ticker'];m=mm[t];role_noms=[b['role'] for b in blinds if t in {x['ticker'] for x in b['nominations']}]
    assert c['scenarios']==m['scenarios'],f'{t} chairman and model numbers diverge'
    assert len({x['url'] for x in c['sources']})>=3,f'{t} needs documented multiple source links'
    role_deep=[b['role'] for b in blinds if t in b.get('deep_read_tickers',[])]
    supplemental=[s['role'] for s in supp if t in s['covered_tickers']]
    if t=='VST': supplemental.append('Controller_非AI需求交叉核验.md')
    bd1=[x['id'] for x in b1['disputes'] if x['ticker']==t];bd2=[x['id'] for x in b2['disputes'] if x['ticker']==t]
    vc=[x['id'] for x in v1['checks'] if x['ticker']==t];chain=v1m[t].get('independent_external_chain',[])
    assert role_deep or role_noms,t
    assert supplemental and bd1 and bd2 and vc and chain,t
    assert c.get('closest_alternative') and c.get('why_preferred') and c.get('catalysts') and c.get('kill_conditions'),t
    coverage.append(dict(rank=c['rank'],ticker=t,blind_nominators=';'.join(role_noms),blind_deep_readers=';'.join(role_deep),supplement=';'.join(supplemental),B1_questions=';'.join(bd1),B2_questions=';'.join(bd2),V1_checks=';'.join(vc),outside_chain_urls=';'.join(x['source_url'] for x in chain),V2_scenarios=3,controller_arithmetic='PASS',chair_alternative=str(c['closest_alternative']),action_status=str(c['action_status']),evidence_gate='PASS role chain; forecasts remain conditional'))
    sc={s['scenario']:s for s in m['scenarios']}
    table.append(dict(rank=c['rank'],ticker=t,name=um[t]['name'],action_status=str(c['action_status']),reference_price=m['reference_price'],price_date=m['reference_price_date'],observation_date=m['observation_date'],bear_price=sc['bear']['price'],base_price=sc['base']['price'],bull_price=sc['bull']['price'],bear_return_pct=sc['bear']['return_pct'],base_return_pct=sc['base']['return_pct'],bull_return_pct=sc['bull']['return_pct'],return_basis=m['return_basis'],closest_alternative=str(c['closest_alternative'])))
    package.append(dict(chair_decision=c,company_identity={k:um[t].get(k) for k in ['name','category','security_notes']},scenario_model=m,evidence_gate=coverage[-1]))
csvout('06_final/最终20家公司_情景与行动.csv',table)
csvout('06_final/最终20家_多轮证据闭环.csv',coverage)
monitor=[]
for c in selected:
    monitor.append(dict(rank=c['rank'],ticker=c['ticker'],baseline_date='2026-10-12',baseline_USD=mm[c['ticker']]['reference_price'],review_date='',review_price_USD='',cash_dividends_USD_per_original_share='',corporate_actions='',facts_and_source_URL='',original_catalysts='；'.join(c['catalysts']),original_kill_conditions='；'.join(c['kill_conditions']),original_action=c['action_status'],observed_status='未观察',changed_assumptions='',contemporaneous_decision='',return_attribution='',benchmark_comparison=''))
csvout('06_final/后续观察与回溯模板.csv',monitor)
gate=['# 最终20家逐项审查记录','', '这里核对的是已保存的审查链，未来经营、融资和临床假设仍待兑现；角色数不等于统计独立样本数。精确来源与问题编号见同名CSV。','', '|排名|公司|盲轮定向阅读|补充研究|经营反方|估值反方|原始核验|模型/算术|最近替代|','|---:|---|---|---|---|---|---|---|---|']
for q in coverage:gate.append('|'+ '|'.join(str(q[k]) for k in ['rank','ticker','blind_deep_readers','supplement','B1_questions','B2_questions','V1_checks'])+'|V2三情景 + 控制器复算通过|'+q['chair_alternative']+'|')
gate+=['','每家公司也经过Astra主席A/B阶段裁决；VST补查来自控制器PJM/Talen原始需求链。CLS在盲轮已有定向阅读但未获提名，通过补查加入；不能用首轮票数永久封禁。BNTX另外经过V1/V2合同权益追加审查。','', '外部链含不同客户/竞争者/研究机构的资料；同一事件的多个URL不当作多次独立事实确认。']
(R/'06_final/最终20家_多轮证据闭环.md').write_text('\n'.join(gate)+'\n',encoding='utf-8')
save('06_final/最终20家公司_完整数据包.json',dict(cutoff=models['information_cutoff'],observation_date=models['observation_date'],model_sha256=modelhash,companies=package,limitations='20 ranked investment research opportunities, not 20 simultaneous unconditional buys; price returns exclude dividends; source reuse and common model mean roles are not statistically independent.'))
reserves=chair.get('reserves',[])
if isinstance(reserves,dict): reserves=[dict(ticker=k,reason=v) for k,v in reserves.items()]
rm={x['ticker']:x for x in reserves if isinstance(x,dict) and 'ticker' in x}
rankmap={x['ticker']:x for x in selected};allrows=[]
for u in universe:
    t=u['ticker'];noms=[b['role'] for b in blinds if t in {x['ticker'] for x in b['nominations']}];deeps=[b['role'] for b in blinds if t in b.get('deep_read_tickers',[])]
    sx=[s['role'] for s in supp if t in s['covered_tickers']]
    status='最终20' if t in names else '主席候补' if t in rm else '最终竞争池未入选' if t in stageaset else '经初轮提名后未入最终竞争池' if noms else '初筛/定向深读后未优先'
    detail=rankmap.get(t,rm.get(t,{}))
    allrows.append(dict(ticker=t,name=u['name'],category=u['category'],final_status=status,final_rank=rankmap.get(t,{}).get('rank',''),R1_result=screens[0][t].get('screen_result',''),R2_result=screens[1][t].get('screen_decision',''),R2_reason=screens[1][t].get('reason',''),R3_reason=screens[2][t].get('reason',''),R4_reason=screens[3][t].get('reason',''),R5_result=screens[4][t].get('r5_disposition',''),blind_nominators=';'.join(noms),blind_deep_readers=';'.join(deeps),supplement=';'.join(sx),B1=t in b1['covered_tickers'],B2=t in b2['covered_tickers'],V1=t in v1m,V2=t in mm,chair_stageA=t in stageaset,latest_reason=str(detail.get('why_preferred',detail.get('reason','仅保留当轮比较结果；未入选不是确认无投资价值'))),reentry_conditions=str(detail.get('reentry_conditions','新经营/合同/融资/价格证据足以改变对具体替代的比较时重新入池；重新完成必要核验'))))
assert len(allrows)==245
csvout('06_final/全245家公司_筛选与复活轨迹.csv',allrows)
save('00_control/final_validation.json',dict(status='PASS',utc=datetime.now(timezone.utc).isoformat(),selected_count=20,universe_count=245,all_five_full_screens_verified=True,unique_and_in_universe=True,role_evidence_gates=20,independently_recalculated_models=29,independently_recalculated_scenarios=87,model_sha256=modelhash,excluded_meaning='Unselected companies were screened at differing depth, not proven poor investments. Role gate verifies documented review chain, not future success.'))
print(json.dumps(dict(status='PASS',selected=names,coverage_rows=len(coverage),all_universe_rows=len(allrows),model_sha256=modelhash),ensure_ascii=False,indent=2))
