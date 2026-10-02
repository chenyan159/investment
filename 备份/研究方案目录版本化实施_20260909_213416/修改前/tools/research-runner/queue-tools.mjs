#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { getDomainAdapter } from "./domains/index.mjs";
import { migrateLegacyCompanyMarkdownQueue } from "./domains/company.mjs";
import { featureQuantizationDomain } from "./domains/feature-quantization.mjs";
import { fileRunDomain } from "./domains/file-run.mjs";
import { industryDomain } from "./domains/industry.mjs";
import { updateIndexForQueueAdd } from "./index-updater.mjs";
import {
  appendActiveQueueItems,
  archiveDoneItems,
  DEFAULT_REASONING_EFFORT,
  DONE_QUEUE_PATH,
  formatLocalDate,
  FUNDAMENTAL_ROOT,
  normalizeProjectPath,
  normalizeQueueItem,
  normalizeReasoningEffort,
  PROJECT_ROOT,
  QUEUE_CONTROL_PATH,
  QUEUE_PATH,
  readActiveQueue,
  readDoneQueue,
  readQueueControl,
  safeIdPart,
  summarizeQueues,
  writeActiveQueue,
  writeDoneQueue,
} from "./queue-store.mjs";
import { validateOutputFilePath } from "./validators/output-validator.mjs";
import { featureIdentityFromStem } from "./domains/feature-contract.mjs";

function printHelp() {
  console.log(`Usage: node queue-tools.mjs <command> [options]

Commands:
  status                       Print a queue summary and the configured runtime concurrency.
  archive-done                 Move status=done items from queue.jsonl to queue.done.jsonl.
  validate                     Validate active queue shape, domain support, and index/category consistency.
  add-company                  Append one company item. Requires indexed --subject/--ticker unless --update-index is used.
  add-company-comparison       Append one company-comparison item. Requires indexed --subject/--ticker.
  add-company-investment-decision
                               Append one company investment-decision item. Requires indexed --subject/--ticker.
  add-company-sentiment        Append one company sentiment item. Requires indexed --subject/--ticker.
  add-industry                 Append one industry item. Requires indexed --subject unless --update-index is used.
  add-feature-quantization     Append one feature-quantization item. Requires --subject.
  add-file-run                 Append one generic file-run item. Requires --run-id and --prompt-file.
  seed-industry-from-index     Append industry items from 基本面/行业调研/行业索引.md. Defaults to missing-only.
  seed-feature-quantization-from-plans
                               Append feature-quantization items from 基本面/特征量化/研究方案/*.md. Defaults to missing-only.
  migrate-company-md           Legacy: convert 基本面/公司调研/queue.md into queue.jsonl and queue.done.jsonl.

Options:
  --subject=VALUE              Queue subject.
  --ticker=TICKER              Alias for --subject on company ticker commands.
  --display-name=VALUE         Queue display name override.
  --category=VALUE             Queue category override or seed filter.
  --source-date=YYYY-MM-DD     Source date. Default today.
  --status=STATUS              Initial status. Default pending.
  --id=ID                      Queue id override.
  --output-file=PATH           Output path for migrated/manual items.
  --run-id=VALUE               file-run run id.
  --prompt-file=PATH           file-run prompt file, relative to Investment root or absolute inside it.
  --expected-output-dir=PATH   file-run output directory; defaults to the prompt file directory.
  --expected-output-file=PATH  Optional exact file-run output file; preferred for new tasks.
  --reasoning=LEVEL            Formal Codex reasoning: low, medium, high, xhigh, max, or ultra. Default ${DEFAULT_REASONING_EFFORT}.
  --reasoning-effort=LEVEL     Alias for --reasoning.
  --update-index               add-company/add-industry: add the subject to the domain index before enqueueing.
  --all                        seed-industry-from-index: include existing subjects too.
  --dry-run                    Print planned seed/add items without writing.
  --force                      Allow migrate-company-md to overwrite existing queue JSONL files.
  -h, --help                   Show this help.
`);
}

