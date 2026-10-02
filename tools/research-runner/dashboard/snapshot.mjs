import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";

import {
  DONE_QUEUE_PATH,
  LOCK_PATH,
  LOG_PATH,
  PROJECT_ROOT,
  QUEUE_CONTROL_PATH,
  QUEUE_PATH,
  RECENT_ANOMALY_LIMIT,
  RECENT_ITEM_LIMIT,
  RECENT_COMPLETED_LIMIT,
  RUNNING_VISIBLE_ROW_LIMIT,
} from "./config.mjs";
import { CODEX_MODEL, DEFAULT_CONCURRENCY } from "../runtime-config.mjs";
import { DEFAULT_REASONING_EFFORT } from "../queue-store.mjs";
import { QUOTA_USAGE_THRESHOLD } from "../quota-control.mjs";

const sdkPackagePath = new URL("../node_modules/@openai/codex-sdk/package.json", import.meta.url);

const DEFAULT_P90_MINUTES = 45;
const DEFAULT_TOKENS = 7_500_000;
// Require explicit marker syntax so legitimate prose such as "still TBD" is not flagged.
const PLACEHOLDER_PATTERN = /\[(?:TODO|TBD)\]|(?:TODO|TBD|PLACEHOLDER)\s*[:：]|[【\[](?:待补充|待填写)[】\]]|(?:待补充|待填写)\s*[:：]/gi;
const ARTIFACT_PATTERN = /(\.tmp|\.partial|\.rollback|\.bak)$|(^|[._-])(tmp|partial|rollback)([._-]|$)/i;
const ANOMALY_PATTERN = /error|fail|retry|timeout|quota|stale|abort|interrupt|recover|capacity/i;

const fileCache = new Map();
let outputAuditCache = { signature: "", value: emptyPathAudit() };

export function isProcessAlive(pid) {
  if (!Number.isInteger(Number(pid)) || Number(pid) <= 0) return false;
  try {
    process.kill(Number(pid), 0);
    return true;
  } catch {
    return false;
  }
}

export function buildDashboardSnapshot({ quota = null, now = new Date() } = {}) {
  const active = readJsonlCached(QUEUE_PATH);
  const done = readJsonlCached(DONE_QUEUE_PATH);
  const logs = readJsonlCached(LOG_PATH);
  const lock = readJsonCached(LOCK_PATH);
  const control = readJsonCached(QUEUE_CONTROL_PATH);
  const runnerAlive = Boolean(lock && isProcessAlive(lock.pid));
  const runStartMs = findRunStartMs(lock, logs);
  const currentRunDone = selectRunCompletedItems({ active, done, lock, runnerAlive, runStartMs });
  const running = active.filter((item) => item.status === "running");
  const queueStats = summarizeQueue(active, currentRunDone);
  const doneStats = summarizeDone(done, currentRunDone);
  const runningStats = summarizeRunning(running, now);
  const anomalyStats = summarizeAnomalies(logs);
  const concurrency = Number.isInteger(control?.concurrency) ? control.concurrency : DEFAULT_CONCURRENCY;
  const eta = estimateCompletion({
    active,
    allDone: done,
    currentRunDone,
    concurrency,
    now,
  });
  const pathHealth = auditCompletedOutputs(currentRunDone);
  const quotaSummary = summarizeQuota({ quota, eta, runnerAlive, runStartMs, currentRunDone, now });
  const lastLog = logs.at(-1) || null;
  const status = deriveRunnerStatus({ lock, runnerAlive, concurrency, quota, lastLog });

  return {
    generatedAt: now.toISOString(),
    runner: {
      configuredModel: CODEX_MODEL,
      defaultReasoningEffort: DEFAULT_REASONING_EFFORT,
      sdkVersion: readJsonCached(sdkPackagePath)?.version ?? null,
      status,
      pid: lock?.pid ?? null,
      pidAlive: runnerAlive,
      startedAt: lock?.startedAt ?? (currentRunDone.length && runStartMs ? new Date(runStartMs).toISOString() : null),
      uptimeSeconds: runnerAlive && lock?.startedAt
        ? Math.max(0, Math.round((now.getTime() - toTimeMs(lock.startedAt)) / 1000))
        : null,
      projectRoot: lock?.projectRoot ?? PROJECT_ROOT,
      queuePath: lock?.queuePath ?? QUEUE_PATH,
      concurrency,
      lockPresent: Boolean(lock),
      lastEvent: lastLog ? compactLog(lastLog) : null,
    },
    queue: queueStats,
    running: runningStats,
    completed: doneStats,
    anomalies: anomalyStats,
    eta,
    quota: quotaSummary,
    pathHealth,
    files: {
      queueUpdatedAt: fileUpdatedAt(QUEUE_PATH),
      doneUpdatedAt: fileUpdatedAt(DONE_QUEUE_PATH),
      logUpdatedAt: fileUpdatedAt(LOG_PATH),
      controlUpdatedAt: fileUpdatedAt(QUEUE_CONTROL_PATH),
    },
    display: {
      recentItemLimit: RECENT_ITEM_LIMIT,
      recentAnomalyLimit: RECENT_ANOMALY_LIMIT,
      runningVisibleRowLimit: RUNNING_VISIBLE_ROW_LIMIT,
    },
  };
}

