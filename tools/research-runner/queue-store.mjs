import fs from "node:fs";
import { bindResearchPlan, researchPlanMetadata } from "./research-plan-store.mjs";
import path from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";

export const TOOL_DIR = path.dirname(fileURLToPath(import.meta.url));
export const TOOLS_DIR = path.resolve(TOOL_DIR, "..");
export const PROJECT_ROOT = resolveProjectRoot(process.env.RESEARCH_RUNNER_PROJECT_ROOT);
export const FUNDAMENTAL_ROOT = path.join(PROJECT_ROOT, "基本面");
export const ANALYSIS_ROOT = path.join(PROJECT_ROOT, "分析报告");
export const FINANCIAL_MATERIALS_ROOT = path.join(PROJECT_ROOT, "金融资料");
export const QUEUE_DIR = resolveQueueDir(process.env.RESEARCH_RUNNER_QUEUE_DIR);
export const QUEUE_PATH = path.join(QUEUE_DIR, "queue.jsonl");
export const DONE_QUEUE_PATH = path.join(QUEUE_DIR, "queue.done.jsonl");
export const QUEUE_CONTROL_PATH = path.join(QUEUE_DIR, "queue.control.json");

const ACTIVE_STATUSES = new Set(["pending", "running", "retry_pending", "done", "failed"]);
const BLOCKING_STATUSES = new Set(["pending", "running", "retry_pending"]);
const RETRYABLE_RENAME_ERROR_CODES = new Set(["EACCES", "EBUSY", "EPERM"]);
const RENAME_RETRY_DELAYS_MS = [50, 100, 200, 500, 1000, 2000];
const TOKEN_COUNTER_KEYS = [
  "inputTokens",
  "cachedInputTokens",
  "outputTokens",
  "reasoningOutputTokens",
  "totalTokens",
];

export const DEFAULT_REASONING_EFFORT = "high";
export const SUPPORTED_REASONING_EFFORTS = Object.freeze([
  "low",
  "medium",
  "high",
  "xhigh",
  "max",
  "ultra",
]);

function resolveProjectRoot(configuredRoot) {
  const raw = String(configuredRoot || "").trim();
  const defaultRoot = path.resolve(TOOLS_DIR, "..");
  if (!raw) return defaultRoot;
  return path.isAbsolute(raw)
    ? path.resolve(raw)
    : path.resolve(defaultRoot, raw);
}

function resolveQueueDir(configuredDir) {
  const raw = String(configuredDir || "").trim();
  if (!raw) return TOOLS_DIR;
  return path.isAbsolute(raw)
    ? path.resolve(raw)
    : path.resolve(TOOLS_DIR, raw);
}

export function readUtf8(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

export function ensureQueueFiles() {
  fs.mkdirSync(QUEUE_DIR, { recursive: true });
  for (const filePath of [QUEUE_PATH, DONE_QUEUE_PATH]) {
    if (!fs.existsSync(filePath)) fs.writeFileSync(filePath, "", "utf8");
  }
}

export function readQueueControl() {
  if (!fs.existsSync(QUEUE_CONTROL_PATH)) return null;

  let parsed;
  try {
    parsed = JSON.parse(readUtf8(QUEUE_CONTROL_PATH));
  } catch (error) {
    throw new Error(`Invalid queue control at ${QUEUE_CONTROL_PATH}: ${error.message}`);
  }

  if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") {
    throw new Error(`Invalid queue control at ${QUEUE_CONTROL_PATH}: expected a JSON object.`);
  }

  return {
    concurrency: normalizeConcurrency(parsed.concurrency, `${QUEUE_CONTROL_PATH}.concurrency`),
  };
}

