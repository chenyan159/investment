import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { collectCodexThreadUsage, enrichTokenCounter, readSuccessfulSessionCompletion } from "../usage-telemetry.mjs";

function writeSession(root, id, events) {
  const file = path.join(root, "sessions", "2026", "07", "10", `rollout-${id}.jsonl`);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${events.map((event) => JSON.stringify(event)).join("\n")}\n`, "utf8");
}

function tokenEvent(total_token_usage) {
  return { type: "event_msg", payload: { type: "token_count", info: { total_token_usage } } };
}

test('completion recovery rejects failed, stale, resumed and truncated sessions', () => {
  const codexHome = fs.mkdtempSync(path.join(os.tmpdir(), 'runner-completion-'));
  const id = '55555555-5555-4555-8555-555555555555';
  const date = '2026-09-09T16:23:21.186Z';
  const valid = [
    { timestamp: date, type: 'session_meta', payload: { id } },
    { timestamp: date, type: 'event_msg', payload: { type: 'task_started', turn_id: 'root-turn' } },
    { type: 'event_msg', payload: { type: 'task_complete', turn_id: 'root-turn', last_agent_message: 'report finished' } },
  ];
  const read = (startedAfter = Date.parse(date) - 100) => readSuccessfulSessionCompletion(id, { startedAfter, codexHome });
  try {
    writeSession(codexHome, id, valid);
    assert.equal(read().finalResponse, 'report finished');
    assert.equal(read(Date.parse(date) + 1), null);
    for (const changes of [
      { error: { message: 'usage limit' } }, { last_agent_message: '' }, { turn_id: 'child-turn' },
    ]) {
      writeSession(codexHome, id, [...valid.slice(0, 2), { ...valid[2], payload: { ...valid[2].payload, ...changes } }]);
      assert.equal(read(), null);
    }
    writeSession(codexHome, id, [...valid, valid[1]]);
    assert.equal(read(), null);
    writeSession(codexHome, id, [...valid, valid[1], valid[2]]);
    assert.equal(read(), null);
    // Seen in six historical sessions: command failures arrived after the
    // terminal event. Do not recover these ambiguous sessions automatically.
    writeSession(codexHome, id, [...valid, { type: 'event_msg', payload: { type: 'item_completed', item: { type: 'CommandExecution', status: 'failed' } } }]);
    assert.equal(read(), null);
    writeSession(codexHome, id, valid);
    const file = path.join(codexHome, 'sessions', '2026', '07', '10', `rollout-${id}.jsonl`);
    fs.appendFileSync(file, '{"type":');
    assert.equal(read(), null);
  } finally {
    fs.rmSync(codexHome, { recursive: true, force: true });
  }
});

test("aggregates parent and subagent session usage without exposing child rows", () => {
  const codexHome = fs.mkdtempSync(path.join(os.tmpdir(), "research-runner-codex-"));
  const parent = "11111111-1111-4111-8111-111111111111";
  const child = "22222222-2222-4222-8222-222222222222";
  const grandchild = "44444444-4444-4444-8444-444444444444";
  try {
    writeSession(codexHome, parent, [
      tokenEvent({ input_tokens: 100, cached_input_tokens: 80, output_tokens: 20, reasoning_output_tokens: 5 }),
      { type: "event_msg", payload: { type: "sub_agent_activity", agent_thread_id: child, kind: "started" } },
    ]);
    writeSession(codexHome, child, [
      tokenEvent({ input_tokens: 50, cached_input_tokens: 40, output_tokens: 10, reasoning_output_tokens: 3 }),
      { type: "event_msg", payload: { type: "sub_agent_activity", agent_thread_id: grandchild, kind: "started" } },
    ]);
    writeSession(codexHome, grandchild, [
      tokenEvent({ input_tokens: 25, cached_input_tokens: 20, output_tokens: 5, reasoning_output_tokens: 1 }),
    ]);

    const result = collectCodexThreadUsage(parent, { codexHome });
    assert.deepEqual(result.counters, {
      inputTokens: 175,
      cachedInputTokens: 140,
      outputTokens: 35,
      reasoningOutputTokens: 9,
      totalTokens: 210,
    });
    assert.equal(result.threadCount, 3);
    assert.equal(result.subagentThreadCount, 2);
    assert.equal(result.unresolvedThreadCount, 0);
    assert.equal(result.usageSource, "sdk+codex_session_telemetry");
    assert.deepEqual(enrichTokenCounter(result.counters, { includesSubagents: true }), {
      inputTokens: 175,
      cachedInputTokens: 140,
      outputTokens: 35,
      reasoningOutputTokens: 9,
      totalTokens: 210,
      uncachedInputTokens: 35,
      cachedInputRatio: 0.8,
      includesSubagents: true,
    });
  } finally {
    fs.rmSync(codexHome, { recursive: true, force: true });
  }
});

test("falls back to SDK usage when session telemetry is unavailable", () => {
  const codexHome = fs.mkdtempSync(path.join(os.tmpdir(), "research-runner-codex-empty-"));
  try {
    const result = collectCodexThreadUsage("33333333-3333-4333-8333-333333333333", {
      codexHome,
      directUsage: {
        input_tokens: 12,
        cached_input_tokens: 4,
        output_tokens: 3,
        reasoning_output_tokens: 1,
      },
    });
    assert.deepEqual(result.counters, {
      inputTokens: 12,
      cachedInputTokens: 4,
      outputTokens: 3,
      reasoningOutputTokens: 1,
      totalTokens: 15,
    });
    assert.equal(result.threadCount, 1);
    assert.equal(result.unresolvedThreadCount, 1);
    assert.equal(result.usageSource, "sdk");
  } finally {
    fs.rmSync(codexHome, { recursive: true, force: true });
  }
});