export function summarizeQueue(active, currentRunDone = []) {
  const byStatus = countBy(active, (item) => item.status || "unknown");
  const domains = new Map();
  for (const item of active) {
    const domain = item.domain || "unknown";
    if (!domains.has(domain)) domains.set(domain, { domain, total: 0, byStatus: {} });
    const row = domains.get(domain);
    row.total += 1;
    row.byStatus[item.status || "unknown"] = (row.byStatus[item.status || "unknown"] || 0) + 1;
  }
  const totalScope = active.length + currentRunDone.length;
  return {
    active: active.length,
    pending: byStatus.pending || 0,
    running: byStatus.running || 0,
    retryPending: byStatus.retry_pending || 0,
    failed: byStatus.failed || 0,
    unarchivedDone: byStatus.done || 0,
    currentRunCompleted: currentRunDone.length,
    currentRunTotal: totalScope,
    progressPercent: totalScope ? round((currentRunDone.length / totalScope) * 100, 1) : 100,
    byStatus,
    domains: [...domains.values()].sort((a, b) => b.total - a.total || a.domain.localeCompare(b.domain)),
    items: active.map((item) => ({
      id: item.id,
      domain: item.domain,
      subject: item.subject,
      displayName: item.displayName || item.subject,
      status: item.status,
      planVersion: item.planVersion || null,
      reasoningEffort: item.reasoningEffort || DEFAULT_REASONING_EFFORT,
    })),
  };
}

export function selectRunCompletedItems({ active, done, lock, runnerAlive, runStartMs }) {
  if (!runStartMs || (!runnerAlive && !lock && active.length)) return [];
  return done.filter((item) => itemTimeMs(item, ["archivedAt", "finishedAt", "updatedAt"]) >= runStartMs);
}

export function summarizeRunning(items, now = new Date()) {
  const rows = items.map((item) => {
    const startedMs = itemTimeMs(item, ["startedAt", "updatedAt"]);
    return {
      id: item.id,
      domain: item.domain,
      subject: item.subject,
      displayName: item.displayName || item.subject,
      status: item.status,
      attempts: Number(item.attempts || 0),
      reasoningEffort: item.reasoningEffort || null,
      planVersion: item.planVersion || null,
      startedAt: item.startedAt || null,
      elapsedMinutes: startedMs ? round(Math.max(0, now.getTime() - startedMs) / 60_000, 1) : null,
      expectedOutput: item.expectedOutputFile || item.outputFile || null,
    };
  });
  const elapsed = rows.map((row) => row.elapsedMinutes).filter(Number.isFinite);
  return {
    count: rows.length,
    averageElapsedMinutes: elapsed.length ? round(average(elapsed), 1) : null,
    maxElapsedMinutes: elapsed.length ? round(Math.max(...elapsed), 1) : null,
    retrying: rows.filter((row) => row.attempts > 1).length,
    items: rows.sort((a, b) => toTimeMs(b.startedAt) - toTimeMs(a.startedAt)),
  };
}