export function writeQueueControl({ concurrency }) {
  const normalizedConcurrency = normalizeConcurrency(concurrency, "queue control concurrency");
  fs.mkdirSync(QUEUE_DIR, { recursive: true });
  const tempPath = `${QUEUE_CONTROL_PATH}.tmp-${process.pid}`;
  const body = `${JSON.stringify({ concurrency: normalizedConcurrency }, null, 2)}\n`;
  fs.writeFileSync(tempPath, body, "utf8");
  renameWithRetrySync(tempPath, QUEUE_CONTROL_PATH);
  return { concurrency: normalizedConcurrency };
}

export function normalizeConcurrency(value, source = "concurrency") {
  if (!Number.isInteger(value) || value < 0) {
    throw new Error(`${source} must be a non-negative integer.`);
  }
  return value;
}

export function readJsonl(filePath) {
  if (!fs.existsSync(filePath)) return [];
  const text = readUtf8(filePath);
  const lines = text.split(/\r?\n/);
  const items = [];

  lines.forEach((line, index) => {
    const trimmed = line.trim();
    if (!trimmed) return;
    try {
      items.push(normalizeQueueItem(JSON.parse(trimmed), `${filePath}:${index + 1}`));
    } catch (error) {
      throw new Error(`Invalid JSONL at ${filePath}:${index + 1}: ${error.message}`);
    }
  });

  return items;
}

export function writeJsonl(filePath, items) {
  const body = items.map((item) => `${JSON.stringify(normalizeQueueItem(item))}\n`).join("");
  const tempPath = `${filePath}.tmp-${process.pid}`;
  fs.writeFileSync(tempPath, body, "utf8");
  renameWithRetrySync(tempPath, filePath);
}

function renameWithRetrySync(sourcePath, targetPath) {
  for (let attempt = 0; ; attempt += 1) {
    try {
      fs.renameSync(sourcePath, targetPath);
      return;
    } catch (error) {
      const shouldRetry = RETRYABLE_RENAME_ERROR_CODES.has(error?.code)
        && attempt < RENAME_RETRY_DELAYS_MS.length;
      if (!shouldRetry) throw error;
      sleepSync(RENAME_RETRY_DELAYS_MS[attempt]);
    }
  }
}

function sleepSync(milliseconds) {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, milliseconds);
}

export function readActiveQueue() {
  ensureQueueFiles();
  return readJsonl(QUEUE_PATH);
}

export function readDoneQueue() {
  ensureQueueFiles();
  return readJsonl(DONE_QUEUE_PATH);
}

export function writeActiveQueue(items) {
  writeJsonl(QUEUE_PATH, items);
}

export function writeDoneQueue(items) {
  writeJsonl(DONE_QUEUE_PATH, items);
}

export function appendActiveQueueItems(newItems) {
  const active = readActiveQueue();
  writeActiveQueue([...active, ...newItems.map((item) => normalizeQueueItem(item))]);
  return newItems.length;
}

export function normalizeQueueItem(item, source = "queue item") {
  const normalized = {
    id: stringField(item.id),
    domain: stringField(item.domain),
    sourceDate: stringField(item.sourceDate),
    subject: stringField(item.subject),
    displayName: stringField(item.displayName),
    category: stringField(item.category),
    status: stringField(item.status || "pending"),
    attempts: numberField(item.attempts),
    outputFile: stringField(item.outputFile),
    startedAt: stringField(item.startedAt),
    finishedAt: stringField(item.finishedAt),
    note: stringField(item.note),
    createdAt: stringField(item.createdAt),
    updatedAt: stringField(item.updatedAt),
    reasoningEffort: normalizeReasoningEffort(item.reasoningEffort, `${source}.reasoningEffort`),
    tokenUsage: objectField(item.tokenUsage),
  };

  for (const [key, value] of Object.entries(item)) {
    if (!(key in normalized)) normalized[key] = value;
  }

  if (!normalized.id) throw new Error(`${source} is missing id`);
  if (!normalized.domain) throw new Error(`${source} is missing domain`);
  if (!normalized.subject) throw new Error(`${source} is missing subject`);
  if (!ACTIVE_STATUSES.has(normalized.status) && normalized.status !== "archived") {
    throw new Error(`${source} has unsupported status: ${normalized.status}`);
  }

  return normalized;
}

