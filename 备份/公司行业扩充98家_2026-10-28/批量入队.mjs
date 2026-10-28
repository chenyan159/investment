import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash, randomUUID } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { getDomainAdapter } from '../../tools/research-runner/domains/index.mjs';
import { bindResearchPlan } from '../../tools/research-runner/research-plan-store.mjs';
import {
  appendActiveQueueItems, readActiveQueue, readDoneQueue, normalizeQueueItem,
  DEFAULT_REASONING_EFFORT, QUEUE_PATH, DONE_QUEUE_PATH, QUEUE_CONTROL_PATH,
  PROJECT_ROOT, TOOL_DIR, safeIdPart,
} from '../../tools/research-runner/queue-store.mjs';
import { createOutputContract } from '../../tools/research-runner/validators/output-validator.mjs';
import { CODEX_MODEL } from '../../tools/research-runner/runtime-config.mjs';

const directory = path.dirname(fileURLToPath(import.meta.url));
const reportPath = path.join(directory, '入队核验.json');
const sourceDate = '2026-10-28';
const batchId = `expand98-${new Date().toISOString().replace(/[-:.]/g, '')}-${randomUUID().slice(0, 8)}`;
const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8').replace(/^\uFEFF/u, ''));
const hash = (file) => createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const relative = (file) => path.relative(PROJECT_ROOT, file).replaceAll('\\', '/');
const assert = (condition, message) => { if (!condition) throw new Error(message); };
const industryRows = readJson(path.join(directory, '行业入队映射.json'));
const companies = readJson(path.join(PROJECT_ROOT, '备份', '纳指100与标普500新增98家公司候选_2026-10-28', '候选公司.json'));
assert(industryRows.length === 27, 'Expected 27 industries');
assert(companies.length === 98, 'Expected 98 companies');
assert(new Set(industryRows.map((row) => row.subject)).size === 27, 'Duplicate industry subjects');
assert(new Set(companies.map((row) => row.ticker.toUpperCase())).size === 98, 'Duplicate company tickers');
assert(!fs.existsSync(path.join(TOOL_DIR, 'runner.lock')), 'Runner lock exists; do not enqueue during this batch operation');
const activeBefore = readActiveQueue();
const doneBefore = readDoneQueue();
assert(activeBefore.length === 0, 'Expected empty active queue; refusing to merge unknown work');
const allIds = new Set([...activeBefore, ...doneBefore].map((item) => item.id));
const pairKeys = new Set();
const outputPaths = new Set();
const contracts = [];
const items = [];
const add = (domain, subject, sourceKey, expectedCategory = '') => {
  const adapter = getDomainAdapter(domain);
  const entry = adapter.resolveIndexEntry(subject);
  assert(entry, `Subject missing from index: ${domain} ${subject}`);
  assert(entry.category, `Empty indexed category: ${subject}`);
  if (expectedCategory) assert(entry.category === expectedCategory, `Mapping category mismatch: ${subject}`);
  const item = bindResearchPlan(normalizeQueueItem({
    ...adapter.createQueueItem({
      subject, sourceDate, status: 'pending', id: `${batchId}-${domain}-${safeIdPart(sourceKey)}`,
    }),
    reasoningEffort: DEFAULT_REASONING_EFFORT,
    batchId,
  }));
  assert(item.category === entry.category, `Queue category mismatch: ${subject}`);
  for (const allowed of [adapter.allowedCategories, adapter.companyCategories]) {
    if (allowed?.size) assert(allowed.has(item.category), `Unsupported ${domain} category: ${item.category}`);
  }
  const pair = `${domain}:${subject.toUpperCase()}`;
  assert(!pairKeys.has(pair), `Duplicate domain/subject: ${pair}`);
  assert(!allIds.has(item.id), `Duplicate queue ID: ${item.id}`);
  pairKeys.add(pair);
  allIds.add(item.id);
  assert(item.planSnapshotFile && item.planSha256 && item.planVersion, `Unbound research plan: ${pair}`);
  const contract = createOutputContract(item, adapter);
  for (const output of [contract.expectedOutputFile, contract.expectedCompanionFile].filter(Boolean)) {
    assert(!outputPaths.has(output), `Conflicting output path: ${output}`);
    outputPaths.add(output);
  }
  contracts.push({ id: item.id, domain, subject, category: item.category, ...contract });
  items.push(item);
};
for (const row of industryRows) add('industry', row.subject, row.id, row.category);
for (const domain of ['company', 'company-investment-decision', 'company-comparison']) {
  for (const row of companies) add(domain, row.ticker, row.ticker);
}
assert(items.length === 321, 'Expected 321 queue items');
const beforeHashes = Object.fromEntries([QUEUE_PATH, DONE_QUEUE_PATH, QUEUE_CONTROL_PATH].map((file) => [relative(file), hash(file)]));
const backupDirectory = path.join(TOOL_DIR, 'queue-backups', batchId);
fs.mkdirSync(backupDirectory, { recursive: false });
for (const file of [QUEUE_PATH, DONE_QUEUE_PATH, QUEUE_CONTROL_PATH]) {
  const destination = path.join(backupDirectory, path.basename(file));
  fs.copyFileSync(file, destination, fs.constants.COPYFILE_EXCL);
  assert(hash(destination) === hash(file), `Backup hash mismatch: ${file}`);
}
fs.writeFileSync(path.join(backupDirectory, 'manifest.json'), JSON.stringify({ batchId, createdAt: new Date().toISOString(), beforeHashes }, null, 2) + '\n');
assert(!fs.existsSync(path.join(TOOL_DIR, 'runner.lock')), 'Runner started before append; aborting');
for (const file of [QUEUE_PATH, DONE_QUEUE_PATH, QUEUE_CONTROL_PATH]) assert(hash(file) === beforeHashes[relative(file)], `Queue state changed before append: ${file}`);
appendActiveQueueItems(items);
const activeAfter = readActiveQueue();
assert(activeAfter.length === 321 && activeAfter.every((item) => item.batchId === batchId && item.status === 'pending'), 'Appended queue state differs from prepared batch');
assert(hash(DONE_QUEUE_PATH) === beforeHashes[relative(DONE_QUEUE_PATH)], 'Done archive changed');
assert(hash(QUEUE_CONTROL_PATH) === beforeHashes[relative(QUEUE_CONTROL_PATH)], 'Concurrency control changed');
let validationOutput;
let validationSuccess = false;
try {
  validationOutput = execFileSync(process.execPath, [path.join(TOOL_DIR, 'queue-tools.mjs'), 'validate'], { cwd: PROJECT_ROOT, encoding: 'utf8' }).trim();
  validationSuccess = true;
} catch (error) {
  validationOutput = String(error.stdout || '') + String(error.stderr || error.message);
}
const counts = Object.fromEntries(['industry', 'company', 'company-investment-decision', 'company-comparison'].map((domain) => [domain, activeAfter.filter((item) => item.domain === domain).length]));
const plans = Object.fromEntries([...new Set(items.map((item) => item.domain))].map((domain) => {
  const item = items.find((item) => item.domain === domain);
  return [domain, { version: item.planVersion, snapshot: item.planSnapshotFile, sha256: item.planSha256 }];
}));
const report = {
  batchId, createdAt: new Date().toISOString(), sourceDate, pendingTotal: activeAfter.length,
  counts, uniqueIds: new Set(activeAfter.map((item) => item.id)).size,
  uniqueDomainSubjects: pairKeys.size, uniqueOutputPaths: outputPaths.size,
  modelAtEnqueue: CODEX_MODEL, modelBinding: 'runner runtime default; per-item model is not pinned',
  reasoningEffort: DEFAULT_REASONING_EFFORT, plans,
  queueBackup: relative(backupDirectory), beforeHashes,
  afterHashes: Object.fromEntries([QUEUE_PATH, DONE_QUEUE_PATH, QUEUE_CONTROL_PATH].map((file) => [relative(file), hash(file)])),
  archiveUnchanged: true, concurrencyUnchanged: true, runnerStarted: false,
  validationSuccess, validationOutput,
  scheduler: 'industry -> company -> company-investment-decision -> company-comparison; pending/running/retry_pending block lower-priority domains; failed does not block downstream',
  outputContracts: contracts,
};
fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({ batchId, counts, pendingTotal: report.pendingTotal, validationSuccess, validationOutput, report: relative(reportPath), queueBackup: report.queueBackup }, null, 2));
assert(validationSuccess, 'Queue validation failed; see saved report');