export function summarizeDone(allDone, currentRunDone) {
  const runDurations = validDurations(currentRunDone);
  const runTokens = currentRunDone.map(totalTokens).filter(Number.isFinite);
  const domainMap = new Map();
  for (const item of currentRunDone) {
    const domain = item.domain || "unknown";
    if (!domainMap.has(domain)) domainMap.set(domain, []);
    domainMap.get(domain).push(item);
  }
  return {
    archiveTotal: allDone.length,
    currentRun: currentRunDone.length,
    duration: numericStats(runDurations),
    totalWorkerMinutes: runDurations.length ? round(sum(runDurations), 1) : 0,
    totalTokens: runTokens.length ? Math.round(sum(runTokens)) : 0,
    averageTokens: runTokens.length ? Math.round(average(runTokens)) : 0,
    firstAttempt: currentRunDone.filter((item) => Number(item.attempts || 0) === 1).length,
    retried: currentRunDone.filter((item) => Number(item.attempts || 0) > 1).length,
    domains: [...domainMap.entries()]
      .map(([domain, items]) => ({
        domain,
        count: items.length,
        duration: numericStats(validDurations(items)),
        totalTokens: Math.round(sum(items.map(totalTokens).filter(Number.isFinite))),
      }))
      .sort((a, b) => b.count - a.count || a.domain.localeCompare(b.domain)),
    latest: [...(currentRunDone.length ? currentRunDone : allDone)]
      .sort((a, b) => itemTimeMs(b, ["archivedAt", "finishedAt"]) - itemTimeMs(a, ["archivedAt", "finishedAt"]))
      .slice(0, RECENT_COMPLETED_LIMIT)
      .map((item) => ({
        id: item.id,
        domain: item.domain,
        subject: item.subject,
        displayName: item.displayName || item.subject,
        attempts: Number(item.attempts || 0),
        planVersion: item.planVersion || null,
        durationMinutes: durationMinutes(item),
        totalTokens: totalTokens(item),
        outputFile: item.outputFile || null,
        finishedAt: item.finishedAt || item.archivedAt || null,
      })),
  };
}

export function summarizeAnomalies(logs) {
  const anomalies = logs.filter((entry) => {
    const level = String(entry.level || "info").toLowerCase();
    const text = `${entry.event || ""} ${entry.message || ""} ${entry.error || ""}`;
    return level !== "info" || ANOMALY_PATTERN.test(text);
  });
  const byKind = countBy(anomalies, classifyAnomaly);
  const byLevel = countBy(anomalies, (entry) => String(entry.level || "info").toLowerCase());
  return {
    total: anomalies.length,
    errors: byLevel.error || 0,
    warnings: (byLevel.warn || 0) + (byLevel.warning || 0),
    byKind,
    latest: anomalies.slice(-RECENT_ANOMALY_LIMIT).reverse().map(compactLog),
  };
}