function parseArgs(argv) {
  const [command, ...rest] = argv;
  const options = {
    all: false,
    dryRun: false,
    force: false,
    subject: "",
    displayName: "",
    category: "",
    sourceDate: formatLocalDate(new Date()),
    status: "pending",
    id: "",
    outputFile: "",
    runId: "",
    promptFile: "",
    expectedOutputDir: "",
    expectedOutputFile: "",
    reasoningEffort: DEFAULT_REASONING_EFFORT,
    updateIndex: false,
  };

  for (const arg of rest) {
    if (arg === "--all") options.all = true;
    else if (arg === "--dry-run") options.dryRun = true;
    else if (arg === "--force") options.force = true;
    else if (arg.startsWith("--subject=")) options.subject = arg.slice("--subject=".length).trim();
    else if (arg.startsWith("--ticker=")) options.subject = arg.slice("--ticker=".length).trim();
    else if (arg.startsWith("--display-name=")) options.displayName = arg.slice("--display-name=".length).trim();
    else if (arg.startsWith("--category=")) options.category = arg.slice("--category=".length).trim();
    else if (arg.startsWith("--source-date=")) options.sourceDate = arg.slice("--source-date=".length).trim();
    else if (arg.startsWith("--status=")) options.status = arg.slice("--status=".length).trim();
    else if (arg.startsWith("--id=")) options.id = arg.slice("--id=".length).trim();
    else if (arg.startsWith("--output-file=")) options.outputFile = arg.slice("--output-file=".length).trim();
    else if (arg.startsWith("--run-id=")) options.runId = arg.slice("--run-id=".length).trim();
    else if (arg.startsWith("--prompt-file=")) options.promptFile = arg.slice("--prompt-file=".length).trim();
    else if (arg.startsWith("--expected-output-dir=")) options.expectedOutputDir = arg.slice("--expected-output-dir=".length).trim();
    else if (arg.startsWith("--expected-output-file=")) options.expectedOutputFile = arg.slice("--expected-output-file=".length).trim();
    else if (arg.startsWith("--reasoning=")) options.reasoningEffort = arg.slice("--reasoning=".length).trim();
    else if (arg.startsWith("--reasoning-effort=")) options.reasoningEffort = arg.slice("--reasoning-effort=".length).trim();
    else if (arg === "--update-index") options.updateIndex = true;
    else if (arg === "-h" || arg === "--help") options.help = true;
    else throw new Error(`Unknown argument: ${arg}`);
  }

  options.reasoningEffort = normalizeReasoningEffort(options.reasoningEffort, "--reasoning");
  return { command, options };
}

function main() {
  const { command, options } = parseArgs(process.argv.slice(2));

  if (!command || command === "-h" || command === "--help" || options.help) {
    printHelp();
    return;
  }

  if (command === "status") {
    printStatus();
    return;
  }

  if (command === "archive-done") {
    const result = archiveDoneItems();
    console.log(`Archived done items: ${result.archived}`);
    console.log(`Duplicate done items removed from active queue: ${result.duplicateDone}`);
    console.log(`Active items remaining: ${result.activeRemaining}`);
    console.log(`Done archive total: ${result.doneTotal}`);
    return;
  }

  if (command === "validate") {
    const result = validateQueues();
    printValidation(result);
    if (result.errors.length) process.exitCode = 1;
    return;
  }

  if (command === "add-company") {
    addOne("company", options);
    return;
  }

  if (command === "add-company-comparison") {
    addOne("company-comparison", options);
    return;
  }

  if (command === "add-company-investment-decision") {
    addOne("company-investment-decision", options);
    return;
  }

  if (command === "add-company-sentiment") {
    addOne("company-sentiment", options);
    return;
  }

  if (command === "add-industry") {
    addOne("industry", options);
    return;
  }

  if (command === "add-feature-quantization") {
    addOne("feature-quantization", options);
    return;
  }

  if (command === "add-file-run") {
    addFileRun(options);
    return;
  }

  if (command === "seed-industry-from-index") {
    seedIndustryFromIndex(options);
    return;
  }

  if (command === "seed-feature-quantization-from-plans") {
    seedFeatureQuantizationFromPlans(options);
    return;
  }

  if (command === "migrate-company-md") {
    migrateCompanyMarkdownQueue(options);
    return;
  }

  throw new Error(`Unknown command: ${command}`);
}

