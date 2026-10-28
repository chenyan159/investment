import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const source = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const readRows = file => fs.readFileSync(file, 'utf8').split(/\r?\n/).filter(Boolean).map(JSON.parse);

// Run the real scheduler and queue store in a disposable workspace. Replace
// research/network adapters only; no real Codex process or production queue runs.
function fixture(count) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'runner-scheduling-'));
  const runner = path.join(root, 'runner');
  const queue = path.join(root, 'queue');
  const write = (relative, body) => {
    const file = path.join(runner, relative);
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, body);
  };
  for (const relative of ['runner.mjs', 'queue-store.mjs', 'research-plan-store.mjs', 'research-plans.json', 'runtime-config.mjs', 'domains/output-path.mjs']) {
    write(relative, fs.readFileSync(path.join(source, relative)));
  }
  write('domains/index.mjs', `
    export const checkRequiredPaths = () => {};
    export const getDomainAdapter = () => ({ buildFormalPrompt: item => JSON.stringify(item) });
  `);
  write('quota-control.mjs', `
    export const QUOTA_USAGE_THRESHOLD = 95;
    export const createQuotaGate = () => ({
      beforeTask: async () => ({allowed:true}), afterTaskFailure: async () => ({blocked:false}),
      shouldExit: () => false, isPaused: () => false,
    });
  `);
  write('node_modules/@openai/codex-sdk/package.json', JSON.stringify({ type: 'module', exports: './index.mjs' }));
  write('node_modules/@openai/codex-sdk/index.mjs', 'export class Codex { startThread() { return {}; } }');
  write('codex-turn.mjs', `
    import fs from 'node:fs';
    import path from 'node:path';
    export async function runCodexTurn(_thread, prompt) {
      const item = JSON.parse(prompt);
      if (item.attempts === 1) throw new Error('fixture transient failure');
      await new Promise(resolve => setTimeout(resolve, 1));
      const file = path.join(process.env.RESEARCH_RUNNER_PROJECT_ROOT, item.expectedOutputFile);
      fs.mkdirSync(path.dirname(file), { recursive: true });
      fs.writeFileSync(file, 'fixture completed');
      return { items: [], finalResponse: 'fixture completed' };
    }
  `);
  write('validators/output-validator.mjs', `
    import fs from 'node:fs';
    import path from 'node:path';
    export const createOutputContract = item => ({ expectedOutputFile: item.expectedOutputFile });
    export const captureOutputSnapshot = () => ({});
    export function validateLocalOutput(item) {
      const file = path.join(process.env.RESEARCH_RUNNER_PROJECT_ROOT, item.expectedOutputFile);
      if (!fs.statSync(file).size) throw new Error('Empty fixture output');
      return item.expectedOutputFile;
    }
  `);
  write('usage-telemetry.mjs', `
    export const collectCodexThreadUsage = () => ({ counters: null });
    export const enrichTokenCounter = value => value;
    export const readSuccessfulSessionCompletion = () => null;
  `);
  fs.mkdirSync(queue);
  fs.writeFileSync(path.join(queue, 'queue.jsonl'), Array.from({ length: count }, (_, i) => JSON.stringify({
    id: 'fixture-' + i, domain: 'file-run', subject: 'fixture-' + i,
    status: 'pending', attempts: 0, expectedOutputFile: 'reports/' + i + '.md',
  })).join('\n') + '\n');
  fs.writeFileSync(path.join(queue, 'queue.done.jsonl'), '');
  return {
    root, runner, queue,
    run(args = []) {
      return spawnSync(process.execPath, [path.join(runner, 'runner.mjs'), '--concurrency=7', ...args], {
        cwd: root, encoding: 'utf8', windowsHide: true, timeout: 30_000, maxBuffer: 16 * 1024 * 1024,
        env: { ...process.env, RESEARCH_RUNNER_PROJECT_ROOT: root, RESEARCH_RUNNER_QUEUE_DIR: queue },
      });
    },
    close() { fs.rmSync(root, { recursive: true, force: true }); },
  };
}

test('runner rejects the removed batch-limit flag before touching queue files', () => {
  const help = spawnSync(process.execPath, [path.join(source, 'runner.mjs'), '--help'], { encoding: 'utf8', windowsHide: true });
  assert.equal(help.status, 0);
  assert.doesNotMatch(help.stdout, /--max-jobs/);
  const rejected = spawnSync(process.execPath, [path.join(source, 'runner.mjs'), '--max-jobs=500'], { encoding: 'utf8', windowsHide: true });
  assert.equal(rejected.status, 1);
  assert.match(rejected.stderr, /Unknown argument: --max-jobs=500/);
});

test('scheduler drains the queue beyond 500 attempts including retries', () => {
  const f = fixture(251);
  try {
    const result = f.run();
    assert.equal(result.status, 0, result.stderr || result.error?.message);
    assert.equal(readRows(path.join(f.queue, 'queue.jsonl')).length, 0);
    const done = readRows(path.join(f.queue, 'queue.done.jsonl'));
    assert.equal(done.length, 251);
    assert.ok(done.every(item => item.attempts === 2 && item.status === 'done'));
    const events = readRows(path.join(f.runner, 'logs/current.jsonl'));
    assert.equal(events.findLast(event => event.event === 'Runner finished.').processed, 502);
    assert.equal(fs.existsSync(path.join(f.runner, 'runner.lock')), false);
  } finally { f.close(); }
});

test('explicit once mode still runs one attempt without a batch-limit setting', () => {
  const f = fixture(4);
  try {
    const result = f.run(['--once']);
    assert.equal(result.status, 0, result.stderr || result.error?.message);
    const active = readRows(path.join(f.queue, 'queue.jsonl'));
    assert.equal(active.filter(item => item.status === 'retry_pending').length, 1);
    assert.equal(active.filter(item => item.status === 'pending').length, 3);
    assert.equal(active.reduce((sum, item) => sum + item.attempts, 0), 1);
  } finally { f.close(); }
});
