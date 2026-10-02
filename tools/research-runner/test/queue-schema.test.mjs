import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  appendTokenUsageAttempt,
  normalizeQueueItem,
  normalizeReasoningEffort,
  sumTokenCounters,
} from "../queue-store.mjs";

function baseItem(overrides = {}) {
  return {
    id: "test-item",
    domain: "company",
    subject: "TEST",
    ...overrides,
  };
}

test("queue items default to max reasoning", () => {
  assert.equal(normalizeQueueItem(baseItem()).reasoningEffort, "max");
});

test("reasoning aliases normalize and Sol-specific levels remain available", () => {
  assert.equal(normalizeReasoningEffort("extra high"), "xhigh");
  assert.equal(normalizeReasoningEffort("extra-high"), "xhigh");
  assert.equal(normalizeReasoningEffort("maximum"), "max");
  assert.equal(normalizeReasoningEffort("ultra"), "ultra");
  assert.throws(() => normalizeReasoningEffort("minimal"), /unsupported value/);
});

test("token usage aggregates successful and retry attempts without double-counting subsets", () => {
  const first = {
    attempt: 1,
    formal: { inputTokens: 100, cachedInputTokens: 60, outputTokens: 20, reasoningOutputTokens: 5, totalTokens: 120 },
    verification: { inputTokens: 10, cachedInputTokens: 4, outputTokens: 2, reasoningOutputTokens: 1, totalTokens: 12 },
    total: sumTokenCounters([
      { inputTokens: 100, cachedInputTokens: 60, outputTokens: 20, reasoningOutputTokens: 5, totalTokens: 120 },
      { inputTokens: 10, cachedInputTokens: 4, outputTokens: 2, reasoningOutputTokens: 1, totalTokens: 12 },
    ]),
  };
  const second = {
    attempt: 2,
    formal: { inputTokens: 50, cachedInputTokens: 20, outputTokens: 10, reasoningOutputTokens: 3, totalTokens: 60 },
    verification: null,
    total: sumTokenCounters([
      { inputTokens: 50, cachedInputTokens: 20, outputTokens: 10, reasoningOutputTokens: 3, totalTokens: 60 },
    ]),
  };

  const usage = appendTokenUsageAttempt(appendTokenUsageAttempt(undefined, first), second);
  assert.equal(usage.attempts.length, 2);
  assert.deepEqual(usage.total, {
    inputTokens: 160,
    cachedInputTokens: 84,
    outputTokens: 32,
    reasoningOutputTokens: 9,
    totalTokens: 192,
    uncachedInputTokens: 76,
    cachedInputRatio: 0.525,
    threadCount: 0,
    subagentThreadCount: 0,
    unresolvedThreadCount: 0,
    includesSubagents: false,
  });
});

test("token usage archive preserves parent-plus-subagent aggregation metadata", () => {
  const usage = appendTokenUsageAttempt(undefined, {
    attempt: 1,
    formal: {
      inputTokens: 100,
      cachedInputTokens: 50,
      outputTokens: 10,
      reasoningOutputTokens: 2,
      totalTokens: 110,
      includesSubagents: true,
      subagentThreadCount: 2,
    },
    verification: null,
    total: {
      inputTokens: 100,
      cachedInputTokens: 50,
      outputTokens: 10,
      reasoningOutputTokens: 2,
      totalTokens: 110,
      includesSubagents: true,
      subagentThreadCount: 2,
    },
    includesSubagents: true,
    usageAggregation: "parent_plus_subagents",
  });
  assert.equal(usage.includesSubagents, true);
  assert.equal(usage.usageAggregation, "parent_plus_subagents");
  assert.equal(usage.total.uncachedInputTokens, 50);
  assert.equal(usage.total.cachedInputRatio, 0.5);
  assert.equal(usage.total.subagentThreadCount, 2);
});

