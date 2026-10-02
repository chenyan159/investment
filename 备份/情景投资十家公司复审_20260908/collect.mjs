import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
const root='D:/drive/Investment';
const dir=path.join(root,'备份/情景投资十家公司复审_20260908');
const tickers=['SOMMY','PSIX','ET','SPACEX','GOOGL','MU','CRWV','SNDK','AVGO','CRDO'];
const read=p=>fs.readFileSync(p,'utf8');
const jsonl=p=>read(p).split(/\r?\n/).filter(Boolean).map(x=>JSON.parse(x));
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const logs=jsonl(path.join(root,'tools/research-runner/logs/current.jsonl'));
const done=jsonl(path.join(root,'tools/queue.done.jsonl'));
const manifest=[], structure={};
for(const v of ['新报告','旧报告','运行提示词']) fs.mkdirSync(path.join(dir,v),{recursive:true});
for(const t of tickers){
 const job=done.findLast(x=>x.domain==='company-investment-decision'&&x.subject===t&&x.id.startsWith('company-investment-decision-')&&x.createdAt.startsWith('2026-09-08T00:58'));
 if(!job) throw new Error(t);
 const claimed=logs.find(x=>x.id===job.id&&x.event.startsWith('Claimed '));
 const prep=logs.find(x=>x.event===`Prepared company-investment-decision/${t} formal run.`);
 const prev=done.filter(x=>x.domain===job.domain&&x.subject===t&&x.id!==job.id).at(-1);
 const oldPath=path.join(root,prep.files[0].to), newPath=path.join(root,job.outputFile);
 const snapshots={};
 for(const [version,source] of [['新报告',newPath],['旧报告',oldPath]]){
  const target=path.join(dir,version,t+'.md'); fs.copyFileSync(source,target);
  const content=read(target),lines=content.split(/\r?\n/);
  structure[`${t}/${version}`]={characters:content.length,bytes:fs.statSync(target).size,lines:lines.length,codeCharacters:[...content.matchAll(/```[^\n]*\n[\s\S]*?```/g)].reduce((n,m)=>n+m[0].length,0),headings:lines.flatMap((text,i)=>/^#{1,5} /.test(text)?[{line:i+1,text}]:[])};
  snapshots[version]={source,target,sha256:hash(target)};
 }
 const prompt=path.join(dir,'运行提示词',t+'.md');fs.copyFileSync(claimed.promptDebug,prompt);
 const body=read(prompt).split('\n\n').slice(0,-1).join('\n\n');
 manifest.push({ticker:t,job,previousJob:prev,model:claimed.model,prompt:claimed.promptDebug,promptSha256:hash(prompt),minutes:(new Date(job.finishedAt)-new Date(job.startedAt))/60000,snapshots});
}
fs.copyFileSync(path.join(root,'分析报告/公司情景投资决策/研究方案.md'),path.join(dir,'新研究方案.md'));
fs.copyFileSync(path.join(root,'分析报告/公司情景投资决策/备份/研究方案_2026-09-08_004726_证据裁决与投资论点调整前.md'),path.join(dir,'旧研究方案_八家对照.md'));
fs.writeFileSync(path.join(dir,'manifest.json'),JSON.stringify(manifest,null,2));
fs.writeFileSync(path.join(dir,'structure.json'),JSON.stringify(structure,null,2));
fs.writeFileSync(path.join(dir,'运行记录.jsonl'),logs.filter(x=>manifest.some(m=>m.job.id===x.id)||/^Prepared company-investment-decision/.test(x.event)).map(x=>JSON.stringify(x)).join('\n'));
console.log(JSON.stringify(manifest.map(m=>({ticker:m.ticker,status:m.job.status,attempts:m.job.attempts,minutes:m.minutes,oldId:m.previousJob.id,newBytes:fs.statSync(m.snapshots['新报告'].target).size,oldBytes:fs.statSync(m.snapshots['旧报告'].target).size})),null,2));
