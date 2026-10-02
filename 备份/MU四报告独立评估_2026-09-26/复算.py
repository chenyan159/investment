from pathlib import Path
import json, re, math, hashlib
import sys
from datetime import date, timedelta

ROOT = Path(r'D:\investment\分析报告\公司情景投资决策\备份\mu')
sys.stdout.reconfigure(encoding='utf-8')
OUT = Path(__file__).parent
files = {n: (ROOT/n).read_text(encoding='utf-8-sig').splitlines() for n in ['MU_cl_hi.md','MU_op_hi.md','mu_op_ex.md','mu_op_sol_mx.md']}
def row(name, line):
    return [x.strip().replace('**','') for x in files[name][line-1].strip('|').split('|')]
def num(s):
    return float(s.replace(',','').replace('−','-').replace('%',''))
def table(name, start, end):
    return [row(name,i) for i in range(start,end+1)]
result = {'scope':'Independent reproduction from published rounded tables, not original author code or proof of economic assumptions', 'sha256': {n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in files}}
prices = {'MU_cl_hi.md': [[350,505],[615,875],[960,1345],[1645,2340]],'MU_op_hi.md':[[339,434],[938,1218],[1747,2241],[1303,1673]],'mu_op_ex.md':[[510,640],[1110,1410],[1750,2240],[1370,1760]],'mu_op_sol_mx.md':[[270,360],[590,860],[970,1360],[1090,1730]]}
result['returns']={n:[[round((p/1082.28-1)*100,3) for p in r] for r in rows] for n,rows in prices.items()}
targets={'MU_cl_hi.md':date(2027,9,30),'MU_op_hi.md':date(2028,10,31),'mu_op_ex.md':date(2028,10,31),'mu_op_sol_mx.md':date(2027,10,29)}
result['base_annualized_returns']={n:[round(((p/1082.28)**(365.25/(targets[n]-date(2026,9,25)).days)-1)*100,2) for p in rows[1]] for n,rows in prices.items()}

# CL and SOL: independent reconstruction of all FY27/FY28 product revenue and COGS.
rc=[4.5,15.593,11.235,5.2,4.743,.185]; cc=[1.4,1.9,1.55,.7,.75,.1]
for name, ranges, opex in [('MU_cl_hi.md',[(406,411)],[[8.3,8.5,8.8,9],[8.8,9.8,10.5,11.5]]),('mu_op_sol_mx.md',[(134,139),(143,148)],[[8.5,9,9.5,10],[9,10.5,11.5,12]])]:
    grid=table(name,*ranges[0])
    params=[]
    for y in range(2):
        if len(ranges)>1: grid=table(name,*ranges[y])
        yrs=[]
        for s in range(4):
            vals=[]
            for i in range(6):
                cell=grid[i][1+s+4*y] if len(ranges)==1 else grid[i][1+s]
                if cell=='同基准': cell=grid[i][2]
                vals.append([num(v) for v in cell.split('/')])
            yrs.append(vals)
        params.append(yrs)
    outputs=[]
    for s in range(4):
        prev_r=[x*4 for x in rc]; prev_c=[x*4 for x in cc]
        for y in range(2):
            rr=[]; co=[]
            for i,(q,p,c) in enumerate(params[y][s]):
                rr.append(prev_r[i]*q*p); co.append(prev_c[i]*(.45+.55*q)*c)
            outputs.append({'scenario':s,'FY':2027+y,'revenue':sum(rr),'COGS':sum(co),'EBIT':sum(rr)-sum(co)-opex[y][s]})
            prev_r,prev_c=rr,co
    result[name+'_near_term']=outputs

# HI: annual FCFF identities and independent DCF, with reported day-count convention.
hi=[]
for r in table('MU_op_hi.md',362,397):
    s,year=r[:2]; rev,ebit,nopat,da,cap,nwc,fcf=map(num,r[2:])
    hi.append(dict(s=s,year=int(year),rev=rev,ebit=ebit,nopat=nopat,da=da,cap=cap,nwc=nwc,fcf=fcf,error=nopat+da-cap-nwc-fcf))
result['hi_cash_identity_max_error_B']=max(abs(x['error']) for x in hi)
start=date(2026,9,26); target=date(2028,10,31)
def hi_end(y):
    d=date(y,8,31)
    return min([d+timedelta(days=i) for i in range(-3,4)], key=lambda x: (x.weekday()!=3,abs((x-d).days)))
