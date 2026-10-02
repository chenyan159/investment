import test from "node:test";
import assert from "node:assert/strict";

// Kept outside Node's default discovery paths so the parent runner test suite stays independent.

import {
  estimateCompletion,
  summarizeAnomalies,
  summarizeDone,
  summarizeQueue,
  summarizeQuota,
  summarizeRunning,
} from "../snapshot.mjs";

const now = new Date("2026-07-17T08:00:00.000Z");

test("queue summary favors counts over long item lists", () => {
  const active = [
    { domain: "company", status: "running" },
    { domain: "company", status: "pending" },
    { domain: "file-run", status: "retry_pending" },
    { domain: "file-run", status: "failed" },
  ];
  const result = summarizeQueue(active, [{ status: "done" }, { status: "done" }]);
  assert.equal(result.active, 4);
  assert.equal(result.running, 1);
  assert.equal(result.pending, 1);
  assert.equal(result.retryPending, 1);
  assert.equal(result.failed, 1);
  assert.equal(result.currentRunTotal, 6);
  assert.equal(result.progressPercent, 33.3);
  assert.equal(result.domains.length, 2);
});

test("running summary returns every row with the newest tasks first", () => {
  const items = Array.from({ length: 12 }, (_, index) => ({
    id: `job-${index}`,
    domain: "company",
    subject: `S${index}`,
    status: "running",
    attempts: index === 0 ? 2 : 1,
    startedAt: new Date(now.getTime() - index * 60_000).toISOString(),
  }));
  const result = summarizeRunning(items, now);
  assert.equal(result.count, 12);
  assert.equal(result.items.length, 12);
  assert.equal(result.items[0].subject, "S0");
  assert.equal(result.items.at(-1).subject, "S11");
  assert.equal(result.retrying, 1);
  assert.equal(result.maxElapsedMinutes, 11);
});

test("quota summary exposes remaining percentages for current and projected usage", () => {
  const result = summarizeQuota({
    quota: { primaryUsedPercent: 68, secondaryUsedPercent: 20, blocked: false },
    eta: { estimatedRemainingTokens: 214_363_951 },
    runnerAlive: false,
    runStartMs: null,
    currentRunDone: [],
    now,
  });
  assert.equal(result.primaryUsedPercent, 68);
  assert.equal(result.primaryRemainingPercent, 32);
  assert.equal(result.projectedAtFinishUsedPercent, 78);
  assert.equal(result.projectedAtFinishRemainingPercent, 22);
});

test("completed summary calculates duration, token and attempt statistics", () => {
  const items = [
    doneItem("A", 10, 5_000_000, 1),
    doneItem("B", 20, 7_000_000, 2),
    doneItem("C", 30, 9_000_000, 1),
  ];
  const result = summarizeDone(items, items);
  assert.equal(result.currentRun, 3);
  assert.equal(result.duration.average, 20);
  assert.equal(result.duration.median, 20);
  assert.equal(result.duration.p90, 30);
  assert.equal(result.totalTokens, 21_000_000);
  assert.equal(result.firstAttempt, 2);
  assert.equal(result.retried, 1);
});

test("anomalies are aggregated by kind and latest rows are bounded", () => {
  const logs = [
    { timestamp: "2026-07-17T00:00:00Z", level: "info", event: "Runner started." },
    { timestamp: "2026-07-17T00:01:00Z", level: "error", event: "Model capacity failure." },
    { timestamp: "2026-07-17T00:02:00Z", level: "warn", event: "Retry pending." },
    { timestamp: "2026-07-17T00:03:00Z", level: "info", event: "Codex quota threshold reached." },
  ];
  const result = summarizeAnomalies(logs);
  assert.equal(result.total, 3);
  assert.equal(result.errors, 1);
  assert.equal(result.warnings, 1);
  assert.equal(result.byKind.capacity, 1);
  assert.equal(result.byKind.retry, 1);
  assert.equal(result.byKind.quota, 1);
});

test("ETA uses current-run domain data and respects concurrency", () => {
  const history = [
    doneItem("A", 20, 6_000_000),
    doneItem("B", 20, 6_000_000),
    doneItem("C", 20, 6_000_000),
  ];
  const active = [
    { domain: "company", status: "pending" },
    { domain: "company", status: "pending" },
    { domain: "company", status: "pending" },
    { domain: "company", status: "pending" },
  ];
  const result = estimateCompletion({ active, allDone: history, currentRunDone: history, concurrency: 2, now });
  assert.equal(result.available, true);
  assert.equal(result.meanMinutesRemaining, 40);
  assert.equal(result.estimatedRemainingTokens, 24_000_000);
  assert.equal(result.basis, "current_run_then_history");
});

test("ETA is unavailable at concurrency zero without changing queue state", () => {
  const result = estimateCompletion({
    active: [{ domain: "company", status: "pending" }],
    allDone: [],
    currentRunDone: [],
    concurrency: 0,
    now,
  });
  assert.equal(result.available, false);
  assert.equal(result.reason, "concurrency_zero_or_unknown");
  assert.equal(result.estimatedRemainingTokens, 7_500_000);
});

function doneItem(subject, minutes, tokens, attempts = 1) {
  const started = new Date("2026-07-17T00:00:00Z");
  const finished = new Date(started.getTime() + minutes * 60_000);
  return {
    id: `done-${subject}`,
    domain: "company",
    subject,
    displayName: subject,
    status: "done",
    attempts,
    startedAt: started.toISOString(),
    finishedAt: finished.toISOString(),
    archivedAt: finished.toISOString(),
    outputFile: `out/${subject}.md`,
    tokenUsage: { total: { totalTokens: tokens } },
  };
}
