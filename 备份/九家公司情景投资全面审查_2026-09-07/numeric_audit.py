from pathlib import Path
import re,json,ast,math,contextlib,io
B=Path('备份/九家公司情景投资全面审查_2026-09-07'); R=Path('分析报告/公司情景投资决策/结果');tickers=['MU','SNDK','CRDO','GNRC','LWLG','SPACEX','GOOGL','AMZN','BE']; reports={t:(R/f'{t}_经营情景市场状态投资决策_2026-09-07.md').read_text(encoding='utf8') for t in tickers}
# Parse documented parameter literals; compute independent values, do not execute report code.
def literal_assignment(code,name):
 for n in ast.walk(ast.parse(code)):
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets): return ast.literal_eval(n.value)
def block(t): return re.search(r'^```python\n(.*?)^```\s*$',reports[t],re.M|re.S)[1]
def cells(t):
 rows=[]
 for line in reports[t].splitlines():
  if line.startswith('|') and line.count('｜')>=10:
   cs=[x.strip() for x in line.strip('|').split('|')]
   if len(cs)==6 and all('｜' in x for x in cs[1:]):
    for x in cs[1:]:
     seg=x.split('｜');nums=re.findall(r'[-−+]?\d+(?:\.\d+)?%',seg[1]);rows.append({'row':cs[0],'label':seg[0],'returns':[float(z[:-1].replace('−','-')) for z in nums]})
 return rows
computed={}; terminals={}
def store(t,vals):computed[t]=vals
m=json.loads(re.search(r'```json\n(.*?)\n```',reports['MU'],re.S)[1]);vals=[]
for s in m['scenarios']:
 for market in m['markets']:
  ps=[]
  for k in (0,1):
   r=market['r'][1-k];g=s['g'][k];tv=s['nopat5'][k]*(1+g)*(1-g/s['roic'][k])/(r-g)/(1+r)**5;ev=sum(v/(1+r)**(i+1) for i,v in enumerate(s['fcff'][k]))+tv;ps.append((ev+s['netNonOperatingAssets'][k])/s['shares'][k])
  vals.append([(p+m['dividend'])/m['price']*100-100 for p in ps])
store('MU',vals)
m=json.loads(re.search(r'```json\n(.*?)\n```',reports['GOOGL'],re.S)[1]);vals=[]
for s in m['scenarios']:
 for market in m['markets']:
  ps=[]
  for k,key in enumerate(['lo','hi']):
   d=s[key];r=market['w'][1-k];g=s['g'][k];u=m['stub'];cf=[e*.8+da-cap-wc for e,da,cap,wc in zip(d['op'],d['da'],d['cap'],d['wc'])];tv=d['op'][-1]*.8*(1+g)*(1-g/s['roic'][k])/(r-g)/(1+r)**(u+4);ev=cf[0]*u/(1+r)**(u/2)+sum(cf[i]/(1+r)**(u+i-.5) for i in range(1,5))+tv;ps.append((ev+s['bridge'][k])/s['shares'][1-k]);terminals[f'GOOGL {s["id"]} {market["id"]} {k}']=tv/ev
  vals.append([(p+m['dividend'])/m['price']*100-100 for p in ps])
store('GOOGL',vals)
m=json.loads(re.search(r'```json\n(.*?)\n```',reports['AMZN'],re.S)[1]);vals=[];amznprices=[]
for s in m['rows']:
 for c in m['cols']:
  ds=[];ss=[];u=m['remaining'];q=s['q'];cf=[e*.78+d+w-cap-fl for e,d,w,cap,fl in zip(s['ebit'],s['da'],s['wc'],s['cap'],s['fl'])];qcf=q['fcf'][2]-(s['sbc'][0]-s['interest'][0]+s['fl'][0])/4;stub=cf[0]-m['elapsed_q1']*qcf;ratio=(q['ebit'][2]/4+sum(q['ebit'][3:6])+.75*q['ebit'][6])/s['ebit'][0]
  for k in (0,1):
   r=c['w'][1-k];g=s['g'][k];f=s['factor'][k];tv=s['ebit'][-1]*f*.78*(1+g)*(1-g/s['roic'][k])/(r-g)/(1+r)**(u+4);ev=stub*f/(1+r)**(u/2)+sum(cf[i]*f/(1+r)**(u+i-.5) for i in range(1,5))+tv;cross=f*ratio*s['sm']*(s['awseb'][0]*c['am'][k]+(s['ebit'][0]-s['awseb'][0])*c['cm'][k]);bridge=s['asset'][k]-s['nd'][1-k];ds.append((ev+bridge)/s['shares'][1-k]);ss.append((cross+bridge)/s['shares'][1-k])
  p=[min(ds[0],ss[0]),max(ds[1],ss[1])];amznprices.append(p);vals.append([x/m['price']*100-100 for x in p])
