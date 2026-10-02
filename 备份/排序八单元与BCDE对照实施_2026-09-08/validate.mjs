import fs from 'node:fs';
import assert from 'node:assert/strict';
import { selectEvaluatedCompanies } from '../../分析报告/公司排序/生成站点数据_公司池.mjs';
import { fileRunDomain } from '../../tools/research-runner/domains/file-run.mjs';
import { QUEUE_PATH } from '../../tools/research-runner/queue-store.mjs';
const root='D:/drive/Investment';
const manifest=JSON.parse(fs.readFileSync(new URL('新方案清单.json',import.meta.url),'utf8'));
assert.deepEqual(selectEvaluatedCompanies([{ticker:'A'},{ticker:'B'},{ticker:'NEW'}],['A','B','A'],2),[{ticker:'A'},{ticker:'B'}]);
assert.throws(()=>selectEvaluatedCompanies([{ticker:'A'}],['A','B'],2),/缺少索引身份/);
assert.throws(()=>selectEvaluatedCompanies([{ticker:'A'}],['A','B'],3),/数量不符/);
assert.throws(()=>selectEvaluatedCompanies([{ticker:'A'},{ticker:'A'}],['A'],1),/重复证券/);
const shape=[];
for(const [i,r] of manifest.created.entries()){
 const item=fileRunDomain.createQueueItem({runId:`sorting-config-check-${i}`,promptFile:r.prompt_file,expectedOutputDir:r.expected_output_dir,expectedOutputFile:r.expected_output_file});
 fileRunDomain.validateQueueItem(item);
 const prompt=fileRunDomain.buildFormalPrompt(item,{expectedOutputDir:r.expected_output_dir,expectedOutputFile:r.expected_output_file});
 assert.ok(prompt.includes(r.expected_output_file));
 assert.ok(!fs.existsSync(`${root}/${r.expected_output_file}`));
 shape.push({promptFile:r.prompt_file,valid:true});
}
const active=fs.readFileSync(QUEUE_PATH,'utf8').split(/\r?\n/).filter(x=>x.trim()).map(x=>JSON.parse(x)).filter(x=>x.domain==='file-run' && String(x.promptFile).includes('公司排序'));
assert.equal(active.length,0,'An active sorting task requires separate reconciliation');
const site=JSON.parse(fs.readFileSync(`${root}/分析报告/公司排序/站点数据/current.json`,'utf8'));
assert.equal(site.defaultRunKey,'01');assert.equal(site.publicationPolicy.consensusMethodCount,5);
assert.ok(!site.runs['03']&&!site.runs['05']);
assert.equal(site.publicationPolicy.publishedMethodCount,8);
for(const run of Object.values(site.runs)){assert.equal(run.rows.length,192);assert.ok(!run.planPath.includes('2026-09-08'));}
const result={companyPoolRegressionChecks:4,fileRunPromptChecks:shape.length,activeSortingTasks:active.length,siteDefault:site.defaultRunKey,sitePublishedMethods:8,sitePublishedLists:10,consensusFamilies:5,oldResultCompanyCount:192,queueWrites:false,researchRuns:false,checks:shape};
fs.writeFileSync(new URL('执行与展示核验.json',import.meta.url),JSON.stringify(result,null,2)+'\n','utf8');
console.log(JSON.stringify({...result,checks:undefined}));