export function normalizeReasoningEffort(value, source = "reasoningEffort") {
  const raw = stringField(value || DEFAULT_REASONING_EFFORT).toLowerCase();
  const compact = raw.replace(/[\s_-]+/g, "");
  const aliases = {
    default: DEFAULT_REASONING_EFFORT,
    low: "low",
    medium: "medium",
    high: "high",
    xhigh: "xhigh",
    extrahigh: "xhigh",
    max: "max",
    maximum: "max",
    ultra: "ultra",
  };
  const normalized = aliases[compact] || "";
  if (!SUPPORTED_REASONING_EFFORTS.includes(normalized)) {
    throw new Error(`${source} has unsupported value: ${value}. Supported values: ${SUPPORTED_REASONING_EFFORTS.join(", ")}`);
  }
  return normalized;
}

export function appendTokenUsageAttempt(existing, attemptUsage) {
  if (!attemptUsage) return objectField(existing);
  const attempts = Array.isArray(existing?.attempts) ? [...existing.attempts] : [];
  attempts.push(attemptUsage);
  const total = enrichTokenSummary(sumTokenCounters(attempts.map((attempt) => attempt?.total)));
  const includesSubagents = attempts.some((attempt) => attempt?.includesSubagents || attempt?.total?.includesSubagents);
  const threadCount = attempts.reduce((sum, attempt) => sum + nonNegativeNumber(attempt?.total?.threadCount), 0);
  const subagentThreadCount = attempts.reduce((sum, attempt) => sum + nonNegativeNumber(attempt?.total?.subagentThreadCount), 0);
  const unresolvedThreadCount = attempts.reduce((sum, attempt) => sum + nonNegativeNumber(attempt?.total?.unresolvedThreadCount), 0);
  total.threadCount = threadCount;
  total.subagentThreadCount = subagentThreadCount;
  total.unresolvedThreadCount = unresolvedThreadCount;
  total.includesSubagents = includesSubagents;
  return {
    attempts,
    total,
    includesSubagents,
    threadCount,
    subagentThreadCount,
    unresolvedThreadCount,
    usageAggregation: includesSubagents
      ? "parent_plus_subagents"
      : (existing?.usageAggregation || attemptUsage.usageAggregation || "direct_threads"),
  };
}

function enrichTokenSummary(counter) {
  const inputTokens = nonNegativeNumber(counter?.inputTokens);
  const cachedInputTokens = Math.min(nonNegativeNumber(counter?.cachedInputTokens), inputTokens);
  return {
    ...counter,
    uncachedInputTokens: Math.max(inputTokens - cachedInputTokens, 0),
    cachedInputRatio: inputTokens ? cachedInputTokens / inputTokens : 0,
  };
}

export function sumTokenCounters(counters) {
  const total = Object.fromEntries(TOKEN_COUNTER_KEYS.map((key) => [key, 0]));
  for (const counter of counters || []) {
    if (!counter) continue;
    for (const key of TOKEN_COUNTER_KEYS) total[key] += nonNegativeNumber(counter[key]);
  }
  return total;
}

export function recoverRunningQueueItems({ maxAttempts }) {
  const items = readActiveQueue();
  const now = new Date();
  const nowText = formatLocalDateTime(now);
  const nowIso = formatLocalIso(now);
  let recovered = 0;
  let failed = 0;

  for (const item of items) {
    if (item.status !== "running" || hasCleanupBlock(item)) continue;
    item.outputFile = "";
    item.finishedAt = nowText;
    item.updatedAt = nowIso;
    if (item.attempts >= maxAttempts) {
      item.status = "failed";
      item.note = "codex_sdk_interrupted_max_attempts";
      failed += 1;
    } else {
      item.status = "retry_pending";
      item.note = "codex_sdk_interrupted_recovered";
      recovered += 1;
    }
  }

  if (recovered || failed) writeActiveQueue(items);
  return { recovered, failed };
}