function printStatus() {
  const result = summarizeQueues();
  console.log(`Active queue: ${QUEUE_PATH}`);
  console.log(`Done archive: ${DONE_QUEUE_PATH}`);
  console.log(`Queue control: ${QUEUE_CONTROL_PATH}`);
  try {
    const control = readQueueControl();
    const configured = control
      ? (control.concurrency === 0
        ? "0 (new queue claims disabled; runner exits after current tasks finish)"
        : control.concurrency)
      : "(not initialized; runner will create it on next non-dry launch)";
    console.log(`Configured concurrency: ${configured}`);
  } catch (error) {
    console.log(`Configured concurrency: invalid (${error.message})`);
  }
  console.log(`Active items: ${result.activeCount}`);
  console.log(`Archived done items: ${result.doneCount}`);
  for (const status of ["pending", "running", "retry_pending", "failed", "done_active", "done_archived"]) {
    console.log(`${status}: ${result.counts[status] || 0}`);
  }
  printDomainCounts();
  printItems("Running", result.running);
  printItems("Retry pending", result.retryPending);
  printItems("Failed", result.failed);
  printItems("Latest done", result.latestDone);
}

function printDomainCounts() {
  const all = [...readActiveQueue(), ...readDoneQueue()];
  const counts = {};
  for (const item of all) {
    counts[item.domain] = (counts[item.domain] || 0) + 1;
  }
  console.log("domains:");
  for (const [domain, count] of Object.entries(counts)) {
    console.log(`  ${domain}: ${count}`);
  }
  if (!Object.keys(counts).length) console.log("  (none)");
}

function addOne(domain, options) {
  const adapter = getDomainAdapter(domain);
  if (!options.subject) throw new Error(`${adapter.label} queue item requires --subject`);

  const entry = adapter.resolveIndexEntry(options.subject);
  if (adapter.requiresIndexedSubject && !entry && !options.updateIndex) {
    throw new Error(`${adapter.label} subject is not in index: ${options.subject}`);
  }

  const item = normalizeNewQueueItem(adapter.createQueueItem({
    subject: options.subject,
    displayName: options.displayName,
    category: options.category,
    sourceDate: options.sourceDate,
    status: options.status,
    id: options.id,
    outputFile: options.outputFile,
  }), options);
  validateCategory(adapter, item.category);
  if (!options.dryRun) ensureNoDuplicateIds([item]);

  let indexUpdate = null;
  if (options.updateIndex) {
    indexUpdate = updateIndexForQueueAdd(domain, options);
  }

  if (options.dryRun) {
    if (indexUpdate) console.log(JSON.stringify({ indexUpdate }));
    console.log(JSON.stringify(item));
    return;
  }

  appendActiveQueueItems([item]);
  if (indexUpdate) {
    console.log(`Index ${indexUpdate.changed ? "updated" : "unchanged"}: ${normalizeProjectPath(path.relative(PROJECT_ROOT, indexUpdate.indexPath))} | ${indexUpdate.subject} | ${indexUpdate.category}`);
  }
  console.log(`Added ${domain} item: ${item.id} | ${item.subject} | ${item.category || "(no category)"} | reasoning=${item.reasoningEffort}`);
}

