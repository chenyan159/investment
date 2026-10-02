#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { checkRequiredPaths, getDomainAdapter } from "./domains/index.mjs";
import {
  archiveDoneItems,
  claimNextQueueItem,
  DEFAULT_REASONING_EFFORT,
  deferQueueItemForQuota,
  DONE_QUEUE_PATH,
  ensureQueueFiles,
  formatLocalDate,
  markQueueItemDone,
  markQueueItemFailure,
  normalizeQueueItem,
  PROJECT_ROOT,
  QUEUE_CONTROL_PATH,
  QUEUE_PATH,
  readActiveQueue,
  readDoneQueue,
  readQueueControl,
  readUtf8,
  recoverRunningQueueItems,
  sumTokenCounters,
  TOOL_DIR,
  writeQueueControl,
} from "./queue-store.mjs";
import { createQuotaGate, QUOTA_USAGE_THRESHOLD } from "./quota-control.mjs";
import {
  captureOutputSnapshot,
  createOutputContract,
  validateLocalOutput,
} from "./validators/output-validator.mjs";
import { collectCodexThreadUsage, enrichTokenCounter } from "./usage-telemetry.mjs";

const LOG_DIR = path.join(TOOL_DIR, "logs");
const LOG_ARCHIVE_DIR = path.join(LOG_DIR, "archive");
const LOG_PATH = path.join(LOG_DIR, "current.jsonl");
const LOG_RETENTION_DAYS = 30;
const LOG_RETENTION_RUNS = 50;
const LOCK_PATH = path.join(TOOL_DIR, "runner.lock");
const PROMPT_DEBUG_DIR = path.join(TOOL_DIR, "prompt-debug");

const CODEX_MODEL = "gpt-6-astra";
const DEFAULT_TIMEOUT_MINUTES = 120;
const DEFAULT_CLAIM_TIMEOUT_MINUTES = 15;
const DEFAULT_MAX_ATTEMPTS = 7;
const DEFAULT_CONCURRENCY = 10;
const CONTROL_POLL_INTERVAL_MS = 1000;
const DEFAULT_SANDBOX_MODE = "danger-full-access";
const ALLOWED_SANDBOX_MODES = new Set(["read-only", "workspace-write", "danger-full-access"]);
const PRIORITY_GROUPS = [
  ["industry"],
  ["company"],
  ["feature-quantization", "company-sentiment"],
  ["company-investment-decision"],
  ["company-comparison", "file-run"],
];