store('AMZN',vals)
code=block('LWLG');rs=literal_assignment(code,'rows');ms=literal_assignment(code,'markets');vals=[];u=299/365
for s in rs:
 for m in ms:
  ps=[]
  for k in (0,1):
   r=m[1][1-k];g=s['g'][k];ev=sum(v*(u if i==0 else 1)/(1+(.048 if v<0 else r))**(u+i) for i,v in enumerate(s['fcf'][k]))+s['terminal'][k]*(1+g)/(r-g)/(1+r)**(u+4);ps.append(max(0,ev+s['cash'][k])/s['shares'][1-k])
  vals.append([p/5.35*100-100 for p in ps])
store('LWLG',vals)
code=block('SPACEX');rs=literal_assignment(code,'ROWS');ms=literal_assignment(code,'MARKETS');vals=[]
for s in rs.values():
 for m in ms.values():
  a,b,h,j,g,t,nh,nl,cl,ch,el,eh=s;rl,rh,ml,mh=m;ds=[];xs=[]
  for cash,fade,growth,r,mul,nop in [(a,h,g,rh,ml,el),(b,j,t,rl,mh,eh)]:
   cf=cash+[cash[-1]*(1+fade)**i for i in range(1,6)];ds.append(sum(v/(1+r)**(i+1) for i,v in enumerate(cf))+cf[-1]*(1+growth)/(r-growth)/(1+r)**10);xs.append(sum(v/(1+r)**(i+1) for i,v in enumerate(cash))+nop*mul/(1+r)**5)
  ps=[max(0,min(ds[0],xs[0])+cl)/nh,max(0,max(ds[1],xs[1])+ch)/nl];vals.append([p/147.95*100-100 for p in ps])
store('SPACEX',vals)
code=block('CRDO');rs=json.loads(re.search(r"S = json.loads\(r'''(.*?)'''\)",code,re.S)[1]);ms=json.loads(re.search(r"M = json.loads\(r'''(.*?)'''\)",code,re.S)[1]);vals=[]
for i,s in enumerate(rs):
 for m in ms:
  ps=[]
  for k in (0,1):
   r=m['w'][1-k];rev=s['rev'][:];cf=[a*b for a,b in zip(rev,s['margin'])]
   for gr in s['fade']:rev.append(rev[-1]*(1+gr));cf.append(rev[-1]*s['margin'][-1])
   ev=(sum(v/(1+r)**(j+1) for j,v in enumerate(cf))+cf[-1]*(1+s['g'])/(r-s['g'])/(1+r)**10)*s['f'][k];cross=s['E'][k]*m['K'][k]*[.8,1,1.2,1.45][i];v=(min(ev,cross) if k==0 else max(ev,cross));ps.append((v+s['cash'][k]-.010)*1000/s['shares'][1-k])
  vals.append([p/170.57*100-100 for p in ps])
store('CRDO',vals)

def table(t, first, last):
 return [[c.strip() for c in line.strip('|').split('|')] for line in reports[t].splitlines()[first-1:last] if line.startswith('|')]
