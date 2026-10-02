import { AsyncLocalStorage } from 'node:async_hooks';
import { channel } from 'node:diagnostics_channel';
import { setTimeout as delay } from 'node:timers/promises';

export const EXIT_GRACE_MS = 120_000;
const CLEANUP_MS = 10_000;
const launchScope = new AsyncLocalStorage();
const childChannel = channel('child_process');

// The SDK does not expose its ChildProcess. Node's documented diagnostic channel
// lets us observe its exit without patching spawn or depending on SDK internals.
// AsyncLocalStorage prevents concurrent turns from capturing each other's child.
function exited(child) {
  return child.exitCode !== null || child.signalCode !== null || !child.pid;
}

export class CodexCleanupError extends Error {
  constructor(children) {
    super(`Codex cleanup could not confirm process exit; preserve output and stop claiming (pids: ${children.map(c => c.pid).join(', ') || 'unknown'}).`);
    this.name = 'CodexCleanupError';
    this.cleanupUnconfirmed = true;
  }
}

export async function runCodexTurn(thread, input, {
  timeoutMs, outputSchema, recoverCompletion = () => null, log = () => {},
  exitGraceMs = EXIT_GRACE_MS, cleanupMs = CLEANUP_MS,
} = {}) {
  const controller = new AbortController();
  const children = [];
  const onChild = ({ process: child }) => {
    if (launchScope.getStore() === children) children.push(child);
  };
  childChannel.subscribe(onChild);
  let completion = null;
  let failure = null;
  let ended = false;
  let stopping = false;
  let timer;
  let wake;
  const deadline = new Promise(resolve => { wake = resolve; });
  const arm = (ms, reason) => {
    clearTimeout(timer);
    timer = setTimeout(() => wake(reason), ms);
  };
  const result = { items: [], finalResponse: '', usage: null };
  arm(timeoutMs, 'research_timeout');

  // Always consume/reject the pending generator, even if cleanup has to return
  // independently of it. Only this function settles the turn's result.
  const consume = launchScope.run(children, async () => {
    try {
      const { events } = await thread.runStreamed(input, { signal: controller.signal, outputSchema });
      for await (const event of events) {
        if (event.type === 'turn.failed' || event.type === 'error') {
          failure = new Error(event.error?.message || event.message || 'Codex turn failed');
          wake('stream_failure');
        } else if (event.type === 'item.completed') {
          result.items.push(event.item);
          if (event.item.type === 'agent_message') result.finalResponse = event.item.text;
        } else if (event.type === 'turn.completed' && !failure && !completion) {
          result.usage = event.usage;
          completion = { ...result, items: [...result.items] };
          log('Codex turn completed; waiting for process exit.', { threadId: thread.id });
          if (!stopping) arm(exitGraceMs, 'exit_timeout');
        }
      }
    } catch (error) {
      // Ignore only an abort caused by our own cleanup. Parse errors, explicit
      // turn failures, and unrelated errors still invalidate a success result.
      if (!(stopping && error?.name === 'AbortError')) failure ??= error;
    } finally {
      ended = true;
    }
  });

  try {
    const reason = await Promise.race([consume.then(() => 'stream_ended'), deadline]);
    clearTimeout(timer);
    if (reason === 'research_timeout' && !completion && !failure) {
      completion = recoverCompletion(thread.id);
      if (completion) log('Recovered successful Codex turn from session at timeout.', { threadId: thread.id });
    }
    if (reason === 'research_timeout' && !completion && !failure) {
      failure = new Error(`Codex formal timeout after ${timeoutMs / 60_000} minutes.`);
    }

    if (!ended || children.some(c => !exited(c))) {
      stopping = true;
      controller.abort();
      // SDK cancellation can leave its iterator waiting after the child has
      // exited. Observe the actual process, then close only its remaining pipes.
      const until = Date.now() + cleanupMs;
      while (children.some(c => !exited(c)) && Date.now() < until) await delay(25);
      if ((!children.length && !ended) || children.some(c => !exited(c))) throw new CodexCleanupError(children);
      for (const child of children) {
        child.stdin?.destroy();
        child.stdout?.destroy();
        child.stderr?.destroy();
      }
      // Give queued error events a chance to be observed before accepting the
      // saved completion; never wait indefinitely on SDK iterator teardown.
      await Promise.race([consume, delay(25)]);
      log('Codex process cleanup confirmed.', { threadId: thread.id, reason, recovered: Boolean(completion) });
    }
    if (failure) throw failure;
    if (!completion) throw new Error('Codex stream ended without a successful turn.completed event.');
    return { ...completion, threadId: thread.id };
  } finally {
    clearTimeout(timer);
    childChannel.unsubscribe(onChild);
  }
}