test("completed queue items archive reasoning and token usage", async () => {
  const queueDir = fs.mkdtempSync(path.join(os.tmpdir(), "research-runner-queue-test-"));
  const previousQueueDir = process.env.RESEARCH_RUNNER_QUEUE_DIR;
  process.env.RESEARCH_RUNNER_QUEUE_DIR = queueDir;
  try {
    const store = await import(`../queue-store.mjs?queue-test=${Date.now()}`);
    store.ensureQueueFiles();
    store.writeActiveQueue([baseItem({ status: "pending", reasoningEffort: "ultra" })]);
    store.markQueueItemDone("test-item", {
      outputFile: "company/test.md",
      tokenUsageAttempt: {
        attempt: 1,
        formal: { inputTokens: 100, cachedInputTokens: 50, outputTokens: 20, reasoningOutputTokens: 5, totalTokens: 120 },
        verification: { inputTokens: 10, cachedInputTokens: 5, outputTokens: 2, reasoningOutputTokens: 1, totalTokens: 12 },
        total: { inputTokens: 110, cachedInputTokens: 55, outputTokens: 22, reasoningOutputTokens: 6, totalTokens: 132 },
      },
    });
    store.archiveDoneItems();

    const [done] = store.readDoneQueue();
    assert.equal(done.reasoningEffort, "ultra");
    assert.equal(done.tokenUsage.attempts.length, 1);
    assert.equal(done.tokenUsage.total.inputTokens, 110);
    assert.equal(done.tokenUsage.total.outputTokens, 22);
    assert.equal(done.tokenUsage.total.totalTokens, 132);
  } finally {
    if (previousQueueDir === undefined) delete process.env.RESEARCH_RUNNER_QUEUE_DIR;
    else process.env.RESEARCH_RUNNER_QUEUE_DIR = previousQueueDir;
    fs.rmSync(queueDir, { recursive: true, force: true });
  }
});

test("queue control persists a non-negative integer concurrency beside the queue", async () => {
  const queueDir = fs.mkdtempSync(path.join(os.tmpdir(), "research-runner-control-test-"));
  const previousQueueDir = process.env.RESEARCH_RUNNER_QUEUE_DIR;
  process.env.RESEARCH_RUNNER_QUEUE_DIR = queueDir;
  try {
    const store = await import(`../queue-store.mjs?queue-control-test=${Date.now()}`);
    assert.equal(store.readQueueControl(), null);

    assert.deepEqual(store.writeQueueControl({ concurrency: 3 }), { concurrency: 3 });
    assert.deepEqual(store.readQueueControl(), { concurrency: 3 });
    assert.equal(path.dirname(store.QUEUE_CONTROL_PATH), queueDir);

    fs.writeFileSync(store.QUEUE_CONTROL_PATH, '{"concurrency":5}\n', "utf8");
    assert.deepEqual(store.readQueueControl(), { concurrency: 5 });

    assert.deepEqual(store.writeQueueControl({ concurrency: 0 }), { concurrency: 0 });
    assert.deepEqual(store.readQueueControl(), { concurrency: 0 });

    fs.writeFileSync(store.QUEUE_CONTROL_PATH, '{"concurrency":-1}\n', "utf8");
    assert.throws(() => store.readQueueControl(), /non-negative integer/);
  } finally {
    if (previousQueueDir === undefined) delete process.env.RESEARCH_RUNNER_QUEUE_DIR;
    else process.env.RESEARCH_RUNNER_QUEUE_DIR = previousQueueDir;
    fs.rmSync(queueDir, { recursive: true, force: true });
  }
});

test("quota deferral returns a claimed item without consuming an attempt", async () => {
  const queueDir = fs.mkdtempSync(path.join(os.tmpdir(), "research-runner-quota-defer-test-"));
  const previousQueueDir = process.env.RESEARCH_RUNNER_QUEUE_DIR;
  process.env.RESEARCH_RUNNER_QUEUE_DIR = queueDir;
  try {
    const store = await import(`../queue-store.mjs?quota-defer-test=${Date.now()}`);
    store.writeActiveQueue([baseItem({ status: "pending", attempts: 0 })]);

    const claimed = store.claimNextQueueItem({ maxAttempts: 7 });
    assert.equal(claimed.status, "running");
    assert.equal(claimed.attempts, 1);

    const pauseUntil = Date.now() + 60_000;
    const deferred = store.deferQueueItemForQuota("test-item", pauseUntil);
    assert.equal(deferred.finalStatus, "retry_pending");
    assert.equal(deferred.attempts, 0);

    const [item] = store.readActiveQueue();
    assert.equal(item.status, "retry_pending");
    assert.equal(item.attempts, 0);
    assert.match(item.note, /^codex_quota_exit: retry on next launch;/);
  } finally {
    if (previousQueueDir === undefined) delete process.env.RESEARCH_RUNNER_QUEUE_DIR;
    else process.env.RESEARCH_RUNNER_QUEUE_DIR = previousQueueDir;
    fs.rmSync(queueDir, { recursive: true, force: true });
  }
});