export function estimateCompletion({ active, allDone, currentRunDone, concurrency, now = new Date() }) {
  const blocking = active.filter((item) => ["pending", "running", "retry_pending"].includes(item.status));
  if (!blocking.length) {
    return {
      available: true,
      complete: true,
      meanMinutesRemaining: 0,
      p90MinutesRemaining: 0,
      meanFinishAt: now.toISOString(),
      p90FinishAt: now.toISOString(),
      estimatedRemainingTokens: 0,
      basis: "queue_empty",
    };
  }
  if (!Number.isInteger(concurrency) || concurrency <= 0) {
    return {
      available: false,
      complete: false,
      reason: "concurrency_zero_or_unknown",
      estimatedRemainingTokens: estimateRemainingTokens(blocking, allDone, currentRunDone),
    };
  }

  const currentByDomain = groupBy(currentRunDone, (item) => item.domain || "unknown");
  const historyByDomain = groupBy(allDone, (item) => item.domain || "unknown");
  let meanWorkerMinutes = 0;
  let p90WorkerMinutes = 0;
  let remainingTokens = 0;
  let usedCurrentRunData = false;

  for (const item of blocking) {
    const domain = item.domain || "unknown";
    const currentItems = (currentByDomain.get(domain) || []).filter((sample) => matchesRuntime(sample, item));
    const historyItems = (historyByDomain.get(domain) || []).filter((sample) => matchesRuntime(sample, item));
    const source = currentItems.length >= 3 ? currentItems : historyItems;
    if (currentItems.length >= 3) usedCurrentRunData = true;
    const durationStats = numericStats(validDurations(source));
    if (!durationStats) {
      return {
        available: false,
        complete: false,
        reason: "model_history_unavailable",
        model: CODEX_MODEL,
        estimatedRemainingTokens: estimateRemainingTokens(blocking, allDone, currentRunDone),
      };
    }
    const mean = durationStats.average;
    const p90 = durationStats?.p90 ?? Math.max(DEFAULT_P90_MINUTES, mean * 1.35);
    const elapsed = item.status === "running"
      ? Math.max(0, now.getTime() - itemTimeMs(item, ["startedAt", "updatedAt"])) / 60_000
      : 0;
    meanWorkerMinutes += remainingDuration(mean, p90, elapsed, false);
    p90WorkerMinutes += remainingDuration(mean, p90, elapsed, true);
    const tokens = source.map(totalTokens).filter(Number.isFinite);
    remainingTokens += tokens.length ? average(tokens) : DEFAULT_TOKENS;
  }

  const meanMinutesRemaining = meanWorkerMinutes / concurrency;
  const p90MinutesRemaining = p90WorkerMinutes / concurrency;
  return {
    available: true,
    complete: false,
    meanMinutesRemaining: round(meanMinutesRemaining, 1),
    p90MinutesRemaining: round(p90MinutesRemaining, 1),
    meanFinishAt: new Date(now.getTime() + meanMinutesRemaining * 60_000).toISOString(),
    p90FinishAt: new Date(now.getTime() + p90MinutesRemaining * 60_000).toISOString(),
    estimatedRemainingTokens: Math.round(remainingTokens),
    basis: usedCurrentRunData ? "current_run_then_history" : "history_then_defaults",
  };
}

