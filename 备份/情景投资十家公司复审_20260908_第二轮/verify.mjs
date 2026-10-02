import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import{fileURLToPath}from'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url)),root='D:/drive/Investment';
const m=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json'),'utf8'));
const data=JSON.parse(fs.readFileSync(path.join(dir,'提取数据.json'),'utf8'));
const result={inputs:[],tables:[],statistics:{}};
const hashPaths=new Map();
for(const r of m)for(const v of ['新报告','旧报告']){
 const txt=fs.readFileSync(path.join(dir,v,r.ticker+'.md'),'utf8');
 for(const hit of txt.matchAll(/(?:基本面|金融资料)\/[^`|\n]+?\.md/g)){const p=hit[0];if(fs.existsSync(path.join(root,p)))hashPaths.set(crypto.createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex'),p);}
}
const cells=line=>line.split(/(?<!\\)\|/).slice(1,-1).map(s=>s.trim().replace(/\*\*/g,'').replace(/\\\|/g,'｜'));
const nums=s=>String(s??'').replace(/[−–]/g,'-').replace(/,/g,'').match(/[+-]?\d+(?:\.\d+)?/g)?.map(Number)||[];
for(const row of m){
 const pair={};
 for(const v of ['新报告','旧报告']){const d=data.find(x=>x.ticker===row.ticker&&x.version===v);pair[v]=new Map();
  for(const l of d.hashes){const h=l.match(/[a-fA-F0-9]{64}/)?.[0].toLowerCase(),file=l.match(/(?:基本面|金融资料)\/[^`|]+?\.md/)?.[0]||hashPaths.get(h);if(file&&h)pair[v].set(file,h);}
 }
 const common=[...pair['新报告']].filter(([p])=>pair['旧报告'].has(p));
 const live=[...pair['新报告']].map(([p,h])=>({path:p,matches:fs.existsSync(path.join(root,p))&&crypto.createHash('sha256').update(fs.readFileSync(path.join(root,p))).digest('hex')===h}));
 result.inputs.push({ticker:row.ticker,newCount:pair['新报告'].size,oldCount:pair['旧报告'].size,common:common.length,changed:common.filter(([p,h])=>pair['旧报告'].get(p)!==h).map(([p])=>p),added:[...pair['新报告'].keys()].filter(p=>!pair['旧报告'].has(p)),dropped:[...pair['旧报告'].keys()].filter(p=>!pair['新报告'].has(p)),live});
 const content=fs.readFileSync(path.join(dir,'新报告',row.ticker+'.md'),'utf8'),lines=content.split(/\r?\n/);
 const header=lines.findIndex(l=>l.startsWith('|')&&/每股|每单位|美元\/ADR/.test(l)&&/建议|强度/.test(l)&&/置信/.test(l));
 if(header<0){result.tables.push({ticker:row.ticker,error:'No detail header'});continue;}
 const hs=cells(lines[header]),priceColumn=hs.findIndex(h=>/每股|每单位|美元\/ADR/.test(h)),returnColumn=hs.findIndex(h=>/回报/.test(h)),ratingColumn=hs.findIndex(h=>/建议|强度/.test(h));
 const details=[];
 for(let i=header+2;i<lines.length&&lines[i].startsWith('|');i++){const c=cells(lines[i]);if(!/悲观|基准|乐观|突破/.test(c[0]))continue;details.push({line:i+1,cells:c,prices:nums(c[priceColumn]),returns:nums(c[returnColumn]),rating:c[ratingColumn]});}
 const d=data.find(x=>x.ticker===row.ticker&&x.version==='新报告');
 for(let i=0;i<details.length;i++){const mat=d.matrices[Math.floor(i/3)]?.cells[(i%3)+1];details[i].matrixMatch=mat?.startsWith(details[i].rating)&&nums(mat).slice(0,2).join(',')===details[i].returns.slice(0,2).join(',');}
 result.tables.push({ticker:row.ticker,header:hs,details});
}
const all=data.filter(x=>x.version==='新报告').flatMap(x=>x.matrices.flatMap(r=>r.cells.slice(1)));
const old=data.filter(x=>x.version==='旧报告').flatMap(x=>x.matrices.flatMap(r=>r.cells.slice(1)));
const count=arr=>arr.reduce((o,c)=>{const s=c.split('｜');o.ratings[s[0].trim()]=(o.ratings[s[0].trim()]||0)+1;o.confidence[s[2]?.trim()]=(o.confidence[s[2]?.trim()]||0)+1;return o},{ratings:{},confidence:{}});
result.statistics={new:count(all),old:count(old),totalNewCells:all.length,totalOldCells:old.length,minutes:m.reduce((a,r)=>a+r.minutes,0)};
fs.writeFileSync(path.join(dir,'核验数据.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify({inputs:result.inputs.map(({live,...r})=>({...r,liveFailures:live.filter(x=>!x.matches)})),tables:result.tables.map(x=>({ticker:x.ticker,rows:x.details?.length,failures:x.details?.filter(d=>!d.matrixMatch).map(r=>({line:r.line,rating:r.rating})),error:x.error})),statistics:result.statistics},null,2));
