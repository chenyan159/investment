import assert from "node:assert/strict";
import test from "node:test";
import {
  createQuotaGate,
  evaluateCodexQuota,
  QUOTA_USAGE_THRESHOLD,
} from "../quota-control.mjs";

const NOW = 1_700_000_000_000;

function quotaResult(primaryUsedPercent, secondaryUsedPercent) {
  return {
    rateLimits: {
      primary: { usedPercent: primaryUsedPercent, resetsAt: NOW / 1000 + 300 },
      secondary: { usedPercent: secondaryUsedPercent, resetsAt: NOW / 1000 + 600 },
      rateLimitReachedType: null,
    },
  };
}

test("quota remains available below the 95 percent threshold", () => {
  const quota = evaluateCodexQuota(quotaResult(94.9, 50), { nowMs: NOW });
  assert.equal(QUOTA_USAGE_THRESHOLD, 95);
  assert.equal(quota.blocked, false);
  assert.equal(quota.pauseUntil, 0);
});

test("quota pauses at 95 percent until the blocked window reset plus buffer", () => {
  const quota = evaluateCodexQuota(quotaResult(95, 50), { nowMs: NOW });
  assert.equal(quota.blocked, true);
  assert.deepEqual(quota.blockedWindows, ["primary"]);
  assert.equal(quota.pauseUntil, NOW + 300_000 + 60_000);
});

test("preflight query failure allows the task to continue", async () => {
  const gate = createQuotaGate({
    log() {},
    probe: async () => { throw new Error("temporary query failure"); },
  });
  assert.deepEqual(await gate.beforeTask(), { allowed: true, queryFailed: true });
});

test("successful failure-time query identifies quota blocking without error text parsing", async () => {
  const gate = createQuotaGate({
    log() {},
    probe: async () => quotaResult(40, 95),
  });
  const quota = await gate.afterTaskFailure();
  assert.equal(quota.blocked, true);
  assert.deepEqual(quota.blockedWindows, ["secondary"]);
  assert.equal(gate.shouldExit(), true);
});

test("task failure plus quota-query failure waits 60 seconds before rechecking", async () => {
  let probes = 0;
  const sleeps = [];
  const gate = createQuotaGate({
    log() {},
    probe: async () => {
      probes += 1;
      if (probes === 1) throw new Error("temporary query failure");
      return quotaResult(20, 30);
    },
    sleep: async (milliseconds) => { sleeps.push(milliseconds); },
  });

  const quota = await gate.afterTaskFailure();
  assert.equal(quota.blocked, false);
  assert.equal(probes, 2);
  assert.deepEqual(sleeps, [60_000]);
});

 test("quota exhaustion requests a sticky exit and never probes again in the same run", async () => {
  let probes = 0;
  const messages = [];
  const gate = createQuotaGate({ log: message => messages.push(message), probe: async () => { probes++; return quotaResult(95, 20); } });
  assert.equal(gate.shouldExit(), false);
  assert.equal((await gate.beforeTask()).allowed, false);
  assert.equal(gate.shouldExit(), true);
  assert.equal((await gate.beforeTask()).allowed, false);
  assert.equal(probes, 1);
  assert.equal(messages.length, 1);
  assert.match(messages[0], /exiting after active tasks/);
});
