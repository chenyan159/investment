import assert from 'node:assert/strict';
import test from 'node:test';
import { spawn } from 'node:child_process';
import { channel } from 'node:diagnostics_channel';
import { runCodexTurn } from '../codex-turn.mjs';

// Real disposable child processes exercise cancellation and exit confirmation;
// the deterministic event stream replaces model/network work only.
function fakeThread({ terminal = 'success', hang = false, stuckIterator = false, ignoreAbort = false, lateError = false } = {}) {
  const thread = {
    id: 'fixture-thread', child: null, aborts: 0,
    async runStreamed(_input, { signal }) {
      return { events: (async function* () {
        signal.addEventListener('abort', () => thread.aborts++);
        const child = thread.child = spawn(process.execPath, ['-e', hang ? 'setInterval(()=>{},1000)' : ''], {
          windowsHide: true, signal: ignoreAbort ? undefined : signal,
        });
        let error;
        child.on('error', e => { error = e; });
        const exit = new Promise(resolve => child.once('exit', resolve));
        yield { type: 'thread.started', thread_id: thread.id };
        yield { type: 'item.completed', item: { type: 'agent_message', text: 'finished' } };
        if (terminal === 'success') yield { type: 'turn.completed', usage: { input_tokens: 10, output_tokens: 2 } };
        if (terminal === 'failure') yield { type: 'turn.failed', error: { message: 'quota unavailable' } };
        if (lateError) yield { type: 'error', message: 'real failure after completion' };
        await exit;
        if (stuckIterator) await new Promise(() => {});
        if (error) throw error;
      })() };
    },
  };
  return thread;
}

const options = { timeoutMs: 2000, exitGraceMs: 300, cleanupMs: 1000 };
const dead = child => child.exitCode !== null || child.signalCode !== null;

test('normal completion returns usage without waiting for grace or cancelling', async () => {
  const thread = fakeThread();
  const result = await runCodexTurn(thread, '', options);
  assert.equal(result.finalResponse, 'finished');
  assert.equal(result.usage.output_tokens, 2);
  assert.equal(thread.aborts, 0);
  assert.ok(dead(thread.child));
});

test('successful turn with a live stuck child is cancelled and preserved', async () => {
  const thread = fakeThread({ hang: true });
  const result = await runCodexTurn(thread, '', { ...options, exitGraceMs: 30 });
  assert.equal(result.finalResponse, 'finished');
  assert.equal(thread.aborts, 1);
  assert.ok(dead(thread.child));
});

test('SDK iterator hanging after actual child exit cannot strand the runner', async () => {
  const thread = fakeThread({ stuckIterator: true });
  const result = await runCodexTurn(thread, '', options);
  assert.equal(result.finalResponse, 'finished');
  assert.ok(dead(thread.child));
});

test('research timeout checks persisted success once and uses the same return path', async () => {
  const thread = fakeThread({ terminal: 'none', hang: true });
  let reads = 0;
  const result = await runCodexTurn(thread, '', {
    ...options, timeoutMs: 50,
    recoverCompletion: id => { assert.equal(id, thread.id); reads++; return { finalResponse: 'recovered', items: [], usage: null }; },
  });
  assert.equal(reads, 1);
  assert.equal(result.finalResponse, 'recovered');
  assert.ok(dead(thread.child));
});

test('a final message alone never bypasses timeout or successful terminal requirement', async () => {
  for (const hang of [false, true]) {
    const thread = fakeThread({ terminal: 'none', hang });
    await assert.rejects(runCodexTurn(thread, '', { ...options, timeoutMs: hang ? 50 : 2000 }), /timeout|without a successful/);
    assert.ok(dead(thread.child));
  }
});

test('explicit failure and post-completion error are not swallowed as cleanup', async () => {
  for (const configuration of [{ terminal: 'failure', hang: true }, { lateError: true, hang: true }]) {
    const thread = fakeThread(configuration);
    await assert.rejects(runCodexTurn(thread, '', {
      ...options, recoverCompletion: () => { throw new Error('must not recover explicit failure'); },
    }), /quota unavailable|real failure after completion/);
    assert.ok(dead(thread.child));
  }
});

test('unconfirmed cancellation protects the output instead of accepting success', async () => {
  const thread = fakeThread({ hang: true, ignoreAbort: true });
  try {
    await assert.rejects(runCodexTurn(thread, '', { ...options, exitGraceMs: 30, cleanupMs: 50 }), e => e.cleanupUnconfirmed === true);
    assert.equal(dead(thread.child), false);
  } finally {
    const exit = new Promise(resolve => thread.child.once('exit', resolve));
    thread.child.kill();
    await exit;
  }
});

test('concurrent turns capture only their own child and unsubscribe on completion', async () => {
  const before = channel('child_process').hasSubscribers;
  const first = fakeThread({ hang: true });
  const second = fakeThread({ hang: true });
  const p1 = runCodexTurn(first, '', { ...options, exitGraceMs: 30 });
  const p2 = runCodexTurn(second, '', { ...options, exitGraceMs: 350 });
  await p1;
  assert.equal(dead(second.child), false);
  await p2;
  assert.ok(dead(first.child) && dead(second.child));
  assert.equal(channel('child_process').hasSubscribers, before);
});

test('completion racing a research deadline is returned only once', async () => {
  const thread = fakeThread({ hang: true });
  let reads = 0;
  const result = await runCodexTurn(thread, '', {
    ...options, timeoutMs: 1, exitGraceMs: 25,
    recoverCompletion: () => { reads++; return null; },
  });
  assert.equal(result.finalResponse, 'finished');
  assert.equal(reads, 0);
  assert.equal(thread.aborts, 1);
});