export function hasCleanupBlock(item) {
  return item.status === 'running' && item.note?.startsWith('codex_cleanup_unconfirmed:');
}

export function markQueueItemCleanupBlocked(id, message) {
  const items = readActiveQueue();
  const item = items.find(row => row.id === id);
  if (!item || item.status !== 'running') throw new Error(`Cannot protect non-running queue item: ${id}`);
  item.note = `codex_cleanup_unconfirmed: ${String(message).slice(0, 500).replace(/[\r\n]/g, ' ')}`;
  item.updatedAt = formatLocalIso(new Date());
  writeActiveQueue(items);
}

export function claimNextQueueItem({ maxAttempts, priorityGroups = [] }) {
  const items = readActiveQueue();
  const now = new Date();
  const nowText = formatLocalDateTime(now);
  const nowIso = formatLocalIso(now);

  let claimed = null;
  let changed = false;

  for (const item of items) {
    if (item.status === "retry_pending" && item.attempts >= maxAttempts) {
      item.status = "failed";
      item.finishedAt = nowText;
      item.note = "codex_sdk_max_attempts";
      item.updatedAt = nowIso;
      changed = true;
      continue;
    }
  }

  const claimableDomains = highestPriorityBlockingDomains(items, priorityGroups);
  if (!claimableDomains) {
    if (changed) writeActiveQueue(items);
    return null;
  }

  for (const item of items) {
    if (!claimableDomains.has(item.domain)) continue;
    if (item.status === "pending" || (item.status === "retry_pending" && item.attempts < maxAttempts)) {
      item.status = "running";
      item.attempts += 1;
      item.outputFile = "";
      item.startedAt = nowText;
      item.finishedAt = "";
      item.note = "codex_sdk_claimed";
      item.updatedAt = nowIso;
      claimed = { ...item };
      changed = true;
      break;
    }
  }

  if (changed) writeActiveQueue(items);
  return claimed;
}

function highestPriorityBlockingDomains(items, priorityGroups) {
  const groups = normalizePriorityGroups(priorityGroups);
  if (!groups.length) return new Set(items.map((item) => item.domain));

  for (const group of groups) {
    if (items.some((item) => group.has(item.domain) && BLOCKING_STATUSES.has(item.status))) {
      return group;
    }
  }

  return null;
}

function normalizePriorityGroups(priorityGroups) {
  return priorityGroups
    .map((group) => Array.isArray(group) ? new Set(group) : new Set([group]))
    .filter((group) => group.size);
}

export function markQueueItemDone(id, { outputFile, note = "codex_sdk_done", tokenUsageAttempt = null }) {
  const items = readActiveQueue();
  const item = items.find((candidate) => candidate.id === id);
  if (!item) throw new Error(`Queue item not found: ${id}`);

  const now = new Date();
  item.status = "done";
  item.outputFile = outputFile || "";
  item.finishedAt = formatLocalDateTime(now);
  item.note = note;
  item.updatedAt = formatLocalIso(now);
  if (tokenUsageAttempt) item.tokenUsage = appendTokenUsageAttempt(item.tokenUsage, tokenUsageAttempt);

  writeActiveQueue(items);
  return { ...item };
}

export function markQueueItemFailure(id, errorMessage, maxAttempts, { tokenUsageAttempt = null } = {}) {
  const items = readActiveQueue();
  const item = items.find((candidate) => candidate.id === id);
  if (!item) {
    return { status: "not_found", id, finalStatus: "unchanged", attempts: 0, reason: "not found" };
  }

  const now = new Date();
  item.status = item.attempts >= maxAttempts ? "failed" : "retry_pending";
  item.outputFile = "";
  item.finishedAt = formatLocalDateTime(now);
  item.note = `codex_sdk_failed: ${String(errorMessage || "unknown failure").slice(0, 500).replace(/\r?\n/g, " ")}`;
  item.updatedAt = formatLocalIso(now);
  if (tokenUsageAttempt) item.tokenUsage = appendTokenUsageAttempt(item.tokenUsage, tokenUsageAttempt);

  writeActiveQueue(items);
  return {
    status: "updated",
    id,
    finalStatus: item.status,
    attempts: item.attempts,
    reason: item.note,
  };
}

