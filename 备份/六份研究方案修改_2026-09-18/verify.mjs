import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {RESEARCH_PLANS, bindResearchPlan, readResearchPlan, resolveCurrentPlan, planHash} from '../../tools/research-runner/research-plan-store.mjs';
import {industryDomain} from '../../tools/research-runner/domains/industry.mjs';
import {fileRunDomain} from '../../tools/research-runner/domains/file-run.mjs';
import {checkRequiredPaths} from '../../tools/research-runner/domains/index.mjs';
import {createOutputContract, validateOutputFilePath} from '../../tools/research-runner/validators/output-validator.mjs';

const base=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(base,'../..');
const published=JSON.parse(fs.readFileSync(path.join(base,'发布结果.json'),'utf8'));
const previous=JSON.parse(fs.readFileSync(path.join(base,'发布前绑定.json'),'utf8'));
const rows=[];
function cli(args, success=true){
  const result=spawnSync(process.execPath,['tools/research-runner/queue-tools.mjs',...args,'--dry-run'],{cwd:root,encoding:'utf8'});
  if(!success){assert.notEqual(result.status,0);return;}
  assert.equal(result.status,0,result.stderr||result.stdout);
  return JSON.parse(result.stdout.trim());
}
for(const p of published){
  const plan=RESEARCH_PLANS.find(x=>x.id===p.planId);
  assert.equal(resolveCurrentPlan(plan.directory),p.planFile);
  const item=plan.id==='industry'
    ? cli(['add-industry',`--subject=${industryDomain.parseIndexEntries()[0].subject}`])
    : cli(['add-file-run',`--run-id=plan-audit-${plan.id}`,`--prompt-file=${plan.directory}`]);
  assert.equal(item.planVersion,p.version);
  const domain=plan.id==='industry'?industryDomain:fileRunDomain;
  const contract=createOutputContract(item,domain);
  const prompt=domain.buildFormalPrompt(item,contract);
  const source=readResearchPlan(item);
  assert.ok(source.includes('实现概率'));
  assert.equal(prompt.includes('联合一致性检查'),false);
  assert.equal(prompt.includes('概率与反向条件检查'),false);
  assert.ok(prompt.includes(contract.expectedOutputFile||contract.expectedOutputDir));
  assert.ok(fs.existsSync(path.join(root,contract.expectedOutputDir)));
  assert.equal(planHash(fs.readFileSync(p.planFile)),item.planSha256);
  if(plan.id==='industry'){
    assert.ok(!prompt.includes('【行业名称】'));
    validateOutputFilePath({item,domain,outputFile:contract.expectedOutputFile});
    assert.throws(()=>validateOutputFilePath({item,domain,outputFile:'基本面/行业调研/产业背景/行业调研_测试_2026-09-18.md'}));
  }else{
    assert.equal(contract.expectedOutputDir,plan.defaultOutputDir);
    const filename=({
      'background-1':'AI产业链全局图谱与口径字典',
      'background-2':'AI产业链瓶颈与反证指标总表',
      'background-3':'全球AI需求与Token经济框架',
      'background-4':'行业调研_AI数据中心建设规模与产业链订单映射',
      'background-5':'行业调研_头部AI芯片全景与产能释放',
    })[plan.id]+'_2026-09-18.md';
    const exact=cli(['add-file-run',`--run-id=exact-${plan.id}`,`--prompt-file=${plan.directory}`,`--expected-output-file=${plan.defaultOutputDir}/${filename}`]);
    createOutputContract(exact,domain);
    cli(['add-file-run',`--run-id=outside-${plan.id}`,`--prompt-file=${plan.directory}`,'--expected-output-dir=基本面/行业调研/横向专题'],false);
    const alias=cli(['add-file-run',`--run-id=alias-${plan.id}`,`--prompt-file=${plan.directoryAliases[0]}`]);
    assert.equal(alias.planSha256,item.planSha256);
  }
  rows.push({id:plan.id,currentPlan:p.planFile,planVersion:item.planVersion,sha256:item.planSha256,inputResearchRoot:plan.id==='industry'?path.join(root,'基本面/行业调研/产业背景'):'无本地研究资料输入，仅外部资料',index:plan.id==='industry'?industryDomain.indexPath:null,outputContract:contract,promptChars:prompt.length});
}
for(const old of previous){
  const oldHash=old.planSha256;
  bindResearchPlan(old);
  assert.equal(planHash(Buffer.from(readResearchPlan(old),'utf8')),oldHash);
}
for(const plan of RESEARCH_PLANS)bindResearchPlan({domain:'file-run',promptFile:plan.directory});
checkRequiredPaths();
for(const relative of ['tools/queue.jsonl','tools/queue.done.jsonl','tools/research-runner/research-plans.json']){
  assert.equal(planHash(fs.readFileSync(path.join(root,relative))),fs.readFileSync(path.join(base,path.basename(relative)+'.sha256'),'utf8'));
}
assert.ok(fs.existsSync(path.join(root,'基本面/行业调研/产业背景')));
fs.writeFileSync(path.join(base,'路径与绑定验收.json'),JSON.stringify({plans:rows,oldBindingsPreserved:previous.length,registeredPlans:RESEARCH_PLANS.length,formalQueuesUnchanged:true,actualResearchExecuted:false},null,2));
console.log('PASS: 6 new plans via real CLI dry-run; 5 explicit outputs and outside-root rejection; aliases; old bound snapshots; all 11 registered plans; required paths; formal queues and registry unchanged. No research execution.');
