from pathlib import Path
import json,re
P=Path(__file__).parent
def vals(s):return [float(x) for x in re.findall(r'\d+(?:\.\d+)?',s)]
params={
'HBF':{'悲观':[.07,.13,.12,.13,.07,.08],'基准':[.18,.07,.23,.08,.04,.04],'乐观':[.28,.04,.35,.04,.025,.025],'突破':[.36,.02,.45,.025,.02,.015]},
'Matrix':{'悲观':[.025,.15,.08,.15,.08,.08],'基准':[.075,.11,.15,.12,.06,.06],'乐观':[.14,.08,.25,.08,.04,.04],'突破':[.22,.05,.35,.05,.025,.025]}}
rows=[];group=None;states={}
lines=(P/'报告快照'/'SNDK.md').read_text(encoding='utf-8-sig').split('\n')
for i,l in enumerate(lines,1):
    if l.startswith('#### HBF：'):group='HBF'
    elif l.startswith('#### 3D Matrix：'):group='Matrix'
    if not (374<=i<=460 and l.startswith('|')):continue
    c=[x.strip() for x in l.strip().strip('|').split('|')]
    if len(c)!=10 or c[0] not in params['HBF'] or not c[1].isdigit():continue
    scenario=c[0];year=int(c[1]);key=(group,scenario)
    prev=states.get(key,[1,0,0,0]);a,b,cc,d,e,f=params[group][scenario]
    if group=='HBF' and year==2027:cc=0
    if group=='Matrix' and year in [2027,2028]:a=0
    if group=='Matrix' and year==2029:cc=0
    n,part,scale,fail=prev
    curr=[n*(1-a-b),n*a+part*(1-cc-d)+scale*e,part*cc+scale*(1-e-f),fail+n*b+part*d+scale*f]
    states[key]=curr
    declared=vals(c[2]);revenue=vals(c[3]);expected=float(c[4])
    state_error=max(abs(p*100-q) for p,q in zip(curr,declared))
    calculated=curr[1]*revenue[0]+curr[2]*revenue[1]
    revenue_error=abs(calculated-expected)
    rows.append(dict(subject='SNDK',opportunity=group,scenario=scenario,year=year,line=i,
        probability_sum_display=sum(declared),max_state_error_pp=state_error,
        expected_revenue=expected,calculated_revenue=calculated,revenue_error=revenue_error,
        passed=state_error<=.051 and revenue_error<=.0011))

weights={'悲观':[.05,.10,.25,.60],'基准':[.20,.25,.25,.30],'乐观':[.40,.30,.20,.10],'突破':[.60,.25,.10,.05]}
lw=[]
for i,l in enumerate((P/'报告快照'/'LWLG.md').read_text(encoding='utf-8-sig').split('\n'),1):
    if not 173<=i<=212:continue
    c=[x.strip() for x in l.strip().strip('|').split('|')]
    s,y=c[0].split('/');r=vals(c[2]);calc=sum(a*b for a,b in zip(weights[s],r));reported=float(c[-1])
    probs=vals(c[1]);error=abs(calc-reported)
    lw.append(dict(subject='LWLG',scenario=s,year=y,line=i,probability_sum_display=sum(probs),
        expected_revenue=reported,calculated_revenue=calc,revenue_error=error,passed=abs(sum(probs)-100)<.01 and error<=.015))
result=dict(sndk_count=len(rows),sndk_fail=[r for r in rows if not r['passed']],lwlg_count=len(lw),lwlg_fail=[r for r in lw if not r['passed']],
            important_reading_note='LWLG table 3.4 shows annual U/P/S/X marginal probabilities beside E/L/N/F branch revenues. Expected revenue must use fixed branch weights from table 3.2; these adjacent columns cannot be multiplied positionally.',rows=rows+lw)
(P/'probability_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False,indent=2))