function parseArgs(argv) {
  const options = {
    dryRun: false,
    once: false,
    maxJobs: Number.POSITIVE_INFINITY,
    timeoutMinutes: DEFAULT_TIMEOUT_MINUTES,
    claimTimeoutMinutes: DEFAULT_CLAIM_TIMEOUT_MINUTES,
    maxAttempts: DEFAULT_MAX_ATTEMPTS,
    concurrency: DEFAULT_CONCURRENCY,
    concurrencyProvided: false,
    sandboxMode: DEFAULT_SANDBOX_MODE,
    domain: "company",
    subject: "",
    runId: "",
    promptFile: "",
    expectedOutputDir: "",
    expectedOutputFile: "",
  };

  for (const arg of argv) {
    if (arg === "--dry-run") options.dryRun = true;
    else if (arg === "--once") options.once = true;
    else if (arg.startsWith("--max-jobs=")) options.maxJobs = Number(arg.slice("--max-jobs=".length));
    else if (arg.startsWith("--timeout-minutes=")) options.timeoutMinutes = Number(arg.slice("--timeout-minutes=".length));
    else if (arg.startsWith("--claim-timeout-minutes=")) options.claimTimeoutMinutes = Number(arg.slice("--claim-timeout-minutes=".length));
    else if (arg.startsWith("--max-attempts=")) options.maxAttempts = Number(arg.slice("--max-attempts=".length));
    else if (arg.startsWith("--concurrency=")) {
      options.concurrency = Number(arg.slice("--concurrency=".length));
      options.concurrencyProvided = true;
    }
    else if (arg.startsWith("--sandbox-mode=")) options.sandboxMode = arg.slice("--sandbox-mode=".length).trim();
    else if (arg.startsWith("--domain=")) options.domain = arg.slice("--domain=".length).trim();
    else if (arg.startsWith("--subject=")) options.subject = arg.slice("--subject=".length).trim();
    else if (arg.startsWith("--run-id=")) options.runId = arg.slice("--run-id=".length).trim();
    else if (arg.startsWith("--prompt-file=")) options.promptFile = arg.slice("--prompt-file=".length).trim();
    else if (arg.startsWith("--expected-output-dir=")) options.expectedOutputDir = arg.slice("--expected-output-dir=".length).trim();
    else if (arg.startsWith("--expected-output-file=")) options.expectedOutputFile = arg.slice("--expected-output-file=".length).trim();
    else if (arg.startsWith("--ticker=")) {
      options.subject = arg.slice("--ticker=".length).trim();
    } else if (arg === "--help" || arg === "-h") {
      printHelp();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  if (options.maxJobs !== Number.POSITIVE_INFINITY && (!Number.isFinite(options.maxJobs) || options.maxJobs <= 0)) {
    throw new Error("--max-jobs must be a positive number.");
  }
  if (!Number.isFinite(options.timeoutMinutes) || options.timeoutMinutes <= 0) {
    throw new Error("--timeout-minutes must be a positive number.");
  }
  if (!Number.isFinite(options.claimTimeoutMinutes) || options.claimTimeoutMinutes <= 0) {
    throw new Error("--claim-timeout-minutes must be a positive number.");
  }
  if (!Number.isInteger(options.maxAttempts) || options.maxAttempts <= 0) {
    throw new Error("--max-attempts must be a positive integer.");
  }
  if (!Number.isInteger(options.concurrency) || options.concurrency < 0) {
    throw new Error("--concurrency must be a non-negative integer.");
  }
  if (!ALLOWED_SANDBOX_MODES.has(options.sandboxMode)) {
    throw new Error(`--sandbox-mode must be one of: ${Array.from(ALLOWED_SANDBOX_MODES).join(", ")}`);
  }
  if (options.once) options.maxJobs = Math.min(options.maxJobs, 1);
  return options;
}

function printHelp() {
  console.log(`Usage: node runner.mjs [options]

Options:
  --dry-run                    Check queue paths and, with --subject/--ticker, write a prompt debug file. Does not call Codex.
  --domain=DOMAIN              Dry-run helper domain. Default company.
  --subject=VALUE              Dry-run helper: build a formal prompt for this subject.
  --run-id=VALUE               Dry-run helper for file-run.
  --prompt-file=PATH           Dry-run helper for file-run.
  --expected-output-dir=PATH   Dry-run helper for file-run; defaults to the prompt file directory.
  --expected-output-file=PATH  Optional exact file-run output file.
  --ticker=TICKER              Alias for --subject=TICKER in dry-run mode.
  --once                       Process at most one claimable queue item.
  --max-jobs=N                 Process at most N items in this launch.
  --timeout-minutes=N          Per-item formal Codex timeout. Default ${DEFAULT_TIMEOUT_MINUTES}.
  --claim-timeout-minutes=N    Legacy no-op; queue claiming is now local JSONL. Default ${DEFAULT_CLAIM_TIMEOUT_MINUTES}.
  --max-attempts=N             Mark failed after N attempts. Default ${DEFAULT_MAX_ATTEMPTS}.
  --concurrency=N              Persist N to queue.control.json at startup and run up to N formal Codex threads concurrently. N=0 stops new claims and exits after current tasks finish. Default on first launch: ${DEFAULT_CONCURRENCY}.
  --sandbox-mode=MODE          Codex sandbox mode. Default ${DEFAULT_SANDBOX_MODE}.
  -h, --help                   Show this help.
`);
}

let loggingReady = false;

function initializeRunLog() {
  fs.mkdirSync(LOG_ARCHIVE_DIR, { recursive: true });
  if (fs.existsSync(LOG_PATH)) {
    const stat = fs.statSync(LOG_PATH);
    if (stat.size) {
      const stamp = stat.mtime.toISOString().replace(/[:.]/g, "-");
      let archivePath = path.join(LOG_ARCHIVE_DIR, `runner_${stamp}.jsonl`);
      for (let suffix = 1; fs.existsSync(archivePath); suffix += 1) {
        archivePath = path.join(LOG_ARCHIVE_DIR, `runner_${stamp}_${suffix}.jsonl`);
      }
      fs.renameSync(LOG_PATH, archivePath);
    } else {
      fs.rmSync(LOG_PATH);
    }
  }
  fs.writeFileSync(LOG_PATH, "", "utf8");
  pruneArchivedLogs();
  loggingReady = true;
}

function pruneArchivedLogs() {
  const cutoff = Date.now() - LOG_RETENTION_DAYS * 24 * 60 * 60 * 1000;
  const files = fs.readdirSync(LOG_ARCHIVE_DIR)
    .filter((name) => name.endsWith(".jsonl"))
    .map((name) => {
      const filePath = path.join(LOG_ARCHIVE_DIR, name);
      return { filePath, mtimeMs: fs.statSync(filePath).mtimeMs };
    })
    .sort((a, b) => b.mtimeMs - a.mtimeMs);

  files.forEach((file, index) => {
    if (index >= LOG_RETENTION_RUNS || file.mtimeMs < cutoff) fs.rmSync(file.filePath);
  });
}

function log(message, extra = undefined) {
  if (!loggingReady) {
    console.warn(message, extra ?? "");
    return;
  }
  const level = /failed|failure|crashed|could not/i.test(message)
    ? "error"
    : /retry|recovered|deferred|quota|stale/i.test(message) ? "warn" : "info";
  const entry = { timestamp: new Date().toISOString(), level, event: message };
  if (extra && typeof extra === "object") Object.assign(entry, extra);
  else if (extra !== undefined) entry.details = extra;
  fs.appendFileSync(LOG_PATH, `${JSON.stringify(entry)}\n`, "utf8");
}

function initializeQueueConcurrency(options) {
  if (options.concurrencyProvided) {
    const control = writeQueueControl({ concurrency: options.concurrency });
    log("Queue concurrency control set from command-line input.", {
      queueControlPath: QUEUE_CONTROL_PATH,
      concurrency: control.concurrency,
    });
    return control.concurrency;
  }

  const storedControl = readQueueControl();
  if (storedControl) {
    log("Queue concurrency control loaded.", {
      queueControlPath: QUEUE_CONTROL_PATH,
      concurrency: storedControl.concurrency,
    });
    return storedControl.concurrency;
  }

  const control = writeQueueControl({ concurrency: DEFAULT_CONCURRENCY });
  log("Queue concurrency control initialized with the default.", {
    queueControlPath: QUEUE_CONTROL_PATH,
    concurrency: control.concurrency,
  });
  return control.concurrency;
}

function createQueueConcurrencyController(initialConcurrency) {
  let concurrency = initialConcurrency;
  let lastReadError = "";

  return {
    current() {
      return concurrency;
    },
    refresh() {
      try {
        const control = readQueueControl();
        if (!control) throw new Error(`Queue concurrency control is missing: ${QUEUE_CONTROL_PATH}`);

        const previousConcurrency = concurrency;
        concurrency = control.concurrency;
        if (lastReadError) {
          log("Queue concurrency control read recovered.", {
            queueControlPath: QUEUE_CONTROL_PATH,
            concurrency,
          });
          lastReadError = "";
        }
        if (previousConcurrency !== concurrency) {
          log("Queue concurrency control changed.", {
            queueControlPath: QUEUE_CONTROL_PATH,
            previousConcurrency,
            concurrency,
          });
        }
      } catch (error) {
        const message = error?.message || String(error);
        if (message !== lastReadError) {
          log("Queue concurrency control could not be read; retaining the previous valid value.", {
            queueControlPath: QUEUE_CONTROL_PATH,
            concurrency,
            message,
          });
          lastReadError = message;
        }
      }
      return concurrency;
    },
  };
}

async function waitForQueueItemOrControlRefresh(activeRuns) {
  let timeoutId;
  const controlPoll = new Promise((resolve) => {
    timeoutId = setTimeout(resolve, CONTROL_POLL_INTERVAL_MS);
  });

  try {
    await Promise.race([...activeRuns, controlPoll]);
  } finally {
    clearTimeout(timeoutId);
  }
}

let queueOperationChain = Promise.resolve();

function runQueueOperation(operation) {
  const next = queueOperationChain.then(() => operation());
  queueOperationChain = next.catch(() => undefined);
  return next;
}

function timestampForFile() {
  return new Date().toISOString().replace(/[:.]/g, "-");
}

function safeFilePart(value) {
  return String(value || "unknown").replace(/[<>:"/\\|?*\x00-\x1f]/g, "_");
}

function writePromptDebug(item, prompt) {
  fs.mkdirSync(PROMPT_DEBUG_DIR, { recursive: true });
  const safeSubject = safeFilePart(`${item.domain}_${item.subject}`);
  const timestampedPath = path.join(PROMPT_DEBUG_DIR, `${timestampForFile()}_${safeSubject}_prompt.md`);
  const latestPath = path.join(PROMPT_DEBUG_DIR, `latest_${safeSubject}_prompt.md`);
  fs.writeFileSync(timestampedPath, prompt, "utf8");
  fs.writeFileSync(latestPath, prompt, "utf8");
  return { timestampedPath, latestPath };
}

function sanitizeEnv(env) {
  const copy = { ...env };
  const removed = [];
  for (const key of Object.keys(copy)) {
    if (/^(OPENAI_API_KEY|CODEX_API_KEY)$/i.test(key)) {
      delete copy[key];
      removed.push(key);
    }
  }
  if (!copy.CODEX_HOME && copy.USERPROFILE) {
    copy.CODEX_HOME = path.join(copy.USERPROFILE, ".codex");
  }
  return { env: copy, removed };
}

async function runCodex(input, runOptions) {
  const { Codex } = await import("@openai/codex-sdk");
  const { env, removed } = sanitizeEnv(process.env);
  if (removed.length) log(`Removed API-key env vars before Codex SDK ${runOptions.phase} launch.`, { removed });

  const codex = new Codex({
    env,
    config: {
      model_verbosity: "high",
    },
  });

  const thread = codex.startThread({
    workingDirectory: PROJECT_ROOT,
    skipGitRepoCheck: true,
    model: CODEX_MODEL,
    modelReasoningEffort: runOptions.reasoning,
    sandboxMode: runOptions.sandboxMode,
    approvalPolicy: "never",
    webSearchMode: runOptions.webSearchMode,
    networkAccessEnabled: runOptions.networkAccessEnabled,
  });

  const controller = new AbortController();
  const timeout = setTimeout(() => {
    controller.abort(new Error(`Codex ${runOptions.phase} timeout after ${runOptions.timeoutMinutes} minutes.`));
  }, runOptions.timeoutMinutes * 60 * 1000);

  try {
    const result = await thread.run(input, { signal: controller.signal, outputSchema: runOptions.outputSchema });
    return { ...result, threadId: thread.id };
  } catch (error) {
    log(`Codex ${runOptions.phase} thread failed.`, {
      threadId: thread.id,
      name: error?.name,
      message: error?.message,
    });
    if (error && typeof error === "object") {
      error.codexThreadId = thread.id;
      error.codexPhase = runOptions.phase;
    }
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

async function phaseTokenUsage(result, reasoningEffort, fallbackThreadId = "") {
  const threadId = String(result?.threadId || fallbackThreadId || "");
  if (!threadId && !result?.usage) return null;
  const aggregate = collectCodexThreadUsage(threadId, { directUsage: result?.usage });
  if (!aggregate.counters) return null;
  return enrichTokenCounter(aggregate.counters, {
    model: CODEX_MODEL,
    reasoningEffort,
    // Keep only the parent thread id in the archive; child counters are folded
    // into this phase summary instead of being emitted as separate records.
    threadId,
    threadCount: aggregate.threadCount,
    subagentThreadCount: aggregate.subagentThreadCount,
    unresolvedThreadCount: aggregate.unresolvedThreadCount,
    usageSource: aggregate.usageSource,
    includesSubagents: aggregate.subagentThreadCount > 0,
  });
}

async function buildAttemptTokenUsage(item, formalResult, {
  formalThreadId = "",
} = {}) {
  const formal = await phaseTokenUsage(
    formalResult,
    item.reasoningEffort || DEFAULT_REASONING_EFFORT,
    formalThreadId,
  );
  if (!formal) return null;
  const total = sumTokenCounters([formal]);
  const includesSubagents = Boolean(formal.includesSubagents);
  return {
    attempt: item.attempts,
    formal,
    total: enrichTokenCounter(total, {
      includesSubagents,
      usageAggregation: "parent_plus_subagents",
      threadCount: nonNegativeNumber(formal.threadCount),
      subagentThreadCount: nonNegativeNumber(formal.subagentThreadCount),
      unresolvedThreadCount: nonNegativeNumber(formal.unresolvedThreadCount),
    }),
    includesSubagents,
    usageAggregation: "parent_plus_subagents",
  };
}

function nonNegativeNumber(value) {
  const parsed = Number(value || 0);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 0;
}

async function runOneQueueItem(item, options, quotaGate) {
  let adapter = null;
  let outputContract = null;
  let outputSnapshot = null;
  let prepareResult = null;
  let formalResult = null;
  try {
    adapter = getDomainAdapter(item.domain);
    checkRequiredPaths(item.domain);
    outputContract = createOutputContract(item, adapter);
    if (typeof adapter.prepareFormalRun === "function") {
      prepareResult = adapter.prepareFormalRun(item, outputContract);
      if (prepareResult?.files?.length) {
        log(`Prepared ${item.domain}/${item.subject} formal run.`, prepareResult);
      }
    }
    outputSnapshot = captureOutputSnapshot(outputContract, item);
    const prompt = adapter.buildFormalPrompt(item, outputContract);
    const debugFiles = writePromptDebug(item, prompt);
    log(`Claimed ${item.domain}/${item.subject}; starting formal Codex SDK run.`, {
      id: item.id,
      displayName: item.displayName,
      category: item.category,
      model: CODEX_MODEL,
      reasoningEffort: item.reasoningEffort,
      promptCharacters: prompt.length,
      promptDebug: debugFiles.timestampedPath,
      expectedOutputFile: outputContract.expectedOutputFile,
      expectedOutputDir: outputContract.expectedOutputDir,
      runDate: outputContract.runDate,
    });

    formalResult = await runCodex(prompt, {
      phase: "formal",
      reasoning: item.reasoningEffort,
      timeoutMinutes: options.timeoutMinutes,
      sandboxMode: options.sandboxMode,
      webSearchMode: "live",
      networkAccessEnabled: true,
    });
    log(`Formal Codex SDK run completed for ${item.domain}/${item.subject}.`, {
      id: item.id,
      model: CODEX_MODEL,
      reasoningEffort: item.reasoningEffort,
      threadId: formalResult.threadId,
      usage: formalResult.usage,
    });

    const outputFile = validateLocalOutput(item, adapter, outputContract, outputSnapshot);
    if (outputContract.recoveredFrom) {
      log(`Normalized a fresh output to the expected path for ${item.domain}/${item.subject}.`, {
        id: item.id,
        from: outputContract.recoveredFrom,
        to: outputFile,
      });
    }
    const tokenUsageAttempt = await buildAttemptTokenUsage(item, formalResult);

    let doneItem;
    let archiveResult;
    try {
      ({ doneItem, archiveResult } = await runQueueOperation(() => {
        const nextDoneItem = markQueueItemDone(item.id, { outputFile, tokenUsageAttempt });
        const nextArchiveResult = archiveDoneItems();
        return { doneItem: nextDoneItem, archiveResult: nextArchiveResult };
      }));
    } catch (queueError) {
      log(`Local output validation passed but queue finalization failed for ${item.domain}/${item.subject}.`, {
        id: item.id,
        outputFile,
        name: queueError?.name,
        message: queueError?.message,
      });
      return { completed: false, status: "queue_finalize_failed", itemId: item.id };
    }

    log(`Local output validation passed for ${item.domain}/${item.subject}.`, {
      id: item.id,
      outputFile: doneItem.outputFile,
      archivedDoneItems: archiveResult.archived,
    });
    return { completed: true, status: "done", itemId: item.id };
  } catch (error) {
    log(`Formal run or local output validation failed for ${item.domain}/${item.subject}.`, {
      id: item.id,
      name: error?.name,
      message: error?.message,
    });
    if (adapter && prepareResult && typeof adapter.rollbackFormalRun === "function") {
      try {
        const rollbackResult = adapter.rollbackFormalRun(item, prepareResult, outputContract);
        if (rollbackResult?.files?.length || rollbackResult?.removed?.length) {
          log(`Rolled back ${item.domain}/${item.subject} formal run side effects.`, rollbackResult);
        }
      } catch (rollbackError) {
        log(`Rollback failed for ${item.domain}/${item.subject}.`, {
          id: item.id,
          name: rollbackError?.name,
          message: rollbackError?.message,
        });
      }
    }
    const quota = error?.codexPhase === "formal"
      ? await quotaGate.afterTaskFailure()
      : { blocked: false };
    if (quota.blocked) {
      const quotaUpdate = await runQueueOperation(() => deferQueueItemForQuota(item.id, quota.pauseUntil));
      log(`Queue item deferred without attempt penalty because Codex quota is unavailable.`, {
        ...quotaUpdate,
        pauseUntil: new Date(quota.pauseUntil).toISOString(),
        primaryUsedPercent: quota.primaryUsedPercent,
        secondaryUsedPercent: quota.secondaryUsedPercent,
      });
      return { completed: false, status: "quota_deferred", itemId: item.id };
    }
    const tokenUsageAttempt = await buildAttemptTokenUsage(
      item,
      formalResult,
      {
        formalThreadId: error?.codexPhase === "formal" ? error.codexThreadId : "",
      },
    );
    const failureUpdate = await runQueueOperation(() => markQueueItemFailure(
      item.id,
      error?.message || error,
      options.maxAttempts,
      { tokenUsageAttempt },
    ));
    if (failureUpdate?.finalStatus === "retry_pending") {
      log(`Retryable failure for ${item.domain}/${item.subject}; item returned to queue.`, failureUpdate);
      return { completed: false, status: "retry_pending", itemId: item.id };
    }
    log(`Terminal failure for ${item.domain}/${item.subject}; skipping to next claimable item.`, {
      ...failureUpdate,
    });
    return { completed: true, status: "failed", itemId: item.id };
  }
}

function processIsAlive(pid) {
  if (!Number.isInteger(pid) || pid <= 0) return false;
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

function acquireLock() {
  const payload = {
    pid: process.pid,
    startedAt: new Date().toISOString(),
    projectRoot: PROJECT_ROOT,
    queuePath: QUEUE_PATH,
  };

  try {
    const fd = fs.openSync(LOCK_PATH, "wx");
    fs.writeFileSync(fd, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
    fs.closeSync(fd);
    return true;
  } catch (error) {
    if (error?.code !== "EEXIST") throw error;

    let existing = null;
    try {
      existing = JSON.parse(readUtf8(LOCK_PATH));
    } catch {
      existing = null;
    }

    if (existing && processIsAlive(Number(existing.pid))) {
      log("Another runner instance is already active; exiting.", existing);
      return false;
    }

    log("Removing stale runner lock.", existing ?? { lockPath: LOCK_PATH });
    fs.rmSync(LOCK_PATH, { force: true });
    return acquireLock();
  }
}

function releaseLock() {
  try {
    if (!fs.existsSync(LOCK_PATH)) return;
    const existing = JSON.parse(readUtf8(LOCK_PATH));
    if (Number(existing.pid) === process.pid) fs.rmSync(LOCK_PATH, { force: true });
  } catch {
    fs.rmSync(LOCK_PATH, { force: true });
  }
}

function buildDryRunItem(options) {
  const adapter = getDomainAdapter(options.domain || "company");
  if (adapter.domain === "file-run") {
    if (!options.runId && !options.promptFile && !options.expectedOutputDir && !options.expectedOutputFile) return null;
    return normalizeQueueItem(adapter.createQueueItem({
      id: `dry-run-${adapter.domain}-${safeFilePart(options.runId || options.subject || "file-run")}`,
      runId: options.runId || options.subject,
      promptFile: options.promptFile,
      expectedOutputDir: options.expectedOutputDir,
      expectedOutputFile: options.expectedOutputFile,
      sourceDate: formatLocalDate(new Date()),
    }));
  }

  if (!options.subject) return null;
  return normalizeQueueItem(adapter.createQueueItem({
    id: `dry-run-${adapter.domain}-${safeFilePart(options.subject)}`,
    subject: options.subject,
    sourceDate: formatLocalDate(new Date()),
  }));
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  ensureQueueFiles();
  if (options.dryRun) checkRequiredPaths(options.domain || "company");

  if (options.dryRun) {
    const active = readActiveQueue();
    const done = readDoneQueue();
    console.log(`Working directory: ${PROJECT_ROOT}`);
    console.log(`Active queue: ${QUEUE_PATH}`);
    console.log(`Done archive: ${DONE_QUEUE_PATH}`);
    console.log(`Active queue items: ${active.length}`);
    console.log(`Done archive items: ${done.length}`);
    console.log("Dry run does not call Codex.");

    const item = buildDryRunItem(options);
    if (item) {
      const adapter = getDomainAdapter(item.domain);
      const outputContract = createOutputContract(item, adapter);
      const prompt = adapter.buildFormalPrompt(item, outputContract);
      const written = writePromptDebug(item, prompt);
      console.log(`Formal prompt characters for ${item.domain}/${item.subject}: ${prompt.length}`);
      console.log(`Prompt debug: ${written.timestampedPath}`);
      console.log(`Latest prompt debug: ${written.latestPath}`);
    }
    return;
  }

  if (!acquireLock()) return;
  let processed = 0;
  try {
    initializeRunLog();
    const initialConcurrency = initializeQueueConcurrency(options);
    options.concurrency = initialConcurrency;
    const concurrencyController = createQueueConcurrencyController(initialConcurrency);
    const quotaGate = createQuotaGate({ log });
    const recovered = await runQueueOperation(() => recoverRunningQueueItems({ maxAttempts: options.maxAttempts }));
    if (recovered.recovered || recovered.failed) {
      log("Recovered interrupted running queue items before launch.", recovered);
    }
    log("Runner started.", {
      projectRoot: PROJECT_ROOT,
      queuePath: QUEUE_PATH,
      queueControlPath: QUEUE_CONTROL_PATH,
      desiredConcurrency: concurrencyController.current(),
      quotaUsageThreshold: QUOTA_USAGE_THRESHOLD,
      options,
      priorityGroups: PRIORITY_GROUPS,
    });

    const activeRuns = new Set();
    let lastCapacityWaitState = "";

    const launchNext = async () => {
      if (processed + activeRuns.size >= options.maxJobs) return false;
      const item = await runQueueOperation(() => claimNextQueueItem({ maxAttempts: options.maxAttempts, priorityGroups: PRIORITY_GROUPS }));
      if (!item) return false;

      const quota = await quotaGate.beforeTask();
      if (!quota.allowed) {
        const quotaUpdate = await runQueueOperation(() => deferQueueItemForQuota(item.id, quota.pauseUntil));
        log(`Queue item returned without attempt penalty before Codex launch because quota reached the threshold.`, {
          ...quotaUpdate,
          pauseUntil: new Date(quota.pauseUntil).toISOString(),
        });
        return false;
      }

      let runPromise;
      runPromise = runOneQueueItem(item, options, quotaGate)
        .then((result) => {
          const countsAsProcessed = result.status !== "quota_deferred";
          if (countsAsProcessed) processed += 1;
          log(`Queue item run settled for ${item.domain}/${item.subject}.`, {
            id: item.id,
            status: result.status,
            completed: result.completed,
            countsAsProcessed,
            processed,
            activeRuns: activeRuns.size - 1,
          });
        })
        .catch((error) => {
          processed += 1;
          log(`Queue item run crashed outside normal handling for ${item.domain}/${item.subject}.`, {
            id: item.id,
            name: error?.name,
            message: error?.message,
            processed,
            activeRuns: activeRuns.size - 1,
          });
        })
        .finally(() => activeRuns.delete(runPromise));

      activeRuns.add(runPromise);
      return true;
    };

    while (processed < options.maxJobs) {
      let launchedAny = false;
      let desiredConcurrency = concurrencyController.refresh();
      while (processed + activeRuns.size < options.maxJobs) {
        desiredConcurrency = concurrencyController.refresh();
        if (activeRuns.size >= desiredConcurrency) break;
        if (quotaGate.isPaused()) break;
        const launched = await launchNext();
        if (!launched) break;
        launchedAny = true;
      }

      desiredConcurrency = concurrencyController.refresh();

      if (desiredConcurrency === 0 && !activeRuns.size) {
        log("Concurrency is 0 and no queue items are running; exiting.", { processed });
        break;
      }

      if (!activeRuns.size) {
        if (quotaGate.isPaused()) {
          await waitForQueueItemOrControlRefresh(activeRuns);
          continue;
        }
        log("No claimable queue items; exiting.");
        break;
      }

      if (!launchedAny && desiredConcurrency === 0) {
        const waitState = `${desiredConcurrency}:${activeRuns.size}:${processed}`;
        if (waitState !== lastCapacityWaitState) {
          log("Concurrency is 0; waiting for current queue items to finish before exiting.", {
            activeRuns: activeRuns.size,
            processed,
          });
          lastCapacityWaitState = waitState;
        }
      } else if (!launchedAny && activeRuns.size >= desiredConcurrency) {
        const waitState = `${desiredConcurrency}:${activeRuns.size}:${processed}`;
        if (waitState !== lastCapacityWaitState) {
          log("Concurrency target reached; waiting for a queue item to settle or the control file to refresh.", {
            desiredConcurrency,
            activeRuns: activeRuns.size,
            processed,
          });
          lastCapacityWaitState = waitState;
        }
      } else {
        lastCapacityWaitState = "";
      }

      await waitForQueueItemOrControlRefresh(activeRuns);
    }

    if (activeRuns.size) await Promise.allSettled(activeRuns);

    log("Runner finished.", { processed });
  } finally {
    releaseLock();
  }
}

main().catch((error) => {
  log("Runner crashed.", { name: error?.name, message: error?.message, stack: error?.stack });
  console.error(error);
  process.exitCode = 1;
});
