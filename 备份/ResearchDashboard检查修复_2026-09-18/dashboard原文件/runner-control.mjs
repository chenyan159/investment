import fs from "node:fs";
import path from "node:path";
import { spawn } from "node:child_process";

import { writeQueueControl } from "../queue-store.mjs";
import {
  DEFAULT_RUNNER_CONCURRENCY,
  LOCK_PATH,
  LOG_PATH,
  MAX_RUNNER_CONCURRENCY,
  RUNNER_DIR,
} from "./config.mjs";
import { isProcessAlive } from "./snapshot.mjs";

export async function validateQueue() {
  const result = await runCommand(process.execPath, ["queue-tools.mjs", "validate"], {
    cwd: RUNNER_DIR,
    timeoutMs: 60_000,
  });
  const combined = [result.stdout, result.stderr].filter(Boolean).join("\n").trim();
  return {
    ok: result.code === 0,
    code: result.code,
    summary: parseValidationSummary(combined),
    output: combined,
  };
}

export async function startRunner({ concurrency = DEFAULT_RUNNER_CONCURRENCY } = {}) {
  const normalizedConcurrency = normalizeConcurrency(concurrency, { allowZero: false });
  const existing = readRunnerLock();
  if (existing && isProcessAlive(existing.pid)) {
    const error = new Error(`Runner is already active with pid ${existing.pid}.`);
    error.statusCode = 409;
    throw error;
  }

  const validation = await validateQueue();
  if (!validation.ok || Number(validation.summary.errors || 0) > 0) {
    const error = new Error("Queue validation failed; runner was not started.");
    error.statusCode = 422;
    error.details = validation;
    throw error;
  }

  const startedRequestAt = Date.now();
  const script = [
    `$p = Start-Process -FilePath "node"`,
    `-ArgumentList @("runner.mjs", "--max-jobs=500", "--timeout-minutes=120", "--concurrency=${normalizedConcurrency}")`,
    `-WorkingDirectory '${escapePowerShellSingleQuoted(RUNNER_DIR)}'`,
    `-WindowStyle Hidden -PassThru`,
    `; $p.Id`,
  ].join(" ");
  const launch = await runPowerShell(script, { timeoutMs: 30_000 });
  if (launch.code !== 0) {
    const error = new Error(`Background runner launch failed: ${launch.stderr || launch.stdout || "unknown error"}`);
    error.statusCode = 500;
    throw error;
  }
  const launcherPid = Number(String(launch.stdout).trim().split(/\s+/).at(-1));

  const deadline = Date.now() + 10_000;
  while (Date.now() < deadline) {
    const lock = readRunnerLock();
    if (lock && isProcessAlive(lock.pid)) {
      return {
        started: true,
        exited: false,
        pid: Number(lock.pid),
        startedAt: lock.startedAt || null,
        concurrency: normalizedConcurrency,
        validation: validation.summary,
      };
    }
    if (Number.isInteger(launcherPid) && !isProcessAlive(launcherPid)) break;
    await delay(250);
  }

  const recentLog = readRecentLogEvents(startedRequestAt);
  const finished = recentLog.find((entry) => /Runner finished|No claimable queue items; exiting/i.test(entry.event || ""));
  if (finished || (Number.isInteger(launcherPid) && !isProcessAlive(launcherPid))) {
    return {
      started: false,
      exited: true,
      pid: Number.isInteger(launcherPid) ? launcherPid : null,
      concurrency: normalizedConcurrency,
      validation: validation.summary,
      message: finished?.event || "Runner exited before a live lock could be confirmed.",
    };
  }

  const error = new Error("Runner launch was requested, but a live runner.lock was not confirmed within 10 seconds.");
  error.statusCode = 504;
  throw error;
}

export function setRunnerConcurrency(value) {
  const concurrency = normalizeConcurrency(value, { allowZero: true });
  const written = writeQueueControl({ concurrency });
  return {
    concurrency: written.concurrency,
    runner: runnerState(),
  };
}

