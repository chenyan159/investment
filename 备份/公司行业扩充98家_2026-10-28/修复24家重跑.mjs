import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readActiveQueue, readDoneQueue, writeActiveQueue, normalizeQueueItem, QUEUE_PATH, DONE_QUEUE_PATH, QUEUE_CONTROL_PATH, TOOL_DIR, PROJECT_ROOT, formatLocalIso } from '../../tools/research-runner/queue-store.mjs';
import { getDomainAdapter } from '../../tools/research-runner/domains/index.mjs';
import { bindResearchPlan } from '../../tools/research-runner/research-plan-store.mjs';
import { createOutputContract } from '../../tools/research-runner/validators/output-validator.mjs';

const prefix='expand98-20261028T080714822Z-5b5a1a07';
const target=new Set('MELI MA AXP JPM BAC MS SCHW BLK CME BRK.B AJG LLY JNJ ABBV MRK GILD MDT EW RMD UNH MCK HCA MDLZ CMG'.split(' '));
const lock=path.join(TOOL_DIR,'runner.lock');
if(fs.existsSync(lock)) {
  const {pid}=JSON.parse(fs.readFileSync(lock,'utf8'));
  let alive=true;
  try { process.kill(pid,0); } catch(e) { if(e.code==='ESRCH') alive=false; else throw e; }
  assert(!alive,`Runner PID ${pid} still exists`);
  const children=execFileSync('pwsh',['-NoProfile','-NonInteractive','-Command',`@(Get-CimInstance Win32_Process -Filter 'ParentProcessId = ${Number(pid)}').Count`],{encoding:'utf8'}).trim();
  assert.equal(children,'0','Runner children still exist');
}
const active=readActiveQueue(), done=readDoneQueue();
const failures=active.filter(x=>x.id.startsWith(prefix)&&x.domain==='company'&&target.has(x.subject)&&x.status==='failed');
assert.equal(failures.length,24,'Expected the original 24 failed companies; refuse repeated repair');
assert(failures.every(x=>x.attempts===7));
assert(!active.some(x=>x.note?.startsWith('codex_cleanup_unconfirmed:')),'Cleanup quarantine requires separate inspection');
const repairId='repair24-'+new Date().toISOString().replace(/[-:.]/g,'');
const backup=path.join(TOOL_DIR,'queue-backups',repairId);
fs.mkdirSync(backup,{recursive:true});
const hash=f=>createHash('sha256').update(fs.readFileSync(f)).digest('hex');
const beforeHashes={};
for(const file of [QUEUE_PATH,DONE_QUEUE_PATH,QUEUE_CONTROL_PATH,...(fs.existsSync(lock)?[lock]:[])]) {
  beforeHashes[path.basename(file)]=hash(file);
  fs.copyFileSync(file,path.join(backup,path.basename(file)));
}
const changed=[], recovered=[], added=[], reused=[];
const now=formatLocalIso(new Date());
for(const item of active) {
  const isTarget=failures.includes(item);
  if(!isTarget && item.status!=='running') continue;
  (isTarget?changed:recovered).push({id:item.id,domain:item.domain,subject:item.subject,previousStatus:item.status,previousAttempts:item.attempts,previousNote:item.note});
  item.repairHistory=[...(item.repairHistory||[]),{repairId,at:now,status:item.status,attempts:item.attempts,note:item.note}];
  item.status='retry_pending';
  item.outputFile=''; delete item.companionFile;
  item.startedAt='';item.finishedAt='';item.updatedAt=now;
  item.note=isTarget?'manual_retry: preserve 7 prior attempts; max-attempts now 12':'codex_sdk_interrupted_recovered: previous runner and children verified stopped';
}
for(const subject of target) for(const domain of ['company-investment-decision','company-comparison']) {
  const existing=active.filter(x=>x.domain===domain&&x.subject===subject&&x.status!=='done');
  assert(existing.length<=1,`Duplicate active task ${domain}/${subject}`);
  if(existing.length) { assert(['pending','retry_pending'].includes(existing[0].status));reused.push({domain,subject,id:existing[0].id});continue; }
  const adapter=getDomainAdapter(domain);
  const previous=done.filter(x=>x.domain===domain&&x.subject===subject&&x.id.startsWith(prefix)).at(-1);
  const item=bindResearchPlan(normalizeQueueItem({...adapter.createQueueItem({subject,sourceDate:'2026-10-28',status:'pending',id:`${repairId}-${domain}-${subject}`}),reasoningEffort:'max',repairBatchId:repairId,rerunOf:previous?.id||'',note:'用户要求：补齐公司调研后重跑对应下游；原完成记录保留。'}));
  active.push(item);added.push({id:item.id,domain,subject,rerunOf:item.rerunOf});
}
const ids=new Set(done.map(x=>x.id)), pairs=new Set(), outputs=new Set();
for(const item of active) {
  assert(!ids.has(item.id),`Duplicate id ${item.id}`);ids.add(item.id);
  const pair=`${item.domain}/${item.subject}`;assert(!pairs.has(pair),`Duplicate task ${pair}`);pairs.add(pair);
  bindResearchPlan({...item});
  const domain=getDomainAdapter(item.domain),entry=domain.resolveIndexEntry(item.subject);
  assert(entry&&entry.category===item.category,`Index mismatch ${pair}`);
  const contract=createOutputContract(item,domain);
  for(const f of [contract.expectedOutputFile,contract.expectedCompanionFile].filter(Boolean)) {assert(!outputs.has(f),`Output collision ${f}`);outputs.add(f);}
}
assert.equal(hash(QUEUE_PATH),beforeHashes['queue.jsonl'],'Active queue changed during repair');
assert.equal(hash(DONE_QUEUE_PATH),beforeHashes['queue.done.jsonl'],'Done queue changed during repair');
writeActiveQueue(active);
if(fs.existsSync(lock)) {assert.equal(hash(lock),beforeHashes['runner.lock']);fs.unlinkSync(lock);}
assert.equal(hash(DONE_QUEUE_PATH),beforeHashes['queue.done.jsonl']);
assert.equal(hash(QUEUE_CONTROL_PATH),beforeHashes['queue.control.json']);
const validation=execFileSync(process.execPath,[path.join(TOOL_DIR,'queue-tools.mjs'),'validate'],{cwd:PROJECT_ROOT,encoding:'utf8'}).trim();
const result={repairId,backup:path.relative(PROJECT_ROOT,backup).replaceAll('\\','/'),maxAttempts:12,remainingAttemptsPerFailedCompany:5,changed,recovered,added,reused,activeTotal:active.length,statusCounts:active.reduce((r,x)=>(r[x.status]=(r[x.status]||0)+1,r),{}),doneArchiveUnchanged:true,controlUnchanged:true,runnerStarted:false,validation,beforeHashes};
fs.writeFileSync(new URL('./重跑修复核验.json',import.meta.url),JSON.stringify(result,null,2)+'\n','utf8');
console.log(JSON.stringify({restored:changed.length,recovered:recovered.length,added:added.length,reused:reused.length,activeTotal:active.length,statusCounts:result.statusCounts,validation,backup:result.backup}));
