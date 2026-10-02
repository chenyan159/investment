import fs from "node:fs";
import path from "node:path";

const TOKEN_KEYS = [
  "inputTokens",
  "cachedInputTokens",
  "outputTokens",
  "reasoningOutputTokens",
  "totalTokens",
];

const SESSION_FILE_RE = /([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\.jsonl$/i;
const SESSION_INDEX_CACHE = new Map();
const SESSION_INDEX_TTL_MS = 10_000;

function nonNegativeNumber(value) {
  const parsed = Number(value || 0);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 0;
}

function zeroCounter() {
  return Object.fromEntries(TOKEN_KEYS.map((key) => [key, 0]));
}

function addCounters(left, right) {
  const total = zeroCounter();
  for (const key of TOKEN_KEYS) {
    total[key] = nonNegativeNumber(left?.[key]) + nonNegativeNumber(right?.[key]);
  }
  return total;
}

function usageToCounter(usage) {
  if (!usage) return null;
  const inputTokens = nonNegativeNumber(usage.input_tokens ?? usage.inputTokens);
  const cachedInputTokens = nonNegativeNumber(usage.cached_input_tokens ?? usage.cachedInputTokens);
  const outputTokens = nonNegativeNumber(usage.output_tokens ?? usage.outputTokens);
  const reasoningOutputTokens = nonNegativeNumber(usage.reasoning_output_tokens ?? usage.reasoningOutputTokens);
  if (!(inputTokens || cachedInputTokens || outputTokens || reasoningOutputTokens)) return null;
  return {
    inputTokens,
    cachedInputTokens,
    outputTokens,
    reasoningOutputTokens,
    // Reasoning output is a subset of output; do not add it a second time.
    totalTokens: inputTokens + outputTokens,
  };
}

function resolveCodexHome(env = process.env) {
  const configured = String(env.CODEX_HOME || "").trim();
  if (configured) return path.resolve(configured);
  const userProfile = String(env.USERPROFILE || env.HOME || "").trim();
  return userProfile ? path.join(path.resolve(userProfile), ".codex") : "";
}

function buildSessionIndex(codexHome) {
  const sessionsRoot = path.join(codexHome, "sessions");
  if (!fs.existsSync(sessionsRoot)) return new Map();

  const cached = SESSION_INDEX_CACHE.get(sessionsRoot);
  if (cached && Date.now() - cached.createdAt < SESSION_INDEX_TTL_MS) return cached.files;

  const files = new Map();
  const pending = [sessionsRoot];
  while (pending.length) {
    const current = pending.pop();
    let entries;
    try {
      entries = fs.readdirSync(current, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const entry of entries) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        pending.push(fullPath);
        continue;
      }
      if (!entry.isFile() || !entry.name.endsWith(".jsonl")) continue;
      const match = entry.name.match(SESSION_FILE_RE);
      if (match) files.set(match[1], fullPath);
    }
  }
  SESSION_INDEX_CACHE.set(sessionsRoot, { createdAt: Date.now(), files });
  return files;
}

function readSessionTelemetry(filePath) {
  let text;
  try {
    text = fs.readFileSync(filePath, "utf8");
  } catch {
    return { usage: null, childThreadIds: [] };
  }

  let usage = null;
  const childThreadIds = new Set();
  for (const line of text.split(/\r?\n/)) {
    if (!line) continue;
    let event;
    try {
      event = JSON.parse(line);
    } catch {
      continue;
    }
    const payload = event?.payload;
    if (event?.type === "event_msg" && payload?.type === "token_count") {
      const candidate = usageToCounter(payload?.info?.total_token_usage);
      if (candidate) usage = candidate;
    }
    if (event?.type === "event_msg" && payload?.type === "sub_agent_activity") {
      const childId = String(payload.agent_thread_id || "").trim();
      if (childId) childThreadIds.add(childId);
    }
  }
  return { usage, childThreadIds: Array.from(childThreadIds) };
}

// Recovery is exceptional and read once at the research deadline. A newly
// started runner thread must contain exactly one root turn; stale/resumed,
// errored, truncated, or still-running sessions are not completion evidence.
export function readSuccessfulSessionCompletion(threadId, { startedAfter, codexHome = resolveCodexHome() } = {}) {
  if (!threadId || !Number.isFinite(startedAfter)) return null;
  const filePath = buildSessionIndex(codexHome).get(threadId);
  if (!filePath) return null;
  try {
    const rows = fs.readFileSync(filePath, 'utf8').trim().split(/\r?\n/).map(JSON.parse);
    const meta = rows[0];
    if (meta?.type !== 'session_meta' || meta.payload?.id !== threadId ||
        !(Date.parse(meta.timestamp) >= startedAfter)) return null;
    const turns = rows.filter(r => r.type === 'event_msg' && r.payload?.type === 'task_started');
    const terminal = rows.at(-1);
    if (turns.length !== 1 || terminal?.type !== 'event_msg' || terminal.payload?.type !== 'task_complete') return null;
    const end = terminal.payload;
    if (!turns[0].payload.turn_id || end.turn_id !== turns[0].payload.turn_id || end.error ||
        typeof end.last_agent_message !== 'string' || !end.last_agent_message.trim()) return null;
    return { items: [], finalResponse: end.last_agent_message, usage: null };
  } catch {
    return null;
  }
}

/**
 * Aggregate a root Codex thread and all subagent threads visible in its
 * session telemetry. The returned counters are task-level counters; child
 * thread identities are intentionally not returned to the queue archive.
 */
export function collectCodexThreadUsage(rootThreadId, { directUsage = null, codexHome = resolveCodexHome() } = {}) {
  const rootId = String(rootThreadId || "").trim();
  const directCounter = usageToCounter(directUsage);
  if (!rootId || !codexHome) {
    return {
      counters: directCounter,
      threadCount: directCounter ? 1 : 0,
      subagentThreadCount: 0,
      unresolvedThreadCount: 0,
      usageSource: directCounter ? "sdk" : "unavailable",
    };
  }

  const index = buildSessionIndex(codexHome);
  const pending = [rootId];
  const seen = new Set();
  let counters = zeroCounter();
  let hasTelemetry = false;
  let unresolvedThreadCount = 0;

  while (pending.length) {
    const threadId = pending.shift();
    if (!threadId || seen.has(threadId)) continue;
    seen.add(threadId);
    const filePath = index.get(threadId);
    if (!filePath) {
      unresolvedThreadCount += 1;
      if (threadId === rootId && directCounter) counters = addCounters(counters, directCounter);
      continue;
    }
    const telemetry = readSessionTelemetry(filePath);
    if (telemetry.usage) {
      counters = addCounters(counters, telemetry.usage);
      hasTelemetry = true;
    } else if (threadId === rootId && directCounter) {
      counters = addCounters(counters, directCounter);
    } else {
      unresolvedThreadCount += 1;
    }
    for (const childId of telemetry.childThreadIds) {
      if (!seen.has(childId)) pending.push(childId);
    }
  }

  if (!hasTelemetry && directCounter) {
    counters = directCounter;
  }
  const threadCount = seen.size;
  return {
    counters: (counters.totalTokens || counters.inputTokens || counters.outputTokens) ? counters : null,
    threadCount,
    subagentThreadCount: Math.max(threadCount - 1, 0),
    unresolvedThreadCount,
    usageSource: hasTelemetry ? "sdk+codex_session_telemetry" : (directCounter ? "sdk" : "unavailable"),
  };
}

export function enrichTokenCounter(counter, metadata = {}) {
  if (!counter) return null;
  const inputTokens = nonNegativeNumber(counter.inputTokens);
  const cachedInputTokens = Math.min(nonNegativeNumber(counter.cachedInputTokens), inputTokens);
  return {
    ...counter,
    inputTokens,
    cachedInputTokens,
    outputTokens: nonNegativeNumber(counter.outputTokens),
    reasoningOutputTokens: nonNegativeNumber(counter.reasoningOutputTokens),
    totalTokens: inputTokens + nonNegativeNumber(counter.outputTokens),
    uncachedInputTokens: Math.max(inputTokens - cachedInputTokens, 0),
    cachedInputRatio: inputTokens ? cachedInputTokens / inputTokens : 0,
    ...metadata,
  };
}