function addFileRun(options) {
  const item = normalizeNewQueueItem(fileRunDomain.createQueueItem({
    runId: options.runId,
    promptFile: options.promptFile,
    expectedOutputDir: options.expectedOutputDir,
    expectedOutputFile: options.expectedOutputFile,
    displayName: options.displayName,
    category: options.category,
    sourceDate: options.sourceDate,
    status: options.status,
    id: options.id,
    outputFile: options.outputFile,
  }), options);
  validateCategory(fileRunDomain, item.category);
  fileRunDomain.validateQueueItem(item);
  if (!options.dryRun) ensureNoDuplicateIds([item]);

  if (options.dryRun) {
    console.log(JSON.stringify(item));
    return;
  }

  appendActiveQueueItems([item]);
  console.log(`Added file-run item: ${item.id} | ${item.runId} | ${item.promptFile} | output=${item.expectedOutputFile || item.expectedOutputDir} | reasoning=${item.reasoningEffort}`);
}

function seedIndustryFromIndex(options) {
  if (options.category) validateCategory(industryDomain, options.category);
  const active = readActiveQueue();
  const done = readDoneQueue();
  const existingSubjects = new Set([...active, ...done]
    .filter((item) => item.domain === "industry")
    .map((item) => item.subject));

  const entries = industryDomain.parseIndexEntries()
    .filter((entry) => !options.category || entry.category === options.category)
    .filter((entry) => options.all || !existingSubjects.has(entry.subject));

  const items = entries.map((entry) => normalizeNewQueueItem(industryDomain.createQueueItem({
    id: options.all ? "" : `industry-${safeIdPart(entry.subject)}`,
    subject: entry.subject,
    displayName: entry.displayName,
    category: entry.category,
    sourceDate: options.sourceDate,
    status: options.status,
  }), options));

  if (options.dryRun) {
    for (const item of items) console.log(JSON.stringify(item));
    console.log(`Planned industry items: ${items.length}`);
    return;
  }

  ensureNoDuplicateIds(items);
  appendActiveQueueItems(items);
  console.log(`Seeded industry items: ${items.length}`);
}

function seedFeatureQuantizationFromPlans(options) {
  const active = readActiveQueue();
  const done = readDoneQueue();
  const existingFeatureIds = new Set([...active, ...done]
    .filter((item) => item.domain === "feature-quantization")
    .map((item) => featureIdentityFromStem(item.subject)?.featureId)
    .filter(Boolean));

  const entries = featureQuantizationDomain.parseIndexEntries()
    .filter((entry) => options.all || !existingFeatureIds.has(featureIdentityFromStem(entry.subject)?.featureId));

  const items = entries.map((entry) => normalizeNewQueueItem(featureQuantizationDomain.createQueueItem({
    id: options.all ? "" : `feature-quantization-${safeIdPart(entry.subject)}`,
    subject: entry.subject,
    displayName: entry.displayName,
    category: entry.category,
    sourceDate: options.sourceDate,
    status: options.status,
  }), options));

  if (options.dryRun) {
    for (const item of items) console.log(JSON.stringify(item));
    console.log(`Planned feature-quantization items: ${items.length}`);
    return;
  }

  ensureNoDuplicateIds(items);
  appendActiveQueueItems(items);
  console.log(`Seeded feature-quantization items: ${items.length}`);
}

function migrateCompanyMarkdownQueue(options) {
  const oldQueuePath = path.join(FUNDAMENTAL_ROOT, "公司调研", "queue.md");
  if (!fs.existsSync(oldQueuePath)) throw new Error(`Legacy company queue does not exist: ${oldQueuePath}`);

  const activeExists = readActiveQueue().length > 0;
  const doneExists = readDoneQueue().length > 0;
  if (!options.force && (activeExists || doneExists)) {
    throw new Error("queue.jsonl or queue.done.jsonl already contains data. Re-run with --force to overwrite.");
  }

  const result = migrateLegacyCompanyMarkdownQueue({ oldQueuePath, force: options.force });
  writeActiveQueue(result.active);
  writeDoneQueue(result.done);
  console.log("Migrated company queue from 基本面/公司调研/queue.md");
  console.log(`Active queue: ${QUEUE_PATH}`);
  console.log(`Done archive: ${DONE_QUEUE_PATH}`);
  console.log(`Active items: ${result.active.length}`);
  console.log(`Done archive items: ${result.done.length}`);
}

