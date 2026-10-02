import { spawn } from "node:child_process";
import { createRequire } from "node:module";
import path from "node:path";
import readline from "node:readline";

export const QUOTA_USAGE_THRESHOLD = 99;
export const QUOTA_QUERY_RETRY_MS = 60_000;
const QUOTA_RESET_BUFFER_MS = 60_000;
const QUOTA_QUERY_TIMEOUT_MS = 15_000;
const require = createRequire(import.meta.url);

export function readCodexQuota({ timeoutMs = QUOTA_QUERY_TIMEOUT_MS } = {}) {
  const packagePath = require.resolve("@openai/codex/package.json");
  const codexScript = path.join(path.dirname(packagePath), "bin", "codex.js");
  const env = { ...process.env };
  delete env.OPENAI_API_KEY;
  delete env.CODEX_API_KEY;
  if (!env.CODEX_HOME && env.USERPROFILE) env.CODEX_HOME = path.join(env.USERPROFILE, ".codex");

  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [codexScript, "app-server"], {
      env,
      stdio: ["pipe", "pipe", "pipe"],
      windowsHide: true,
    });
    const lines = readline.createInterface({ input: child.stdout });
    child.stderr.resume();
    let settled = false;
    let timeout;

    const finish = (error, result) => {
      if (settled) return;
      settled = true;
      clearTimeout(timeout);
      lines.close();
      if (!child.stdin.destroyed) child.stdin.end();
      child.kill();
      if (error) reject(error);
      else resolve(result);
    };

    const send = (message) => child.stdin.write(`${JSON.stringify(message)}\n`);
    timeout = setTimeout(
      () => finish(new Error(`Codex quota query timed out after ${timeoutMs}ms.`)),
      timeoutMs,
    );

    child.on("error", (error) => finish(error));
    child.stdin.on("error", (error) => {
      if (!settled) finish(error);
    });
    child.on("exit", (code) => {
      if (!settled) finish(new Error(`Codex App Server exited before returning quota data (code ${code}).`));
    });
    lines.on("line", (line) => {
      let message;
      try {
        message = JSON.parse(line);
      } catch {
        return;
      }

      if (message.id === 0) {
        if (message.error) {
          finish(new Error(`Codex App Server initialization failed: ${message.error.message || "unknown error"}`));
          return;
        }
        send({ method: "initialized", params: {} });
        send({ method: "account/rateLimits/read", id: 6 });
      } else if (message.id === 6) {
        if (message.error) {
          finish(new Error(`Codex quota query failed: ${message.error.message || "unknown error"}`));
          return;
        }
        finish(null, message.result);
      }
    });

    send({
      method: "initialize",
      id: 0,
      params: {
        clientInfo: {
          name: "research_runner",
          title: "Research Runner",
          version: "0.1.0",
        },
      },
    });
  });
}

export function evaluateCodexQuota(result, {
  threshold = QUOTA_USAGE_THRESHOLD,
  nowMs = Date.now(),
} = {}) {
  const limits = result?.rateLimits || result?.rateLimitsByLimitId?.codex;
  if (!limits) throw new Error("Codex quota response does not contain the codex rate-limit bucket.");

  const windows = [
    ["primary", limits.primary],
    ["secondary", limits.secondary],
  ].filter(([, value]) => value && Number.isFinite(Number(value.usedPercent)));
  const blockedWindows = windows.filter(([, value]) => Number(value.usedPercent) >= threshold);
  const blocked = Boolean(limits.rateLimitReachedType) || blockedWindows.length > 0;
  const resetSource = blockedWindows.length ? blockedWindows : windows;
  const resetTimes = resetSource
    .map(([, value]) => Number(value.resetsAt) * 1000)
    .filter((value) => Number.isFinite(value) && value > nowMs);
  const pauseUntil = blocked
    ? (resetTimes.length ? Math.max(...resetTimes) + QUOTA_RESET_BUFFER_MS : nowMs + QUOTA_QUERY_RETRY_MS)
    : 0;

  return {
    blocked,
    pauseUntil,
    rateLimitReachedType: limits.rateLimitReachedType || null,
    primaryUsedPercent: limits.primary ? Number(limits.primary.usedPercent) : null,
    secondaryUsedPercent: limits.secondary ? Number(limits.secondary.usedPercent) : null,
    blockedWindows: blockedWindows.map(([name]) => name),
  };
}

export function createQuotaGate({
  log,
  probe = readCodexQuota,
  sleep = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds)),
} = {}) {
  let pauseUntil = 0;

  const applyResult = (result, source) => {
    const quota = evaluateCodexQuota(result);
    if (quota.blocked && quota.pauseUntil > pauseUntil) {
      pauseUntil = quota.pauseUntil;
      log?.("Codex quota threshold reached; pausing new queue claims.", {
        source,
        threshold: QUOTA_USAGE_THRESHOLD,
        pauseUntil: new Date(pauseUntil).toISOString(),
        primaryUsedPercent: quota.primaryUsedPercent,
        secondaryUsedPercent: quota.secondaryUsedPercent,
        rateLimitReachedType: quota.rateLimitReachedType,
      });
    }
    return quota;
  };

  return {
    isPaused() {
      return Date.now() < pauseUntil;
    },
    pauseUntil() {
      return pauseUntil;
    },
    async beforeTask() {
      if (Date.now() < pauseUntil) return { allowed: false, pauseUntil };
      try {
        const quota = applyResult(await probe(), "before_task");
        return { allowed: !quota.blocked, ...quota };
      } catch (error) {
        log?.("Codex quota preflight query failed; continuing with the task.", {
          message: error?.message || String(error),
        });
        return { allowed: true, queryFailed: true };
      }
    },
    async afterTaskFailure() {
      while (true) {
        try {
          return applyResult(await probe(), "after_task_failure");
        } catch (error) {
          const retryAt = Date.now() + QUOTA_QUERY_RETRY_MS;
          pauseUntil = Math.max(pauseUntil, retryAt);
          log?.("Task failed and the Codex quota query also failed; retrying the quota query in 60 seconds.", {
            message: error?.message || String(error),
            retryAt: new Date(retryAt).toISOString(),
          });
          await sleep(QUOTA_QUERY_RETRY_MS);
        }
      }
    },
  };
}
