import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const data=JSON.parse(fs.readFileSync(path.join(dir,'提取数据.json'),'utf8'));
const ver=JSON.parse(fs.readFileSync(path.join(dir,'核验数据.json'),'utf8'));
const manifest=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json'),'utf8'));
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const norm=s=>s.replace(/\s/g,'').replaceAll('／','/');
let changed=0;
let table='# 两轮120格逐项结果对照\n\n这是报告给定经营路径下的条件价值回报，不是已实现收益、实际胜率或本次审查独立投资推荐。每格为建议／累计回报／估值置信度；短期主格为6个月，长期为3年累计回报。\n\n';
for(const row of manifest){
 const n=data.find(x=>x.ticker===row.ticker&&x.version==='新报告');
 const o=data.find(x=>x.ticker===row.ticker&&x.version==='旧报告');
 table+=`## ${row.ticker}\n\n| 经营情景 | 期限 | 上轮 | 本轮 |\n|---|---|---|---|\n`;
 for(let i=0;i<4;i++)for(let j=1;j<4;j++){
  const old=o.matrices[i].cells[j],now=n.matrices[i].cells[j];
  if(norm(old.split('｜')[0])!==norm(now.split('｜')[0]))changed++;
  table+=`| ${['悲观','基准','乐观','突破'][i]} | ${['','6个月','1年','3年'][j]} | ${old} | ${now} |\n`;
 }
 table+='\n';
}
fs.writeFileSync(path.join(dir,'120格逐项对照.md'),table);
const structure=['旧报告','新报告'].map(version=>{
 let chars=0,codeChars=0;
 for(const row of manifest){const txt=fs.readFileSync(path.join(dir,version,row.ticker+'.md'),'utf8');chars+=txt.length;codeChars+=[...txt.matchAll(/```[^\n]*\n([\s\S]*?)```/g)].reduce((a,m)=>a+m[1].length,0);}
 return {version,chars,codeChars,codeFraction:codeChars/chars};
});
const noDividendPrices={PSIX:40.49,SPACEX:147.95,CRWV:102.86,SNDK:1740,CRDO:170.57};
const arithmetic=[];
for(const t of ver.tables){if(!(t.ticker in noDividendPrices))continue;for(const r of t.details){
 const expected=r.prices.slice(0,2).map(v=>(Math.abs(v)/noDividendPrices[t.ticker]-1)*100);
 arithmetic.push({ticker:t.ticker,line:r.line,expected,reported:r.returns.slice(0,2),maxErrorPP:Math.max(...expected.map((v,i)=>Math.abs(v-r.returns[i])))});
}
}
const plan=fs.readFileSync(path.join(dir,'新研究方案.md'),'utf8');
const prompts=manifest.map(r=>{const t=fs.readFileSync(path.join(dir,'运行提示词',r.ticker+'.md'),'utf8');return {ticker:r.ticker,containsExactInstantiatedPlan:t.replaceAll('\r\n','\n').includes(plan.replaceAll('【公司股票代号】',r.ticker).replaceAll('\r\n','\n').trim())};});
const result={ratingChangedCells:changed,commonInputs:ver.inputs.reduce((s,r)=>s+r.common,0),changedCommonInputs:ver.inputs.flatMap(r=>r.changed),structure,planSha:sha(plan),prompts,arithmetic:{checkedCells:arithmetic.length,maxErrorPP:Math.max(...arithmetic.map(x=>x.maxErrorPP)),overPointTwoPP:arithmetic.filter(x=>x.maxErrorPP>.2)},controlledPrice:{AVGO:{oldPrice:357.9,newPrice:369.35,priceChangePct:(369.35/357.9-1)*100,newBaseThreeYearValue:358.74,distribution:7.8,returnAtOldPricePct:((358.74+7.8)/357.9-1)*100,returnAtNewPricePct:((358.74+7.8)/369.35-1)*100},CRWV:{oldPrice:89.36,newPrice:102.86,priceChangePct:(102.86/89.36-1)*100,newBaseThreeYearAtOldPrice:[10.22,37.34].map(p=>(p/89.36-1)*100)}},sommyBridge:{oldParentEV:1229.8,newParentEV:2366.8-414.2,oldParentNetDebt:745,newParentNetDebt:574.9+59,nonOperatingAssetChange:175-205,newParentEquity:2366.8-414.2-574.9-59+175}};
fs.writeFileSync(path.join(dir,'补充核验.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify(result,null,2));
