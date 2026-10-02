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

test("quota remains available below the 99 percent threshold", () => {
  const quota = evaluateCodexQuota(quotaResult(98, 50), { nowMs: NOW });
  assert.equal(QUOTA_USAGE_THRESHOLD, 99);
  assert.equal(quota.blocked, false);
  assert.equal(quota.pauseUntil, 0);
});

test("quota pauses at 99 percent until the blocked window reset plus buffer", () => {
  const quota = evaluateCodexQuota(quotaResult(99, 50), { nowMs: NOW });
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
    probe: async () => quotaResult(40, 99),
  });
  const quota = await gate.afterTaskFailure();
  assert.equal(quota.blocked, true);
  assert.deepEqual(quota.blockedWindows, ["secondary"]);
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
