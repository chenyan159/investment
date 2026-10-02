import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { fileRunDomain } from '../../tools/research-runner/domains/file-run.mjs';
import { QUEUE_PATH } from '../../tools/research-runner/queue-store.mjs';

const root='D:/drive/Investment';
const promptFile='基本面/行业调研/研究方法/会议调研方案.md';
const body=fs.readFileSync(path.join(root,promptFile),'utf8').trim();
const expectedOutputDir='基本面/行业调研/产业背景/顶级会议信息';
const checks=['DAC','FMS','RSS','Farnborough'].map(name=>{
 const expectedOutputFile=`${expectedOutputDir}/conference_update_${name}_2026_2026-09-08.md`;
 const item=fileRunDomain.createQueueItem({runId:`single-entry-validation-${name}`,promptFile,expectedOutputDir,expectedOutputFile});
 fileRunDomain.validateQueueItem(item);
 const compiled=fileRunDomain.buildFormalPrompt(item,{expectedOutputDir,expectedOutputFile});
 assert.ok(compiled.startsWith(body));
 assert.ok(compiled.includes(expectedOutputFile));
 assert.equal(item.promptFile,promptFile);
 return {conference:name,promptFile,outputFileVisibleInCompiledPrompt:true,shapeValid:true};
});
const queue=QUEUE_PATH;
const entries=fs.readFileSync(queue,'utf8').split(/\r?\n/).filter(x=>x.trim()).map(x=>JSON.parse(x));
const stale=entries.filter(x=>String(x.promptFile??'').replaceAll('\\','/').includes('基本面/行业调研/研究方法/会议/'));
assert.equal(stale.length,0);
const result={checked_on:'2026-09-08',uniquePromptFiles:new Set(checks.map(x=>x.promptFile)).size,checks,activeQueueWithdrawnReferences:stale.length,queueWrites:false,researchRuns:false};
fs.writeFileSync(new URL('会议入口构建核验.json',import.meta.url),JSON.stringify(result,null,2)+'\n','utf8');
console.log(JSON.stringify(result,null,2));