export function deferQueueItemForQuota(id, pauseUntil) {
  const items = readActiveQueue();
  const item = items.find((candidate) => candidate.id === id);
  if (!item) {
    return { status: "not_found", id, finalStatus: "unchanged", attempts: 0, reason: "not found" };
  }

  const now = new Date();
  item.status = "retry_pending";
  item.attempts = Math.max(0, item.attempts - 1);
  item.outputFile = "";
  item.finishedAt = formatLocalDateTime(now);
  item.note = `codex_quota_exit: retry on next launch; reported_reset_with_buffer: ${new Date(pauseUntil).toISOString()}`;
  item.updatedAt = formatLocalIso(now);

  writeActiveQueue(items);
  return {
    status: "updated",
    id,
    finalStatus: item.status,
    attempts: item.attempts,
    reason: item.note,
  };
}

export function archiveDoneItems() {
  const active = readActiveQueue();
  const done = readDoneQueue();
  const doneIds = new Set(done.map((item) => item.id));
  const nowIso = formatLocalIso(new Date());
  const remaining = [];
  const archived = [];
  let duplicateDone = 0;

  for (const item of active) {
    if (item.status !== "done") {
      remaining.push(item);
      continue;
    }

    if (doneIds.has(item.id)) {
      duplicateDone += 1;
      continue;
    }

    const archivedItem = {
      ...item,
      archivedAt: nowIso,
    };
    done.push(archivedItem);
    doneIds.add(item.id);
    archived.push(archivedItem);
  }

  // Write the done archive first. If this fails, active queue remains unchanged;
  // if active cleanup fails later, the next archive pass can remove duplicates.
  if (archived.length) writeDoneQueue(done);
  writeActiveQueue(remaining);
  return { archived: archived.length, duplicateDone, activeRemaining: remaining.length, doneTotal: done.length };
}

export function summarizeQueues() {
  const active = readActiveQueue();
  const done = readDoneQueue();
  const counts = countByStatus(active, done);
  return {
    activeCount: active.length,
    doneCount: done.length,
    counts,
    failed: active.filter((item) => item.status === "failed"),
    running: active.filter((item) => item.status === "running"),
    retryPending: active.filter((item) => item.status === "retry_pending"),
    pending: active.filter((item) => item.status === "pending"),
    doneActive: active.filter((item) => item.status === "done"),
    latestDone: done.slice(-10).reverse(),
  };
}

export function parseMarkdownTableRows(mdText, expectedHeader) {
  const rows = [];
  for (const line of mdText.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed.startsWith("|")) continue;
    if (/^\|\s*-+/.test(trimmed)) continue;

    const cells = splitMarkdownRow(trimmed);
    if (!cells.length || cells[0] === expectedHeader) continue;
    rows.push(cells);
  }
  return rows;
}

export function parseLegacyCompanyQueue(mdText) {
  return parseMarkdownTableRows(mdText, "序号")
    .filter((cells) => cells.length >= 10)
    .map((cells) => ({
      row: cells[0],
      sourceDate: cells[1],
      subject: cells[2],
      displayName: cells[3],
      status: cells[4],
      attempts: Number(cells[5] || 0),
      outputFile: cells[6],
      startedAt: cells[7],
      finishedAt: cells[8],
      note: cells[9],
    }));
}

export function formatLocalDateTime(date) {
  const yyyy = date.getFullYear();
  const mm = pad2(date.getMonth() + 1);
  const dd = pad2(date.getDate());
  const hh = pad2(date.getHours());
  const mi = pad2(date.getMinutes());
  const ss = pad2(date.getSeconds());
  return `${yyyy}-${mm}-${dd} ${hh}:${mi}:${ss}`;
}