export function countMarkdownH1(text) {
  let fence = null;
  let count = 0;
  for (const line of text.split(/\r?\n/)) {
    const marker = line.match(/^ {0,3}(`{3,}|~{3,})(.*)$/);
    if (fence) {
      if (marker && marker[1][0] === fence.char && marker[1].length >= fence.length && !marker[2].trim()) fence = null;
      continue;
    }
    if (marker) {
      fence = { char: marker[1][0], length: marker[1].length };
      continue;
    }
    if (/^ {0,3}#(?:[ \t]+|$)/.test(line)) count += 1;
  }
  return count;
}

export function auditCompletedOutputs(items) {
  const signature = items.map((item) => {
    const outputPath = resolveOutputPath(item.outputFile);
    let fileSignature = "missing";
    try {
      const stat = fs.statSync(outputPath);
      fileSignature = `${stat.size}:${stat.mtimeMs}`;
    } catch {
      // Missing files are represented in the signature so later appearance invalidates the cache.
    }
    return `${item.id}:${item.outputFile}:${item.finishedAt}:${fileSignature}`;
  }).join("|");
  if (signature === outputAuditCache.signature) return outputAuditCache.value;
  if (!items.length) {
    outputAuditCache = { signature, value: emptyPathAudit() };
    return outputAuditCache.value;
  }

  const rows = [];
  const pathCounts = new Map();
  const hashCounts = new Map();
  const directories = new Set();
  for (const item of items) {
    const outputPath = resolveOutputPath(item.outputFile);
    const row = {
      id: item.id,
      subject: item.subject,
      outputFile: item.outputFile || null,
      exists: false,
      bytes: 0,
      h1Count: 0,
      placeholderCount: 0,
      insideProject: Boolean(outputPath && isInside(PROJECT_ROOT, outputPath)),
      hash: null,
      problems: [],
    };
    if (!outputPath || !fs.existsSync(outputPath)) {
      row.problems.push("missing");
    } else {
      const stat = fs.statSync(outputPath);
      if (!stat.isFile()) row.problems.push("not_file");
      else {
        row.exists = true;
        row.bytes = stat.size;
        directories.add(path.dirname(outputPath));
        const content = fs.readFileSync(outputPath);
        const text = content.toString("utf8");
        row.h1Count = countMarkdownH1(text);
        row.placeholderCount = [...text.matchAll(PLACEHOLDER_PATTERN)].length;
        row.hash = createHash("sha256").update(content).digest("hex");
        if (row.bytes <= 0) row.problems.push("empty");
        if (row.h1Count !== 1) row.problems.push("h1_count");
        if (row.placeholderCount > 0) row.problems.push("placeholder");
      }
    }
    if (!row.insideProject) row.problems.push("outside_project");
    const key = outputPath ? path.normalize(outputPath).toLowerCase() : "";
    if (key) pathCounts.set(key, (pathCounts.get(key) || 0) + 1);
    if (row.hash) hashCounts.set(row.hash, (hashCounts.get(row.hash) || 0) + 1);
    rows.push(row);
  }

  for (const row of rows) {
    const outputPath = resolveOutputPath(row.outputFile);
    const key = outputPath ? path.normalize(outputPath).toLowerCase() : "";
    if (key && pathCounts.get(key) > 1) row.problems.push("duplicate_path");
    if (row.hash && hashCounts.get(row.hash) > 1) row.problems.push("duplicate_content");
  }

  let artifactCount = 0;
  for (const directory of directories) {
    try {
      artifactCount += fs.readdirSync(directory, { withFileTypes: true })
        .filter((entry) => entry.isFile() && ARTIFACT_PATTERN.test(entry.name)).length;
    } catch {
      artifactCount += 1;
    }
  }

  const problems = rows.filter((row) => row.problems.length > 0);
  const value = {
    checked: rows.length,
    clean: problems.length === 0 && artifactCount === 0,
    missing: rows.filter((row) => row.problems.includes("missing")).length,
    empty: rows.filter((row) => row.problems.includes("empty")).length,
    badH1: rows.filter((row) => row.problems.includes("h1_count")).length,
    placeholderFiles: rows.filter((row) => row.problems.includes("placeholder")).length,
    duplicatePaths: rows.filter((row) => row.problems.includes("duplicate_path")).length,
    duplicateContent: rows.filter((row) => row.problems.includes("duplicate_content")).length,
    outsideProject: rows.filter((row) => row.problems.includes("outside_project")).length,
    artifacts: artifactCount,
    latestProblems: problems.slice(-RECENT_ITEM_LIMIT).reverse().map((row) => ({
      id: row.id,
      subject: row.subject,
      outputFile: row.outputFile,
      problems: row.problems,
    })),
  };
  outputAuditCache = { signature, value };
  return value;
}

export function summarizeQuota({ quota, eta, runnerAlive, runStartMs, currentRunDone, now }) {
  if (!quota) return { available: false, loading: true };
  if (quota.error) {
    return {
      available: false,
      loading: false,
      error: quota.error,
      checkedAt: quota.checkedAt || null,
    };
  }
  const used = quota.primaryUsedPercent;
  const remaining = Number.isFinite(used) ? Math.max(0, 100 - used) : null;
  // Subscription quota is not a fixed token budget. The former Astra calibration
  // cannot predict Sol usage; retain live percentages without fabricating forecasts.
  return {
    available: true,
    loading: false,
    blocked: Boolean(quota.blocked),
    primaryUsedPercent: used,
    primaryRemainingPercent: Number.isFinite(remaining) ? round(remaining, 1) : null,
    secondaryUsedPercent: quota.secondaryUsedPercent,
    thresholdPercent: QUOTA_USAGE_THRESHOLD,
    resetsAt: quota.resetsAt || null,
    resetCredits: quota.resetCredits ?? null,
    checkedAt: quota.checkedAt || null,
    projectedAtFinishUsedPercent: null,
    projectedAtFinishRemainingPercent: null,
    estimatedThresholdAt: null,
    estimatedTokensPerHour: null,
    forecastReason: "quota_conversion_uncalibrated",
  };
}

function deriveRunnerStatus({ lock, runnerAlive, concurrency, quota, lastLog }) {
  if (lock && !runnerAlive) return "stale_lock";
  if (!runnerAlive) return "stopped";
  if (quota?.blocked) return "quota_paused";
  if (concurrency === 0) return "concurrency_zero";
  if (/finished|exiting/i.test(lastLog?.event || "")) return "stopping";
  return "running";
}

function findRunStartMs(lock, logs) {
  const lockStart = toTimeMs(lock?.startedAt);
  if (lockStart) return lockStart;
  const startLog = logs.findLast((entry) => /Runner started\./i.test(entry.event || ""));
  return toTimeMs(startLog?.timestamp);
}

function estimateRemainingTokens(active, allDone, currentRunDone) {
  const currentByDomain = groupBy(currentRunDone, (item) => item.domain || "unknown");
  const historyByDomain = groupBy(allDone, (item) => item.domain || "unknown");
  return Math.round(sum(active
    .filter((item) => ["pending", "running", "retry_pending"].includes(item.status))
    .map((item) => {
      const domain = item.domain || "unknown";
      const current = (currentByDomain.get(domain) || []).filter((sample) => matchesRuntime(sample, item));
      const history = (historyByDomain.get(domain) || []).filter((sample) => matchesRuntime(sample, item));
      const source = current.length >= 3 ? current : history;
      const tokens = source.map(totalTokens).filter(Number.isFinite);
      return tokens.length ? average(tokens) : DEFAULT_TOKENS;
    })));
}

function matchesRuntime(sample, item) {
  const formalTurns = (sample.tokenUsage?.attempts || []).map((attempt) => attempt.formal).filter(Boolean);
  const effort = item.reasoningEffort || DEFAULT_REASONING_EFFORT;
  return formalTurns.length > 0 && formalTurns.every((turn) =>
    turn.model === CODEX_MODEL && (turn.reasoningEffort || sample.reasoningEffort) === effort);
}

function remainingDuration(mean, p90, elapsed, conservative) {
  const target = conservative ? p90 : mean;
  if (!elapsed) return target;
  if (elapsed < target) return target - elapsed;
  const tail = conservative ? Math.max(10, p90 * 0.2) : Math.max(5, (p90 - mean) * 0.5);
  return tail;
}

function numericStats(values) {
  const sorted = values.filter(Number.isFinite).sort((a, b) => a - b);
  if (!sorted.length) return null;
  return {
    count: sorted.length,
    average: round(average(sorted), 2),
    median: round(percentile(sorted, 0.5), 2),
    p90: round(percentile(sorted, 0.9), 2),
    min: round(sorted[0], 2),
    max: round(sorted.at(-1), 2),
  };
}

function validDurations(items) {
  return items.map(durationMinutes).filter(Number.isFinite);
}

function durationMinutes(item) {
  const start = itemTimeMs(item, ["startedAt"]);
  const finish = itemTimeMs(item, ["finishedAt", "archivedAt"]);
  if (!start || !finish || finish < start) return null;
  return round((finish - start) / 60_000, 2);
}

function totalTokens(item) {
  const value = Number(item?.tokenUsage?.total?.totalTokens ?? item?.tokenUsage?.totalTokens);
  return Number.isFinite(value) ? value : null;
}

function classifyAnomaly(entry) {
  const text = `${entry.event || ""} ${entry.message || ""} ${entry.error || ""}`.toLowerCase();
  if (text.includes("quota")) return "quota";
  if (text.includes("timeout")) return "timeout";
  if (text.includes("capacity")) return "capacity";
  if (text.includes("retry")) return "retry";
  if (text.includes("stale") || text.includes("recover")) return "recovery";
  if (text.includes("abort") || text.includes("interrupt")) return "interrupted";
  if (text.includes("validation")) return "validation";
  if (text.includes("fail") || text.includes("error")) return "failure";
  return String(entry.level || "other").toLowerCase();
}

function compactLog(entry) {
  return {
    timestamp: entry.timestamp || null,
    level: entry.level || "info",
    event: entry.event || entry.message || "",
    id: entry.id || null,
    status: entry.status || null,
    details: entry.error || entry.message || null,
  };
}

function readJsonlCached(filePath) {
  return readCached(filePath, (text) => text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => JSON.parse(line)), []);
}

function readJsonCached(filePath) {
  return readCached(filePath, (text) => JSON.parse(text), null);
}

function readCached(filePath, parser, missingValue) {
  let stat;
  try {
    stat = fs.statSync(filePath);
  } catch {
    fileCache.delete(filePath);
    return missingValue;
  }
  const signature = `${stat.size}:${stat.mtimeMs}`;
  const cached = fileCache.get(filePath);
  if (cached?.signature === signature) return cached.value;
  const value = parser(fs.readFileSync(filePath, "utf8"));
  fileCache.set(filePath, { signature, value });
  return value;
}

function fileUpdatedAt(filePath) {
  try {
    return fs.statSync(filePath).mtime.toISOString();
  } catch {
    return null;
  }
}

function resolveOutputPath(outputFile) {
  if (!outputFile || typeof outputFile !== "string") return null;
  return path.isAbsolute(outputFile) ? path.resolve(outputFile) : path.resolve(PROJECT_ROOT, outputFile);
}

function isInside(root, target) {
  const relative = path.relative(path.resolve(root), path.resolve(target));
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

function itemTimeMs(item, keys) {
  for (const key of keys) {
    const value = toTimeMs(item?.[key]);
    if (value) return value;
  }
  return 0;
}

function toTimeMs(value) {
  if (!value) return 0;
  if (value instanceof Date) return value.getTime();
  const raw = String(value).trim();
  const normalized = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(raw)
    ? raw.replace(" ", "T")
    : raw;
  const parsed = Date.parse(normalized);
  return Number.isFinite(parsed) ? parsed : 0;
}

function countBy(items, keyFn) {
  const counts = {};
  for (const item of items) {
    const key = String(keyFn(item));
    counts[key] = (counts[key] || 0) + 1;
  }
  return counts;
}

function groupBy(items, keyFn) {
  const groups = new Map();
  for (const item of items) {
    const key = keyFn(item);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(item);
  }
  return groups;
}

function percentile(sorted, ratio) {
  return sorted[Math.ceil((sorted.length - 1) * ratio)];
}

function average(values) {
  return values.length ? sum(values) / values.length : 0;
}

function sum(values) {
  return values.reduce((total, value) => total + Number(value || 0), 0);
}

function round(value, digits = 0) {
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function emptyPathAudit() {
  return {
    checked: 0,
    clean: true,
    missing: 0,
    empty: 0,
    badH1: 0,
    placeholderFiles: 0,
    duplicatePaths: 0,
    duplicateContent: 0,
    outsideProject: 0,
    artifacts: 0,
    latestProblems: [],
  };
}