export async function forceStopRunner({ confirm }) {
  if (confirm !== "STOP") {
    const error = new Error("Force stop requires the exact confirmation value STOP.");
    error.statusCode = 400;
    throw error;
  }
  const lock = readRunnerLock();
  if (!lock) return { stopped: false, reason: "lock_missing" };
  const pid = Number(lock.pid);
  if (!isProcessAlive(pid)) return { stopped: false, reason: "pid_not_running", pid };

  const result = process.platform === "win32"
    ? await runCommand("taskkill.exe", ["/PID", String(pid), "/T", "/F"], { timeoutMs: 30_000 })
    : await stopPosix(pid);
  await delay(300);
  return {
    stopped: !isProcessAlive(pid),
    pid,
    code: result.code,
    output: [result.stdout, result.stderr].filter(Boolean).join("\n").trim(),
    lockPreserved: fs.existsSync(LOCK_PATH),
  };
}

export function runnerState() {
  const lock = readRunnerLock();
  return {
    lock,
    alive: Boolean(lock && isProcessAlive(lock.pid)),
  };
}

export function readRunnerLock() {
  try {
    return JSON.parse(fs.readFileSync(LOCK_PATH, "utf8"));
  } catch {
    return null;
  }
}

function normalizeConcurrency(value, { allowZero }) {
  const number = Number(value);
  const minimum = allowZero ? 0 : 1;
  if (!Number.isInteger(number) || number < minimum || number > MAX_RUNNER_CONCURRENCY) {
    throw new Error(`Concurrency must be an integer from ${minimum} to ${MAX_RUNNER_CONCURRENCY}.`);
  }
  return number;
}

function parseValidationSummary(output) {
  const readNumber = (label) => {
    const match = output.match(new RegExp(`${label}:\\s*(\\d+)`, "i"));
    return match ? Number(match[1]) : null;
  };
  return {
    activeItems: readNumber("Active items"),
    doneArchiveItems: readNumber("Done archive items"),
    errors: readNumber("Errors"),
    warnings: readNumber("Warnings"),
  };
}

function readRecentLogEvents(afterMs) {
  if (!fs.existsSync(LOG_PATH)) return [];
  try {
    return fs.readFileSync(LOG_PATH, "utf8")
      .split(/\r?\n/)
      .map((line) => line.trim())
      .filter(Boolean)
      .map((line) => JSON.parse(line))
      .filter((entry) => Date.parse(entry.timestamp || "") >= afterMs);
  } catch {
    return [];
  }
}

async function runPowerShell(script, options) {
  const args = ["-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", script];
  try {
    return await runCommand("pwsh.exe", args, options);
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
    return runCommand("powershell.exe", args, options);
  }
}

function runCommand(command, args, { cwd = RUNNER_DIR, timeoutMs = 30_000 } = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd,
      windowsHide: true,
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    let settled = false;
    const timeout = setTimeout(() => {
      if (settled) return;
      settled = true;
      child.kill();
      const error = new Error(`${path.basename(command)} timed out after ${timeoutMs}ms.`);
      error.code = "ETIMEDOUT";
      reject(error);
    }, timeoutMs);
    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", (error) => {
      if (settled) return;
      settled = true;
      clearTimeout(timeout);
      reject(error);
    });
    child.on("close", (code) => {
      if (settled) return;
      settled = true;
      clearTimeout(timeout);
      resolve({ code: Number(code), stdout: stdout.trim(), stderr: stderr.trim() });
    });
  });
}

async function stopPosix(pid) {
  try {
    process.kill(pid, "SIGTERM");
    return { code: 0, stdout: "SIGTERM sent", stderr: "" };
  } catch (error) {
    return { code: 1, stdout: "", stderr: error.message };
  }
}

function escapePowerShellSingleQuoted(value) {
  return String(value).replaceAll("'", "''");
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
