import fs from 'node:fs';
const root='D:/investment/';
const pairs=JSON.parse(fs.readFileSync(new URL('./metrics.json',import.meta.url),'utf8'));
const checks=[];
const lines=k=>fs.readFileSync(root+pairs.find(x=>x.key===k).new,'utf8').split(/\r?\n/u);
const cells=l=>l.split('|').slice(1,-1).map(x=>x.trim());
const num=s=>Number(s.replaceAll(',',''));
const nums=s=>(s.replaceAll(',','').match(/-?\d+(?:\.\d+)?/gu)||[]).map(Number);
function check(k,line,field,actual,expected,tol=.011){checks.push({key:k,line,field,actual,expected,error:actual-expected,pass:Math.abs(actual-expected)<=tol});}
function rows(k,a,b,cb){lines(k).slice(a-1,b).forEach((l,i)=>{if(l.startsWith('|')&&!/^\|[-: |]+$/u.test(l))cb(cells(l),a+i);});}
rows('hbm',371,397,(c,l)=>{const [d,s,q,p,cost,r,g]=c.slice(2).map(num);check('hbm',l,'Q',q,Math.min(d,s));if(q){check('hbm',l,'R',r,q*p);check('hbm',l,'GP',g,q*(p-cost));}});
rows('memory',402,429,(c,l)=>{const [d,s,q,p,cost,r,g]=c.slice(2).map(num);check('memory',l,'Q',q,Math.min(d,s));check('memory',l,'R',r,q*p);check('memory',l,'GP',g,q*(p-cost));});
rows('ssd',313,330,(c,l)=>{const [d,s,q]=nums(c[2]),[p,cost]=nums(c[3]),[r,g]=nums(c[4]);check('ssd',l,'Q',q,Math.min(d,s));check('ssd',l,'R',r,q*p/1000);check('ssd',l,'GP',g,q*(p-cost)/1000);});
rows('wafer',363,417,(c,l)=>{if(c.length!==9||!['悲观','基准','乐观'].includes(c[0]))return;const [d,s,q,p,cost]=c.slice(2,7).map(num);const r=nums(c[7])[0],g=num(c[8]),scale=['E','N'].includes(c[1])?1000:1;check('wafer',l,'Q',q,Math.min(d,s));check('wafer',l,'R',r,q*p/scale);check('wafer',l,'GP',g,q*(p-cost)/scale);});
rows('foundry',423,483,(c,l)=>{if(c.length!==10)return;const [d,s,q,p,cost,r,g,op]=c.slice(2).map(num);const f={'N2及以下':.15,N3:.09,'N4/5':.08,'N6/7':.09,'高密度封装':.1,'其他逻辑先进封装':.08}[c[0]];check('foundry',l,'Q',q,Math.min(d,s));check('foundry',l,'R',r,q*p);check('foundry',l,'GP',g,q*(p-cost));check('foundry',l,'OP',op,q*(p-cost)-q*p*f);});
rows('gpu',359,403,(c,l)=>{const [d,s,q,p,cost,f,r,g,op]=c.slice(3).map(num);check('gpu',l,'Q',q,Math.min(d,s));check('gpu',l,'R',r,q*p);check('gpu',l,'GP',g,q*(p-cost));check('gpu',l,'OP',op,q*(p-cost)-f);});
rows('package',365,384,(c,l)=>{const [d,w,g,k,s,q]=c.slice(3,9).map(num),[p,cost]=nums(c[9]),[r,gp]=nums(c[10]);check('package',l,'S',s,Math.round(w*g*k*10)/10);check('package',l,'Q',q,Math.min(d,s));check('package',l,'R',r,q*p/1000);check('package',l,'GP',gp,q*(p-cost)/1000);});
rows('package',394,403,(c,l)=>{const [d,s,q]=c.slice(2,5).map(num),[p,cost]=nums(c[5]),[r,gp]=nums(c[6]);check('package',l,'Q',q,Math.min(d,s));check('package',l,'R',r,q*p/1000);check('package',l,'GP',gp,q*(p-cost)/1000);});
rows('optics',412,429,(c,l)=>{const [d,s,q,p,cost,r,g]=c.slice(2,9).map(num);check('optics',l,'Q',q,Math.min(d,s));check('optics',l,'R',r,q*p/1000,.013);check('optics',l,'GP',g,q*(p-cost)/1000,.013);});
function range(s){const n=nums(s);return n.length===1?[n[0],n[0]]:n;}
const cr=[];rows('cooling',352,367,(c,l)=>{const [n,a,r,d,s,q,b]=c.slice(1).map(range);for(let t=0;t<2;t++){check('cooling',l,'D'+t,d[t],n[t]*a[t]/100+r[t]);check('cooling',l,'Q'+t,q[t],Math.min(d[t],s[t]));}cr.push({label:c[0],q,b});});
const prices=[];rows('cooling',406,421,(c,l)=>{prices.push(c.slice(1,4).map(x=>range(x.split('/')[0])));});
rows('cooling',433,448,(c,l)=>{const i=l-433,{q,b}=cr[i],p=prices[i];const calc=[q.map((v,t)=>v*p[0][t]/1000),q.map((v,t)=>v*p[1][t]/1000),b.map((v,t)=>v*p[2][t]/1000)];for(let t=0;t<2;t++){for(let j=0;j<3;j++)check('cooling',l,'R'+j+'_'+t,range(c[j+1])[t],calc[j][t]);check('cooling',l,'total'+t,range(c[4])[t],calc.reduce((s,x)=>s+x[t],0));}});
const v=[[.05,.12],[.075,.16],[.06,.14],[.15,.30]],rs=[[.02,.05],[.08,.15],[.05,.12],[.08,.18]],m0=[.18,.15,.20,.22],pow=[];
rows('power',369,378,(c,l)=>{const d=range(c[1]),pars=c.slice(2).map(x=>x.split('/').map(range));const out=[];for(let j=0;j<4;j++){const [f,p,g,cost]=pars.map(x=>x[j]);const r=[0,1].map(t=>d[t]*f[t]*v[j][t]*p[t]*g[t]*(1+rs[j][t]));const m=[1-(1-m0[j])*cost[1]/p[0],1-(1-m0[j])*cost[0]/p[1]];const vals=r.flatMap(a=>m.map(b=>a*b));const mid=a=>(a[0]+a[1])/2;const rmid=mid(d)*mid(f)*mid(v[j])*mid(p)*mid(g)*(1+mid(rs[j]));out.push({r,m,ebit:[Math.min(...vals),Math.max(...vals)],rmid,emid:rmid*(1-(1-m0[j])*mid(cost)/mid(p))});}pow.push(out);});
rows('power',386,425,(c,l)=>{if(c.length!==5)return;const i=Math.floor((l-386)/4),j=(l-386)%4,a=pow[i][j];for(let t=0;t<2;t++){check('power',l,'R'+t,range(c[2])[t],a.r[t]);check('power',l,'margin'+t,range(c[3])[t]/100,a.m[t],.0011);check('power',l,'EBIT'+t,range(c[4])[t],a.ebit[t]);}});
rows('power',431,440,(c,l)=>{const p=pow[l-431];for(let t=0;t<2;t++){check('power',l,'totalR'+t,range(c[1])[t],p.reduce((s,x)=>s+x.r[t],0));check('power',l,'totalEBIT'+t,range(c[3])[t],p.reduce((s,x)=>s+x.ebit[t],0));}check('power',l,'midR',num(c[2]),p.reduce((s,x)=>s+x.rmid,0));check('power',l,'midEBIT',num(c[4]),p.reduce((s,x)=>s+x.emid,0));});
const summary=pairs.map(p=>{const a=checks.filter(x=>x.key===p.key);return {key:p.key,rows:new Set(a.map(x=>x.line)).size,checks:a.length,failed:a.filter(x=>!x.pass),maxAbsError:Math.max(...a.map(x=>Math.abs(x.error)))};});
const metrics={old:{},new:{}};for(const r of ['old','new'])for(const f of ['characters','nonWhitespace','tableRows','urls'])metrics[r][f]=pairs.reduce((s,x)=>s+x.metrics[r][f],0);
fs.writeFileSync(new URL('./calculations.json',import.meta.url),JSON.stringify({summary,metrics,checks},null,2));console.log(JSON.stringify({summary,metrics},null,2));
