import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { companyInvestmentDecisionDomain as domain } from '../../domains/company-investment-decision.mjs';
import { appendActiveQueueItems, readActiveQueue, readDoneQueue, normalizeQueueItem } from '../../queue-store.mjs';

const backup = 'D:/drive/Investment/备份/情景投资早期机会年度概率_20260907-163146';
const manifestPath = path.join(backup, 'batch.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const entries = domain.parseIndexEntries();
const source = fs.readFileSync(domain.promptPath, 'utf8');
const active = readActiveQueue();
if (fs.existsSync('D:/drive/Investment/tools/research-runner/runner.lock')) throw new Error('Runner state changed; recheck before queue mutation.');
if (active.some(x => ['pending','running','retry_pending'].includes(x.status))) throw new Error('Active queue changed; inspect before appending.');
const oldIds = new Set([...active,...readDoneQueue()].map(x=>x.id));
const items = entries.map(entry => normalizeQueueItem(domain.createQueueItem({
  ...entry, id: `${manifest.batchId}-${entry.subject.replace(/[^A-Za-z0-9._-]/g,'_')}`,
  sourceDate: '2026-09-07', extra: { reasoningEffort:'high' }
})));
const ids = new Set(items.map(x=>x.id));
const outputs = items.map(x=>domain.expectedOutputFile(x,'2026-09-07'));
if (ids.size!==entries.length || new Set(outputs).size!==entries.length) throw new Error('Duplicate IDs or formal output targets.');
if (items.some(x=>oldIds.has(x.id))) throw new Error('Batch already exists.');
for (const x of items) {
  const expectedOutputFile = domain.expectedOutputFile(x,'2026-09-07');
  const prompt = domain.buildFormalPrompt(x, {expectedOutputFile});
  const prefix = source.replaceAll(domain.placeholder,x.subject).replaceAll('<公司股票代号>',x.subject).trim();
  if (!prompt.startsWith(prefix) || !prompt.includes('早期机会的逐年概率与期望贡献') || prompt.includes(domain.placeholder)) throw new Error(`Prompt preflight failed ${x.subject}`);
}
const categories={};for(const x of items) categories[x.category]=(categories[x.category]||0)+1;
manifest.planSha256=crypto.createHash('sha256').update(fs.readFileSync(domain.promptPath)).digest('hex');
manifest.tasks=items.map((x,i)=>({id:x.id,subject:x.subject,category:x.category,expectedOutputFile:outputs[i]}));
manifest.categories=categories;
manifest.preflight={companies:entries.length,uniqueOutputs:new Set(outputs).size,allPromptPrefixesExact:true,reasoning:'high'};
fs.copyFileSync(domain.promptPath,path.join(backup,'研究方案_修改后.md'));
fs.writeFileSync(path.join(backup,'待加入队列.json'),JSON.stringify(items,null,2));
if (process.argv.includes('--apply')) {
  appendActiveQueueItems(items);
  manifest.enqueuedAt=new Date().toISOString();
}
fs.writeFileSync(manifestPath,JSON.stringify(manifest,null,2));
console.log(JSON.stringify({applied:process.argv.includes('--apply'),...manifest.preflight,categories},null,2));
