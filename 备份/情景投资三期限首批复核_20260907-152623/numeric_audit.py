from pathlib import Path
import json, re, math

B = Path(__file__).parent
PRICES = dict(GNRC=187.35, MU=1016.59, LWLG=5.35, BE=252.87, SNDK=1740)
NUM = re.compile(r'[+-]?\d[\d,]*(?:\.\d+)?')
def ns(x): return [float(v.replace(',', '')) for v in NUM.findall(x)]
def cells(l): return [x.strip() for x in l.strip().strip('|').split('|')]
def precision(x):
    s=NUM.findall(x)[0]
    return 0.5*10**(-len(s.split('.')[1])) if '.' in s else 0.5
out={'scope':'Rounded report arithmetic, equity/share bridges, selected independent valuations. Does not establish forecast truth or reproduce every quarterly DCF.', 'reports':{}, 'independent_models':{}}
for t,p in PRICES.items():
    a=(B/f'{t}_新报告.md').read_text(encoding='utf-8-sig').splitlines()
    detail=[]
    for i,l in enumerate(a,1):
        c=cells(l)
        if len(c)==10 and '个月' in c[1] and '202' in c[1] and '%' in c[5]:
            detail.append((i,c))
    assert len(detail)==12,(t,len(detail))
    start,end,col,factor={'GNRC':(271,282,4,1000),'MU':(289,300,5,1),'LWLG':(383,394,5,1),'BE':(325,336,6,1000),'SNDK':(479,490,8,1000)}[t]
    fd=[ns(cells(l)[col]) for l in a[start-1:end]]
    checks=[]
    for j,(line,c) in enumerate(detail):
        pv,ret,eq=ns(c[4])[:2],ns(c[5])[:2],ns(c[3])[:2]
        div=([0.3,0.6,1.8][j%3] if t=='MU' else 0)
        expected=[100*((v+div)/p-1) for v in pv]
        rtol=.050001+precision(c[4])/p*100
        share=fd[j] if len(fd[j])==2 else fd[j]*2
        implied=[eq[k]*factor/share[k] for k in range(2)]
        eqtol=precision(c[3])*factor/min(share)+precision(c[4])+max(pv)*precision(a[start-1+j].split('|')[col+1])/min(share)
        checks.append({'line':line,'scenario':c[0],'horizon':c[1], 'rating':c[6], 'prices':pv,'returns':ret,
                       'return_error_pp':[expected[k]-ret[k] for k in range(2)],
                       'return_pass':all(abs(expected[k]-ret[k])<=rtol for k in range(2)),
                       'equity_bridge_pass':all(abs(implied[k]-pv[k])<=eqtol+1e-5 for k in range(2))})
    out['reports'][t]=checks

# MU: re-create all four long-term DCFs from published annual operating assumptions.
mu=[([115,122,129,135,140,145,150],[.50,.48,.46,.44,.42,.40,.38],.13,.19,107,.02,.12,[.14,.12],154.85,1.159),
    ([250,262,275,289,303,318,334],[.62,.60,.58,.56,.54,.52,.50],.09,.17,238,.03,.15,[.12,.10],339.032,1.156),
    ([415,455,496,540,585,630,675],[.70,.68,.65,.62,.59,.56,.53],.09,.19,378,.035,.18,[.12,.10],499.15,1.1566),
    ([570,655,745,835,920,1000,1070],[.71,.69,.66,.63,.60,.57,.54],.095,.215,490,.04,.20,[.125,.105],544.71,1.1575)]
m=[]
for j,(rev,marg,da,cap,prior,g,roic,rates,bridge,shares) in enumerate(mu):
    fc=[]
    for r,mr in zip(rev,marg):
        fc.append(r*mr*.82+r*(da-cap)-.12*(r-prior)); prior=r
    ev=[sum(cf/(1+w)**(i+1) for i,cf in enumerate(fc))+rev[-1]*marg[-1]*.82*(1+g)*(1-g/roic)/(w-g)/(1+w)**7 for w in rates]
    prices=[(e+bridge)/shares for e in ev]
    target=out['reports']['MU'][j*3+2]['prices']
    m.append({'prices':prices,'displayed':target,'pass':max(abs(prices[k]-target[k]) for k in range(2))<.6})
out['independent_models']['MU_4_long_DCF']=m

# SNDK: re-create all 12 forward earnings multiple valuations.
sdata=[(14.91,11.70,152.59,6.5,8.5),(12.26,15.39,151.46,6,8),(10.66,32.30,151.71,6,8),
 (28.35,11.92,150.86,9,11.5),(28.36,17.24,147.69,9,12),(30.46,40.46,135.37,9,12),
 (37.86,11.67,150.45,11,14),(41.98,17.84,146.87,11,14),(54.90,45.35,131.28,11,15),
 (43.43,11.90,150.68,12,16),(50.29,19.08,147.29,12,16),(72.18,46.68,132.36,12,17)]
s=[]
for j,(e,bridge,shares,lo,hi) in enumerate(sdata):
    prices=[1000*(e*k+bridge)/shares for k in (lo,hi)]
    target=out['reports']['SNDK'][j]['prices']
    s.append({'prices':prices,'displayed':target,'pass':max(abs(prices[k]-target[k]) for k in range(2))<1.3})
out['independent_models']['SNDK_12_multiples']=s
out['decision_sensitivities']={
 'SNDK_12m_required_multiple_20pct':(1740*1.20*147.69/1000-17.24)/28.36,
 'GNRC_12m_required_multiple_15pct':(187.35*1.15*60.209375/1000+.786)/1.2229715,
 'LWLG_break_3y_success_probability_low':(5.35*1.25**3-.2)/(11.56-.2),
 'LWLG_break_3y_success_probability_high':(5.35*1.25**3-.2)/(16.85-.2),
 'SNDK_3y_optimistic_probability_threshold':(1740*1.15**3-705)/(5782-705),
 'BE_break_3y_work_annual_return':(379.63/252.87)**(1/3)-1,
 'BE_break_3y_afterhours_annual_return':(379.63/266.14)**(1/3)-1,
}
out['summary']={'cells':sum(map(len,out['reports'].values())),
 'return_pass':sum(x['return_pass'] for r in out['reports'].values() for x in r),
 'bridge_pass':sum(x['equity_bridge_pass'] for r in out['reports'].values() for x in r),
 'independent_model_cells':sum(map(len,out['independent_models'].values())),
 'independent_model_pass':sum(x['pass'] for r in out['independent_models'].values() for x in r)}
(B/'numeric_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'summary':out['summary'],'sensitivities':out['decision_sensitivities'],
 'failures':[(t,x) for t,r in out['reports'].items() for x in r if not x['return_pass'] or not x['equity_bridge_pass']],
 'model_failures':[(t,x) for t,r in out['independent_models'].items() for x in r if not x['pass']]},ensure_ascii=False,indent=2))