export function formatLocalDate(date) {
  return `${date.getFullYear()}-${pad2(date.getMonth() + 1)}-${pad2(date.getDate())}`;
}

export function formatLocalIso(date) {
  const offsetMinutes = -date.getTimezoneOffset();
  const sign = offsetMinutes >= 0 ? "+" : "-";
  const absolute = Math.abs(offsetMinutes);
  const offset = `${sign}${pad2(Math.floor(absolute / 60))}:${pad2(absolute % 60)}`;
  return `${formatLocalDate(date)}T${pad2(date.getHours())}:${pad2(date.getMinutes())}:${pad2(date.getSeconds())}${offset}`;
}

export function normalizeProjectPath(value) {
  return stringField(value).replace(/\\/g, "/");
}

export function projectRelativeToAbsolute(projectRelativePath) {
  const normalized = normalizeProjectPath(projectRelativePath);
  if (!normalized) return "";
  return path.join(PROJECT_ROOT, ...normalized.split("/"));
}

export function categoryFromOutputFile(outputFile) {
  const normalized = normalizeProjectPath(outputFile);
  const parts = normalized.split("/");
  const researchDirIndex = parts.findIndex((part) => part === "公司调研" || part === "行业调研");
  if (researchDirIndex >= 0) {
    const categoryIndex = researchDirIndex + (parts[researchDirIndex + 1] === "结果" ? 2 : 1);
    return parts[categoryIndex] || "";
  }
  return "";
}

export function safeIdPart(value) {
  const raw = stringField(value);
  if (!raw) return "unknown";
  const hash = createHash("sha1").update(raw).digest("hex").slice(0, 10);
  const safe = raw.replace(/[^A-Za-z0-9._-]+/g, "_").replace(/^_+|_+$/g, "");
  if (!safe) return `u${hash}`;

  const needsHash = safe.length !== raw.length || /[^A-Za-z0-9._-]/u.test(raw) || safe.length > 80;
  const prefix = safe.slice(0, needsHash ? 64 : 80);
  return needsHash ? `${prefix}-${hash}` : prefix;
}

export function splitMarkdownRow(row) {
  return row
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => cell.trim());
}

function countByStatus(active, done) {
  const counts = {};
  for (const item of active) {
    const key = item.status === "done" ? "done_active" : item.status;
    counts[key] = (counts[key] || 0) + 1;
  }
  counts.done_archived = done.length;
  return counts;
}

function stringField(value) {
  if (value === undefined || value === null) return "";
  return String(value).trim();
}

function numberField(value) {
  const parsed = Number(value || 0);
  return Number.isFinite(parsed) ? parsed : 0;
}

function nonNegativeNumber(value) {
  const parsed = Number(value || 0);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 0;
}

function objectField(value) {
  return value && typeof value === "object" && !Array.isArray(value) ? value : undefined;
}

function pad2(value) {
  return String(value).padStart(2, "0");
}

// Bind only active executable items. Completed historical rows remain untouched.
export function bindActiveResearchPlans() {
  const items = readActiveQueue();
  let changed = false;
  const records = [];
  for (const item of items) {
    if (!["pending", "retry_pending", "running"].includes(item.status)) continue;
    const before = JSON.stringify(item);
    bindResearchPlan(item);
    changed ||= before !== JSON.stringify(item);
    if (item.planVersion) records.push({ id: item.id, ...researchPlanMetadata(item) });
  }
  if (changed) writeActiveQueue(items);
  return records;
}

export function recordResearchPlanRun(id, fields) {
  const items = readActiveQueue();
  const item = items.find(row => row.id === id);
  if (!item) throw new Error('Queue item not found: ' + id);
  Object.assign(item, fields);
  writeActiveQueue(items);
}