function validateQueues() {
  const active = readActiveQueue();
  const errors = [];
  const warnings = [];
  const seenIds = new Map();

  validateActiveItems(active, errors, warnings, seenIds);

  return { active: active.length, errors, warnings };
}

function validateActiveItems(items, errors, warnings, seenIds) {
  for (const [index, item] of items.entries()) {
    const label = `active:${index + 1}:${item.id}`;

    if (seenIds.has(item.id)) {
      errors.push(`${label} duplicates id already seen at ${seenIds.get(item.id)}`);
    } else {
      seenIds.set(item.id, label);
    }

    let adapter = null;
    try {
      adapter = getDomainAdapter(item.domain);
    } catch (error) {
      errors.push(`${label} ${error.message}`);
      continue;
    }

    if (item.status === "archived") {
      errors.push(`${label} active queue item must not have status=archived`);
    }

    const entry = adapter.resolveIndexEntry(item.subject);
    if (!entry) {
      const message = `${label} subject not found in ${adapter.label} index: ${item.subject}`;
      if (adapter.requiresIndexedSubject) errors.push(message);
      else warnings.push(message);
    } else if (item.category && entry.category && item.category !== entry.category) {
      errors.push(`${label} category mismatch: queue=${item.category}, index=${entry.category}`);
    }

    if (item.category) validateCategory(adapter, item.category, `${label} `, errors);

    if (typeof adapter.validateQueueItem === "function") {
      try {
        adapter.validateQueueItem(item);
      } catch (error) {
        errors.push(`${label} ${error.message}`);
      }
    }

    if (item.outputFile) {
      try {
        validateOutputFilePath({
          domain: adapter,
          item,
          outputFile: normalizeProjectPath(item.outputFile),
          originalOutputFile: item.outputFile,
        });
      } catch (error) {
        errors.push(`${label} ${error.message}`);
      }

    } else if (item.status === "done") {
      errors.push(`${label} done item has empty outputFile`);
    }
  }
}

function validateCategory(adapter, category, prefix = "", errors = null) {
  if (!category || !adapter.allowedCategories?.size) return;
  if (!adapter.allowedCategories.has(category)) {
    const message = `${prefix}unsupported ${adapter.domain} category: ${category}`;
    if (errors) errors.push(message);
    else throw new Error(message);
  }
}

function normalizeNewQueueItem(item, options) {
  return normalizeQueueItem({
    ...item,
    reasoningEffort: options.reasoningEffort,
  });
}

function ensureNoDuplicateIds(newItems) {
  const existingIds = new Set([...readActiveQueue(), ...readDoneQueue()].map((item) => item.id));
  const newIds = new Set();
  for (const item of newItems) {
    if (existingIds.has(item.id)) throw new Error(`queue item id already exists: ${item.id}`);
    if (newIds.has(item.id)) throw new Error(`new queue items contain duplicate id: ${item.id}`);
    newIds.add(item.id);
  }
}

function printValidation(result) {
  console.log(`Active items: ${result.active}`);
  console.log(`Errors: ${result.errors.length}`);
  for (const error of result.errors) console.log(`  ERROR ${error}`);
  console.log(`Warnings: ${result.warnings.length}`);
  for (const warning of result.warnings) console.log(`  WARN ${warning}`);
}

function printItems(label, items) {
  console.log("");
  console.log(`${label}:`);
  if (!items.length) {
    console.log("  (none)");
    return;
  }

  for (const item of items.slice(0, 20)) {
    const name = item.displayName ? `${item.subject} / ${item.displayName}` : item.subject;
    const tail = item.note ? ` | ${item.note}` : "";
    console.log(`  - ${item.id} | ${item.domain} | ${name} | ${item.status} | attempts=${item.attempts} | reasoning=${item.reasoningEffort}${tail}`);
  }
  if (items.length > 20) console.log(`  ... ${items.length - 20} more`);
}

try {
  main();
} catch (error) {
  console.error(error?.message || error);
  process.exitCode = 1;
}