def dcf(seq,k,g,roic,net,start_date=start,first_frac=1):
    pv=sum(x['fcf']*(first_frac if i==0 else 1)/(1+k)**((hi_end(x['year'])-start_date).days/365.25) for i,x in enumerate(seq))
    tv=seq[-1]['nopat']*(1+g)*(1-g/roic)/(k-g)/(1+k)**((hi_end(2035)-start_date).days/365.25)
    return {'price':(pv+tv+net)/1.15,'terminal_share':tv/(pv+tv)}
result['hi_DCF']={}
for idx,s in enumerate(['受损','基准','乐观','突破']):
    seq=[x for x in hi if x['s']==s]
    result['hi_DCF'][s]=dcf(seq,.115,.03,[.12,.15,.2,.2][idx],34,first_frac=341/364)

# EX: annual cash identities and DCF at stated September 1 cash dates.
ex=[]
for s,lo,high in [('悲观',428,436),('基准',442,450),('乐观',456,464),('突破',470,478)]:
    for r in table('mu_op_ex.md',lo,high):
        year,rev,cost,opex,ebit,tax,da,cap,nwc,fcf=map(num,r)
        ex.append(dict(s=s,year=int(year),rev=rev,ebit=ebit,nopat=ebit*(1-tax/100),da=da,cap=cap,nwc=nwc,fcf=fcf,error=ebit*(1-tax/100)+da-cap-nwc-fcf))
result['ex_cash_identity_max_error_B']=max(abs(x['error']) for x in ex)
def ex_dcf(seq,k,g,roic,subtract_three=True):
    pv=sum((x['fcf']-(3 if i==0 and subtract_three else 0))/(1+k)**((date(x['year'],9,1)-start).days/365.25) for i,x in enumerate(seq))
    tv=seq[-1]['nopat']*(1+g)*(1-g/roic)/(k-g)/(1+k)**((date(2035,9,1)-start).days/365.25)
    return {'price':(pv+tv+35.1)/1.15,'terminal_share':tv/(pv+tv)}
result['ex_DCF']={}
for idx,s in enumerate(['悲观','基准','乐观','突破']):
    seq=[x for x in ex if x['s']==s]
    result['ex_DCF'][s]={'deduct_already_counted_3B':ex_dcf(seq,.1,[.015,.025,.03,.03][idx],[.12,.16,.18,.18][idx]),'without_deduction':ex_dcf(seq,.1,[.015,.025,.03,.03][idx],[.12,.16,.18,.18][idx],False)}
hi_base=[x for x in hi if x['s']=='基准']; ex_base=[x for x in ex if x['s']=='基准']
result['common_discount_comparison']={'hi_at_10pct':dcf(hi_base,.1,.03,.15,34,first_frac=341/364),'ex_at_11_5pct':ex_dcf(ex_base,.115,.025,.16)}

# Sol's DCF terminal endpoints.
sol=[]
for s,fcfs,terminal,ks,net in [('受损',[25.59,29.4,33.8,35.5,35.5],[29,39],[.13,.115],78.7),('基准',[72.01,67,63,59,57],[54,74],[.11,.095],121),('乐观',[121.32,124,119,109,99],[84,104],[.105,.09],144.5),('突破',[71.89,89,109,124,129],[119,159],[.105,.09],117.6)]:
    endpoints=[]
    for j in range(2):
        # g is only given as a total 0%-2% range in the source report.
        # These endpoint values are inferred from its disclosed terminal PV, not explicitly listed.
        k=ks[j]; g=([0,.01] if s=='受损' else [.01,.02])[j]
        pv=sum(x/(1+k)**(t+1) for t,x in enumerate(fcfs)); tv=terminal[j]/(k-g)/(1+k)**5
        endpoints.append({'price':(pv+tv+net)/1.15,'pv':pv,'tv':tv,'g_inferred_not_explicit':g})
    sol.append({'scenario':s,'endpoints':endpoints})
result['sol_DCF']=sol
result['sol_deferred_10B_terminal_sensitivity_per_share']=10/(.105-.015)/(1.105**5)/1.15
result['trade_DSO']=26.894/41.456*91
result['total_receivables_ratio_days']=31.025/41.456*91
# EX vs HI target-price midpoint attribution, using published rounded NOPAT/net cash.
result['ex_minus_hi_midpoint']={'NOPAT_effect':(114.7-107.17)*9.5/1.15,'multiple_effect':114.7*(10.5-9.5)/1.15,'cash_effect':(244.6-221.4)/1.15}
result['cl_vs_sol_base_2027_profit_difference_B']=190.8-146.6
result['cl_vs_sol_base_2032_profit_difference_B']=69-75
(OUT/'复算结果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
