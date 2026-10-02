import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const manifest=JSON.parse(fs.readFileSync(path.join(root,'manifest.json'),'utf8'));
const prices={SOMMY:20,PSIX:40.49,ET:21.5,DTE:136.08,SHECY:18.61,MU:1016.59,CRWV:89.36,SNDK:1740,AVGO:357.90,CRDO:170.57};
const split=s=>s.trim().replace(/^\||\|$/g,'').split('|').map(x=>x.trim());
const nums=s=>[...s.replaceAll(',','').replaceAll('−','-').matchAll(/[+-]?\d+(?:\.\d+)?/g)].map(x=>Number(x[0]));
const range=s=>nums(s.replaceAll('—','~').replaceAll('～','~'));
const rating=s=>s.match(/强烈不建议投资|不建议投资|谨慎建议投资|强烈建议投资|建议投资|中性\s*[／/]\s*等待/)?.[0].replace(/\s|／/g,m=>m==='／'?'/':'')??s;
const parse=text=>{const ls=text.split(/\r?\n/),ts=[];for(let i=0;i<ls.length;i++)if(/^\s*\|/.test(ls[i])){let start=i;while(i+1<ls.length&&/^\s*\|/.test(ls[i+1]))i++;ts.push({line:start+1,header:split(ls[start]),rows:ls.slice(start+2,i+1).map(split)});}return {ls,ts};};
const result=[];const output=[];
for(const m of manifest){
 const raw={new:fs.readFileSync(m.newSnapshot,'utf8'),old:fs.readFileSync(m.oldSnapshot,'utf8')};
 const docs=Object.fromEntries(Object.entries(raw).map(([k,v])=>[k,parse(v)]));
 const detail=docs.new.ts.find(t=>t.rows.length===12 && t.header.some(x=>/每股价值|每股美元|每ADR价值|每单位价值/.test(x))&&t.header.some(x=>/建议/.test(x)));
 if(!detail)throw Error(m.subject+' detail missing');
 const matrix=docs.new.ts.find(t=>t.header.length===4 && t.header.join('').includes('短期')&&t.header.join('').includes('长期')&&t.rows.length===4);
 const vi=detail.header.findIndex(x=>/每股价值|每股美元|每ADR价值|每单位价值/.test(x));
 const ri=detail.header.findIndex(x=>/总回报|累计回报/.test(x));
 const ai=detail.header.findIndex(x=>/建议/.test(x));
 const ci=detail.header.findIndex(x=>/置信/.test(x));
 let dividendRows=null;
 if(['SHECY','AVGO','MU'].includes(m.subject))dividendRows=docs.new.ts.find(t=>t.rows.length===12&&t.header.some(x=>/期间分红|期间每股分红|持有期累计每股分红/.test(x)));
 const dteDiv=[[2.330,4.660,13.980],[2.400,4.870,15.503],[2.412,4.905,15.768],[2.417,4.922,15.902]];
 let etDiv;
 if(m.subject==='ET'){const t=docs.new.ts.find(t=>t.header.at(-1)==='可得现金/单位'&&t.rows.length===40);etDiv=Array.from({length:4},(_,j)=>t.rows.slice(j*10,j*10+3).map(r=>Number(r.at(-1))));}
 const checks=detail.rows.map((r,i)=>{
  const sc=Math.floor(i/3),h=i%3;const vals=range(r[vi]).slice(0,2);const rets=range(r[ri]).slice(0,2);if(vals.length===1)vals.push(vals[0]);if(rets.length===1)rets.push(rets[0]);
  let div=[0,0];
  if(dividendRows){const di=dividendRows.header.findIndex(x=>/期间分红|期间每股分红|持有期累计每股分红/.test(x));div=Array(2).fill(Number(dividendRows.rows[i][di]));}
  if(m.subject==='DTE')div=Array(2).fill(dteDiv[sc][h]);
  if(m.subject==='ET')div=Array(2).fill(h===0?etDiv[sc][0]/2:h===1?etDiv[sc][0]:etDiv[sc].reduce((a,b)=>a+b,0));
  if(m.subject==='SOMMY'&&sc>0)div=[160,140].map(fx=>[8,16,48][h]*5/fx);
  const calculated=vals.map((p,j)=>(p+div[j])/prices[m.subject]*100-100);
  const errors=calculated.map((v,j)=>Math.abs(v-rets[j]));
  const label=rating(r[ai]);const matrixLabel=rating(matrix.rows[sc][h+1].split('｜')[0]);
  return {scenario:['悲观','基准','乐观','突破'][sc],months:[6,12,36][h],line:detail.line+2+i,value:vals,distribution:div,return:rets,calculated,error:errors,label,matrixLabel,labelMatch:label===matrixLabel,confidence:r[ci]};
 });
 function hashes(version){const entries=[];for(let i=0;i<docs[version].ls.length;i++){const l=docs[version].ls[i],h=l.match(/\b[A-Fa-f0-9]{64}\b/);let p=l.match(/((?:基本面|金融资料)\/[^|`)]+?\.md)/);const ref=l.match(/\]\[([^\]]+)\]/);if(!p&&ref){const def=docs[version].ls.find(x=>x.startsWith('['+ref[1]+']:'));p=def?.match(/((?:基本面|金融资料)\/[^|`)]+?\.md)/);}if(h)entries.push({path:p?p[1].replaceAll('\\','/'):'unresolved:'+i,hash:h[0].toUpperCase(),line:i+1});}return entries;}
 const newHash=hashes('new'),oldHash=hashes('old');const compared=newHash.map(n=>{const old=oldHash.find(o=>o.path===n.path)||oldHash.find(o=>o.hash===n.hash);let currentMatch=null;const f=path.resolve('D:/drive/Investment',n.path);if(fs.existsSync(f))currentMatch=crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex').toUpperCase()===n.hash;return {...n,oldHash:old?.hash??null,same:old?old.hash===n.hash:null,currentMatch};});
 const counts=Object.fromEntries(Object.entries(raw).map(([v,t])=>{const code=[...t.matchAll(/```[^\n]*\n([\s\S]*?)```/g)].reduce((sum,m)=>sum+m[1].length,0);return[v,{chars:t.length,codeChars:code,nonCodeChars:t.length-code}];}));
 const probabilityChecks=[];for(const t of docs.new.ts){for(let col=0;col<t.header.length;col++){const h=t.header[col];if(!/(?:U\/P\/S\/F|U\/L\/S\/F|D\/P\/S\/F)/.test(h)||!/(?:概率|当年)/.test(h)||/收入/.test(h))continue;for(let j=0;j<t.rows.length;j++){const v=nums(t.rows[j][col]);if(v.length!==4)continue;const sum=v.reduce((a,b)=>a+b,0);probabilityChecks.push({line:t.line+j+2,values:v,sum,pass:Math.abs(sum-100)<=.21&&v.every(x=>x>=0&&x<=100)});}}}
 result.push({subject:m.subject,checks,probabilityChecks,inputs:compared,oldInputCount:oldHash.length,newInputCount:newHash.length,counts});
 output.push(`## ${m.subject}\n\n|情景|6个月|一年|三年|\n|---|---|---|---|\n`+Array.from({length:4},(_,s)=>'|'+['悲观','基准','乐观','突破'][s]+'|'+checks.slice(s*3,s*3+3).map(c=>`${c.label}；${c.return[0]}%～${c.return[1]}%`).join('|')+'|').join('\n'));
}
const summary={cells:result.flatMap(r=>r.checks).length,labelMismatches:result.flatMap(r=>r.checks.filter(c=>!c.labelMatch).map(c=>({subject:r.subject,...c}))),returnErrorsOverPoint15:result.flatMap(r=>r.checks.filter(c=>c.error.some(e=>e>.15)).map(c=>({subject:r.subject,...c}))),maxReturnError:Math.max(...result.flatMap(r=>r.checks.flatMap(c=>c.error))),confidence:result.flatMap(r=>r.checks).reduce((o,c)=>(o[c.confidence]=(o[c.confidence]||0)+1,o),{}),sameInputPairs:result.map(r=>({subject:r.subject,new:r.newInputCount,old:r.oldInputCount,matched:r.inputs.filter(x=>x.same).length,changed:r.inputs.filter(x=>x.same===false).length,currentMismatch:r.inputs.filter(x=>x.currentMatch===false).length})),chars:result.reduce((o,r)=>{for(const v of ['new','old'])for(const k of ['chars','codeChars','nonCodeChars'])o[v][k]+=r.counts[v][k];return o;},{new:{chars:0,codeChars:0,nonCodeChars:0},old:{chars:0,codeChars:0,nonCodeChars:0}})};
summary.probabilityDistributions=result.flatMap(r=>r.probabilityChecks).length;
summary.probabilityFailures=result.flatMap(r=>r.probabilityChecks.filter(c=>!c.pass).map(c=>({subject:r.subject,...c})));
fs.writeFileSync(path.join(root,'数值与输入校验.json'),JSON.stringify({summary,reports:result},null,2));
fs.writeFileSync(path.join(root,'十家公司条件建议全表.md'),'# 本轮十家公司条件建议\n\n数字为报告在给定经营路径及主估值方法下的累计总回报，非本审查对真实未来回报的预测；短期数字统一6个月，3个月见原报告。置信度、明细、当前实际选择应同时阅读。\n\n'+output.join('\n\n'));
console.log(JSON.stringify(summary,null,2));