def nums(x): return [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?',x)]
# SNDK: five-year FCFF and near-term EBIT boundary from the prose tables.
rows=table('SNDK',314,321); vals=[]; sndk_detail=[]
for i in range(4):
 for j,(rl,rh,ml,mh) in enumerate([(11,13,7,10),(10.5,13,7,11),(12,14,6,9),(14,17,4.5,7),(18,24,3,5)]):
  ds=[];xs=[];price=[]
  for k in (0,1):
   d=rows[i*2+k];cf=nums(d[5]);g=nums(d[6])[0]/100;r=[rh,rl][k]/100
   ev=sum(v/(1+r)**(y+1) for y,v in enumerate(cf))+cf[-1]*(1+g)/(r-g)/(1+r)**5
   cross=[18.16,34.14,51.58,63.46][i]*[.9,1.1][k]*[ml,mh][k]*[.8,1,1.1,1.15][i]
   cap=[[8,13],[13,19],[15,23],[15,25]][i][k];n=[[159,156],[158,155],[158,155],[160,156]][i][k]
   ds.append((ev+cap)*1000/n);xs.append((cross+cap)*1000/n);price.append((min(ev,cross) if k==0 else max(ev,cross))+cap)
   price[-1]*=1000/n
  sndk_detail.append({'dcf':ds,'cross':xs,'envelope':price});vals.append([(p/1740-1)*100 for p in price])
store('SNDK',vals)
# GNRC: derive cash flows from operating components, before rounding display tables.
rows=table('GNRC',187,214);vals=[]
for i in range(4):
 rr=[nums(d[1]) for d in []]; v=[[float(x) for x in d[1:]] for d in rows[i*7:i*7+7]]
 rev,ebitda,da,sbc,o,cap,wc=v;nopat=[(e-d-b-z)*.75 for e,d,b,z in zip(ebitda,da,sbc,o)];cf=[a+d-c-w for a,d,c,w in zip(nopat,da,cap,wc)]
 for rl,rh,ml,mh in [(8.5,9.5,10,15),(9,10.5,9,16),(9.5,10.5,9,13),(11,12.5,7,11),(14,17,5,9)]:
  ps=[]
  for k in (0,1):
   r=[rh,rl][k]/100;g=[.025,.035][k];f=([.9,1.1] if i in (0,3) else [.95,1.05])[k];tv=f*nopat[-1]*(1+g)*(1-g/[.10,.16,.19,.22][i])/(r-g)
   ev=f*cf[0]*24/366+sum(f*c/(1+r)**(y+1+24/365) for y,c in enumerate(cf))+tv/(1+r)**(5+24/365)
   cross=ebitda[0]*[ml,mh][k];ev=min(ev,cross) if k==0 else max(ev,cross);ps.append((ev-[1.29,.99,.95,1.27][i])*1000/[60.2,60.3,60.5,61][i])
  vals.append([(p/187.35-1)*100 for p in ps])
store('GNRC',vals)
# BE: ten-year FCFF, reinvestment-constrained terminal, debt/conversion branch.
rows=table('BE',181,188);fades=table('BE',317,324);vals=[];beprices=[]
for i in range(4):
 for rl,rh in [(9.5,11.5),(9,11),(11,13),(13,15),(16,20)]:
  ps=[]
  for k in (0,1):
   d=rows[i*2+k];rv=nums(d[1]);mg=[x/100 for x in nums(d[2])];cap=nums(d[3]);wc=nums(d[4]);pr=nums(d[5]);fd=fades[i*2+k];growth=[x/100 for x in nums(fd[1])];g=nums(fd[2])[0]/100;roic=nums(fd[3])[0]/100;r=[rh,rl][k]/100;u=299/365
   cf=[a*b*(1-t)+a*.015-c-w-p for a,b,t,c,w,p in zip(rv,mg,[.1,.15,.2,.22,.22],cap,wc,pr)]
   ev=sum(c*(u if y==0 else 1)/(1+r)**(u+y) for y,c in enumerate(cf));rev=rv[-1]
   for y,gr in enumerate(growth):
    old=rev;rev*=1+gr;ev+=(rev*mg[-1]*.78-(rev-old)*mg[-1]*.78/roic)/(1+r)**(u+5+y)
   ev+=rev*(1+g)*mg[-1]*.78*(1-g/roic)/(r-g)/(1+r)**(u+9)
   cash=[[2.15,2.6],[2.8,3.15],[2.9,3.3],[2.7,3.15]][i][k];n=[[318,314],[320,316],[322,318],[326,320]][i][k]/1000;p=(ev+cash-1.045-2.5)/n
   if p>=194.97:p=(ev+cash-1.045)/(n+.0128225)
   ps.append(max(0,p))
  beprices.append(ps);vals.append([(p/252.87-1)*100 for p in ps])
store('BE',vals)

summary={}
for t in tickers:
 cs=cells(t);out={'cells':len(cs),'positive':sum(c['label'] in ['谨慎建议投资','建议投资','强烈建议投资'] for c in cs),'body_lines':len(reports[t].splitlines())}
 if t in computed:
  errors=[{'cell':i+1,'shown':c['returns'],'computed':v} for i,(c,v) in enumerate(zip(cs,computed[t])) if len(c['returns'])!=2 or max(abs(a-b) for a,b in zip(c['returns'],v))>(.51 if t=='BE' else .15)];out.update(recomputed=len(computed[t]),discrepancies=errors,max_return_error_pp=max(abs(a-b) for c,v in zip(cs,computed[t]) for a,b in zip(c['returns'],v)))
 summary[t]=out
(B/'numeric-audit.json').write_text(json.dumps({'summary':summary,'computed_returns':computed,'terminal_shares':terminals,'amzn_prices':amznprices,'be_prices':beprices,'sndk_detail':sndk_detail},ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False,indent=2));print('GOOGL base terminal',[(k,v) for k,v in terminals.items() if ' N W ' in k]);print('AMZN baseline',amznprices[5], 'midpoint_return',(sum(amznprices[5])/2/258.51-1)*100,'75%return',((.25*amznprices[5][0]+.75*amznprices[5][1])/258.51-1)*100)
