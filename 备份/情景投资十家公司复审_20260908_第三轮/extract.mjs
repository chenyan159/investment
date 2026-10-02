import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const dir=path.dirname(fileURLToPath(import.meta.url));
const m=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json'),'utf8'));
let text='# 十家公司两轮条件矩阵原文\n\n所有回报均为报告的条件模型结果，不是本次审查重新预测的交易回报。\n';
const result=[];
for(const row of m){for(const v of ['新报告','旧报告']){
 const content=fs.readFileSync(path.join(dir,v,row.ticker+'.md'),'utf8');const lines=content.split(/\r?\n/);
 const matrices=lines.flatMap((line,i)=>/^\|\s*\*{0,2}(悲观|基准|乐观|突破)/.test(line)&&(line.match(/｜|\\\|/g)||[]).length>=6?[{line:i+1,text:line,cells:line.split(/(?<!\\)\|/).slice(1,-1).map(s=>s.trim().replace(/\*\*/g,'').replace(/\\\|/g,'｜'))}]:[]);
 const hashes=lines.filter(l=>/[a-fA-F0-9]{64}/.test(l));
 const snippets=lines.flatMap((line,i)=>line.startsWith('## ')&&/(条件|矩阵)/.test(line)?[{start:i,end:lines.findIndex((x,j)=>j>i&&x.startsWith('## '))}]:[]);
 text+=`\n## ${row.ticker} ${v}\n\n`+snippets.map(({start,end})=>lines.slice(start,end<0?lines.length:end).join('\n')).join('\n');
 result.push({ticker:row.ticker,version:v,matrices,hashes});
}}
fs.writeFileSync(path.join(dir,'两轮条件矩阵.md'),text);
fs.writeFileSync(path.join(dir,'提取数据.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify(result.map(x=>({ticker:x.ticker,version:x.version,matrixRows:x.matrices.length,base:x.matrices.find(r=>r.cells[0].startsWith('基准'))?.cells})),null,2));
